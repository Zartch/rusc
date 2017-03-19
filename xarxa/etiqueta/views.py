# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages as notif_messages
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django_tables2   import RequestConfig

from xarxa.etiqueta.forms import tesauroForm, newEtiquetaForm
from xarxa.etiqueta.models import TesauroFilter,Tesauro
from xarxa.etiqueta.tables import tesauroTable, etiquetaTable
from xarxa.post.models import Post,Vote, folksonomia
from xarxa.etiqueta.models import Etiqueta, EtiquetaFilter
from cela.models import Cela, get_cela


def etiquetaview(request,etq):
    cela = get_cela(request)
    etiqueta = Etiqueta.objects.filter(pk=etq, cela = cela).first()
    posts_relacionats = Post.with_votes.get_queryset().filter(etiquetes = etiqueta, cela = cela.pk).exclude(moderacio='R').order_by()

    if not request.user.is_anonymous():
        voted = Vote.objects.filter(voter=request.user)
        voted = voted.values_list('post_id', flat=True)
    else:
        voted = []

    d = folksonomia(posts_relacionats)
    sorted_rel = sorted(d, key=d.get) #ordenem les etiquetes relacionades per post segons numero de vincles

    tesauros_forts = Tesauro.objects.filter(etq1=etiqueta)
    tesauros_debils = Tesauro.objects.filter(etq2=etiqueta)

    tesauro = {}
    tesauro['relacio']= d
    sinonims= list(Tesauro.objects.filter(etq1=etiqueta,tipo='S').values_list('etq2__nom', flat=True)) + list (Tesauro.objects.filter(etq2=etiqueta,tipo='S').values_list('etq1__nom', flat=True))
    antonims =list(Tesauro.objects.filter(etq1=etiqueta,tipo='A').values_list('etq2__nom', flat=True)) + list (Tesauro.objects.filter(etq2=etiqueta,tipo='A').values_list('etq1__nom', flat=True))
    associat = list(Tesauro.objects.filter(etq1=etiqueta,tipo='B').values_list('etq2__nom', flat=True)) + list (Tesauro.objects.filter(etq2=etiqueta,tipo='B').values_list('etq1__nom', flat=True))
    tesauro['sinonims']= sinonims
    tesauro['antonims']= antonims
    tesauro['associat']= associat
    tesauro['conte']= Tesauro.objects.filter(etq1=etiqueta).values_list('etq2__nom', flat=True)
    tesauro['contingut']= Tesauro.objects.filter(etq2=etiqueta).values_list('etq1__nom', flat=True)


    return render(request,"etiqueta.html", {'etiqueta':etiqueta, 'posts_rel': sorted_rel, 'tesaurosforts':tesauros_forts,
                                            'tesaurosdebils':tesauros_debils, 'voted':voted, 'posts': posts_relacionats,
                                            'tesauro':tesauro})

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

    tesauros_forts = Tesauro.objects.filter(etq1 = etiqueta).exclude(etq2 = etiqueta)
    tesauros_debils = Tesauro.objects.filter(etq2 = etiqueta).exclude(etq1 = etiqueta)
    d = folksonomia(posts_relacionats)
    sorted_rel = sorted(d, key=d.get) #ordenem les etiquetes relacionades per post segons numero de vincles

    tesauro = {}
    tesauro['relacio'] = d
    sinonims = list(Tesauro.objects.filter(etq1 = etiqueta, tipo='S').values_list('etq2__nom', flat=True)) + list (Tesauro.objects.filter(etq2=etiqueta,tipo='S').values_list('etq1__nom', flat=True))
    antonims = list(Tesauro.objects.filter(etq1 = etiqueta, tipo='A').values_list('etq2__nom', flat=True)) + list (Tesauro.objects.filter(etq2=etiqueta,tipo='A').values_list('etq1__nom', flat=True))
    associat = list(Tesauro.objects.filter(etq1 = etiqueta, tipo='B').values_list('etq2__nom', flat=True)) + list (Tesauro.objects.filter(etq2=etiqueta,tipo='B').values_list('etq1__nom', flat=True))
    tesauro['sinonims'] = sinonims
    tesauro['antonims'] = antonims
    tesauro['associat'] = associat
    tesauro['conte'] = Tesauro.objects.filter(etq1=etiqueta).values_list('etq2__nom', flat=True)
    tesauro['contingut'] = Tesauro.objects.filter(etq2=etiqueta).values_list('etq1__nom', flat=True)



    return render(request,"etiqueta.html", {'etiqueta':etiqueta, 'posts_rel': sorted_rel, 'tesaurosforts':tesauros_forts,
                                            'tesaurosdebils':tesauros_debils, 'voted':voted, 'posts': posts_relacionats,
                                            'tesauro':tesauro})


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


class EtiquetaCreateView(CreateView):
    model = Etiqueta
    form_class = newEtiquetaForm

    def get_context_data(self, **kwargs):
        context = super(EtiquetaCreateView, self).get_context_data(**kwargs)
        try:
            cela = get_cela(self.request)
            listado_etq = EtiquetaFilter(self.request.GET, queryset=Etiqueta.objects.filter(cela = cela))
            table = etiquetaTable(listado_etq)
            RequestConfig(self.request,paginate={"per_page": 25}).configure(table)
            context['table_etiquetes'] = table
        except ValueError:
            pass
        return context

    def get_form_kwargs(self):
        kwargs = super(EtiquetaCreateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_success_url(self):
        notif_messages.add_message(self.request, notif_messages.INFO, "Has creat una nova relacio", 'success')
        return reverse('etiqueta_nova')

    def form_valid(self, form):
        form.instance.cela = get_cela(self.request)
        form.save()
        return super(EtiquetaCreateView, self).form_valid(form)

    def form_invalid(self, form):
        notif_messages.add_message(self.request, notif_messages.INFO, "corregeix els errors indicats", 'warning')
        return super(EtiquetaCreateView, self).form_invalid(form)

class etiquetaUpdateView(UpdateView):
    model = Etiqueta
    form_class = newEtiquetaForm


    def get_context_data(self, **kwargs):
        context = super(etiquetaUpdateView, self).get_context_data(**kwargs)
        cela = get_cela(self.request)
        listado_etq = EtiquetaFilter(self.request.GET, queryset=Etiqueta.objects.filter(cela = cela))
        table = etiquetaTable(listado_etq)
        RequestConfig(self.request,paginate={"per_page": 25}).configure(table)
        context['table_etiquetes'] = table
        return context

    def form_valid(self, form):
        notif_messages.add_message(self.request, notif_messages.INFO, "Has modificat la etiqueta", 'success')
        return super(etiquetaUpdateView, self).form_valid(form)

    def form_invalid(self, form):
        notif_messages.add_message(self.request, notif_messages.INFO, "corregeix els errors indicats", 'warning')
        return super(etiquetaUpdateView, self).form_invalid(form)

    def get_success_url(self):
        notif_messages.add_message(self.request, notif_messages.INFO, "etiqueta modificada correctament", 'success')
        return reverse('etiqueta_nova')

    def get_form_kwargs(self):
        kwargs = super(etiquetaUpdateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

class etiquetaDeleteView(DeleteView):
    model = Etiqueta
    success_url = reverse_lazy('etiqueta_nova')

    def get_form_kwargs(self):
        kwargs = super(etiquetaDeleteView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class tesauroCreateView(CreateView):
    model = Tesauro
    form_class = tesauroForm

    def get_context_data(self, **kwargs):
        context = super(tesauroCreateView, self).get_context_data(**kwargs)
        try:
            cela = get_cela(self.request)
            context['llista_tesauros'] = Tesauro.objects.filter(etq1__cela = cela, etq2__cela = cela)
            context['llista_etiquetes'] = Etiqueta.objects.filter(cela= cela)
            listado = TesauroFilter(self.request.GET, queryset=Tesauro.objects.filter(etq1__cela = cela, etq2__cela = cela))
            table = tesauroTable(listado)
            RequestConfig(self.request,paginate={"per_page": 25}).configure(table)
            context['table'] = table
        except ValueError:
            pass
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