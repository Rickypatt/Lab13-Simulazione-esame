import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model


    def handleDDYearSelection(self, e):
        pass

    def handleCreaGrafo(self,e):
        anno =  self._view._ddAnno.value
        dictPesi, best = self._model.buildGraph(anno)
        numNodi, numArchi = self._model.getGraphDetails()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Grafo creato correttamente"))
        self._view.txt_result.controls.append(ft.Text(f"numero di nodi: {numNodi}"))
        self._view.txt_result.controls.append(ft.Text(f"numero di archi: {numArchi}"))
        self._view.txt_result.controls.append(ft.Text(f"Best driver: {best}, wih score {dictPesi[best]}"))
        self._view.update_page()


    def handleCerca(self, e):
        k = self._view._txtIntK.value
        if k is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Attenzione, inserisci un numero intero"))
        else:
            try:
                intK = int(k)
                path, score = self._model.getDreamTeam(intK)
                self._view.txt_result.controls.clear()
                self._view.txt_result.controls.append(ft.Text(f"Miglior team di {k} piloti:"))
                for i in path:
                    self._view.txt_result.controls.append(ft.Text(f"{i}"))
                self._view.txt_result.controls.append(ft.Text(f"Tasso di sconfitta {score}"))

            except ValueError:
                self._view.txt_result.controls.clear()
                self._view.txt_result.controls.append(ft.Text(f"Attenzione, inserisci un numero intero"))



    def fillDDYear(self):
        anni = self._model.getAllYears()
        for a in anni:
            self._view._ddAnno.options.append(ft.dropdown.Option(a))