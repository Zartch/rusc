from cela.models import Cela, get_cela
from post.models import Post
from recurs.models import Recurs
from etiqueta.models import Etiqueta
from django.shortcuts import render
from cela.moderaciomodels import ModeracioMissatge
from notifications import notify
from django.shortcuts import get_object_or_404


#Vista de la missatgeria entre admin-user de la moderació
#El contentType Definirá si es un Post, un Recurs, ¿o una etiqueta?
def moderacioPost(request, pk, tipus):
    receptor = ""
    desc = ""

    #Depenent del tipos de objecte que estem moderant li tornarem a la template un o un altre objecte
    if tipus == 'Post':
        objecte = get_object_or_404(Post, pk=pk)
        receptor = objecte.autor
        desc = " del post: " + objecte.titol
    elif tipus == 'Recurs':
        objecte = get_object_or_404(Recurs, pk=pk)
        receptor = objecte.post_debat.autor
        desc = " del recurs: " + objecte.descripcio
    elif tipus == 'Etiqueta':
        objecte = get_object_or_404(Etiqueta, pk=pk)
        raise NotImplementedError('Not yet implemented')
    else:
        raise ValueError('Tipus ha de ser Post o Recurs')

    user = request.user

    miss = request.POST.get('textmissatge' or None)
    if miss:
        p = objecte.missModeracio.create(author=user, body=miss)
        #posem el post en el estat de moderació 'en tramit
        objecte.moderacio= 'E'
        objecte.save()

        #El usuari ha de rebre una notificació quan un missatge es creat al debat de moderació de un post
        notify.send(user, recipient = receptor, verb = u'comentat el missatge de moderacio', action_object = objecte,
                 description = desc, target = objecte.cela)

    missatge = objecte.missModeracio.all()

    return render(request, "missatgeriaModeracio.html", { 'missatge': missatge, 'objecte':objecte, 'tipus':tipus})
