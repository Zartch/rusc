from unittest import TestCase

from django.contrib.auth.models import User

from rusc.post.models import Post
from rusc.etiqueta.models import Etiqueta
from cela.models import Cela


class TestPost(TestCase):

    def setUp(self):
        us= User.objects.filter(id=1).first()
        c1 = Cela.objects.filter(id=1).first()

        #Etiquetes Etiquetes
        tg1= Etiqueta.objects.create(nom='e1',descripcio= 'd1',usuari=us, tipologia = 'E',cela=c1)
        tg2= Etiqueta.objects.create(nom='e2',descripcio= 'd2',usuari=us, tipologia = 'E',cela=c1)
        tg3= Etiqueta.objects.create(nom='e3',descripcio= 'd3',usuari=us, tipologia = 'E',cela=c1)
        tg4= Etiqueta.objects.create(nom='e4',descripcio= 'd4',usuari=us, tipologia = 'E',cela=c1)


        p1=Post.objects.create(cela=c1 ,autor=us, titol='Era se una vez la vida', text='La vida es así.. la vida es así')
        p11=Post.objects.create(cela=c1 ,autor=us, titol='La Sangre', pare = p1, text='La sangre es una cosa viscosa y roja')
        p111=Post.objects.create(cela=c1 ,autor=us, titol='Las plaquetas', pare = p11, text='Las Plaquetas sirven para tapar heridas')
        p112=Post.objects.create(cela=c1 ,autor=us, titol='los globulos blancos', pare = p11, text='Los globulos blancos matan virus')
        p113=Post.objects.create(cela=c1 ,autor=us, titol='los globulos rojos', pare = p11, text='Los globulos rojos transportan sangre')
        p12 =Post.objects.create(cela=c1 ,autor=us, titol='Los huesos', pare = p1,  text='Los huesos matienen el esqueleto')
        p13 =Post.objects.create(cela=c1 ,autor=us, titol='El sistema digestivo ', pare = p1, text='El sistema digestivo absorve nutrientes de la comida')
        p1.save()
        p1.etiquetes.add(tg1)



        p2=Post.objects.create(cela=c1 ,autor=us, titol='Era se una vez los exploradores', text='Los exploradores exploran como dora la exploradora')
        p21= Post.objects.create(cela=c1 ,autor=us, titol='Colón', pare = p2, text='Colón no descubrió america, america fue invadida y saqueada')
        p220= Post.objects.create(cela=c1 ,autor=us, titol='Vikingos', pare = p2,  text='Ellos descubrieron america')
        p2.save()
        p2.etiquetes.add(tg1)
        p2.etiquetes.add(tg2)

        p3=Post.objects.create(cela=c1 ,autor=us, titol='Era se una vez los inventores',text='Los inventores inventan')
        p31=Post.objects.create(cela=c1 ,autor=us, titol='Leonardo Davinchi', pare = p3, text='Un tipo excentrico')
        p32=Post.objects.create(cela=c1 ,autor=us, titol='Nicola Tesla', pare = p3, text='El mejor inventor de todos')
        p3.save()
        p3.etiquetes.add(tg1)
        p3.etiquetes.add(tg2)
        p3.etiquetes.add(tg3)

        p4 = Post.objects.create(cela=c1 ,autor=us, titol='Django',  text='Django Discussion')
        p4.save()
        p4.etiquetes.add(tg1)
        p4.etiquetes.add(tg2)
        p4.etiquetes.add(tg3)
        p4.etiquetes.add(tg4)

    def test_existen(self):
        post = Post.objects.get(titol='Las plaquetas')
        self.assertEqual(post.pare.pare.titol,'Era se una vez la vida')