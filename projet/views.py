from django.shortcuts import render, redirect


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
    if request.method == 'POST':
        pass
    return redirect('index')