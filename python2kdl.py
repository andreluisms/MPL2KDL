from genericpath import exists
from asdl import parse, VisitorBase
from ast import Constant, NodeVisitor, iter_fields
from ast import parse as astparse
import sys
import os

#Equivalence of Python ADSL types to WSML types
_DCT_WSMLTYPES={'string': '_string', 'int': '_int', 'identifier':'_string',
                'constant':'_string'}

#Types whose content is to be returned
# _LST_CNT_TYPES=['str', 'list']
def print_header(fileName):
    base = os.path.basename(fileName)
    base = base.replace(".py", "")
    print("""wsmlVariant _"http://www.wsmo.org/wsml/wsml-syntax/wsml-rule\"""" +
          """\nnamespace { _"http://ufs.br/ontologies/mpl2kdl#"}""" +
          """\n\nontology """ + base + 
          """\n   importsOntology{_"http://ufs.br/ontologies/mpl2kdl#PythonAbstractSyntax"}  \n""")


class AstToWsmlVis(NodeVisitor):

    def __init__(self, fileName):
        super().__init__()
        print_header(fileName)

    def printWSML(self, node):
        print("   instance ", node.__class__.__name__, 
              hex(id(node)), " memberOf ", node.__class__.__name__, sep='')
        for field, value in iter_fields(node):
            if value:
                if (type(value).__name__ == 'str'):
                    print("      _", field, ' hasValue "', 
                         value.replace('"', '\\"'),'"',sep='')  

                elif (type(value).__name__ == 'list'):
                    print("      _", field, ' hasValue {',sep='', end='')
                    size = len(value)
                    cont = 0
                    for l in value:
                        cont+=1
                        prefix = l.__class__.__name__ + hex(id(l))
                        out =  prefix if cont == size else prefix + ', ' 
                        print (out, end='')
                    print('}')

                else:    
                    print("      _", field, " hasValue ", value.__class__.__name__, 
                          hex(id(value)),sep='')  

    def printWSMLC(self, node):
        print("   instance ", node.__class__.__name__, 
              hex(id(node)), " memberOf ", node.__class__.__name__, sep='')
        for field, value in iter_fields(node):
            if value:
                r = value
                if (type(value).__name__=='str'):
                    r = value.replace('"', '\\"')
                print("      _", field, ' hasValue "', r,'"',sep='')  

    def visit(self, node):
        if not isinstance(node, Constant):  
            self.printWSML(node)    
        super().visit(node)

    def visit_generic(self, node):
        self.printWSML(node)
        super().visit_generic(node)

    def visit_Constant(self, node):
        self.printWSMLC(node)
        super().visit_Constant(node)


class AsdlToWSML(VisitorBase):
    def __init__(self):
        super(AsdlToWSML, self).__init__()

    def visitModule(self, mod):
        print("""wsmlVariant _"http://www.wsmo.org/wsml/wsml-syntax/wsml-rule\"""" +
              """\nnamespace { _"http://ufs.br/ontologies#"}""" +
              """\n\nontology """ + mod.name + """AbstractSyntax""")
        for dfn in mod.dfns:
            print("   concept", dfn.name)  
            self.visit(dfn)

    def visitType(self, type):
        self.visit(type.value, str(type.name))

    def visitSum(self, sum, name):
        for t in sum.types:
            self.visit(t, name)

    def visitConstructor(self, cons, name):
        pass
        key = str(cons.name)
        print("   concept",key, "subConceptOf", name)  
        for f in cons.fields:
            self.visit(f, key)

    def visitField(self, field, name):
        key = str(field.type)
        print ("      _",field.name, " ofType ", end="", sep="")
        if field.seq:
            print('(0 *) ', end="")
        elif field.opt:
            print('(0 1) ', end="")
        print (_DCT_WSMLTYPES.get(key, key))

    def visitProduct(self, prod, name):
        for f in prod.fields:
            self.visit(f, name)


_PYTHON_ASDL = 'python.asdl'
_PYTHON_PROGRAM = 'test.py'
_PYTHON_ABSTRACT = 'PythonAbstractSyntax.wsml'

def generate_concepts(fileInput = _PYTHON_ASDL):
    vis = AsdlToWSML()
    r = parse(fileInput)
    vis.visit(r)



def generate_instances(fileInput = _PYTHON_PROGRAM):
    vis = AstToWsmlVis(fileInput) 
    r = open(fileInput, 'r')
    tree = astparse(r.read())
    vis.visit(tree)


def generate(fileName, function, fname):
    if not exists(fileName):
        tmp = sys.stdout
        sys.stdout = open(fileName, "w")
        function(fname)    
        sys.stdout.close()
        sys.stdout = tmp


def generate_ontology(srcpath, fileOAS = _PYTHON_ABSTRACT):
    generate(fileOAS, generate_concepts, _PYTHON_ASDL)
    target = srcpath.replace(".py", ".wsml")
    generate(target, generate_instances, srcpath)


