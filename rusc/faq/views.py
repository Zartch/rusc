from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView
from django.core.urlresolvers import reverse
from django.contrib import messages as notif_messages

from rusc.faq.models import Pregunta
from cela.models import get_cela
from rusc.faq.forms import faqForm


def faqview(request):
    faqs = Pregunta.objects.filter(cela= get_cela(request))

    return render(request, "faq.html",{'faqs':faqs})


class faqCreateView(CreateView):
    model = Pregunta
    form_class = faqForm

    def form_valid(self, form):
        f = form.save(commit=False)
        f.cela = get_cela(self.request)
        f.created_by = self.request.user
        f.updated_by = self.request.user

        return super(faqCreateView, self).form_valid(form)

    def get_success_url(self):
        notif_messages.add_message(self.request, notif_messages.INFO, "Has creat una nova pregunta als FAQ", 'success')
        return reverse('faq')

    def form_invalid(self, form):
        notif_messages.add_message(self.request, notif_messages.INFO, "corregeix els errors indicats", 'warning')
        return super(faqCreateView, self).form_invalid(form)

class faqUpdateView(UpdateView):
    model = Pregunta
    form_class= faqForm
    template_name = "faq/Pregunta_form.html"

    def form_valid(self,form):
        notif_messages.add_message(self.request, notif_messages.INFO, "Has modificat una FAQ", 'success')
        return super(faqUpdateView, self).form_valid(form)

    def form_invalid(self, form):
        notif_messages.add_message(self.request, notif_messages.INFO, "corregeix els errors indicats", 'warning')
        return super(faqUpdateView, self).form_invalid(form)

    def get_success_url(self):
        notif_messages.add_message(self.request, notif_messages.INFO, "Has modificat la pregunta als FAQ", 'success')
        return reverse('faq')