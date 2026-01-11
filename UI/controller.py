import flet as ft
from UI.view import View
from model.modello import Model

class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self.annoSelezionato = None
        self.formaSelezionata = None

    def handle_graph(self, e):
        if self.formaSelezionata == None or self.annoSelezionato == None:
            self._view.txt_result1.controls.clear()
            self._view.txt_result1.controls.append(ft.Text("Inserire una forma ed un anno per creare il grafo"))
            self._view.update_page()
            return

        self._model.creaGrafo(self.formaSelezionata, self.annoSelezionato)
        nNodi, nArchi = self._model.infoGrafo()
        self._view.txt_result1.controls.clear()
        self._view.txt_result1.controls.append(ft.Text(f"Numero di vertici {nNodi}"))
        self._view.txt_result1.controls.append(ft.Text(f"Numero di archi {nArchi}"))

        num_cc, primaCC = self._model.dettaglioGrafo()
        if primaCC != 0:
            self._view.txt_result1.controls.append(
                ft.Text(f"La componente connessa più grande è costituita da {num_cc}"))
            for nodo in primaCC:
                self._view.txt_result1.controls.append(ft.Text(f"{nodo}"))
        else:
            self._view.txt_result1.controls.append(
                ft.Text(f"Componente connessa vuota. "))

        self._view.update_page()


        self._model.dettaglioGrafo()

    def handle_path(self, e):
        pass

    def riempi_ddyear(self):
        anni = self._model.getAllAnni()
        for anno in anni:
            self._view.ddyear.options.append(ft.dropdown.Option(data = anno, text = anno, on_click=self.pickAnnoSelezionato))

        self._view.update_page()

    def pickAnnoSelezionato(self,e):
        self.annoSelezionato = e.control.data
        print(self.annoSelezionato)

    def riempi_ddshape(self):
        forme = self._model.getAllForme()
        for forma in forme:
            self._view.ddshape.options.append(ft.dropdown.Option(data = forma, text = forma, on_click=self.pickFormaSelezionata))

        self._view.update_page()

    def pickFormaSelezionata(self,e):
        self.formaSelezionata = e.control.data
        print(self.formaSelezionata)

