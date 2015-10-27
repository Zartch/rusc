from cela.models import get_cela

def cela_context(request):
        return {
            'cela':get_cela(request),
        }