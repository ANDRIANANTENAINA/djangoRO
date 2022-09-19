import json

from django.shortcuts import render, redirect

from projet.models import miniLi, balasHammer


def about(request):
    return render(request, 'about.html')


def index(request):
    etat = False
    print("teste")
    if request.method == 'POST':
        dataX = request.POST.get('dataX')
        dataY = request.POST.get('dataY')

        dataX = dataX.split(";")
        dataY = dataY.split(";")

        # tmp1 = list([i for i in range(1, len(dataX) + 1)])
        # tmp2 = list([i for i in range(1, len(dataY) + 1)])

        print(dataX, dataY)

        etat = True
        return render(request, 'index.html', context={"tailleTabX": dataX,
                                                      "tailleTabY": dataY,
                                                      "etat": etat})

    return render(request, 'index.html', context={"etat": etat})


def resoudre(request):
    res = 0
    if request.method == 'POST':
        l = list()
        dataX = request.POST.get('dataX')
        dataY = request.POST.get('dataY')
        requette = request.POST.get('selection');

        dataX = list(map(int, dataX.split(";")))
        dataY = list(map(int, dataY.split(";")))

        for y in range(len(dataY)):
            tmp = []
            for x in range(len(dataX)):
                tmp.append(int(request.POST.get(str(y)+str(x))))
            l.append(tmp)

        if requette == "miniLi":
            resU, resC, resLink, zMin, z = miniLi(tuple(l), dataY, dataX)
        if requette == "bHammer":
            resU, resC, resLink, zMin, z = balasHammer(tuple(l), dataY, dataX)
        print(resU)
        print(resC)
    return render(request, 'index.html', context={"z": z,
                                                  "coutMin": zMin,
                                                  "resLink": json.dumps(resLink),
                                                  "resUC": json.dumps(resU + resC)})