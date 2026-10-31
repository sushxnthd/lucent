#!/usr/bin/env python3
"""E002-571: real Chromium measured-path smoke test; synthetic PNGs only.

No actual human annotation, sensor timing, or physiological certificate.
"""
import json
import tempfile
from pathlib import Path

from playwright.sync_api import expect, sync_playwright
from e002_492_anatomical_review import adjudicate, build_manifest, template
from e002_557_browser_e2e import HERE, blocked_requests, chromium, png_packet


def measure(page, upper, lower):
    canvas = page.locator('#view')
    rect = canvas.bounding_box()
    if not rect or rect['width'] <= 0 or rect['height'] <= 0:
        raise AssertionError('CANVAS_NOT_RENDERED')
    # Native x=160 is the geometric center; CSS includes a 1px border.
    # Use a fixed interior point instead of DOM evaluation (strict CSP).
    for y in (upper, lower):
        canvas.click(position={'x': rect['width'] / 2,
                               'y': 1 + y * (rect['height'] - 2) / 288})
    expect(page.locator('#points')).to_contain_text('Upper:')
    expect(page.locator('#points')).to_contain_text('Lower:')
    page.locator('#diameter').fill('48')
    page.locator('#uncertainty').fill('1')


def run_rater(browser, work, frames, rater):
    blank = work / ('blank_' + rater + '.json')
    blank.write_text(json.dumps(template(build_manifest(), rater)))
    context = browser.new_context(accept_downloads=True)
    try:
        page = context.new_page()
        leaks = blocked_requests(page)
        page.goto((HERE / 'e002_497_offline_rater.html').as_uri())
        page.locator('#template').set_input_files(str(blank))
        page.locator('#fallback').set_input_files(frames)
        page.locator('#load').click()
        expect(page.locator('#status')).to_contain_text('Private local frame loaded')
        expect(page.locator('#position')).to_contain_text('1/260')
        page.locator('#export').click()
        expect(page.locator('#status')).to_contain_text('BLOCKED:')

        # One overlapping and one disjoint conservative aperture interval.
        points = [(90, 110), (90, 110)] if rater == 'A' else [(91, 109), (100, 110)]
        for i, (upper, lower) in enumerate(points):
            measure(page, upper, lower)
            page.locator('#next').click()
            expect(page.locator('#position')).to_contain_text(f'{i + 2}/260')
            expect(page.locator('#status')).to_contain_text('Private local frame loaded')

        for i in range(2, 260):
            page.locator('fieldset input[value="POOR_GEOMETRY"]').check()
            page.locator('#next').click()
            if i < 259:
                expect(page.locator('#position')).to_contain_text(f'{i + 2}/260')
        with page.expect_download() as download:
            page.locator('#export').click()
        output = work / ('synthetic_rater_' + rater + '.json')
        download.value.save_as(output)
        packet = json.loads(output.read_text())
        assert packet['rater'] == rater
        assert all(packet['clips']['clip_00'][j]['flags'] == [] for j in (0, 1))
        assert sum(f['flags'] == ['POOR_GEOMETRY']
                   for clip in packet['clips'].values() for f in clip) == 258
        assert not leaks, 'EXTERNAL_REQUEST_ATTEMPTED'
        return packet
    finally:
        context.close()


def main():
    with tempfile.TemporaryDirectory(prefix='lucent571_') as td:
        work = Path(td)
        frames = png_packet(work)
        with sync_playwright() as playwright:
            browser = chromium(playwright)
            try:
                a = run_rater(browser, work, frames, 'A')
                b = run_rater(browser, work, frames, 'B')
            finally:
                browser.close()
        result = adjudicate(build_manifest(), a, b)
        expected = {
            'total_review_positions': 260, 'dual_reviewed': 260,
            'dual_measurable': 2, 'interval_disagreement': 1,
            'agreement_intervals': 1, 'nuisance_abstention': 258,
            'unreviewed': 0, 'geometry_abstention': 0,
            'disagreement_fraction_among_dual_measurable': 0.5,
            'falsification_disagreement_gt_20pct': True,
            'human_reference_validated': False, 'release': 'BLOCKED',
            'product': 'ABSTAIN_UNCALIBRATED',
        }
        for key, value in expected.items():
            assert result[key] == value, (key, result[key], value)
    # Never emit frame content, per-frame coordinates, or private rater exports.
    print(json.dumps({
        'experiment': 'E002-571', 'status': 'SYNTHETIC_MEASURED_BROWSER_PASS',
        'rater_browser_contexts': 2, 'synthetic_frames_each': 260,
        'measured_frames_each': 2, 'nuisance_abstentions_each': 258,
        'synthetic_interval_disagreements': 1, 'real_human_raters': 0,
        'authenticated_physical_captures': 0, 'certified_hard_human_speed_bounds': 0,
        'heldout_physical_predictions': 0,
        'product': 'ABSTAIN_UNCALIBRATED', 'release': 'BLOCKED'
    }, sort_keys=True))


if __name__ == '__main__':
    main()
