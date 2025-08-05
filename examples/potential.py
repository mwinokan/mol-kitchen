import mrich
from typer import Typer

app = Typer()


@app.command()
def main(file: str, device: str = "cpu", model: str = "medium"):

    mrich.h1("mol-kitchen: example 'potential'")

    with mrich.loading("imports"):
        from mace.calculators import mace_off
        from ase import build
        import molparse as mp
        from molparse.rdkit import mol_to_AtomGroup
        from rdkit.Chem import MolFromMolFile

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

    mrich.var("potential", atoms.get_potential_energy(), unit="eV")


if __name__ == "__main__":
    app()
