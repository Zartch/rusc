from cela.models import get_cela

def cela_context(request):
        return {
            'cela_context':get_cela(request),
        }