"""
File History:
08.12.2015: Creation
"""

from xml.dom.minidom import parse
from xml.sax import make_parser
from Node import Data
from Dot import DotUtil
import Node

_OUTDIR = "../graphs"
gSpeechStateTemplate = "[arrowhead=\"none\" color=\"grey\"]"
IDX_SPEECH_EXAMPLE = 0
IDX_CONDITION = 1
IDX_PROMPT = 2

_HTML_FILE_FORMAT = """
<!DOCTYPE html>
<html>
<head>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
<script>
$(document).ready(function(){
    $(".edge").click(function(){
        var child = $(this).children( "path" ).css({ 'stroke': 'black'});
    });
});
</script>
</head>
<body>

<h1>State machine</h1>
%s
</body>
</html>
"""

def readXml(filename):
    parser = make_parser()
    xml = parse(filename, parser)
    stateMachine = Data.StateMachine() 
    stateMachine.states = _readStates(xml)
    
    if len(stateMachine.states):
        root = Data.Graph("Idle")
        root.createGraph(stateMachine)
        root.printGraph()
        text = createTextFromGraph(root)
        writeGraphFiles("graph.gv", text)
        writeHTMLFile("graph.svg", "graph.html")
    
def _readStates(xml):
    states = []
    stateNodes = xml.getElementsByTagName('state')

    for state in stateNodes:
        newState = Data.State()
        newState.name = state.getAttribute('name')
        newState.transitions = _readTransitions(state)
        states.append(newState)
    return states

def _readTransitions(state):
    transitions = []
    nextStateNodes = state.getElementsByTagName('nextState')
    for nextStateNode in nextStateNodes:
        transition = Data.Transition()
        transition.name = nextStateNode.getAttribute('name')
        transition.command = nextStateNode.getAttribute('command')
        transition.BussinessLogicCall = nextStateNode.getAttribute('BussinessLogicCall')
        transition.text = nextStateNode.getAttribute('text')
        transition.imageId = nextStateNode.getAttribute('imageId')
        transitions.append(transition)
    return transitions

def createTextFromGraph(rootNode):
    text = writeHeader(rootNode.name)
    text += createNodesText(rootNode)
    text += writeFooter()
    return text
    
def writeHeader(diagramName):
    text = ""
    text += 'digraph "%s" {\n' % diagramName
    text += "  rankdir=LR\n" 
    text += "  node [shape=Mrecord, color=\"#AAAAAA\", fontname=\"Arial\", fontsize=10, height=0.02, width=0.02]\n" 
    text += "  edge [color=pink, len=0.5, penwidth=4.0, fontname=\"Arial\", fontsize=12, fontcolor=\"#AA00CC\"]\n"
    text += "\n"
    return text
    
def createNodesText(rootNode):
        text = ""
        if rootNode.name:
            text = '  %s [label=%s]\n' % (rootNode.title, rootNode.name)
            for node in rootNode.next:
                text += ' %s -> %s\n' % (rootNode.title, node.title) 
                text += createNodesText(node)   
        text += '\n'
        return text
        
def writeFooter():
        return "}\n" 

def writeGraphFiles(outfile, text):
    file(outfile, "wb").write(text)
    for format_ in ("svg",):
        DotUtil.convertDotGraph(outfile, format_)
        
def writeHTMLFile(inputFileName, outputFileName):
    read_data = ""
    with open(inputFileName, 'r') as f:
        read_data = f.read()
    f.closed
    
    htmlString = _HTML_FILE_FORMAT % read_data
    file(outputFileName, "wb").write(htmlString)
    
    
if __name__ == "__main__":

    dialogSpecFilename = "C:/Work/SmartHome/demoSH/specs/SmartHomeSpecs.xml"
    readXml(dialogSpecFilename)
    

