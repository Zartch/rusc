import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rusc.settings")

from .models import  Post

def rank_all():
    for link in Post.with_votes.all():
        link.set_rank()

import time

def show_all():
    print ("\n".join("%10s %0.2f" % (l.titol, l.rank_score,
                         ) for l in Post.with_votes.all()))
    print ("----\n\n\n")

if __name__=="__main__":
    while 1:
        print ("---")
        rank_all()
        show_all()
        time.sleep(5)

# aquest codi python s'ha de executar de fondo per a que es vagin recalculant el ranking_score de cada entrada,
# pq no nomes va per vots també hi influeixen altres variables en el ranking


# Turn it into a background job
#
# (nohup python -u rerank.py&)
# tail -f nohup.out
#
# Note that this is a very simplistic implementation of a background job. For a more robust solution, check out Celery.
