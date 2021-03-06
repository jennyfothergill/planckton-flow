#!/usr/bin/env python
"""Initialize the project's data space.

Iterates over all defined state points and initializes
the associated job workspace directories."""
from collections import OrderedDict
from itertools import product

import signac


# Parameters used for generating the morphology
parameters = OrderedDict({
    # input can be the path to a molecule file or a SMILES string
    # or a key to the COMPOUND_FILE dictionary
    # Mixtures can be specified like so
    # "input" = [["PCBM", "P3HT_16"]]
    # note the additional brackets
    "input": [
        #["CZTPTZ8FITIC"],
        #["CZTPTZITIC"],
        ["PCBM"],
        #["P3HT_16"],
        #["ITIC"],
        #["ITIC-Th"],
        #["IEICO"],
        #["IDT-2BR"],
        #["EH-IDTBR"],
        #["TruxTP6FITIC"],
        #["TruxTPITIC"],
        ],

    # If a mixture is used, the number of each compound in the mixture
    # needs to be specified:
    # "n_compounds" = [(100,100), (1000,500)]
    "n_compounds": [100],

    # Density must be specified as a pair containing (value, unit)
    "density": [(1.0, "g/cm**3")],
    # Energy scaling "solvent" parameter
    "e_factor": [0.5],

    # Force fields are specified as keys to the FORCE_FIELD dictionary in
    # planckton/force_fields/__init__.py
    "forcefield": ["opv_gaff"],

    # Reduced temperatures specified in simulation units
    "kT_reduced": [1.0],

    # Simulation parameters
    # Thermostat coupling
    "tau": [3],
    # Number of steps to shrink the box
    "shrink_steps": [1e3],
    # Number of steps to run final simulation
    "n_steps": [1e3],
    # Timestep size
    "dt": [0.0001],
    # Whether to remove hydrogen atoms
    "remove_hydrogens": [False],  # True or False
    "mode": ["gpu"]  # "cpu" or "gpu"
})


def get_parameters(parameters):
    return list(parameters.keys()), list(product(*parameters.values()))


def main(parameters):
    project = signac.init_project("debug")
    param_names, param_combinations = get_parameters(parameters)
    # Create the generate jobs
    for params in param_combinations:
        parent_statepoint = dict(zip(param_names, params))
        parent_job = project.open_job(parent_statepoint)
        parent_job.init()
        parent_job.doc.setdefault("steps", parent_statepoint["n_steps"])
    project.write_statepoints()


if __name__ == "__main__":
    main(parameters)
