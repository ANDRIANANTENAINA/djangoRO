
def PrintOut(n,m,aCost,aSupply,aDemand,aDual,aRoute):
    GetDual(n,m,aCost,aDual,aRoute)
    nCost = 0
    resListU = []
    resListC = []
    resListLink = []

    for x in range(n):
        for y in range(m):
            nCost += aCost[x][y] * aRoute[x][y]
            if aRoute[x][y] == 0:
                # print('[<%2i>%4i]' % (aCost[x][y], aDual[x][y]), )
                pass
            else:
                print('[<%2i>(%2i)(%2i)]' % (aCost[x][y], x + 1, y + 1), )

                if {'key':"U" + str(x + 1), 'loc': "0 0"} not in resListU:
                    resListU.append({'key':"U" + str(x + 1), 'loc': "0 0"})

                resListLink.append({'from':"U" + str(x + 1), 'to':"C" + str(y + 1) , 'text':  str(aCost[x][y]) })

            if {'key': "C" + str(y + 1), 'loc': "0 0"} not in resListC:
                resListC.append({'key': "C" + str(y + 1), 'loc': "0 0"})

    print()
    postion = 0
    for i in range(len(resListU)):
        resListU[i]['loc'] = "0 " + str(postion)
        postion += 100

    postion = 0
    for i in range(len(resListC)):
        resListC[i]['loc'] = "200 " + str(postion)
        postion += 60

    print('Cost: ', nCost)
    # input()
    return resListU, resListC, resListLink, nCost


def NorthWest(m,n,aDemand,aSupply,aRoute):
    ''' The simplest method to get an initial solution.
    Not the most efficient'''
    # global aRoute

    u = 0
    v = 0
    aS = [0] * m
    aD = [0] * n
    while u <= n - 1 and v <= m - 1:
        if aDemand[v] - aS[v] < aSupply[u] - aD[u]:
            z = aDemand[v] - aS[v]
            aRoute[u][v] = z
            aS[v] += z
            aD[u] += z
            v += 1
        else:
            z = aSupply[u] - aD[u]
            aRoute[u][v] = z
            aS[v] += z
            aD[u] += z
            u += 1


def NotOptimal(n,m,aCost,aDual,aRoute,nVeryLargeNumber):
    global PivotN
    global PivotM
    nMax = -nVeryLargeNumber
    GetDual(n,m,aCost,aDual,aRoute)
    for u in range(0, n):
        for v in range(0, m):
            x = aDual[u][v]
            if x > nMax:
                nMax = x
                PivotN = u
                PivotM = v
    return nMax > 0


def GetDual(n,m,aCost,aDual,aRoute):
    for u in range(0, n):
        for v in range(0, m):
            aDual[u][v] = -0.5  # null value
            if aRoute[u][v] == 0:
                aPath = FindPath(u, v,m,aRoute,n)
                z = -1
                x = 0
                for w in aPath:
                    x += z * aCost[w[0]][w[1]]
                    z *= -1
                aDual[u][v] = x


def FindPath(u, v,m,aRoute,n):
    aPath = [[u, v]]
    if not LookHorizontaly(aPath, u, v, u, v,m,aRoute,n):
        print('Path error, press key', u, v)
        # input()
    return aPath


def LookHorizontaly(aPath, u, v, u1, v1,m,aRoute,n):
    for i in range(0, m):
        if i != v and aRoute[u][i] != 0:
            if i == v1:
                aPath.append([u, i])
                return True  # complete circuit
            if LookVerticaly(aPath, u, i, u1, v1,n,aRoute,m):
                aPath.append([u, i])
                return True
    return False  # not found


def LookVerticaly(aPath, u, v, u1, v1,n,aRoute,m):
    for i in range(0, n):
        if i != u and aRoute[i][v] != 0:
            if LookHorizontaly(aPath, i, v, u1, v1,m,aRoute,n):
                aPath.append([i, v])
                return True
    return False  # not found


def BetterOptimal(nVeryLargeNumber,m,aRoute,n):

    aPath = FindPath(PivotN, PivotM,m,aRoute,n)
    nMin = nVeryLargeNumber
    for w in range(1, len(aPath), 2):
        t = aRoute[aPath[w][0]][aPath[w][1]]
        if t < nMin:
            nMin = t
    for w in range(1, len(aPath), 2):
        aRoute[aPath[w][0]][aPath[w][1]] -= nMin
        aRoute[aPath[w - 1][0]][aPath[w - 1][1]] += nMin


def stepping(aCost, aDemand, aSupply, aRoute):
    # example 0
    # aCost = [[45,60,45,30,45,50]
    #     , [35,15,35,35,25,25]
    #     , [30,25,45,55,15,55]
    #     , [30,40,55,10,10,50]]
    #
    # aDemand = [20,15,35,10,20,10]
    # aSupply = [25,30,10,45]
    # example 1
    # aCost = [[9, 12, 9, 6, 9, 10]
    #     , [7, 3, 7, 7, 5, 5]
    #     , [6, 5, 9, 11, 3, 11]
    #     , [6, 8, 11, 2, 2, 10]]
    #
    # aDemand = [40, 30, 70, 20, 40, 20]
    # aSupply = [50, 60, 20, 90]

    # example 2
    # aCost = [[ 1, 2, 1, 4, 5, 2]
    #         ,[ 3, 3, 2, 1, 4, 3]
    #         ,[ 4, 2, 5, 9, 6, 2]
    #         ,[ 3, 1, 7, 3, 4, 6]]
    # aDemand = [ 20, 40, 30, 10, 50, 25]
    # aSupply = [ 30, 50, 75, 20]
    #
    # example3
    # aCost = [[ 5, 3, 6, 2]
    #         ,[ 4, 7, 9, 1]
    #         ,[ 3, 4, 7, 5]]
    # aDemand = [ 16, 18, 30, 25]
    # aSupply = [ 19, 37, 34]

    n = len(aSupply)
    m = len(aDemand)
    nVeryLargeNumber = 99999999999
    # add a small amount to prevent degeneracy
    # degeneracy can occur when the sums of subsets of supply and demand equal
    elipsis = 0.001
    for k in aDemand:
        k += elipsis / len(aDemand)
    aSupply[1] += elipsis
    # initialisation
    # aRoute = []
    # for x in range(n):
    #     aRoute.append([0] * m)
    aDual = []
    for x in range(n):
        aDual.append([-1] * m)

    # print("AVANT", aRoute)
    # NorthWest(m,n,aDemand,aSupply,aRoute)
    # print("APRES", aRoute)

    PivotN = -1
    PivotM = -1
    PrintOut(n,m,aCost,aSupply,aDemand,aDual,aRoute)
    print("etoooooooooooo", aRoute)

    # MAIN
    while NotOptimal(n,m,aCost,aDual,aRoute,nVeryLargeNumber):
        print('PIVOTING ON', PivotN, PivotM)
        BetterOptimal(nVeryLargeNumber,m,aRoute,n)

    resListU, resListC, resListLink, nCost = PrintOut(n, m, aCost, aSupply, aDemand, aDual, aRoute)
    return resListU, resListC, resListLink, nCost
