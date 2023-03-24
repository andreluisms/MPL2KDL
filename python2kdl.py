from genericpath import exists
from asdl import parse, VisitorBase
from ast import Constant, NodeVisitor, iter_fields
from ast import parse as astparse
import ast as ast
import asdl as asdl
import sys as sys
import os


#Equivalence of Python ADSL types to WSML types
DCT_WSMLTYPES={'string': '_string', 'int': '_integer', 'identifier':'_string',
                'constant':'_string'}

NONESTMT = "NoneStmt"

#Types whose content is to be returned
# _LST_CNT_TYPES=['str', 'list']
def print_header(fileName):
    base = os.path.basename(fileName)
    base = base.replace(".py", "")
    print("""wsmlVariant _"http://www.wsmo.org/wsml/wsml-syntax/wsml-rule\"""" +
          """\nnamespace { _"http://ufs.br/ontologies/mpl2kdl#"}""" +
          """\n\nontology """ + base + 
          """\n   importsOntology{_"http://ufs.br/ontologies/mpl2kdl#PythonAbstractSyntax"}  \n""")

class ScopeManager:
    def __init__(self):
        self.lists = []

    def append(self, list):
        self.lists.append(list)

    def getParent(self, node):
        for list in self.lists:
            if node in list:
                return list[0]
        return None

    def getPred(self, node):
        for list in self.lists:
            if node in list:
               pos = list.index(node)
               if pos == 1:
                   return None
               else:
                   return list[pos-1]
        return None


    def getSucc(self, node):
        for list in self.lists:
            if node in list:
               pos = list.index(node)
               if list[-1] == node:
                   return None
               else:
                   return list[pos+1]
        return None
    
    def getList(self):
        return self.lists

stackstmt = ScopeManager()


class AstToWsmlVis(NodeVisitor):

    def __init__(self, fileName):
        super().__init__()
        print_header(fileName)


    def printWSML(self, node):
        global stackstmt
        print("   instance ", node.__class__.__name__, 
              hex(id(node)), " memberOf ", node.__class__.__name__, sep='')
        for field, value in iter_fields(node):
            if value:
                if (type(value).__name__ == 'str'):
                    print("      _", field, ' hasValue "', 
                            value.replace('"', '\\"'),'"',sep='')
                elif (type(value).__name__ == 'int'):
                    print("      _", field, ' hasValue ', value,sep='')  
                elif (type(value).__name__ == 'list'):
                    print("      _", field, ' hasValue {',sep='', end='')
                    size = len(value)
                    cont = 0
                    if  isinstance(value[0], ast.stmt) :
                        copylst = value.copy()
                        copylst.insert(0, node)
                        stackstmt.append(copylst)
                    for l in value:
                        cont+=1
                        prefix = l.__class__.__name__ + hex(id(l))
                        out =  prefix if cont == size else prefix + ', ' 
                        print (out, end='')
                    print('}')

                else:    
                    print("      _", field, " hasValue ", value.__class__.__name__, hex(id(value)),sep='')  
        if isinstance(node, ast.stmt):
            neighbor = (stackstmt.getParent(node), stackstmt.getPred(node), stackstmt.getSucc(node))

            if neighbor[0] != None:
                print("      _isStepOf hasValue ", neighbor[0].__class__.__name__,  hex(id(neighbor[0])), sep="")
            else:
                print("      _isStepOf hasValue", NONESTMT)
            if neighbor[1] != None:
                print("      _isPreceededBy hasValue ", neighbor[1].__class__.__name__,  hex(id(neighbor[1])), sep="")
            else:
                print("      _isPreceededBy hasValue", NONESTMT)
            if neighbor[2] != None:
                print("      _isSucceededBy hasValue ", neighbor[2].__class__.__name__,  hex(id(neighbor[2])), sep="")
            else:
                print("      _isSucceededBy hasValue", NONESTMT)

    


    def printWSMLC(self, node):
        print("   instance ", node.__class__.__name__, 
              hex(id(node)), " memberOf ", node.__class__.__name__, sep='')
        for field, value in iter_fields(node):
            r = value
            if (type(value).__name__=='str'):
                r = r.replace('"', '\\"')
                r = '\\"' + r + '\\"'
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
              """\nnamespace { _"http://ufs.br/ontologies/mpl2kdl#"}""" +
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
        if name == "stmt":
            print("      _isPreceededBy ofType stmt")
            print("      _isSucceededBy ofType stmt")
            

    def visitField(self, field, name):
        key = str(field.type)
        print ("      _",field.name, " ofType ", end="", sep="")
        if field.seq:
            print('(0 *) ', end="")
        elif field.opt:
            print('(0 1) ', end="")
        print (DCT_WSMLTYPES.get(key, key))

    def visitProduct(self, prod, name):
        for f in prod.fields:
            self.visit(f, name)


PYTHON_ASDL = 'python.asdl'
PYTHON_PROGRAM = 'test.py'
PYTHON_ABSTRACT = 'PythonAbstractSyntax.wsml'

def generate_concepts(fileInput = PYTHON_ASDL):
    vis = AsdlToWSML()
    r = parse(fileInput)
    vis.visit(r)
    print("   concept stmtContainer subConceptOf {mod, stmt, excepthandler}")



def generate_instances(fileInput = PYTHON_PROGRAM):
    vis = AstToWsmlVis(fileInput) 
    r = open(fileInput, 'r')
    tree = astparse(r.read())
    vis.visit(tree)
    print ("   instance", NONESTMT, "memberOf stmt")


def generate(fileName, function, fname):
    if not exists(fileName):
        tmp = sys.stdout
        sys.stdout = open(fileName, "w")
        function(fname)    
        sys.stdout.close()
        sys.stdout = tmp
        

def generate_ontology(srcpath, fileOAS = PYTHON_ABSTRACT):
    generate(fileOAS, generate_concepts, PYTHON_ASDL)
    target = srcpath.replace(".py", ".wsml")
    generate(target, generate_instances, srcpath)

class RdfTypes: 
    N3 = '-n3'
    NTRIPLES = '-ntriples'
    XML = '-xml'
    TURTLE = '-turtle'

RDFOPTIONS = {RdfTypes.N3:('1', '.n3'), RdfTypes.NTRIPLES: ('2', '.nt'), RdfTypes.XML: ('3', '.rdf'), RdfTypes.TURTLE:('4', '.ttl')}
CALLJAR = "java -jar wsml2rdfs.jar "
def generate_rdf(pythonsrc, type):
    source = pythonsrc.replace(".py", ".wsml")
    target = pythonsrc.replace(".py", RDFOPTIONS.get(type)[1])
    os.system(CALLJAR +  source + " " + target + " " + RDFOPTIONS.get(type)[0]) 



