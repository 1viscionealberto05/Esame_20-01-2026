import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def handle_create_graph(self, e):
        try:
            self.num_album = int(self._view.txtNumAlbumMin.value)

            if self.num_album < 0:
                self._view.alert.show_alert("Inserisci un numero positivo di album")
            else:
                self._model.load_artists_with_min_albums(self.num_album)
                self._model.build_graph()

                self._view.txt_result.controls.clear()

                num_nodi = self._model._graph.number_of_nodes()
                num_archi = self._model._graph.number_of_edges()

                self._view.txt_result.controls.append(ft.Text(f"Grafo creato: {num_nodi} nodi (artisti), {num_archi} archi"))

                self._view.btnArtistsConnected.disabled = False
                self._view.ddArtist.disabled = False

                #riempio la dropdown

                self._view.ddArtist.options.clear()

                for nodo in self._model._graph.nodes():
                    self._view.ddArtist.options.append(ft.DropdownOption(key=nodo.id, text=nodo.name))

                #print("corretto")
                self._view.update_page()

        except ValueError:
            self._view.alert.show_alert("Inserisci un numero di album valido")

    def artist_setter(self,e):
        self.id_artista_scelto = int(e.control.value)

        print(self.id_artista_scelto)

    def handle_connected_artists(self, e):
        self._view.txtMaxArtists.disabled = False
        self._view.txtMinDuration.disabled = False
        self._view.btnSearchArtists.disabled = False

        self._model.connected_artists(self.id_artista_scelto)

        self._view.txt_result.controls.clear()

        artista_scelto = self._model.dizionario_artisti[self.id_artista_scelto]

        self._view.txt_result.controls.append(ft.Text(f"Artisti direttamente collegati all'artista {artista_scelto}"))

        for i in range(0,len(self._model.lista_ordinata_vicini)):
            artista = self._model.lista_ordinata_vicini[i]["vicino"]
            n_generi = self._model.lista_ordinata_vicini[i]["peso"]
            self._view.txt_result.controls.append(ft.Text(f"{artista} - Numero di generi in comune: {n_generi}"))

        self._view.update_page()

    def search_artists(self, e):
        try:
            durata_minuti = float(self._view.txtMinDuration.value)
            n_max_artisti = int(self._view.txtMaxArtists.value)

            if durata_minuti < 0 or (n_max_artisti >= self._model._graph.number_of_nodes() or n_max_artisti <1):
                self._view.alert.show_alert("Inserisci dei valori nei range corretti per le caselle di testo")
            else:
                self._model.cerca_cammino(durata_minuti,n_max_artisti)


                self._view.txt_result.controls.clear()
                self._view.txt_result.controls.append(ft.Text(f"Cammino di peso massimo dall'artista {self._model.dizionario_artisti[self.id_artista_scelto]}"))

                self._view.txt_result.controls.append(ft.Text(f"Lunghezza: {len(self._model.cammino_ottimo)}"))

                for nodo in self._model.cammino_ottimo:
                    self._view.txt_result.controls.append(ft.Text(f"{nodo}"))

                self._view.txt_result.controls.append(ft.Text(f"Peso massimo {self._model.peso_ottimo}"))


                self._view.update_page()

        except ValueError:
            self._view.alert.show_alert("Inserisci dei valori corretti per le caselle di testo")

