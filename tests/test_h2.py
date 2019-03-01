import pathlib
import itertools

import pytest
import numpy
import numpy.testing as npt

from . import codes
from . import TestQC

CASE = 'h2'
test_root = pathlib.Path(__file__).parent
test_dir = test_root/f'test_{CASE}.d'
settings = [dict(
    case=CASE,
    xyz=test_dir/f'{CASE}.xyz',
    inp=test_dir/f'{CASE}.inp',
    out=test_dir/f'{CASE}.out',
    basis=test_root/'bases'/'STO-3G',
    _tmpdir=test_dir,
)]


#
# code fixture takes params from  codes, avaliable in request.param
# purpose to inject parameters into the fixture
#
codes_settings = list(itertools.product(codes.values(), settings))
ids = list(codes.keys())


@pytest.mark.parametrize('code', codes_settings, indirect=True, ids=ids)
class TestH2(TestQC):

    def test_get_wrkdir(self, code):
        """Get factory workdir"""
        assert code.get_workdir() == test_dir

    def test_set_wrkdir(self, code):
        """Get factory workdir"""
        code.set_workdir('/tmp/123')
        assert code.get_workdir() == '/tmp/123'

    def test_get_overlap(self, code):
        """Get overlap"""
        npt.assert_allclose(
            code.get_overlap(),
            [[1.0, 0.65987313], [0.65987313, 1.0]]
        )

    def test_get_h1(self, code):
        """Get one-electron Hamiltonian"""
        npt.assert_allclose(
            code.get_one_el_hamiltonian(),
            [[-1.12095946, -0.95937577], [-0.95937577, -1.12095946]]
            )

    def test_get_z(self, code):
        """Nuclear repulsion energy"""
        assert code.get_nuclear_repulsion() == pytest.approx(0.7151043)

    def test_get_mo(self, code):
        """Read MO coefficients"""
        code.run_scf()
        cmo = code.get_mo()
        expected = [
             [.54884227, -1.212451936],
             [.54884227, 1.21245193]
        ]
        try:
            npt.assert_allclose(cmo, expected)
        except AssertionError:
            npt.assert_allclose(-cmo, expected)

    def test_set_get_dens_a(self, code):
        """Set density test"""
        code.run_scf()
        da = [[1., 0.], [0., 1.]]
        db = [[1., 0.], [0., 0.]]
        code.set_densities(da, db)
        da1, db1 = code.get_densities()
        npt.assert_allclose(da1, da)
        npt.assert_allclose(db1, db)

    def test_get_two_fa(self, code):
        """Get alpha Fock matrix"""
        code.run_scf()

        da = numpy.array([[1., 0.], [0., 1.]])
        db = numpy.array([[1., 0.], [0., 0.]])
        faref = numpy.array([
            [1.04701025, 0.44459112],
            [0.44459112, 0.8423992]
        ])

        fbref = numpy.array([
            [1.34460081, 0.88918225],
            [0.88918225, 1.61700513]
        ])
        code.set_densities(da, db)
        fa, fb = code.get_two_el_fock()
        npt.assert_allclose(fa, faref)
        npt.assert_allclose(fb, fbref)

    def test_get_orbhess(self, code):
        """Get diagonal orbital hessian"""
        self.skip_if_not_implemented('get_orbital_diagonal', code)
        od = code.get_orbital_diagonal()
        npt.assert_allclose(od, [4.99878931, 4.99878931])

    def test_get_rhs(self, code):
        """Get property gradient right-hand side"""
        self.skip_if_not_implemented('get_rhs', code)

        x, y, z = code.get_rhs('x', 'y', 'z')
        npt.assert_allclose(x, [0, 0])
        npt.assert_allclose(y, [0, 0])
        npt.assert_allclose(z, [1.86111268, -1.86111268])
        npt.assert_allclose((x, y, z), ([0, 0], [0, 0], [1.86111268, -1.86111268]))

    @pytest.mark.parametrize(
        'trials',
        [
            ([1, 0], [1.89681370, -0.36242092]),
            ([0, 1], [-0.36242092, 1.89681370]),
            ([[1, 0],
              [0, 1]],
             [[1.89681370, -0.36242092],
              [-0.36242092, 1.89681370]]),
        ]
    )
    def test_oli(self, code, trials):
        """Linear transformation E2*N"""
        self.skip_if_not_implemented('e2n', code)
        n, e2n = trials
        numpy.testing.assert_allclose(code.e2n(n), e2n)

    def test_sli(self, code):
        """Linear transformation S2*N"""
        self.skip_if_not_implemented('s2n', code)
        if 's2n' not in dir(code):
            pytest.skip('not implemented')
        absolute_tolerance = 1e-10
        s2n = code.s2n([1, 0])
        npt.assert_allclose(
            s2n, [2.00000000,  0.00000000],
            atol=absolute_tolerance
        )
        s2n = code.s2n([0, 1])
        npt.assert_allclose(
            s2n, [0.00000000, -2.00000000],
            atol=absolute_tolerance
        )

    @pytest.mark.parametrize(
        'args',
        [
            ('x', (0,), {('x', 0): [0, 0]},),
            ('z', (0,), {('z', 0): [0.37231269, -0.37231269]}),
            ('z', (0.5,), {('z', 0.5): [0.46541904, -0.31024805]}),
            (
                'z', (0, 0.5),
                {
                    ('z', 0): [0.37231269, -0.37231269],
                    ('z', 0.5): [0.46541904, -0.31024805]
                }
            ),
            (
                'xz', (0,),
                {
                    ('x', 0): [0.0, 0.0],
                    ('z', 0): [0.37231269, -0.37231269],
                }
            ),
            (
                'xz', (0.5,),
                {
                    ('x', 0.5): [0., 0.],
                    ('z', 0.5): [-0.31024805, 0.46541904]
                }
            ),
            (
                'xz', (0, 0.5),
                {
                    ('x', 0): [0., 0.],
                    ('x', 0.5): [0., 0.],
                    ('z', 0): [0.37231269, -0.37231269],
                    ('z', 0.5): [0.46541904, -0.31024805],
                }
            )
        ],
        ids=['x-0', 'z-0', 'z-0.5', 'z-(0, 0.5)', 'xz-0', 'xz-0.5', 'xz-(0, 0.5)']
    )
    def test_initial_guess(self, code, args):
        """form paired trialvectors from rhs/orbdiag"""
        self.skip_if_not_implemented('initial_guess', code)

        ops, freqs, expected = args
        initial_guess = code.initial_guess(ops=ops, freqs=freqs)
        for op, freq in zip(ops, freqs):
            npt.assert_allclose(
                initial_guess[(op, freq)],
                expected[(op, freq)],
                rtol=1e-5,
                )


    @pytest.mark.parametrize(
        'args',
        [
            (
                {('x', 0): [0, 0]},
                []
            ),
            (
                {('z', 0): [0.37231269, -0.37231269]},
                [[0.37231269, -0.37231269]]
            ),
            (
                {('z', 0.5): [0.46541904, -0.31024805]},
                [[0.46541904, -0.31024805], [-0.31024805, 0.46541904]]
            ),
            (
                {
                    ('z', 0): [0.37231269, -0.37231269],
                    ('z', 0.5): [0.46541904, -0.31024805]
                },
                [
                    [0.37231269, -0.37231269],
                    [0.46541904, -0.31024805],
                    [-0.31024805, 0.46541904],
                ]
            ),
            (
                {
                    ('x', 0): [0.0, 0.0],
                    ('z', 0): [0.37231269, -0.37231269],
                },
                [
                    [0.37231269, -0.37231269],
                ]
            ),
            (
                {
                    ('x', 0.5): [0., 0.],
                    ('z', 0.5): [-0.31024805, 0.46541904]
                },
                [
                    [-0.31024805, 0.46541904],
                    [0.46541904, -0.31024805],
                ]
            ),
            (
                {
                    ('x', 0): [0., 0.],
                    ('x', 0.5): [0., 0.],
                    ('z', 0): [0.37231269, -0.37231269],
                    ('z', 0.5): [0.46541904, -0.31024805],
                },
                [
                    [0.37231269, -0.37231269],
                    [0.46541904, -0.31024805],
                    [-0.31024805, 0.46541904],
                ]
            )
        ],
        ids=['x-0', 'z-0', 'z-0.5', 'z-(0, 0.5)', 'xz-0', 'xz-0.5', 'xz-(0, 0.5)']
    )
    def test_setup_trials(self, code, args):
        """
        Form paired trialvectors from initial guesses (rhs/diagonal)
        Parameterized input lists are reformatted to arrays.
        """
        self.skip_if_not_implemented('setup_trials', code)

        initial_guesses, expected = args
        ig = {
            key: numpy.array(vector)
            for key, vector in initial_guesses.items()
        }
        b = code.setup_trials(ig, renormalize=False)
        npt.assert_allclose(b.T, expected, rtol=1e-5)


    @pytest.mark.parametrize(
        'args',
        [
            ('x', (0,), {('x', 0): [0, 0]}),
            ('z', (0,), {('z', 0): [0.82378017, -0.82378017]}),
            ('z', (0.5,), {('z', 0.5): [1.91230027, -0.40322064]}),
            (
                'z', (0, 0.5),
                {
                    ('z', 0): [0.82378017, -0.82378017],
                    ('z', 0.5): [1.91230027, -0.40322064]
                }
            ),
        ],
        ids=['x-0', 'z-0', 'z-0.5', 'z-(0, 0.5)']
    )
    def test_solve(self, code, args):
        self.skip_if_not_implemented('lr_solve', code)

        ops, freqs, expected = args
        solutions = code.lr_solve(ops=ops, freqs=freqs)
        for op, freq in solutions:
            npt.assert_allclose(
                solutions[(op, freq)],
                expected[(op, freq)]
            )


    @pytest.mark.parametrize(
        'args',
        [
            ('z', 'z', (0,), {('z', 'z', 0): -3.066295447276}),
            ('z', 'z', (0.5,), {('z', 'z', 0.5): -4.309445328973108}),
        ],
        ids=['0', '0.5']
    )
    def test_lr(self, code, args):
        self.skip_if_not_implemented('lr', code)

        aops, bops, freqs, expected = args
        lr = code.lr(aops, bops, freqs)
        for k, v in lr.items():
            npt.assert_allclose(v, expected[k])

    @pytest.mark.parametrize(
        'args',
        [
            ('z', 1, {('z', 0): 1.1946797}),
        ],
        ids=['z1', ]
    )
    def test_pp(self, code, args):
        self.skip_if_not_implemented('pp', code)

        aops, nfreqs, expected = args
        pp = code.pp(aops, nfreqs)
        for k, v in pp.items():
            npt.assert_allclose(v, expected[k])

    def test_excitation_energies(self, code):
        self.skip_if_not_implemented('excitation_energies', code)

        w = code.excitation_energies(1)
        assert w == pytest.approx(0.93093411)

    def test_eigenvectors(self, code):
        self.skip_if_not_implemented('eigenvectors', code)

        X = code.eigenvectors(1)
        npt.assert_allclose(X.T, [[0.7104169615, 0.0685000673]])

    def test_dim(self, code):
        self.skip_if_not_implemented('response_dim', code)
        if 'response_dim' not in dir(code):
            pytest.skip('not implemented')

        assert code.response_dim() == 2
