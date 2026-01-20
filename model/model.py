import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._artists_list = []
        self.dizionario_artisti = {}
        self.load_all_artists()

    def load_all_artists(self):
        self._artists_list = DAO.get_all_artists()
        print(f"Artisti: {self._artists_list}")

        for artist in self._artists_list:
            self.dizionario_artisti[artist.id] = artist

    def load_artists_with_min_albums(self, min_albums):         #la funzione viene chiamata nel controller immediatamente prima della funzione di costruzione grafo
        lista_artisti = DAO.get_artisti_album(int(min_albums))

        self.lista_artisti_validi = []

        for id_artista in lista_artisti:
            artista = self.dizionario_artisti[id_artista]
            self.lista_artisti_validi.append(artista)

        print(f"Nodi trovati")
        print(self.lista_artisti_validi)

    def build_graph(self):
        self._graph.clear()

        self._graph.add_nodes_from(self.lista_artisti_validi)

        #Ottengo gli archi

        lista_archi = DAO.get_edges()

        #verifico che negli archi creati entrambi gli artisti (nodi) siano effettivamente
        #effettivamente presenti tra quelli creati

        for arco in lista_archi:
            a1 = self.dizionario_artisti[arco[0]]
            a2 = self.dizionario_artisti[arco[1]]
            if a1 in self.lista_artisti_validi and a2 in self.lista_artisti_validi:
                self._graph.add_edge(a1,a2,weight = arco[2])

        #print(self._graph) check prova risultato - CONFORME AL TESTO

    def connected_artists(self, id_artista):
        artista = self.dizionario_artisti[id_artista]

        #print(artista) check passaggio valori da controller - corretto

        lista_vicini = []

        for vicino in self._graph.neighbors(artista):
            diz = {"vicino":vicino, "peso":0}
            peso = self._graph[artista][vicino]["weight"]
            diz["peso"] = peso
            lista_vicini.append(diz)

        self.lista_ordinata_vicini = sorted(lista_vicini, key = lambda x: x["peso"], reverse = False)
        print(self.lista_ordinata_vicini[0:5])




