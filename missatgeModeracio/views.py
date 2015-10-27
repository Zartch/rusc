from django.shortcuts import render
from notifications import notify
from django.shortcuts import get_object_or_404

from rusc.post.models import Post
from rusc.recurs.models import Recurs
from rusc.etiqueta.models import Etiqueta





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
        #posem el post en el estat de moderació 'en tramit, només si el usari es moderador
        #(això es per que els usaris co tornin a posar en estat E un post ja rebutjat)
        #Però que si siguin capaços de fero els admins
        cela = objecte.cela
        if request.user in cela.moderadors.all():
            objecte.moderacio= 'E'
            objecte.save()

        #El usuari ha de rebre una notificació quan un missatge es creat al debat de moderació de un post
        notify.send(user, recipient = receptor, verb = u'comentat el missatge de moderacio', action_object = objecte,
                 description = desc, target = objecte.cela)

    missatge = objecte.missModeracio.all()

    return render(request, "missatgeriaModeracio.html", { 'missatge': missatge, 'objecte':objecte, 'tipus':tipus})
