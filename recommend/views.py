from django.shortcuts import render
from .service.recommend import recommend
from django.http import HttpResponse


def index(request):
    if request.method == 'POST':
        title = request.POST['title']
        recommendations = recommend(title)
        if recommendations:
            header = "Nuestras sugerencias son"
            return render(request, 'index.html', {"header":header,'recommendations': recommendations["Url"], 'titles':recommendations["Title"]})
        else:
            header = "No se han encontrado recomendaciones para ese titulo"
            return render(request, 'index.html', {"header":header})

    header = "CONTANOS DE ALGUNA PELÍCULA QUE TE HAYA GUSTADO"
    return render(request, 'index.html', {"header":header})
