import copy

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
        self.artista = self.dizionario_artisti[id_artista]  #valore inizializzato con self, richiamato nel punto 2

        #print(artista) check passaggio valori da controller - corretto

        lista_vicini = []

        for vicino in self._graph.neighbors(self.artista):
            diz = {"vicino":vicino, "peso":0}
            peso = self._graph[self.artista][vicino]["weight"]
            diz["peso"] = peso
            lista_vicini.append(diz)

        self.lista_ordinata_vicini = sorted(lista_vicini, key = lambda x: x["vicino"], reverse = False)

        #print(self.lista_ordinata_vicini[0:5])

    def cerca_cammino(self, durata_minuti, n_max_artisti):
        #print("collegamento corretto")

        #cammino di peso massimo con lunghezza fissata che è il n. max artisti

        nodo_inizale = self.artista

        lista_id_artisti_minutaggi_validi = DAO.get_durate_artisti(durata_minuti)   #recupero dal dao gli id degli artisti che rispettano la condizione di minutaggio
        self.lista_artisti_minutaggi_validi = []
        #dizionario_artisti_validi = {}

        for id_art in lista_id_artisti_minutaggi_validi: #degli artisti trovati dal DAO mi serve che comunque rispettino le condizioni iniziali
            art_pot = self.dizionario_artisti[id_art]
            if art_pot in self.lista_artisti_validi:
                self.lista_artisti_minutaggi_validi.append(art_pot)

        #print(self.lista_artisti_minutaggi_validi)

        self.n_max_artisti = n_max_artisti

        self.cammino_ottimo = []
        self.peso_ottimo = 0

        parziale = [nodo_inizale]
        peso_parziale = 0

        self.ricorsione(parziale, peso_parziale)

        print(self.cammino_ottimo)
        print(self.peso_ottimo)


    def ricorsione(self, parziale, peso):

        if len(parziale) == self.n_max_artisti :    #condizione di escape basata sul numero di artisti già presenti
            if peso > self.peso_ottimo :
                self.peso_ottimo = peso
                self.cammino_ottimo = copy.deepcopy(parziale)
                return

        for nodo_vicino in self._graph.neighbors(parziale[-1]):
            if nodo_vicino in self.lista_artisti_minutaggi_validi and nodo_vicino not in parziale:
                peso_arco = self._graph[parziale[-1]][nodo_vicino]["weight"]
                parziale.append(nodo_vicino)
                self.ricorsione(parziale, peso + peso_arco)
                parziale.pop()  #backtracking







