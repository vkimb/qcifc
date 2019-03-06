import os

from mpi4py import MPI
import numpy as np
import veloxchem as vlx

from .core import QuantumChemistry


class VeloxChem(QuantumChemistry):

    def __init__(self, **kwargs):
        self._tmpdir = kwargs.get('tmpdir', '/tmp')
        self.comm = MPI.COMM_WORLD
        self.rank = self.comm.Get_rank()
        self.size = self.comm.Get_size()
        self.basis = kwargs.get('basis')
        self.xyz = kwargs.get('xyz')
        self.inp = kwargs.get('inp')
        self.out = kwargs.get('out')

    def is_master(self):
        return self.rank  == vlx.mpi_master()

    def get_workdir(self):
        return self._tmpdir

    def set_workdir(self, tmpdir):
        self._tmpdir = tmpdir

    def get_overlap(self):
        overlap_driver = vlx.OverlapIntegralsDriver(
            self.rank, self.size, self.comm
        )
        master_node = (self.rank == vlx.mpi_master())
        if master_node:
            mol = vlx.InputParser.create_molecule_from_xyz(
                self.xyz
            )
            bas = vlx.InputParser(
                self.basis
            ).create_basis_set(mol)
        else:
            mol = vlx.Molecule()
            bas = vlx.MolecularBasis()

        mol.broadcast(self.rank, self.comm)
        bas.broadcast(self.rank, self.comm)

        S = overlap_driver.compute(mol, bas, self.comm)
        return S.to_numpy()

    def get_one_el_hamiltonian(self):
        kinetic_driver = vlx.KineticEnergyIntegralsDriver(
            self.rank, self.size, self.comm
        )
        potential_driver = vlx.NuclearPotentialIntegralsDriver(
            self.rank, self.size, self.comm
        )
        master_node = (self.rank == vlx.mpi_master())
        if master_node:
            mol = vlx.InputParser.create_molecule_from_xyz(self.xyz)
            bas = vlx.InputParser(self.basis).create_basis_set(mol)
        else:
            mol = vlx.Molecule()
            bas = vlx.MolecularBasis()

        mol.broadcast(self.rank, self.comm)
        bas.broadcast(self.rank, self.comm)

        T = kinetic_driver.compute(mol, bas, self.comm).to_numpy()
        V = potential_driver.compute(mol, bas, self.comm).to_numpy()

        return T-V

    def get_nuclear_repulsion(self):
        mol = vlx.InputParser.create_molecule_from_xyz(self.xyz)
        return mol.nuclear_repulsion_energy()

    def run_scf(self):
        self.scf_driver = vlx.ScfRestrictedDriver()
        inp = str(self.inp)
        out = str(self.out)
        os.chdir(self.get_workdir())
        task = vlx.MpiTask((inp, out), self.comm)
        self.scf_driver.compute_task(task)

    def get_mo(self):
        mos = self.scf_driver.mol_orbs.alpha_to_numpy()
        return mos

    def set_densities(self, da, db):
        from veloxchem import denmat
        self._da = vlx.AODensityMatrix(
            [np.array(da), np.array(db)], denmat.rest
        )

    def get_densities(self):
        from veloxchem import denmat
        da = self._da.alpha_to_numpy(0)
        db = self._da.beta_to_numpy(1)
        return da, db

    def get_two_el_fock(self):
        from veloxchem.veloxchemlib import denmat, fockmat
        master_node = (self.rank == vlx.mpi_master())
        if master_node:
            mol = vlx.InputParser.create_molecule_from_xyz(self.xyz)
            bas = vlx.InputParser(self.basis).create_basis_set(mol)
        else:
            mol = vlx.Molecule()
            bas = vlx.MolecularBasis()
        mol.broadcast(self.rank, self.comm)
        bas.broadcast(self.rank, self.comm)

        da, db = self.get_densities()
        dt = da + db
        ds = da - db
        dens = vlx.AODensityMatrix([dt, ds], denmat.rest)
        fock = vlx.AOFockMatrix(dens)
        fock.set_fock_type(fockmat.restjk, 0)
        fock.set_fock_type(fockmat.restk, 1)

        eri_driver = vlx.ElectronRepulsionIntegralsDriver(
            self.rank, self.size, self.comm
        )
        screening = eri_driver.compute(vlx.ericut.qqden, 1.0e-12, mol, bas)
        eri_driver.compute(vlx.ericut.qqden, 1.0e-12, mol, bas)
        eri_driver.compute(fock, dens, mol, bas, screening, self.comm)
        fock.reduce_sum(self.rank, self.size, self.comm)


        ft = fock.to_numpy(0)
        fs = -fock.to_numpy(1)

        fa = (ft + fs)/2
        fb = (ft - fs)/2

        return fa, fb