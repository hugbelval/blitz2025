from queue import PriorityQueue, Queue

from game_message import *
import random


class Bot:
    nextCorner = 0
    lastPos = None

    def __init__(self):
        print("Initializing your super mega duper bot")


    def get_next_move(self, game_message: TeamGameState):
        """
        Here is where the magic happens, for now the moves are not very good. I bet you can do better ;)
        """
        actions = []

        actions.append(
            random.choice(
                [
                    MoveUpAction(),
                    MoveRightAction(),
                    MoveDownAction(),
                    MoveLeftAction(),
                ]
            )
        )

        corners = [Position(1,1), Position(game_message.map.width, 1), Position(game_message.map.width, game_message.map.height),
                   Position(1, game_message.map.height), Position(1, 1)]

        if self.samePosition(game_message.yourCharacter.position, corners[self.nextCorner]):
            self.nextCorner = (self.nextCorner + 1) % 4

        for threat in game_message.threats:
            print("Style " + threat.style + "Personality " + threat.personality + "Position " +
                  str(threat.position.x) + ", " + str(threat.position.y))

        print("Going to corner " + str(self.nextCorner))


        currentPosition = game_message.yourCharacter.position


        positions = [Position(currentPosition.x, currentPosition.y + 1),
                         Position(currentPosition.x, currentPosition.y - 1),
                         Position(currentPosition.x + 1, currentPosition.y),
                         Position(currentPosition.x - 1, currentPosition.y)]
        #for position in positions:

            #if self.samePosition(position, self.lastPos):
                #positions.remove(position)

        self.lastPos = currentPosition

        for i in range(0,8):
            for position in positions:
                if(self.isPositionWallOrOut(position, game_message)):
                    positions.remove(position)
                if not self.checkPositionsIsSafeDeep(position, game_message, i):
                    if len(positions) > 1:
                        positions.remove(position)
        #path = self.breadthFirstSearch(game_message.yourCharacter.position, game_message, corners[self.nextCorner])

        #return path
        return [MoveToAction(positions[0])]


    def samePosition(self, a, b):
        if(a is None or b is None):
            return False
        return a.x == b.x and a.y == b.y

    def breadthFirstSearch(self, start, game_message, goal):
        visited = []
        nodeStack = Queue()
        nodeStack.put(start)
        pathStack = Queue()
        pathStack.put([])
        currentNode = nodeStack.get()
        currentPath = pathStack.get()
        visited.append(currentNode)
        print("searching")
        while not self.samePosition(currentNode, goal):
            successors = self.getSuccessors(currentNode, game_message)
            for successor, action in successors:
                if all(not self.samePosition(successor, x) for x in successors):
                    nodeStack.put(successor)
                    newPath = currentPath.copy()
                    newPath.append(action)
                    pathStack.put(newPath)
                    visited.append(successor)

            currentNode = nodeStack.get()
            currentPath = pathStack.get()

        return currentPath

    def getSuccessors(self, currentNode, game_message):
        successors = []

        position = Position(currentNode.x, currentNode.y-1)
        if self.isPositionSafe(position, game_message):
            successors.append((position, MoveUpAction()))

        position = Position(currentNode.x, currentNode.y + 1)
        if self.isPositionSafe(position, game_message):
            successors.append((position, MoveDownAction()))

        position = Position(currentNode.x + 1, currentNode.y)
        if self.isPositionSafe(position, game_message):
            successors.append((position, MoveRightAction()))

        position = Position(currentNode.x - 1, currentNode.y)
        if self.isPositionSafe(position, game_message):
            successors.append((position, MoveLeftAction()))
        return successors


    def isPositionWallOrOut(self, position, game_message):
        try:
            if(game_message.map.tiles[position.x][position.y] == TileType.WALL):
                return True
            return False
        except:
            print("except")
            return True

    def checkPositionsIsSafeDeep(self, position, game_message, level):
        if level > 0:
            positions = [Position(position.x, position.y + 1),
                         Position(position.x, position.y - 1),
                         Position(position.x + 1, position.y),
                         Position(position.x - 1, position.y)]
            for position in positions:
                if not self.isPositionWallOrOut(position, game_message) and not self.checkPositionsIsSafeDeep(position, game_message, level - 1):
                    return False
            return True
        else:
            return self.isPositionSafe(position, game_message)


    def isAllAdjacentPositionsSafe(self, position, game_message):
        try:
            positions = [position, Position(position.x, position.y+1),
                         Position(position.x, position.y-1),
                         Position(position.x+1, position.y),
                         Position(position.x-1, position.y)]
            for threat in game_message.threats:
                for position in positions:
                    if self.samePosition(position, threat.position):
                        return False
            return True
        except:
            print("except")
            return False

    def isPositionSafe(self, position, game_message):
        for threat in game_message.threats:
            if self.samePosition(position, threat.position):
                return False
        return True
