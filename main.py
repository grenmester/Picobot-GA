# Names: Jacky Lee, Christopher Ferrarin, Evan Liang
# Date: December 7th
# Our program is based off of Picobot, a programming challenge that wherein a pixel with user-defined instructions must touch every pixel in a map without any memory. The Program class creates a list of all possible Picobot rules, specifies how a program will move given its surroundings, and controls mutations and program breeding, while the World class creates an ASCII representation of the Picobot map and provides the means for the Picobot programs to gauge their surroundings and move. Finally, the final global functions control a genetic algorithm in which the Picobot programs that reach the most number of squares are allowed to breed to create a new generation of programs in the hopes that each generation produces a better set of rules than the last.

import random
import time

WIDTH = 25
HEIGHT = 25
NUMSTATES = 5

TRIALS = 10
STEPS = 2500
MUTATE_RATE = 0.2
BEST_RATE = 0.10

class Program(object):
    def __init__(self):
        ''' initializes the Picobot program '''
        self.rules = {}

    def __repr__(self):
        ''' returns the string representation of the rules of the program '''
        Keys = list( self.rules.keys() )
        SortedKeys = sorted( Keys )
        s = ''
        for i in SortedKeys:
            s += str(i[0]) + ' ' + str(i[1]) + ' -> ' + str(self.rules[i][0]) + ' ' + str(self.rules[i][1])
            s += '\n'
        return s

    def randomize(self):
        ''' makes a completely random set of Picobot rules, one for each 45 possible states and moves '''
        pattern = ['xxxx','Nxxx','NExx','NxWx','xxxS','xExS','xxWS','xExx','xxWx']
        POSSIBLE_MOVES = ['x','N','E','W','S']
        states = [i for i in range(NUMSTATES)]
        for i in states:
            for j in pattern:
                movedir = random.choice( POSSIBLE_MOVES )
                movestr = random.choice( states )
                while movedir in j:
                    movedir = random.choice( POSSIBLE_MOVES )
                self.rules[(i,j)] = (movedir, movestr)

    def __gt__(self,other):
        ''' greater than operator - works randomly, but works! '''
        return random.choice( [ True, False ] )

    def __lt__(self,other):
        ''' less than operator - works randomly, but works! '''
        return random.choice( [ True, False ] )

    def getMove(self, state, surroundings):
        ''' takes in the state and surrounding patterns and returns the move, represented as a tuple that corresponds to those parameters '''
        return self.rules[(state, surroundings)]

    def mutate(self):
        ''' randomly chooses a rule and replaces the move tuple with a randomly generated move '''
        POSSIBLE_MOVES = ['x','N','E','W','S']
        states = [i for i in range(NUMSTATES)]
        key = random.choice(list(self.rules.keys()))
        movedir = random.choice( POSSIBLE_MOVES )
        movestr = random.choice( states )

        while movedir in key[1]:
            movedir = random.choice( POSSIBLE_MOVES )

        self.rules[key] = (movedir, movestr)

    def crossover(self, other):
        ''' takes in another program object named other, and returns an program that combines some of the rules from other and some of the rules from self '''
        offspringDict = {}
        pattern = ['xxxx','Nxxx','NExx','NxWx','xxxS','xExS','xxWS','xExx','xxWx']
        POSSIBLE_MOVES = ['x','N','E','W','S']
        states = [i for i in range(NUMSTATES)]
        cstate = random.choice([1,2,3])

        for i in range(cstate + 1):
            for j in pattern:
                offspringDict[i,j] = self.rules[i,j]

        for i in range(cstate, NUMSTATES):
            for j in pattern:
                offspringDict[i,j] = other.rules[i,j]

        offspringProgram = Program()
        offspringProgram.rules = offspringDict

        return offspringProgram

class World(object):
    def __init__(self, initialRow, initialCol, program):
        ''' initializes the Picobot world '''
        self.prow = initialRow
        self.pcol = initialCol
        self.state = 0
        self.prog = program
        self.room = [ [' ']*WIDTH for row in range(HEIGHT) ]
        for i in range(HEIGHT):
            for j in range(WIDTH):
                if i == self.prow and j == self.pcol:
                    self.room[i][j] = 'P'
                elif i == 0 or i == HEIGHT-1 or j == 0 or j == HEIGHT-1:
                    self.room[i][j] = '+'

    def __repr__(self):
        ''' returns the string representation of the world '''
        world = ''
        for i in range(HEIGHT):
            for j in range(WIDTH):
                world += self.room[i][j]
            world += '\n'
        return world

    def getCurrentSurroundings(self):
        ''' returns the surrounding pattern string for the current position of Picobot '''
        surroundings = ''
        coords = [(-1,0),(0,1),(0,-1),(1,0)]
        directions = ['N','E','W','S']
        for i in range(4):
            searchRow = self.prow+coords[i][0]
            searchCol = self.pcol+coords[i][1]
            if self.room[searchRow][searchCol] == '+':
                surroundings += directions[i]
            else:
                surroundings += 'x'
        return surroundings

    def step(self):
        ''' moves the Picobot by one step according to current surrounding state and the next move'''
        nextMove = self.prog.getMove(self.state, self.getCurrentSurroundings())

        coords = [(-1,0),(0,1),(0,-1),(1,0)]
        directions = ['N','E','W','S']
        index = directions.index(nextMove[0])
        rowMove = coords[index][0] + self.prow
        colMove = coords[index][1] + self.pcol
        if self.room[rowMove][colMove] != '+':
            self.room[self.prow][self.pcol] = 'o'
            self.prow = rowMove
            self.pcol = colMove
            self.room[self.prow][self.pcol] = 'P'
            self.state = nextMove[1]

    def run(self, steps):
        ''' runs Picobot by the specified number of steps'''
        for i in range(steps):
            self.step()

    def fractionVisitedCells(self):
        ''' returns the fraction of cells that have been visited '''
        numCells = 0
        numVisited = 0
        for i in range(HEIGHT):
            for j in range(WIDTH):
                if self.room[i][j] != '+':
                    numCells += 1
                    if self.room[i][j] in ['P','o']:
                        numVisited += 1
        return numVisited / numCells

def evaluateFitness(program, trials, steps):
    ''' evaluates the fitness of the Picobot program '''
    fitnesses = []
    for trial in range(trials):
        initialRow = random.choice(range(1,HEIGHT-1))
        initialCol = random.choice(range(1,WIDTH-1))
        world = World(initialRow,initialCol,program)
        world.run(steps)
        fitnesses.append(world.fractionVisitedCells())
    return sum(fitnesses) / len(fitnesses)

def randomPop(popsize):
    ''' returns a list of popsize programs '''
    programs = []
    for i in range(popsize):
        program = Program()
        program.randomize()
        programs.append(program)
    return programs

def GA(popsize, numgens):
    ''' returns the Picobot program with the highest fitness '''
    programs = randomPop(popsize)
    for i in range(numgens):
        startTime = time.time()
        fitnesses = []
        for program in programs:
            fitnesses.append((evaluateFitness(program, TRIALS, STEPS), program))
        topIndex = int(len(fitnesses) * BEST_RATE)
        fitFitnesses = sorted(fitnesses)[-topIndex:]
        fitPrograms = [program[1] for program in fitFitnesses]
        newPrograms = [program for program in fitPrograms]
        for j in range(popsize-topIndex):
            program1 = random.choice(fitPrograms)
            program2 = random.choice(fitPrograms)
            newProgram = program1.crossover(program2)
            if random.random() < MUTATE_RATE:
                newProgram.mutate()
            newPrograms.append(newProgram)
        programs = newPrograms
        print('Generation ' + str(i))
        print('Highest Fitness: ' + str(fitFitnesses[-1][0]))
        averageFitness = sum([program[0] for program in fitFitnesses]) / len(fitFitnesses)
        print('Average Fitness: ' + str(averageFitness) + '\n')
        endTime = time.time()
        print('Computation Time: ' + str(endTime-startTime))
    return fitPrograms[-1]

def saveToFile(filename, p):
    ''' saves the data from Program p to a file named filename '''
    f = open(filename, 'w')
    print >> f, p
    f.close()
