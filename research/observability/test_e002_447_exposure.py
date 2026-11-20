"""Independent numerical and adversarial oracles for frozen E002-447."""
import unittest
import numpy as np
from scipy.optimize import linprog
from e002_447_exposure import (mean_distance_boxcar, lower_boxcar, lower_known_kernel,
                                lower_support_only, shutter_average_piecewise_witness,
                                product_gate, experiment)

class ExposureTests(unittest.TestCase):
    def test_preregistered_equal_means_different_closure(self):
        e=experiment()
        self.assertEqual(e["boxcar_sharp_center_lower_mm"],2.4)
        self.assertTrue(e["point_substitution_claims_open"])
        self.assertTrue(e["witness_has_hidden_closure"])
        self.assertFalse(e["observation_identifies_closure_status"])

    def test_independent_discrete_linear_programming_oracle(self):
        # Independent 81-knot LP: minimize center aperture subject to
        # trapezoid mean 3, neighboring slope <=240, nonnegative apertures.
        n=81; t=np.linspace(-.005,.005,n); h=t[1]-t[0]
        wt=np.ones(n);wt[0]=wt[-1]=.5;wt=wt/wt.sum()
        c=np.zeros(n);c[n//2]=1
        A=[]; b=[]
        for i in range(n-1):
            p=np.zeros(n);p[i+1]=1;p[i]=-1
            A.extend([p,-p]);b.extend([240*h,240*h])
        sol=linprog(c,A_ub=np.asarray(A),b_ub=np.asarray(b),
                    A_eq=wt[None,:],b_eq=np.array([3.]),bounds=(0,None),method="highs")
        self.assertTrue(sol.success,sol.message)
        self.assertAlmostEqual(sol.x[n//2],2.4,delta=1e-6)

    def test_dense_independent_quadrature(self):
        x=np.linspace(-.005,.005,100001)
        y=2.4+240*np.abs(x)
        self.assertAlmostEqual(float(np.trapezoid(y,x)/.01),3.,delta=1e-8)
        self.assertAlmostEqual(float(np.min(y)),2.4,delta=1e-12)
        self.assertLessEqual(float(np.max(np.abs(np.diff(y)/np.diff(x)))),240.00001)

    def test_unknown_kernel_support_only(self):
        self.assertAlmostEqual(lower_support_only(3,240,0,0,.01),1.8)
        self.assertGreater(lower_boxcar(3,240,0,0,.01),lower_support_only(3,240,0,0,.01))

    def test_known_two_point_kernel(self):
        self.assertAlmostEqual(lower_known_kernel(3,240,0,[-.005,.005],[.5,.5]),1.8)
        self.assertAlmostEqual(lower_known_kernel(3,240,0,[0],[1]),3)

    def test_clock_error_exact_boxcar(self):
        self.assertAlmostEqual(lower_boxcar(3,240,0,0,.01,.001),2.376)
        self.assertAlmostEqual(lower_boxcar(3,240,0,0,.01,.006),1.56)

    def test_noncentered_integral(self):
        self.assertAlmostEqual(mean_distance_boxcar(.002,0,.01),.0029)
        self.assertAlmostEqual(mean_distance_boxcar(.01,0,.01),.01)

    def test_rolling_shutter_per_row_offset(self):
        center_row0=lower_boxcar(3,240,0,0,.01)
        center_row1=lower_boxcar(3,240,0,.004,.01)
        self.assertGreater(center_row0,center_row1)
        self.assertAlmostEqual(center_row1,2.016)

    def test_strict_threshold_equality_not_certificate(self):
        self.assertFalse(lower_boxcar(3,240,0,0,.01)>2.4)

    def test_scaled_nonnegative_witness(self):
        xs=np.linspace(-.005,.005,10001)
        ys=np.array([shutter_average_piecewise_witness(.3,240,.01,float(t)) for t in xs])
        self.assertAlmostEqual(float(np.trapezoid(ys,xs)/.01),.3,delta=1e-7)
        self.assertAlmostEqual(float(ys.min()),0,delta=1e-12)
        self.assertLessEqual(float(np.max(np.abs(np.diff(ys)/np.diff(xs)))),240.00001)

    def test_nonnegative_clamp(self):
        self.assertEqual(lower_boxcar(.01,240,0,0,.01),0)

    def test_invalid_physical_parameters_rejected(self):
        for bad in (-1.,float('nan'),float('inf'),True):
            with self.assertRaises(ValueError):lower_boxcar(3,bad,0,0,.01)
            with self.assertRaises(ValueError):lower_boxcar(bad,240,0,0,.01)
        with self.assertRaises(ValueError):lower_boxcar(3,240,0,0,0)
        with self.assertRaises(ValueError):lower_boxcar(3,240,0,0,.01,-.001)

    def test_invalid_kernel_rejected(self):
        for times,weights in [([],[]),([0],[.5]),([0,1],[1]),([0],[float('nan')]),([0],[-1]),([float('inf')],[1])]:
            with self.assertRaises(ValueError):lower_known_kernel(3,240,0,times,weights)

    def test_missing_calibration_fails_closed(self):
        self.assertEqual(product_gate()["status"],"ABSTAIN_UNCALIBRATED")
        self.assertFalse(product_gate()["physical_release_authorized"])
        self.assertFalse(product_gate(physical_aperture=True,calibrated_shutter=True,
                                    calibrated_clock=True,independently_bounded_velocity=True,
                                    nuisance_validated=True)["physical_release_authorized"])

    def test_unknown_image_transfer_cannot_claim_anatomy(self):
        self.assertEqual(product_gate(physical_aperture=False,calibrated_shutter=True,
                                    calibrated_clock=True,independently_bounded_velocity=True,
                                    nuisance_validated=True)["status"],"ABSTAIN_UNCALIBRATED")

    def test_negative_results_are_not_human_results(self):
        e=experiment()
        self.assertFalse(e["human_eyelid_aperture_measured"])
        self.assertFalse(e["physical_shutter_calibrated"])
        self.assertEqual(e["e002_371_physical_validation"],"NOT_ESTABLISHED")
        self.assertFalse(e["product"]["physical_release_authorized"])

if __name__ == "__main__":unittest.main()
