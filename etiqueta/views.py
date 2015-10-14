# -*- coding: utf-8 -*-
from .models import Etiqueta, Tesauro
from post.models import Post,Vote, folksonomia
from cela.models import Cela, get_cela
from django.shortcuts import render,get_object_or_404,redirect
from django.db.models import Q
from etiqueta.forms import tesauroForm
from django.template.defaultfilters import slugify

def etiquetaview(request,etq):
    cela = get_cela(request)
    etiqueta = Etiqueta.objects.filter(pk=etq, cela = cela).first()
    posts_relacionats = Post.with_votes.get_queryset().filter(etiquetes = etiqueta, cela = cela.pk).exclude(moderacio='R').order_by()

    if not request.user.is_anonymous():
        voted = Vote.objects.filter(voter=request.user)
        voted = voted.values_list('post_id', flat=True)
    else:
        voted= []

    tesauros_forts = Tesauro.objects.filter(Q(etq1=etiqueta))
    tesauros_debils = Tesauro.objects.filter(Q(etq2=etiqueta))

    # d = dict()
    # for post_rel in posts_relacionats:
    #     a=post_rel.folksonomia(etiqueta)
    #     for key,value in a.items():
    #         if key in d:
    #             #suma els values
    #             val = d[key]
    #             val = val + value
    #             d[key] = val
    #         else:
    #             d[key]= value

    d = folksonomia(posts_relacionats)

    sorted_rel = sorted(d, key=d.get) #ordenem les etiquetes relacionades per post segons numero de vincles

    return render(request,"etiqueta.html", {'etiqueta':etiqueta, 'posts_rel': sorted_rel, 'tesaurosforts':tesauros_forts, 'tesaurosdebils':tesauros_debils, 'voted':voted, 'posts_relacionats': posts_relacionats})

def nometiquetaview(request,nometq,nomcela):
    #cela = get_cela(request)
    cela = Cela.objects.filter(slug= nomcela).first()
    etiqueta = Etiqueta.objects.filter(slug=nometq, cela = cela.pk).first()
    posts_relacionats = Post.with_votes.get_queryset().filter(etiquetes = etiqueta, cela = cela.pk).exclude(moderacio='R')

    if not request.user.is_anonymous():
        voted = Vote.objects.filter(voter=request.user)
        voted = voted.values_list('post_id', flat=True)
    else:
        voted= []

    tesauros_forts = Tesauro.objects.filter(Q(etq1=etiqueta))
    tesauros_debils = Tesauro.objects.filter(Q(etq2=etiqueta))
    d = folksonomia(posts_relacionats)
    sorted_rel = sorted(d, key=d.get) #ordenem les etiquetes relacionades per post segons numero de vincles

    return render(request,"etiqueta.html", {'etiqueta':etiqueta, 'posts_rel': sorted_rel, 'tesaurosforts':tesauros_forts, 'tesaurosdebils':tesauros_debils, 'voted':voted, 'posts_relacionats': posts_relacionats})


def todoview(request):
    cela = get_cela(request)
    etiqueta = Etiqueta.objects.filter(nom='ToDo', cela = cela)
    posts = Post.objects.filter(etiquetes=etiqueta, cela = cela)

    return render(request,"toDo.html", {'posts':posts})

def feinafeta(request,pkpost):
    cela = get_cela(request)
    todo = Etiqueta.objects.get(nom='ToDo', cela = cela)
    todo_post = Post.objects.filter(pk=pkpost, cela = cela).first()
    todo_post.etiquetes.remove(todo)

    posts = Post.objects.filter(etiquetes=todo, cela = cela)

    return render(request,"toDo.html", {'posts':posts})


from django.contrib import messages as notif_messages
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView


from .models import TesauroFilter,Tesauro
from .tables import tesauroTable
from django_tables2   import RequestConfig

class tesauroCreateView(CreateView):
    model = Tesauro
    form_class = tesauroForm

    def get_context_data(self, **kwargs):
        context = super(tesauroCreateView, self).get_context_data(**kwargs)
        cela = get_cela(self.request)
        context['llista_tesauros'] = Tesauro.objects.filter(etq1__cela = cela, etq2__cela = cela)
        context['llista_etiquetes'] = Etiqueta.objects.filter(cela= cela)
        listado = TesauroFilter(self.request.GET, queryset=Tesauro.objects.filter(etq1__cela = cela, etq2__cela = cela))
        table = tesauroTable(listado)
        RequestConfig(self.request,paginate={"per_page": 25}).configure(table)
        context['table'] = table

        return context

    def get_success_url(self):
        notif_messages.add_message(self.request, notif_messages.INFO, "Has creat una nova relacio", 'success')
        return reverse('tesauro_nou')


    def form_invalid(self, form):
        notif_messages.add_message(self.request, notif_messages.INFO, "corregeix els errors indicats", 'warning')
        return super(tesauroCreateView, self).form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super(tesauroCreateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

class tesauroUpdateView(UpdateView):
    model = Tesauro
    form_class = tesauroForm


    def get_context_data(self, **kwargs):
        context = super(tesauroUpdateView, self).get_context_data(**kwargs)
        cela = get_cela(self.request)
        context['llista_tesauros'] = Tesauro.objects.filter(etq1__cela = cela, etq2__cela = cela)

        listado = TesauroFilter(self.request.GET, queryset=Tesauro.objects.filter(etq1__cela = cela, etq2__cela = cela))
        table = tesauroTable(listado)
        RequestConfig(self.request,paginate={"per_page": 25}).configure(table)
        context['table'] = table

        return context

    def form_valid(self, form):
        notif_messages.add_message(self.request, notif_messages.INFO, "Has modificat el tesauro", 'success')
        return super(tesauroUpdateView, self).form_valid(form)

    def form_invalid(self, form):
        notif_messages.add_message(self.request, notif_messages.INFO, "corregeix els errors indicats", 'warning')
        return super(tesauroUpdateView, self).form_invalid(form)

    #Si afegim moderadors, hem de crear el user profile, per a que el moderador no s'hagi d'acceptar a si mateix
    def get_success_url(self):
        notif_messages.add_message(self.request, notif_messages.INFO, "tesauro modificada correctament", 'success')
        return reverse('tesauro_nou')

    def get_form_kwargs(self):
        kwargs = super(tesauroUpdateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy

class tesauroDeleteView(DeleteView):
    model = Tesauro
    success_url = reverse_lazy('tesauro_nou')

    def get_form_kwargs(self):
        kwargs = super(tesauroDeleteView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


# def tesauroDelete(request,pk):
#     TesDell= Tesauro.objects.filter(pk= pk).delete()
#     cela = get_cela(request)
#     llista_tesauros = Tesauro.objects.filter(etq1__cela = cela, etq2__cela = cela)
#     form = tesauroForm
#
#     return HttpResponseRedirect(reverse('tesauro_nou', kwargs={'request': request}))
#     #return render(request, "etiqueta/tesauro_form.html", {'llista_tesauros':llista_tesauros, 'form':form,'request':request})