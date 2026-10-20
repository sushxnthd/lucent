from interval_instrument import interval
def run():
    assert interval([.06,.06],[1,1],[[1],[1]],[-.055],[.055],[.01,.01])["status"]=="abstain"
    assert interval([.06,.06],[1,1],[[1],[-1]],[-.2],[.2],[.01,.01])["status"]=="certify_positive"
    assert interval([.06],[1],[[1]],[-.2],[.2],[.01])["status"]=="abstain"
    assert interval([0,.015,.03,.045,.06],[0,.25,.5,.75,1],[[0],[.25],[.5],[.75],[1]],[-.1],[.1],[.01]*5)["status"]=="abstain"
    print("PASS: geometry, brightness, missingness, temporal smoothness controls")
if __name__=="__main__":run()
