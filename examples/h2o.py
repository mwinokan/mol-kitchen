import mrich
from typer import Typer

app = Typer()


@app.command()
def main(device: str = "cpu", model: str = "medium"):

    mrich.h1("mol-kitchen: example 'h2o'")

    with mrich.loading():
        from mace.calculators import mace_off
        from ase import build

    atoms = build.molecule("H2O")
    calc = mace_off(model=model, device=device)
    atoms.calc = calc
    mrich.var("atoms", atoms)
    mrich.var("potential", atoms.get_potential_energy(), unit="eV")


if __name__ == "__main__":
    app()
