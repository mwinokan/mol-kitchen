import mrich
from typer import Typer
import time

app = Typer()


@app.command()
def main(
    file: str,
    device: str = "cpu",
    model: str = "medium",
    fmax: float = 0.05,
    logfile: bool = False,
):

    mrich.h1("mol-kitchen: example 'strain'")

    with mrich.loading("imports"):
        from mace.calculators import mace_off
        from ase import build
        import molparse as mp
        from molparse.rdkit import mol_to_AtomGroup
        from rdkit.Chem import MolFromMolFile
        from ase.optimize import BFGS

    if not file.endswith(".mol"):
        raise ValueError("unsupported file extension")

    mrich.var("file", file)

    mol = MolFromMolFile(file)
    group = mol_to_AtomGroup(mol)
    atoms = group.ase_atoms

    mrich.var("atoms", atoms)

    calc = mace_off(model=model, device=device)
    mrich.var("calc", calc)

    atoms.calc = calc

    start_energy = atoms.get_potential_energy()
    mrich.var("start_energy", start_energy, unit="eV")

    ### DO SOME MINIMISATION

    trajfile = file.replace(".mol", ".traj")

    if logfile:
        logfile = file.replace(".mol", ".log")
    else:
        logfile = None

    opt = BFGS(atoms, trajectory=trajfile, logfile=logfile)
    mrich.var("opt", opt)

    start_time = time.time()
    with mrich.loading("optimising"):
        opt.run(fmax=fmax)
    end_time = time.time()

    end_energy = atoms.get_potential_energy()
    mrich.var("end_energy", end_energy, unit="eV")

    strain = end_energy - start_energy
    mrich.var("strain", strain, unit="eV")

    mrich.var("optimisation time", end_time - start_time, unit="seconds")


if __name__ == "__main__":
    app()
