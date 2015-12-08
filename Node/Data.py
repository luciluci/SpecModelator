class StateMachine:
    def __init__(self):
        self.states = []
    
    def getStateByName(self, stateName):
        for state in self.states:
            if state.name == stateName:
                return state
        return None

class State:
    def __init__(self):
        self.name = ""
        self.transitions = []
        
class Transition:
    def __init__(self):
        self.name = ""
        self.command = ""
        self.BussinessLogicCall = ""
        self.text = ""
        self.imageId = ""
        
class Graph:
    printDepth = 0
    rootNodes = ["Idle"]
    
    def __init__(self, rootNodeName):
        self.name = rootNodeName
        self.title = rootNodeName
        self.next = []
        self.incomingTransition = None
        self._visitedNodeTitles = []
        
    def createGraph(self, stateMachine):
        rootState = stateMachine.getStateByName("Idle")
        if rootState:
            self.name = "Idle"
            self._readGraph(self, stateMachine)
    
    def _readGraph(self, rootNode, stateMachine):
        state = stateMachine.getStateByName(rootNode.name)
        if rootNode.title in self._visitedNodeTitles:
            rootNode.printDepth -= 1
            return 
        rootNode.printDepth += 1
        self._visitedNodeTitles.append(rootNode.title)
        
        for transition in state.transitions:
            newstate = stateMachine.getStateByName(transition.name)
            childNode = self._createNewNode(transition, newstate, stateMachine)
            rootNode.next.append(childNode)
            self._readGraph(childNode, stateMachine)
            
    def _createNewNode(self, transition, state, stateMachine):
        newNode = Graph(transition.name)
        newNode.incomingTransition = transition
        if newNode.name not in self.rootNodes:
            newNode.title = newNode.name + transition.imageId
        return newNode
    
    def printGraph(self):
        print "   "*Graph.printDepth + self.title
        Graph.printDepth += 1
        for node in self.next:
            node.printGraph()
        Graph.printDepth -= 1
            