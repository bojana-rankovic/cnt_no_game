from random import random, randint, shuffle, choice
import math
from copy  import deepcopy
from math import log
import numpy as np
from pythonds.basic.stack import Stack

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def postfix_evaluation(s):
    s = s.split()
    n = len(s)
    stack = []
    for i in range(n):
        if s[i].isdigit():
            #push
            stack.append(int(s[i]))
        elif s[i] == "+":
            a = stack.pop()
            b = stack.pop()
            stack.append(int(a)+int(b))
        elif s[i] == "*":
            a = stack.pop()
            b = stack.pop()
            stack.append(int(a)*int(b))
        elif s[i] == "/":
            a = stack.pop()
            b = stack.pop()
            if int(a) != 0:
                stack.append(int(b)/float(a))
            else: return 10**6
        elif s[i] == "-":
            a = stack.pop()
            b = stack.pop()
            stack.append(int(b)-int(a))

    return stack.pop()

def generate_rnd_postfix(given_numbers):
    br_op = 0
    br_br = 0
    nums_count = len(given_numbers)
    ops = ["+","-","*","/"]
    result= ""
    brojevi = deepcopy(given_numbers) 
    shuffle(brojevi)
    done = False
    result += str(brojevi.pop())
    br_br += 1
    while not done and not (br_br == nums_count and br_op == nums_count-1):
        if br_op < br_br-1 and br_br != nums_count:
            i = randint(0, 1)
            if i == 0:
                result += " "+choice(ops)
                br_op += 1
            else:
                shuffle(brojevi)
                result += " "+str(brojevi.pop())
                br_br += 1
        elif br_br == nums_count:
            result += " "+choice(ops)
            br_op += 1
            if br_op == br_br-1:
                break

        else:
            shuffle(brojevi)
            result += " "+str(brojevi.pop())
            br_br += 1
        if br_br == br_op + 1:
            i = randint(0, 1)
            if i == 0:
                done = True
            else:
                done = False

    return result

def scorefunction(postfix, number):
    #rez = postfix_evaluation(postfix)
    rez = evalPostfix(postfix)
    if (abs(rez - int(rez)) > 0) or (rez) < 0:
        return 10**6
    return int(abs(rez-number))

class Intermediate:

    def __init__(self, expr, oper):
        self.expr = expr
        self.oper = oper

def postfixToInfix(postfix):

    
    postfixTokens = postfix.split()

    stack= []

    for token in postfixTokens:
        if token == "+" or token == "-":
            
            rightIntermediate = stack.pop()
            leftIntermediate = stack.pop()

         
            newExpr = leftIntermediate.expr + token + rightIntermediate.expr

            stack.append(Intermediate(newExpr, token))
        
        elif token == "*" or token == "/":
            leftExpr= ""
            rightExpr= ""

            rightIntermediate = stack.pop()

            if rightIntermediate.oper == "+" or rightIntermediate.oper == "-":
                rightExpr = "(" + rightIntermediate.expr + ")"
            else:
                rightExpr = rightIntermediate.expr
            leftIntermediate = stack.pop()

            if leftIntermediate.oper == "+" or leftIntermediate.oper == "-":
                leftExpr = "(" + leftIntermediate.expr + ")"
            else:
                leftExpr = leftIntermediate.expr
            
            newExpr = leftExpr + token + rightExpr

            stack.append(Intermediate(newExpr, token))
        else:
            stack.append(Intermediate(token, ""))

    return stack[0].expr

def mutate(chromosome, given_numbers, probchance=0.1):
    operations_positions = []
    numbers_positions = []
    operations = ['+', '-', '/', '*']
    tokens = chromosome.split(' ')
    if random() < probchance:
        return generate_rnd_postfix(given_numbers)
    else:
        for i in range(len(tokens)):
            if tokens[i] in '+-*/':
                operations_positions.append(i)
            else:
                numbers_positions.append(i)
        r = randint(0, 2)
        if r == 0:
            mutating_op_position = choice(operations_positions)
            mutating_op = tokens[mutating_op_position]
            operations.remove(mutating_op)
            tokens[mutating_op_position] = choice(operations)

        elif r == 1:
            i = choice(numbers_positions)
            numbers_positions.remove(i)
            j = choice(numbers_positions)

            tmp = tokens[i]
            tokens[i] = tokens[j]
            tokens[j] = tmp
        else:
            mutating_op_position = choice(operations_positions)
            mutating_op = tokens[mutating_op_position]
            operations.remove(mutating_op)
            tokens[mutating_op_position] = choice(operations)

            i = choice(numbers_positions)
            numbers_positions.remove(i)
            j = choice(numbers_positions)

            tmp = tokens[i]
            tokens[i] = tokens[j]
            tokens[j] = tmp

        result = tokens[0]
        for i in range(1, len(tokens)):
            result += " "+tokens[i]
        
        return result

def is_valid_postfix(postfix, brojevi):
    numbers_used = {}
    numbers_used = dict((x, brojevi.count(x)) for x in brojevi)
    br_op = 0
    tokens = postfix.split()
    if not is_number(tokens[0]):
        return False
    key = int(tokens[0])
    value = numbers_used[key]
    numbers_used[key] = value-1
    br_br = 1
    for i in range(1, len(tokens)):
        if is_number(tokens[i]):
            key = int(tokens[i])
            value = numbers_used[key]
            numbers_used[key] = value-1
            if numbers_used[key] < 0:
                return False
            br_br += 1
        else:
            br_op += 1
        if(br_op >= br_br):
            return False
    if br_br == br_op+1: return True
    else: return False

def crossover(p1, p2, given_numbers, probswap=0.7, top=1):
   
    if random() < probswap:
        return deepcopy(p2)
    tokens1 = p1.split()
    tokens2 = p2.split()
    operations_positions1 = []
    operations_positions2 = []
    mutual_operations = []
    for i in range(len(tokens1)):
        if tokens1[i] in '+-*/':
            operations_positions1.append(i)

    for i in range(len(tokens2)):
        if tokens2[i] in '+-*/':
            operations_positions2.append(i)

    mutual = operations_positions1+operations_positions2
    mutual_op_positions = dict((x, mutual.count(x)) for x in mutual)
    d = dict((k, v) for k, v in mutual_op_positions.items() if v > 1)
    mutual = list(d.keys())
    
    if len(mutual) > 0:
        i = choice(mutual)
        result_tokens = tokens1[0:i]+tokens2[i:]
        result = result_tokens[0]
    
    else: return generate_rnd_postfix(given_numbers)
    
    for i in range(1, len(result_tokens)):
        result += " "+result_tokens[i]
    
    if is_valid_postfix(result, given_numbers):
        return result
    else: return deepcopy(p1)


def evolve(popsize, rankfunction, given_numbers, maxgen=1000, mutationrate=0.1, breedingrate=0.4, pexp=0.7, pnew=0.05):
    def selectindex():
        return int(log(random())/log(pexp))

    population = [generate_rnd_postfix(given_numbers) for i in range(popsize)]
    for i in range(maxgen):
        scores = rankfunction(population)
        print(str(scores[0][0]) + " " + scores[0][1])

        if scores[0][0] == 0:
            print(str(i)+"-a generacija")
            break
        newpop = [scores[0][1], scores[1][1]]
        while len(newpop) < popsize:
            if random() > pnew:
                child = mutate(crossover(scores[selectindex()][1], scores[selectindex()][1], 
                given_numbers, probswap=breedingrate), given_numbers, probchance=mutationrate)
                newpop.append(child)
            else:
                newpop.append(generate_rnd_postfix(given_numbers))

        population=newpop
    print(postfixToInfix(scores[0][1])+"="+str(int(evalPostfix(scores[0][1]))))
    return scores[0][1]


def getKey(item):
    return item[0]

def getrankfunction(number):
    def rankfunction(population):
        scores=[(scorefunction(e,number),e) for e in population]
        data = sorted(scores, key=lambda tup: tup[0])
        return data
    return rankfunction

def evalPostfix(text):
    s = list()
    tokens = text.split()
    n = 0
    for symbol in tokens:
        if symbol not in '+-*/':
            result = float(symbol)
        elif symbol == '-':
            result = -s[n-1] + s[n-2]
            del s[-1]
            del s[-1]
        elif symbol == '/':
            try:
                result = 1/s[n-1] * s[n-2]
                del s[-1]
                del s[-1]
            except ZeroDivisionError:
                return 10**6
        elif symbol == '*':
            result = s[n-1] * s[n-2]
            del s[-1]
            del s[-1]
        else:
            result = s[n-1] + s[n-2]
            del s[-1]
            del s[-1]
        s.append(result)
        n = len(s)
    return s[n-1]


given_numbers=[3,4,5,9,20,75]
number = 811
rf = getrankfunction(number)
postfix = generate_rnd_postfix(given_numbers)
#print(postfix)
#print(mutate(postfix,given_numbers))
#print(evalPostfix(" 50 5 - 20 2 4 + - *"))
evolve(1000,rf,given_numbers,mutationrate=0.2,breedingrate=0.1,pexp=0.9,pnew=0.2)
#print(postfix_evaluation('25 20 * 6 9 5 7 / - * +'))
#print(eval_postfix("25 20 * 6 9 5 7 / - * +"))
#print(25*20+6*(9-5/7))
#print(eval('25*20+6*(9-5/7)'))
#print(6.0*8.285714285714286)