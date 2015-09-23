__author__ = 'Zartch'
from usuari.models import UserProfile
from cela.models import get_cela

def notifications_user(request):
    if not request.user.is_authenticated():
        return ''

    if request.user.is_anonymous():
        return ''

    ret = request.user.notifications.all()
    return { 'notifications_user' : ret}

def perfil_usuari(request):
    if not request.user.is_authenticated():
        return ''

    if request.user.is_anonymous():
        return ''

    user = request.user
    cela=get_cela(request)
    if cela:
        userprofile = UserProfile.objects.filter(cela=get_cela(request), user=user).first()
        return { 'perfilusuari' : userprofile}
    else:
        return ''

