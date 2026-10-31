#!/usr/bin/env python3
"""E002-557: real-browser integration of existing blinded-rater tools.
Synthetic media only; no human images or ratings are used or uploaded.
"""
import hashlib, json, os, shutil, subprocess, sys, tempfile, threading
from contextlib import contextmanager
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from e002_492_anatomical_review import build_manifest, template, adjudicate
from e002_555_rater_audit import audit

def chromium(p):
    binary=os.environ.get("LUCENT557_CHROMIUM") or next((shutil.which(x) for x in ("chromium","google-chrome","chromium-browser") if shutil.which(x)),None)
    if not binary: raise RuntimeError("CHROMIUM_MISSING")
    return p.chromium.launch(headless=True,executable_path=binary,args=["--no-sandbox","--disable-dev-shm-usage"])

def blocked_requests(page, allowed_loopback_origin=None):
    out=[]
    def record(r):
        if r.url.startswith(("http://","https://")) and not (
            allowed_loopback_origin and r.url.startswith(allowed_loopback_origin+"/")
        ):
            out.append(r.url)
    page.on("request",record)
    if allowed_loopback_origin:
        page.route("**/*", lambda route: route.continue_() if (
            not route.request.url.startswith(("http://","https://")) or
            route.request.url.startswith(allowed_loopback_origin+"/")
        ) else route.abort())
    return out

@contextmanager
def local_only_video_rater():
    # file:// is an opaque origin on some Chrome builds; a loopback secure
    # context gives blob: URLs a real origin without uploading private video.
    class QuietHandler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(HERE), **kwargs)
        def log_message(self, *args): pass
    server=ThreadingHTTPServer(("127.0.0.1",0),QuietHandler)
    worker=threading.Thread(target=server.serve_forever,daemon=True)
    worker.start()
    try:
        yield "http://127.0.0.1:"+str(server.server_port)
    finally:
        server.shutdown()
        server.server_close()
        worker.join(timeout=5)

def png_packet(work):
    from PIL import Image, ImageDraw
    folder=work/"frames";folder.mkdir()
    paths=[]
    for i in range(20):
        for j in range(13):
            f=folder/f"clip_{i:02d}_frame_{j:02d}.png"
            im=Image.new("RGB",(320,288),(100,100,100))
            ImageDraw.Draw(im).rectangle((120,100+j,200,120+j),fill=(20,20,20))
            im.save(f);paths.append(str(f))
    return paths

def test_native(browser,work):
    frames=png_packet(work);packets=[]
    for rater in ("A","B"):
        t=work/f"template_{rater}.json"
        t.write_text(json.dumps(template(build_manifest(),rater)))
        ctx=browser.new_context(accept_downloads=True);page=ctx.new_page()
        leaks=blocked_requests(page)
        page.goto((HERE/"e002_497_offline_rater.html").as_uri())
        page.locator("#template").set_input_files(str(t))
        page.locator("#fallback").set_input_files(frames[:-1])
        page.locator("#load").click()
        expect(page.locator("#status")).to_contain_text("BLOCKED:")
        assert "Exactly 260" in page.locator("#status").inner_text()
        page.locator("#fallback").set_input_files(frames)
        page.locator("#load").click()
        expect(page.locator("#status")).to_contain_text("Private local frame loaded")
        assert "1/260" in page.locator("#position").inner_text()
        page.locator("#export").click()
        assert "BLOCKED:" in page.locator("#status").inner_text()
        for k in range(260):
            page.locator('fieldset input[value="POOR_GEOMETRY"]').check()
            page.locator("#next").click()
            if k<259:
                expect(page.locator("#position")).to_contain_text(f"{k+2}/260")
                expect(page.locator("#status")).to_contain_text("Private local frame loaded")
        with page.expect_download() as dl:page.locator("#export").click()
        output=work/f"rater_{rater}.json";dl.value.save_as(output)
        packet=json.loads(output.read_text())
        assert packet["rater"]==rater
        assert all(f["flags"]==["POOR_GEOMETRY"] for fs in packet["clips"].values() for f in fs)
        assert not leaks,leaks
        packets.append(packet);ctx.close()
    r=adjudicate(build_manifest(),*packets)
    assert r["total_review_positions"]==260 and r["unreviewed"]==0,r
    assert r["nuisance_abstention"]==260 and r["dual_measurable"]==0,r
    assert r["human_reference_validated"] is False,r
    return {"packets":2,"frames_each":260,"synthetic_nuisance_abstentions":260}

def test_video(browser,work,origin):
    # CI Chromium is built without proprietary H.264 decoding. Use browser-native VP8/WebM
    # to validate the annotation workflow; this does NOT validate arbitrary human codecs.
    video=work/"synthetic_eye.webm"
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-f","lavfi",
        "-i","color=c=gray:s=320x240:r=30:d=2",
        "-vf","drawbox=x=100:y=100:w=120:h=20:color=black:t=fill",
        "-an","-c:v","libvpx","-deadline","realtime","-cpu-used","8","-b:v","500k",str(video)],
        check=True,timeout=60)
    sha=hashlib.sha256(video.read_bytes()).hexdigest()
    packets=[]
    for rater in ("rater-A","rater-B"):
        ctx=browser.new_context(accept_downloads=True);page=ctx.new_page()
        leaks=blocked_requests(page,origin)
        page.goto(origin+"/e002_555_offline_rater.html")
        page.locator("#packet").fill("synthetic-e002-557")
        page.locator("#rater").fill(rater)
        page.locator("#sample").fill("synthetic-frame-01")
        page.locator("#file").set_input_files(str(video))
        expect(page.locator("#digest")).to_contain_text(sha)
        try:
            expect(page.locator("#video")).to_have_js_property("videoWidth", 320, timeout=15000)
        except AssertionError as exc:
            diagnostic=page.locator("#video").evaluate(
                "(v)=>({width:v.videoWidth,readyState:v.readyState,networkState:v.networkState,errorCode:v.error?.code,errorMessage:v.error?.message,src:v.src,canPlayWebm:v.canPlayType('video/webm; codecs=vp8')})"
            )
            raise AssertionError("VIDEO_DECODE_BLOCKED: "+json.dumps(diagnostic,sort_keys=True)) from exc
        page.evaluate('document.getElementById("video").currentTime=0.5')
        expect(page.locator("#video")).to_have_js_property("currentTime", 0.5)
        page.locator("#capture").click()
        expect(page.locator("#points")).to_contain_text("Click the upper")
        page.locator("#canvas").click(position={"x":160,"y":95})
        page.locator("#canvas").click(position={"x":160,"y":125})
        page.locator("#label").select_option("closed")
        page.locator("#save").click()
        with page.expect_download() as dl:page.locator("#export").click()
        output=work/(rater+".json");dl.value.save_as(output)
        packet=json.loads(output.read_text())
        assert packet["video_sha256"]==sha and packet["timing_type"]=="browser_presentation_only"
        assert len(packet["annotations"])==1 and not leaks
        packets.append(packet);ctx.close()
    r=audit(*packets)
    assert r["presentation_timing_only"] is True and r["human_physical_validation"] is False,r
    assert r["release"]=="BLOCKED",r
    return {"packets":2,"synthetic_closed_agreements":r["counts"]["RATER_CONCORDANT_UNCALIBRATED"],"hardware_clock_verified":False}

def main():
    with tempfile.TemporaryDirectory(prefix="lucent557_") as td:
        with sync_playwright() as p:
            b=chromium(p)
            try:
                native=test_native(b,Path(td))
                with local_only_video_rater() as origin:
                    video=test_video(b,Path(td),origin)
            finally:b.close()
    print(json.dumps({"experiment":"E002-557","status":"SYNTHETIC_BROWSER_E2E_PASS",
        "native":native,"video":video,"real_human_raters":0,"physical_captures":0,
        "certified_human_motion_bounds":0,"heldout_physical_predictions":0,
        "product":"ABSTAIN_UNCALIBRATED","release":"BLOCKED"},sort_keys=True))

if __name__=="__main__":main()
