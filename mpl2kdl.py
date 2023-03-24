from python2kdl import generate_ontology
from python2kdl import generate_rdf
from python2kdl import RDFOPTIONS
from python2kdl import RdfTypes

from os.path import exists
import sys

if __name__ == "__main__":
    invalFiles = []
    args = sys.argv
    z = 0
    if (args[1] == '-rdf'):
       z = 1
       if (args[2] and args[2] in RDFOPTIONS.keys()):
            z = 2
    for i, arg in enumerate(args):
        if exists(arg):
            if (i > z):
                generate_ontology(arg)
                if (z == 1):
                    generate_rdf(arg, RdfTypes.XML)
                elif (z == 2):
                    generate_rdf(arg, args[2])
        elif (i > z):
            invalFiles.append(arg)
    for file in invalFiles:
        print(f"The ontology for the {file} could not be generated. The {file} does not exist.")