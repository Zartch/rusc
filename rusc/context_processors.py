__author__ = 'Zartch'
from cela.models import get_cela
from usuari.models import UserProfile

def notifications_user(request):
    if not request.user.is_authenticated():
        return ''

    if request.user.is_anonymous():
        return ''

    ret = request.user.notifications.all()
    for r in ret:
        userp = UserProfile.objects.filter(pk= r.actor_object_id).first()
        if userp.avatar:
            r.url = userp.avatar.url

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

