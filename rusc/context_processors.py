__author__ = 'Zartch'


def notifications_user(request):
    if not request.user.is_authenticated():
        return ''

    if request.user.is_anonymous():
        return ''

    ret = request.user.notifications.unread()
    return { 'notifications_user' : ret}

