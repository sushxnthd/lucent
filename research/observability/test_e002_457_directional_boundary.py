#!/usr/bin/env python3
"""E002-457 adversarial tests: exact directional theorem and shutter fail-closed."""
import math
import random
import unittest

from e002_457_directional_boundary import (
    ABSTAIN, NUISANCES, audit_rows, exact_boundary, parse_csv, shutter_gate,
)


def case(**changes):
    d = {
        "nuisance": {k: "PASS" for k in NUISANCES},
        "hard_directional_bound_verified": True,
        "closing_mm_s": 300.0,
        "opening_mm_s": 200.0,
        "threshold_mm": 2.0,
        "apertures_mm": [3.0, 3.0],
        "uncertainties_mm": [0.0, 0.0],
        "times_ms": [0.0, 10.0],
        "exposure_ms": 0.0,
        "clock_error_ms": 0.0,
        "kernel": "uniform_symmetric",
    }
    d.update(changes)
    return d


class DirectionalBoundary(unittest.TestCase):
    def test_exact_asymmetric_equality_has_witness(self):
        C, O, c = 300.0, 200.0, 2.0
        dt = (3-c)/C + (3-c)/O
        result = exact_boundary(3, 3, c, C, O, dt)
        self.assertEqual(result["decision"], "NOT_EXCLUDED")
        # Independent piecewise-linear path hits c exactly at the junction.
        tclose = (3-c)/C
        def path(t):
            return 3-C*t if t <= tclose else c+O*(t-tclose)
        self.assertAlmostEqual(path(0), 3)
        self.assertAlmostEqual(path(tclose), c)
        self.assertAlmostEqual(path(dt), 3)

    def test_below_and_above_boundary(self):
        critical = 1/300+1/200
        self.assertEqual(exact_boundary(3,3,2,300,200,critical-0.0001)["decision"],
                         "EXCLUDED_CONDITIONALLY")
        self.assertEqual(exact_boundary(3,3,2,300,200,critical+0.0001)["decision"],
                         "NOT_EXCLUDED")

    def test_symmetric_reduction(self):
        for V in (50, 200, 567):
            critical = 2/V
            self.assertAlmostEqual(exact_boundary(3,3,2,V,V,critical)["critical_gap_s"],
                                   critical)

    def test_unequal_endpoints_and_direction_swap(self):
        C,O,c,a0,a1 = 100,400,2,3,4
        dt=(a0-c)/C+(a1-c)/O
        self.assertEqual(exact_boundary(a0,a1,c,C,O,dt)["decision"],
                         "NOT_EXCLUDED")
        reverse=(a0-c)/O+(a1-c)/C
        self.assertNotAlmostEqual(dt,reverse)
        self.assertEqual(exact_boundary(a0,a1,c,C,O,dt-0.0001)["decision"],
                         "EXCLUDED_CONDITIONALLY")

    def test_infeasible_endpoints(self):
        self.assertEqual(exact_boundary(3,8,2,100,200,0.001)["decision"], "ABSTAIN")
        self.assertEqual(exact_boundary(8,3,2,100,200,0.001)["decision"], "ABSTAIN")

    def test_bad_speeds_and_nan(self):
        for v in (0,-1,float("nan"),float("inf")):
            with self.assertRaises(ValueError):
                exact_boundary(3,3,2,v,200,0.01)

    def test_random_piecewise_witness_never_excluded(self):
        rng=random.Random(457)
        for _ in range(3000):
            C=rng.uniform(20,800)
            O=rng.uniform(20,800)
            c=rng.uniform(0,3)
            a0=c+rng.uniform(0.01,2)
            a1=c+rng.uniform(0.01,2)
            tdown=(a0-c)/C
            tup=(a1-c)/O
            dt=tdown+tup+rng.uniform(0,0.05)
            self.assertEqual(exact_boundary(a0,a1,c,C,O,dt)["decision"],
                             "NOT_EXCLUDED")


class ShutterAdversarial(unittest.TestCase):
    def test_instantaneous_critical(self):
        # 5 ms is below the 8.333-ms directional critical gap; 10 ms is not.
        result=shutter_gate(case(times_ms=[0.0,5.0]))
        self.assertEqual(result["decision"], "EXCLUDED_CONDITIONALLY")
        self.assertAlmostEqual(result["critical_gap_ms"], 1000*(1/300+1/200))

    def test_monotone_shutter_clock_and_uncertainty(self):
        base=case()
        b=shutter_gate(base)
        for changes in (
            {"exposure_ms": 2.0},
            {"exposure_ms": 3.0},
            {"clock_error_ms": 0.5},
            {"uncertainties_mm": [0.2,0.2]},
        ):
            r=shutter_gate(case(**changes))
            if r["decision"] != "ABSTAIN":
                self.assertLessEqual(r.get("critical_gap_ms",0),
                                     b["critical_gap_ms"]+1e-10)

    def test_unknown_nuisance_abstains(self):
        for k in NUISANCES:
            d=case()
            d["nuisance"][k]="UNKNOWN"
            self.assertEqual(shutter_gate(d)["decision"],"ABSTAIN")

    def test_empirical_peak_cannot_claim_verified(self):
        d=case(hard_directional_bound_verified=False)
        self.assertEqual(shutter_gate(d)["decision"],"ABSTAIN")

    def test_unknown_kernel_abstains(self):
        self.assertEqual(shutter_gate(case(kernel="rolling"))["decision"],"ABSTAIN")

    def test_overlapping_shutter_abstains(self):
        self.assertEqual(shutter_gate(case(exposure_ms=10))["decision"],"ABSTAIN")

    def test_support_only_more_conservative(self):
        uniform=shutter_gate(case(exposure_ms=2))
        support=shutter_gate(case(exposure_ms=2,kernel="support_symmetric"))
        self.assertLessEqual(support.get("critical_gap_ms",0),
                             uniform.get("critical_gap_ms",0))

    def test_shutter_averaged_witness_no_false_exclusion(self):
        # Independently integrate a piecewise-linear path with known signed slopes.
        C,O,c=300,200,2
        dt=(3-c)/C+(3-c)/O
        tclose=(3-c)/C
        def a(t):
            return 3-C*t if t <= tclose else c+O*(t-tclose)
        e=0.002
        def avg(center):
            n=1000
            return sum(a(center-e/2+e*(j+0.5)/n) for j in range(n))/n
        d=case(apertures_mm=[avg(0),avg(dt)],
               times_ms=[0,dt*1000],exposure_ms=e*1000)
        self.assertEqual(shutter_gate(d)["decision"],"NOT_EXCLUDED")

    def test_shutter_randomized_piecewise_witness(self):
        rng=random.Random(1457)
        for _ in range(400):
            C=rng.uniform(100,600);O=rng.uniform(100,600)
            c=rng.uniform(0.2,2)
            a0=c+rng.uniform(0.1,1.5)
            a1=c+rng.uniform(0.1,1.5)
            tdown=(a0-c)/C
            tup=(a1-c)/O
            dt=tdown+tup+rng.uniform(0,0.01)
            e=min(dt*0.15,0.001)
            def path(t):
                if t<=tdown: return a0-C*t
                if t<=tdown+(dt-tdown-tup): return c
                return c+O*(t-(dt-tup))
            def avg(t):
                n=50
                return sum(path(t-e/2+e*(j+.5)/n) for j in range(n))/n
            d=case(closing_mm_s=C,opening_mm_s=O,threshold_mm=c,
                   apertures_mm=[avg(0),avg(dt)],
                   times_ms=[0,dt*1000],exposure_ms=e*1000)
            self.assertNotEqual(shutter_gate(d)["decision"],"EXCLUDED_CONDITIONALLY")


class HumanAuditControls(unittest.TestCase):
    def test_wrong_checksum_rejected(self):
        with self.assertRaisesRegex(ValueError,"SHA256"):
            parse_csv(b"subject,target_pos,peak_closing_velocity,peak_opening_velocity\n")

    def test_aggregate_no_identifiers(self):
        rows=[]
        for subject in range(1,18):
            rows.append({"subject":subject,"gaze":"center",
                         "closing":100.0+subject,"opening":60.0+subject})
        r=audit_rows(rows,{"negative":17})
        self.assertEqual(r["participants"],{"calibration":12,"holdout":5})
        self.assertFalse(r["physical_release_authorized"])
        self.assertEqual(r["product_claim"],ABSTAIN)
        self.assertNotIn("subject",r)

    def test_overlap_rejected(self):
        rows=[{"subject":s,"gaze":"center","closing":100,"opening":100}
              for s in range(1,16)]
        with self.assertRaises(ValueError):
            audit_rows(rows,{"positive":15})


if __name__=="__main__":
    unittest.main()
