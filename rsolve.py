__author__ = 'William Goodall'

import copy as copy
import re

# Define settings
max_coefficient = 20

class Molecule:
    atoms = {}
    original_atoms = {}
    coefficient = 1

    def __init__(self, atoms=None):
        self.atoms = (atoms if not (atoms is None) else {})
        self.original_atoms = (atoms if not (atoms is None) else {})

    def __mul__(self, other):

        if not(isinstance(other, int)): raise TypeError("Can only multiply a Molecule by a number")

        new_mol = copy.deepcopy(self)

        new_mol.coefficient = new_mol.coefficient * other

        for key, value in new_mol.atoms.items():
            new_mol.atoms[key] = value * other

        return new_mol
    __rmul__ = __mul__

    def __add__(self, other):
        new_molecule = copy.deepcopy(self)

        for atom, subscript in other.atoms.items():  # for each atom and subscript of that atom
            if atom in new_molecule.atoms:  # if we already have a record of this atom, add it to the existing atom
                new_molecule.atoms[atom] = new_molecule.atoms[atom] + subscript
            else:  # if we don't, insert it in the set
                new_molecule.atoms[atom] = subscript
        return new_molecule
    __radd__ = __add__

    def __eq__(self, other):
        if not(isinstance(other, Molecule)): return False

        return self.atoms == other.atoms

    def __contains__(self, other):
        print('in checking')

        if not(isinstance(other, Molecule)): return False

        for atom in other.atoms:
            if not (atom in self.atoms):
                return False


        return True

    def __str__(self):
        return str(self.atoms)

    def __len__(self):
        return len(self.atoms)


class M(Molecule):
    pass

def solve(left, right):
    mols_left = all_subscripts(left)
    mols_right = all_subscripts(right)

    for l in mols_left:
        for r in mols_right:
            if add_list_items(r) == add_list_items(l):
                return [r, l]

def all_subscripts(mols:list):
    all = []
    if len(mols) == 1:
        for co in range(1, max_coefficient + 1):
            all.append([mols[0] * co])
    else:
        for co in range(1, max_coefficient + 1):
            for m in all_subscripts(mols[1:]):
                all.append([(mols[0] * co), m])
    return all

def add_list_items(list):
    try:
        all = list[0]
        for i in list[1:]:
            all = all + i
            return all
    except TypeError:
        return list

def parse(query):
    split_query = re.findall('[A-Z][a-z0-9]*|[+=]', query)

    #TODO make regex?
    #Validate query string, if invalid return None
    if(split_query.count('=') > 1): return None  # If there is more than one =
    if((split_query[0] == '+') | (split_query[0] == "=")): return None  # If there is an operator as the first term
    if((split_query[len(split_query - 1)] == '+') | (split_query[len(split_query - 1)] == "=")): return None  # if there is an op. as last term

    for term in split_query:
        pass