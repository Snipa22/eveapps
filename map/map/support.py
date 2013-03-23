from map.models import wormholes, whspace
import networkx as nx
from django.conf import settings
import matplotlib.pyplot as plt

def generatemap():
    dbholes = wormholes.objects.get()
    G=nx.path_graph()
    for wh in dbholes:
        if wh.sig.location not in G:
            G.add_node(wh.sig.location, type=wh.whtype.whtype)
        if wh.link not in G:
            G.add_node(wh.link, type=wh.whtype.whtype)
        G.add_edge(wh.sig.location, wh.link)
        G.edge[wh.sig.location][wh.link]['massleft'] = wh.massleft
        G.edge[wh.sig.location][wh.link]['maxtime'] = wh.whtype.maxtime
        G.edge[wh.sig.location][wh.link]['exipretime'] = wh.sigs.expiretime
        G.edge[wh.sig.location][wh.link]['maxmass'] = wh.whtype.maxmass
        G.edge[wh.sig.location][wh.link]['jumpmass'] = wh.whtype.jumpmass
    nx.draw(G)
    plt.savefig("test.png")
    plt.show()