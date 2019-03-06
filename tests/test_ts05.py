import pytest

# import numpy as np
import numpy.testing as npt

from . import TestQC, get_codes_settings, get_codes_ids

CASE = 'ts05'

codes_settings = get_codes_settings(CASE)
ids = get_codes_ids()


@pytest.mark.parametrize('code', codes_settings, indirect=True, ids=ids)
class TestTS05(TestQC):

    def test_get_orbhess(self, code):
        """Get diagonal orbital hessian"""
        self.skip_if_not_implemented('get_orbital_diagonal', code)
        od = code.get_orbital_diagonal()
        npt.assert_allclose(
            od,
            [
               41.00677865, 22.60231944,  3.06863161,  2.17350289,  1.72007956,
                1.59437433,  1.53775784,  1.30506014,  1.22608156, 83.48518295,
               83.90437486, 83.90830227, 84.28146386, 84.35893666, 46.67626453,
               47.09545645, 47.09938385, 47.47254544, 47.55001824,  7.60888886,
                8.02808077,  8.03200818,  8.40516977,  8.48264257,  5.81863142,
                6.23782333,  6.24175074,  6.61491233,  6.69238513,  4.91178477,
                5.33097669,  5.33490409,  5.70806568,  5.78553848,  4.66037430,
                5.07956622,  5.08349362,  5.45665522,  5.53412801,  4.54714131,
                4.96633323,  4.97026064,  5.34342223,  5.42089502,  4.08174591,
                4.50093783,  4.50486523,  4.87802683,  4.95549962,  3.92378875,
                4.34298067,  4.34690807,  4.72006966,  4.79754246,  1.70617871,
                1.91577467,  1.91773837,  2.10431917,  2.14305557
            ]*2
        )

    def test_get_s2_diagonal(self, code):
        """Get diagonal overlap hessian"""
        self.skip_if_not_implemented('get_overlap_diagonal', code)
        sd = code.get_overlap_diagonal()
        npt.assert_allclose(
            sd,
            [
                1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  2.,  2.,  2.,  2.,
                2.,  2.,  2.,  2.,  2.,  2.,  2.,  2.,  2.,  2.,  2.,  2.,  2.,
                2.,  2.,  2.,  2.,  2.,  2.,  2.,  2.,  2.,  2.,  2.,  2.,  2.,
                2.,  2.,  2.,  2.,  2.,  2.,  2.,  2.,  2.,  2.,  2.,  2.,  2.,
                2.,  2.,  1.,  1.,  1.,  1.,  1., -1., -1., -1., -1., -1., -1.,
               -1., -1., -1., -2., -2., -2., -2., -2., -2., -2., -2., -2., -2.,
               -2., -2., -2., -2., -2., -2., -2., -2., -2., -2., -2., -2., -2.,
               -2., -2., -2., -2., -2., -2., -2., -2., -2., -2., -2., -2., -2.,
               -2., -2., -2., -2., -2., -2., -2., -2., -2., -1., -1., -1., -1.,
               -1.
            ]
        )

    def test_get_rhs(self, code):
        """Get property gradient right-hand side"""
        self.skip_if_not_implemented('get_rhs', code)
        rhs,  = code.get_rhs('z',)
        npt.assert_allclose(
           rhs,
           [
            -1.48251297e-02,  5.13302629e-02,  9.18657332e-03,
             1.54660818e-01,  2.28809494e-01,  9.05135605e-01,
             2.27239876e-01,  6.06045447e-01,  7.18913015e-01,
             5.37075465e-02, -1.43519982e-02, -1.72356542e-04,
             4.05547064e-02, -1.97833927e-03,  1.79278651e-02,
             3.02657642e-02, -1.06429371e-01, -6.80873427e-02,
             4.92520891e-02, -1.19349286e-01,  3.09367480e-02,
             2.58027313e-03, -1.17530078e-01,  1.55781719e-02,
             2.24349241e-01,  3.59499781e-02,  1.19769226e-01,
             2.34064525e-01,  2.18829032e-01,  7.32395054e-01,
            -5.38952462e-02,  1.93478321e-01,  6.20689962e-01,
             1.95374331e-01,  1.66007607e-01,  1.71714303e-01,
            -2.17422402e-01, -1.12765080e-01,  2.51505716e-02,
            -3.95298805e-01,  1.69579904e-01,  1.14130059e+00,
             2.93965289e-01,  2.45672320e-01, -5.57117405e-01,
             1.36970683e-01,  6.17930613e-01, -1.41165371e-01,
            -1.60576142e-02,  1.92781844e-01, -7.86646168e-02,
            -7.49187628e-02,  9.21618696e-02, -3.04688483e-01,
             1.74171495e-01,  4.07313930e-01, -1.21940203e-01,
            -3.18514647e-01,  1.08885566e+00,  1.48251297e-02,
            -5.13302629e-02, -9.18657332e-03, -1.54660818e-01,
            -2.28809494e-01, -9.05135605e-01, -2.27239876e-01,
            -6.06045447e-01, -7.18913015e-01, -5.37075465e-02,
             1.43519982e-02,  1.72356542e-04, -4.05547064e-02,
             1.97833927e-03, -1.79278651e-02, -3.02657642e-02,
             1.06429371e-01,  6.80873427e-02, -4.92520891e-02,
             1.19349286e-01, -3.09367480e-02, -2.58027313e-03,
             1.17530078e-01, -1.55781719e-02, -2.24349241e-01,
            -3.59499781e-02, -1.19769226e-01, -2.34064525e-01,
            -2.18829032e-01, -7.32395054e-01,  5.38952462e-02,
            -1.93478321e-01, -6.20689962e-01, -1.95374331e-01,
            -1.66007607e-01, -1.71714303e-01,  2.17422402e-01,
             1.12765080e-01, -2.51505716e-02,  3.95298805e-01,
            -1.69579904e-01, -1.14130059e+00, -2.93965289e-01,
            -2.45672320e-01,  5.57117405e-01, -1.36970683e-01,
            -6.17930613e-01,  1.41165371e-01,  1.60576142e-02,
            -1.92781844e-01,  7.86646168e-02,  7.49187628e-02,
            -9.21618696e-02,  3.04688483e-01, -1.74171495e-01,
            -4.07313930e-01,  1.21940203e-01,  3.18514647e-01,
            -1.08885566e+00
           ],
           atol=1e-8
        )

    @pytest.mark.parametrize(
        'args',
        [
            (
                'z', (0.0,),
                {
                    ('z', 0.0):
                    [
                    -3.61528758e-04,  2.27101749e-03,  2.99370355e-03,
                     7.11574016e-02,  1.33022622e-01,  5.67705831e-01,
                     1.47773512e-01,  4.64381242e-01,  5.86350078e-01,
                     6.43318306e-04, -1.71051846e-04, -2.05410594e-06,
                     4.81181799e-04, -2.34514487e-05,  3.84089543e-04,
                     6.42647220e-04, -2.25967650e-03, -1.43424672e-03,
                     1.03579538e-03, -1.56855079e-02,  3.85356711e-03,
                     3.21248818e-04, -1.39830701e-02,  1.83647628e-03,
                     3.85570463e-02,  5.76322479e-03,  1.91884026e-02,
                     3.53843729e-02,  3.26982127e-02,  1.49109761e-01,
                    -1.01098259e-02,  3.62665041e-02,  1.08739106e-01,
                     3.37694290e-02,  3.56210889e-02,  3.38049147e-02,
                    -4.27702713e-02, -2.06656048e-02,  4.54463134e-03,
                    -8.69334771e-02,  3.41458972e-02,  2.29625903e-01,
                     5.50144228e-02,  4.53195126e-02, -1.36489977e-01,
                     3.04315874e-02,  1.37169611e-01, -2.89390314e-02,
                    -3.24036230e-03,  4.91315552e-02, -1.81130479e-02,
                    -1.72349545e-02,  1.95255316e-02, -6.35092832e-02,
                     1.02082797e-01,  2.12610562e-01, -6.35854215e-02,
                    -1.51362327e-01,  5.08085591e-01,  3.61528758e-04,
                    -2.27101749e-03, -2.99370355e-03, -7.11574016e-02,
                    -1.33022622e-01, -5.67705831e-01, -1.47773512e-01,
                    -4.64381242e-01, -5.86350078e-01, -6.43318306e-04,
                     1.71051846e-04,  2.05410594e-06, -4.81181799e-04,
                     2.34514487e-05, -3.84089543e-04, -6.42647220e-04,
                     2.25967650e-03,  1.43424672e-03, -1.03579538e-03,
                     1.56855079e-02, -3.85356711e-03, -3.21248818e-04,
                     1.39830701e-02, -1.83647628e-03, -3.85570463e-02,
                    -5.76322479e-03, -1.91884026e-02, -3.53843729e-02,
                    -3.26982127e-02, -1.49109761e-01,  1.01098259e-02,
                    -3.62665041e-02, -1.08739106e-01, -3.37694290e-02,
                    -3.56210889e-02, -3.38049147e-02,  4.27702713e-02,
                     2.06656048e-02, -4.54463134e-03,  8.69334771e-02,
                    -3.41458972e-02, -2.29625903e-01, -5.50144228e-02,
                    -4.53195126e-02,  1.36489977e-01, -3.04315874e-02,
                    -1.37169611e-01,  2.89390314e-02,  3.24036230e-03,
                    -4.91315552e-02,  1.81130479e-02,  1.72349545e-02,
                    -1.95255316e-02,  6.35092832e-02, -1.02082797e-01,
                    -2.12610562e-01,  6.35854215e-02,  1.51362327e-01,
                    -5.08085591e-01
                    ]
                }
            ),
            (
                'z', (0.5,),
                {
                    ('z', 0.5):
                    [
                    -3.65991329e-04,  2.32239259e-03,  3.57644642e-03,
                     9.24174192e-02,  1.87536535e-01,  8.27080442e-01,
                     2.18971968e-01,  7.52795250e-01,  9.90127087e-01,
                     6.51117504e-04, -1.73115089e-04, -2.07888158e-06,
                     4.86959577e-04, -2.37327796e-05,  3.92498496e-04,
                     6.56588881e-04, -2.30869400e-03, -1.46510896e-03,
                     1.05804661e-03, -1.80589035e-02,  4.40187713e-03,
                     3.66932612e-04, -1.58713550e-02,  2.08190779e-03,
                     4.65587054e-02,  6.86353391e-03,  2.28490884e-02,
                     4.16862296e-02,  3.84424152e-02,  1.87227850e-01,
                    -1.24441321e-02,  4.46326648e-02,  1.31835451e-01,
                     4.08259869e-02,  4.53526316e-02,  4.20913140e-02,
                    -5.32442123e-02, -2.53026260e-02,  5.54694785e-03,
                    -1.11441516e-01,  4.27548302e-02,  2.87462384e-01,
                     6.76805694e-02,  5.55707202e-02, -1.80779799e-01,
                     3.91239976e-02,  1.76306526e-01, -3.64013396e-02,
                    -4.05956660e-03,  6.59356268e-02, -2.35312808e-02,
                    -2.23844698e-02,  2.47742322e-02, -8.02330681e-02,
                     1.44399410e-01,  2.87696862e-01, -8.60103705e-02,
                    -1.98535711e-01,  6.62701662e-01,  3.57173701e-04,
                    -2.22186621e-03, -2.57425656e-03, -5.78495047e-02,
                    -1.03063646e-01, -4.32174703e-01, -1.11514662e-01,
                    -3.35748064e-01, -4.16500027e-01, -6.35703737e-04,
                     1.69037205e-04,  2.02991389e-06, -4.75539520e-04,
                     2.31767094e-05, -3.76033343e-04, -6.29285309e-04,
                     2.21269718e-03,  1.40465788e-03, -1.01446077e-03,
                     1.38634948e-02, -3.42672477e-03, -2.85681000e-04,
                     1.24963271e-02, -1.64280914e-03, -3.29023857e-02,
                    -4.96695987e-03, -1.65387115e-02, -3.07376519e-02,
                    -2.84474878e-02, -1.23887300e-01,  8.51294340e-03,
                    -3.05416339e-02, -9.25289035e-02, -2.87927527e-02,
                    -2.93280265e-02, -2.82444991e-02,  3.57397270e-02,
                     1.74649375e-02, -3.84910911e-03,  7.12617153e-02,
                    -2.84228013e-02, -1.91164282e-01, -4.63417504e-02,
                    -3.82613825e-02,  1.09631102e-01, -2.48995148e-02,
                    -1.12251724e-01,  2.40157753e-02,  2.69626651e-03,
                    -3.91531509e-02,  1.47229836e-02,  1.40116048e-02,
                    -1.61120187e-02,  5.25547652e-02, -7.89471377e-02,
                    -1.68605928e-01,  5.04356485e-02,  1.22302462e-01,
                    -4.11968507e-01
                    ],
                }
            ),
        ],
        ids=['0.0', '0.5']
    )
    def test_initial_guess(self, code, args):
        """form paired trialvectors from rhs/orbdiag"""
        self.skip_if_not_implemented('initial_guess', code)
        ops, freqs, expected = args
        initial_guess = code.initial_guess(ops, freqs)
        for op, freq in zip(ops, freqs):
            npt.assert_allclose(
                initial_guess[(op, freq)],
                expected[(op, freq)],
                rtol=1e-5,
            )

    @pytest.mark.parametrize(
        'args',
        [
            ('x', 'x', (0,), {('x', 'x', 0): -1.215905666867e+01}),
            ('y', 'y', (0,), {('y', 'y', 0): -9.699185321673e+00}),
            ('z', 'z', (0,), {('z', 'z', 0): -1.508379114291e+01}),
            ('x', 'x', (0.5,), {('x', 'x', 0.5): -1.706905765691e+01}),
            ('y', 'y', (0.5,), {('y', 'y', 0.5): -1.429413459045e+01}),
            ('z', 'z', (0.5,), {('z', 'z', 0.5): -2.184427949501e+01}),
        ],
        ids=['xx0', 'yy0', 'zz0', 'xx0.5', 'yy0.5', 'zz0.5']
    )
    def test_lr(self, code, args):
        aops, bops, freqs, expected = args
        self.skip_if_not_implemented('lr', code)
        lr = code.lr(aops, bops, freqs)
        for k, v in lr.items():
            npt.assert_allclose(v, expected[k], rtol=1e-4)
