import unittest
from fractions import Fraction as Q
from e002_570_exposure_average import (A,F,H,KNOTS,MINIMUM,THETA,V,W,at,bound,mean_on,
                                        report,validate_path)


class ExposureAverageTests(unittest.TestCase):
    def test_path_and_shutter_means(self):
        self.assertTrue(validate_path())
        self.assertEqual(mean_on(0,W),A)
        self.assertEqual(mean_on(F,F+W),A)

    def test_exact_naive_false_exclusion(self):
        self.assertGreater((2*A-V*H)/2,THETA)
        self.assertLess(at((W+F)/2),THETA)

    def test_correct_bound_sharp(self):
        got=bound(A,A,v=V,gap=H,width_a=W,width_b=W,boxcar_authenticated=True)
        self.assertEqual(got['lower_bound'],MINIMUM)
        self.assertLess(got['lower_bound'],THETA)

    def test_uncertified_transfer_abstains(self):
        self.assertEqual(bound(A,A,v=V,gap=H,width_a=W,width_b=W)['decision'],
                         'ABSTAIN_UNCALIBRATED')

    def test_more_uncertainty_never_strengthens(self):
        base=bound(A,A,v=V,gap=H,width_a=W,width_b=W,boxcar_authenticated=True)['lower_bound']
        for params in ({'aperture_error':Q(1,100)}, {'clock_error':Q(1,1000)},
                       {'width_a':2*W}, {'width_b':2*W}, {'gap':H+Q(1,1000)}):
            kwargs={'v':V,'gap':H,'width_a':W,'width_b':W,'boxcar_authenticated':True}
            kwargs.update(params)
            self.assertLessEqual(bound(A,A,**kwargs)['lower_bound'],base)

    def test_invalid_inputs_rejected(self):
        for kwargs in ({'v':0}, {'gap':-1}, {'width_a':0}, {'aperture_error':-1},
                       {'clock_error':-1}, {'v':True}, {'gap':'NaN'}):
            args={'v':V,'gap':H,'width_a':W,'width_b':W,'boxcar_authenticated':True}
            args.update(kwargs)
            with self.assertRaises(ValueError):bound(A,A,**args)

    def test_invalid_path_rejected(self):
        bad=list(KNOTS);bad[2]=(bad[2][0],Q(-1,10))
        with self.assertRaises(ValueError):validate_path(bad)
        bad=list(KNOTS);bad[2]=(bad[2][0],Q(0))
        with self.assertRaises(ValueError):validate_path(bad)

    def test_report_preserves_release_block(self):
        r=report()
        self.assertEqual(r['product'],'ABSTAIN_UNCALIBRATED')
        self.assertFalse(r['human_measurement'])
        self.assertTrue(r['naive_false_exclusion'])

    def test_numerical_independent_midpoint_quadrature(self):
        # Independent numerical midpoint Riemann integration, not mean_on's trapezoids.
        for s,e in ((Q(0),W),(F,F+W)):
            n=4096
            avg=sum(float(at(s+(e-s)*Q(2*i+1,2*n))) for i in range(n))/n
            self.assertAlmostEqual(avg,float(A),delta=1e-6)


if __name__=='__main__':unittest.main()
