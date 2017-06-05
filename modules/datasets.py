import numpy as np
# import matplotlib.pyplot as plt
import os
np.random.seed(10)
FORCE_RESET = False
RAWPATH='modules/data/'

def getDataset(name):
    if name =='linearIncrease':
        return linearIncrease()
    elif name == 'linearDecrease':
        return linearDecrease()
    elif name == 'log':
        return log()
    elif name == 'exp':
        return exp()
    elif name == 'constant':
        return constant()
    else:
        return None


def linearIncrease():
    global FORCE_RESET,RAWPATH
    filename='{}linearIncrease.npy'.format(RAWPATH)
    if (os.path.isfile(filename) and not (FORCE_RESET)):
        linearIncrease = np.load(filename)
    else:
        minLinIncrease = 0
        maxLinIncrease = 100
        stepLinIncrease = 3

        linearIncrease = [np.arange(minLinIncrease, maxLinIncrease, stepLinIncrease)]
        linearIncrease = np.append(linearIncrease, linearIncrease, axis=0)
        noise = np.random.normal(0, 5, np.size(linearIncrease[0]))
        linearIncrease[1] = noise + linearIncrease[1]
        np.save(filename, linearIncrease)
    return linearIncrease
    # plt.scatter(linearIncrease[0], linearIncrease[1])

def linearDecrease():
    global FORCE_RESET,RAWPATH
    filename='{}linearDecrease.npy'.format(RAWPATH)

    if (os.path.isfile(filename) and not (FORCE_RESET)):
        linearDecrease = np.load(filename)
    else:
        minLinDecrease = 0
        maxLinDecrease = 100
        stepLinDecrease = 3

        linearDecrease = [np.arange(minLinDecrease, maxLinDecrease, stepLinDecrease)]
        linearDecrease = np.append(linearDecrease, [np.arange(maxLinDecrease, minLinDecrease, (-1 * stepLinDecrease))],
                                   axis=0)
        noise = np.random.normal(0, 5, np.size(linearDecrease[0]))
        linearDecrease[1] = noise + linearDecrease[1]
        np.save(filename, linearDecrease)

    return linearDecrease
    # plt.scatter(linearDecrease[0], linearDecrease[1])

def log():
    global FORCE_RESET,RAWPATH
    filename='{}log.npy'.format(RAWPATH)

    if (os.path.isfile(filename) and not (FORCE_RESET)):
        log = np.load(filename)
    else:
        minLog = 1
        maxLog = 100
        stepLog = 3

        log = [np.arange(minLog, maxLog, stepLog), np.log(np.arange(minLog, maxLog, stepLog))]
        noiseLog = np.random.normal(0, .1, np.size(log[1]))
        log[1] = noiseLog + log[1]
        np.save(filename, log)

    return log
    # plt.scatter(log[0], log[1])

def exp():
    global FORCE_RESET,RAWPATH
    filename='{}exp.npy'.format(RAWPATH)

    if (os.path.isfile(filename) and not (FORCE_RESET)):
        exp = np.load(filename)
    else:
        minExp = 1
        maxExp = 5
        stepExp = 0.1

        exp = [np.arange(minExp, maxExp, stepExp), np.exp(np.arange(minExp, maxExp, stepExp))]
        noiseExp = np.random.normal(0, 5, np.size(exp[1]))
        exp[1] = noiseExp + exp[1]
        np.save(filename, exp)

    return exp
    # plt.scatter(exp[0], exp[1])

def constant():
    global FORCE_RESET,RAWPATH
    filename='{}constant.npy'.format(RAWPATH)

    if (os.path.isfile(filename) and not (FORCE_RESET)):
        constant = np.load(filename)
    else:
        minConstant = 0
        constantSize = 50
        constantStep = 1

        constant = [np.arange(minConstant, constantSize, constantStep), np.full((1, constantSize), 5)]
        noiseConst = np.random.normal(0, .5, np.size(constant[1]))
        constant[1] = noiseConst + constant[1]
        np.save(filename, constant)

    return constant
    # plt.ylim(0, 10)
    # plt.scatter(constant[0], constant[1])