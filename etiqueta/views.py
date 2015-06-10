from .models import Etiqueta
from post.models import Post
from cela.models import Cela, get_cela
from django.shortcuts import render,get_object_or_404,redirect

def etiquetaview(request,etq):
    cela = get_cela(request)
    etiqueta = Etiqueta.objects.filter(pk=etq, cela = cela).first()

    return render(request,"etiqueta.html", {'etiqueta':etiqueta, 'cela': cela})

def todoview(request):
    cela = get_cela(request)
    etiqueta = get_object_or_404(Etiqueta,nom='ToDo', cela = cela)
    posts = Post.objects.filter(etiquetes=etiqueta, cela = cela)

    return render(request,"toDo.html", {'posts':posts, 'cela': cela})

def feinafeta(request,pkpost):
    cela = get_cela(request)
    todo = Etiqueta.objects.get(nom='ToDo', cela = cela)
    todo_post = Post.objects.filter(pk=pkpost, cela = cela).first()
    todo_post.etiquetes.remove(todo)

    posts = Post.objects.filter(etiquetes=todo, cela = cela)

    return render(request,"toDo.html", {'posts':posts, 'cela': cela})


