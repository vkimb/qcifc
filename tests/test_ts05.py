import pytest
import os
import subprocess
import numpy.testing as npt

from qcifc.core import QuantumChemistry, DaltonFactory

CASE = 'ts05'

@pytest.fixture(params=[
    'DaltonDummy',
    'Dalton'
    ])
def qcp(request):
    tmp = os.path.join(os.path.dirname(__file__), f'test_{CASE}.d')
    factory = QuantumChemistry.set_code(
            request.param,
            tmpdir=tmp,
            )
    return factory

@pytest.fixture(scope='module')
def mod():
    tmpdir = os.path.join(os.path.dirname(__file__), f'test_{CASE}.d')
    os.chdir(tmpdir)
    subprocess.call(['dalton', '-get', 'AOPROPER AOONEINT AOTWOINT', 'hf', CASE])
    subprocess.call(['tar', 'xvfz', f'hf_{CASE}.tar.gz'])
    yield
    subprocess.call('rm *.[0-9] DALTON.* *AO* *SIR* *RSP* molden.inp', shell=True)
    
@pytest.mark.skip()
def test_get_orbhess(mod, qcp):
    """Get diagonal orbital hessian"""
    od = qcp.get_orbital_diagonal() 
    npt.assert_allclose(od,
        [
       22.50562709,  2.24032568,  1.53428489,  1.53011492,  1.53007521,
       46.83994822, 47.05912145, 47.05930122, 47.36602961,  6.3093454 ,
        6.52851863,  6.52869841,  6.8354268 ,  4.89726383,  5.11643706,
        5.11661683,  5.42334522,  4.88892388,  5.1080971 ,  5.10827688,
        5.41500527,  4.88884446,  5.10801769,  5.10819746,  5.41492585,
        1.96034256,  2.06992917,  2.07001906,  2.22338326,
       22.50562709,  2.24032568,  1.53428489,  1.53011492,  1.53007521,
       46.83994822, 47.05912145, 47.05930122, 47.36602961,  6.3093454 ,
        6.52851863,  6.52869841,  6.8354268 ,  4.89726383,  5.11643706,
        5.11661683,  5.42334522,  4.88892388,  5.1080971 ,  5.10827688,
        5.41500527,  4.88884446,  5.10801769,  5.10819746,  5.41492585,
        1.96034256,  2.06992917,  2.07001906,  2.22338326,
        ]
    )

@pytest.mark.skip()
def test_get_s2_diagonal(mod, qcp):
    """Get diagonal overlap hessian"""
    sd = qcp.get_overlap_diagonal() 
    lsd = len(sd)
    npt.assert_allclose(
        sd,
        [
         1.,  1.,  1.,  1.,  1.,  2.,  2.,  2.,  2.,  2.,  2.,  2.,  2.,
         2.,  2.,  2.,  2.,  2.,  2.,  2.,  2.,  2.,  2.,  2.,  2.,  1.,
         1.,  1.,  1., -1., -1., -1., -1., -1., -2., -2., -2., -2., -2.,
        -2., -2., -2., -2., -2., -2., -2., -2., -2., -2., -2., -2., -2.,
        -2., -2., -1., -1., -1., -1.
        ]
    )
    

@pytest.mark.skip()
def test_get_rhs(mod, qcp):
    """Get property gradient right-hand side"""
    rhs,  = qcp.get_rhs('z',) 
    npt.assert_allclose(
       rhs,
       [ 
         -0.06424202, -0.26969476, -1.35999663,  0.00432427, -0.01249358,
          0.08319511,  0.03594166,  0.06190557,  0.06392394,  0.05298973,
         -0.0725147 , -0.1248824 ,  0.18943574, -0.11208718, -0.0943026 ,
         -0.16221828, -0.42765456,  0.51903989,  0.47306665,  0.8145972 ,
         -0.13004304, -0.30197662, -0.27519894, -0.47387762,  0.07232298,
          0.55885248, -0.06104317, -0.10486355,  1.13508306,  0.06424202,
          0.26969476,  1.35999663, -0.00432427,  0.01249358, -0.08319511,
         -0.03594166, -0.06190557, -0.06392394, -0.05298973,  0.0725147 ,
          0.1248824 , -0.18943574,  0.11208718,  0.0943026 ,  0.16221828,
          0.42765456, -0.51903989, -0.47306665, -0.8145972 ,  0.13004304,
          0.30197662,  0.27519894,  0.47387762, -0.07232298, -0.55885248,
          0.06104317,  0.10486355, -1.13508306
       ],
       atol=1e-8 
    )

@pytest.mark.skip()
@pytest.mark.parametrize('args',
    [
        (
            'z', (0.0,),
            {('z', 0.0): 
                [
                  -2.85448687e-03, -1.20381943e-01, -8.86404238e-01,
                   2.82611068e-03, -8.16533753e-03,  1.77615710e-03,
                   7.63755351e-04,  1.31547995e-03,  1.34957346e-03,
                   8.39861013e-03, -1.11073739e-02, -1.91282228e-02,
                   2.77138129e-02, -2.28877145e-02, -1.84313019e-02,
                  -3.17042063e-02, -7.88543858e-02,  1.06166490e-01,
                   9.26111310e-02,  1.59466142e-01, -2.40153119e-02,
                  -6.17685055e-02, -5.38758778e-02, -9.27680707e-02,
                   1.33562272e-02,  2.85078991e-01, -2.94904623e-02,
                  -5.06582514e-02,  5.10520645e-01,  2.85448687e-03,
                   1.20381943e-01,  8.86404238e-01, -2.82611068e-03,
                   8.16533753e-03, -1.77615710e-03, -7.63755351e-04,
                  -1.31547995e-03, -1.34957346e-03, -8.39861013e-03,
                   1.11073739e-02,  1.91282228e-02, -2.77138129e-02,
                   2.28877145e-02,  1.84313019e-02,  3.17042063e-02,
                   7.88543858e-02, -1.06166490e-01, -9.26111310e-02,
                  -1.59466142e-01,  2.40153119e-02,  6.17685055e-02,
                   5.38758778e-02,  9.27680707e-02, -1.33562272e-02,
                  -2.85078991e-01,  2.94904623e-02,  5.06582514e-02,
                  -5.10520645e-01
                ]
            }
        ),
        (
            'z', (0.5,),
            { ('z', 0.5): 
                [
                -2.91934499e-03, -1.54967981e-01, -1.31491491e+00,
                 4.19785602e-03, -1.21288042e-02,  1.81490403e-03,
                 7.80337417e-04,  1.34404052e-03,  1.37868041e-03,
                 9.98046429e-03, -1.31164788e-02, -2.25880286e-02,
                 3.24630479e-02, -2.87604795e-02, -2.29087909e-02,
                -3.94057261e-02, -9.66812525e-02,  1.33466200e-01,
                 1.15154690e-01,  1.98281963e-01, -2.94547871e-02,
                -7.76520169e-02, -6.69906894e-02, -1.15349281e-01,
                 1.63814710e-02,  3.82685881e-01, -3.88827530e-02,
                -6.67912565e-02,  6.58636464e-01,  2.79244799e-03,
                 9.84170457e-02,  6.68537940e-01, -2.13006371e-03,
                 6.15424516e-03, -1.73903003e-03, -7.47863356e-04,
                -1.28810794e-03, -1.32167013e-03, -7.24958656e-03,
                 9.63200076e-03,  1.65875150e-02, -2.41768246e-02,
                 1.90066410e-02,  1.54178969e-02,  2.65209151e-02,
                 6.65781679e-02, -8.81383256e-02, -7.74491043e-02,
                -1.33359574e-01,  2.02716966e-02,  5.12794349e-02,
                 4.50553602e-02,  7.75805999e-02, -1.12741724e-02,
                -2.27144174e-01,  2.37528601e-02,  4.08026335e-02,
                -4.16791523e-01
                ],
            }
        ),
    ],
    ids=['0.0', '0.5']
)
def test_initial_guess(mod, qcp, args):
    """form paired trialvectors from rhs/orbdiag"""
    ops, freqs, expected = args
    initial_guess = qcp.initial_guess(ops, freqs)
    for op, freq in zip(ops, freqs):
        npt.assert_allclose(
            initial_guess[(op, freq)],
            expected[(op, freq)],
            rtol=1e-5,
        )

@pytest.mark.parametrize('args',
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
def test_lr(mod, qcp, args):
    aops, bops, freqs, expected = args
    lr = qcp.lr(aops, bops, freqs)
    for k, v in lr.items():
        npt.assert_allclose(v, expected[k], rtol=1e-4)