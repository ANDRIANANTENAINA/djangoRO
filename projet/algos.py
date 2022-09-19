import numpy as np


# algo miniLi **************************************************************************
# min sans le min precedent
def minWithOut(m, indiceC):
    m[indiceC] = max(m) + 100
    return m


# pour isoler tous le valuer de cout deja prise
def maximisation(m, indiceC):
    lin = 0
    while lin < len(m):
        m[lin][indiceC] = max(m[lin]) + 100
        lin = lin + 1
    return m


def algoMinili(ct, x, y):
    line = 0
    cout = np.array(ct, int)
    tmpCout = cout.copy()

    Vx = np.array([x], int)
    Vy = np.array([y], int)
    baseSolution = np.zeros(cout.shape)

    while line < len(cout):
        indiceCol = cout[line].argmin()
        minVxVy = min(Vx.item(line), Vy.item(indiceCol))
        nextL = Vx.item(line) - minVxVy
        Vx.itemset(line, Vx.item(line) - minVxVy)
        Vy.itemset(indiceCol, Vy.item(indiceCol) - minVxVy)
        baseSolution[line][indiceCol] = minVxVy

        if Vy.item(indiceCol) == 0:
            cout = maximisation(cout, indiceCol)

        while not (nextL == 0):
            mI = minWithOut(cout[line], indiceCol).argmin()
            minVxVy = min(Vx.item(line), Vy.item(mI))
            tmp = Vx.item(line) - minVxVy
            Vx.itemset(line, Vx.item(line) - minVxVy)
            Vy.itemset(mI, Vy.item(mI) - minVxVy)
            if Vy.item(mI) == 0:
                cout = maximisation(cout, mI)
            baseSolution[line][mI] = minVxVy

            nextL = tmp

        line += 1

    z = int((tmpCout * baseSolution).sum())
    return z, baseSolution


# algo balas Hammer ***********************************************************************
# recherche une valeur minim dNS UN LISTE CONTENANT NBR ET None
def reachMin(liste):
    i = 0
    val = 0

    while i < len(liste):
        if liste[i] is not None:
            if val == 0:
                val = liste[i]
            elif val != 0 and val > liste[i]:
                val = liste[i]

        i += 1
    if np.isnan(val):
        val = np.nanmin(liste)
    return val


# recherche une valeur maxim dNS UN LISTE CONTENANT NBR ET None
def reachMax(liste):
    i = 0
    val = None
    while i < len(liste):
        if liste[i] is not None:
            if val is None:
                val = liste[i]
            elif val < liste[i]:
                val = liste[i]
        i = i + 1
    return val


# pour faire le difference minimale par line
def diffMinLine(cout):
    initx = 0
    nombreColonneCout = len(cout[0])
    nombreLineCout = len(cout)
    y = []
    while initx < nombreLineCout:
        cout2List = []
        i = 0
        while i < nombreColonneCout:
            cout2List.append(cout[initx][i])
            i = i + 1
        minL1 = reachMin(cout[initx])
        nbrMinL1 = cout2List.count(minL1)
        if nbrMinL1 == 1:
            cout2List.remove(minL1)
            minL2 = reachMin(cout2List)
            if np.isnan(minL2):
                diff = minL1
            else:
                diff = minL2 - minL1
        else:
            diff = 0
        y.append(diff)
        initx = initx + 1
    return y


# minimum pour CHAQUE COLONNE
def diffMinColonne(cout):
    initx = 0
    nombreColonneCout = len(cout[0])
    nombreLineCout = len(cout)
    x = []
    while initx < nombreColonneCout:
        inity = 0
        z = []
        while inity < nombreLineCout:
            z.append(cout[inity][initx])
            inity = inity + 1

        min1 = reachMin(z)
        nombreMin1 = z.count(min1)
        if nombreMin1 == 1:
            z.remove(min1)
            min2 = reachMin(z)
            if np.isnan(min2):
                diff = min1
            else:
                diff = min2 - min1
        else:
            diff = 0
        x.append(diff)
        initx = initx + 1
    return x


def index(tab):
    qteDemande = diffMinColonne(tab)
    qteDisponible = diffMinLine(tab)
    maxY = reachMax(qteDisponible)
    maxX = reachMax(qteDemande)
    if maxX > maxY:
        indexX = qteDemande.index(maxX)
        tmpY = []
        i = 0
        m = len(tab)
        while i < m:
            tmpY.append(tab[i][indexX])
            i = i + 1
        indexY = tmpY.index(reachMin(tmpY))

    else:

        indexY = qteDisponible.index(maxY)
        linPrienCharge = tab[indexY]
        tmpX = []
        i = 0
        while i < len(tab[0]):
            tmpX.append(tab[indexY][i])
            i += 1
        indexX = tmpX.index(reachMin(linPrienCharge))

    return indexX, indexY


def funcBase(solution, cout, Vx, Vy):
    k = 0
    while k < len(solution):
        j = 0

        while j < len(solution[0]):
            if solution[k][j] == 0:
                indiceCol = index(cout)[0]
                indiceLine = index(cout)[1]

                minVxVy = min(Vx.item(indiceLine), Vy.item(indiceCol))

                a = Vx[0][indiceLine] - minVxVy
                b = Vy[0][indiceCol] - minVxVy
                Vy = np.array(Vy, dtype=np.float64)
                Vx = np.array(Vx, dtype=np.float64)
                solution = np.array(solution, dtype=np.float64)
                cout = np.array(cout, dtype=np.float64)
                if a == 0:
                    Vx[0][indiceLine] = None
                    Vy[0][indiceCol] = b
                    i = 0
                    while i < len(cout[0]):
                        cout[indiceLine][i] = None
                        if solution[indiceLine][i] == 0:
                            solution[indiceLine][i] = None
                        i += 1

                if b == 0:
                    Vy[0][indiceCol] = None
                    Vx[0][indiceLine] = a
                    i = 0
                    while i < len(cout):
                        cout[i][indiceCol] = None
                        if solution[i][indiceCol] == 0:
                            solution[i][indiceCol] = None

                        i += 1
                solution[indiceLine][indiceCol] = minVxVy
            j += 1

        k += 1
    return solution, cout, Vx, Vy


def algoBalasHammer(ct, x, y):
    cout = np.array(ct, int)
    # tmpCout = copy de cout
    tmpCout = cout.copy()
    # Vx = quantite disponible dans le depot
    Vx = np.array([x], int)
    #  Vy = quantite demande
    Vy = np.array([y], int)
    # baseSolution = copy de cout mais le valeur sont zeros
    baseSolution = np.zeros(cout.shape)
    resBase = funcBase(baseSolution, cout, Vx, Vy)
    baseSolution = resBase[0]
    newCout = resBase[1]
    newVx = resBase[2]
    newVy = resBase[3]
    j = 0
    while j < len(baseSolution):
        i = 0
        while i < len(baseSolution[0]):
            if baseSolution[j][i] == 0:
                var = funcBase(baseSolution, newCout, newVx, newVy)
                baseSolution = funcBase(baseSolution, newCout, newVx, newVy)[0]
                newCout = var[1]
                newVx = var[2]
                newVy = var[3]
                pass
            else:
                i += 1
        j += 1

    j = 0
    while j < len(baseSolution):
        i = 0
        while i < len(baseSolution[0]):
            if np.isnan(baseSolution[j][i]):
                baseSolution[j][i] = 0
            i += 1
        j += 1

    cout_base = int((tmpCout * baseSolution).sum())
    return cout_base, baseSolution
