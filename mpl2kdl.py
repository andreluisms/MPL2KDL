from python2kdl import generate_ontology
from os.path import exists
import sys

if __name__ == "__main__":
    invalFiles = []
    for i, arg in enumerate(sys.argv):
        if exists(arg):
            if (i != 0):
                generate_ontology(arg)
        else:
            invalFiles.append(arg)
    for file in invalFiles:
        print(f"The ontology for the {file} could not be generated. The {file} does not exist.")

