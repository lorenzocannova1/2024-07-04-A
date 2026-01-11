import copy

from database.DAO import DAO
import networkx as nx

from model.sighting import Sighting


class Model:
    def __init__(self):
        self.grafo = nx.DiGraph()
        self.idMapAvvisamenti = {}

        self.nodi = []
        self._cammino_ottimo = []
        self._score_ottimo = 0
        self._occorrenze_mese = dict.fromkeys(range(1, 13), 0)

    def getAllAnni(self):
        return DAO.getAllAnni()

    def getAllForme(self):
        return DAO.getAllForme()

    def creaGrafo(self, forma, anno):
        self.grafo.clear()
        self.nodi = DAO.getAllNodi(forma, anno) #sono sighting = avvistamenti
        self.grafo.add_nodes_from(self.nodi)

        for nodo in self.nodi:
            self.idMapAvvisamenti[nodo.id] = nodo

        """
        archi = DAO.getAllArchi(forma, anno, self.idMapAvvisamenti)
        for arco in archi:
            self.grafo.add_edge(arco[0], arco[1])
        """
        #in alternativa posso inserire gli archi su python
        for n1 in self.nodi:
            for n2 in self.nodi:
                if n1.datetime < n2.datetime and n1.state == n2.state:
                    self.grafo.add_edge(n1, n2)

        print(len(self.grafo.edges))

    def dettaglioGrafo(self):
        num_cc = nx.number_weakly_connected_components(self.grafo) #numero di componenti debolmente connesse
        cc = list(nx.weakly_connected_components(self.grafo))
        cc.sort(key=lambda x:len(x), reverse=True)
        primaCC = 0
        if len(cc) > 0:
            primaCC = cc[0]

        return num_cc, primaCC

    def infoGrafo(self):
        return len(self.grafo.nodes), len(self.grafo.edges)

    def getPercorso(self):
        self._cammino_ottimo = []
        self._score_ottimo = 0
        self._occorrenze_mese = dict.fromkeys(range(1, 13), 0)

        for nodo in self.nodi:
            self._occorrenze_mese[nodo.datetime.month] += 1
            successivi_durata_crescente = self._calcola_successivi(nodo)
            self._calcola_cammino_ricorsivo([nodo], successivi_durata_crescente)
            self._occorrenze_mese[nodo.datetime.month] -= 1
        return self._cammino_ottimo, self._score_ottimo

    def _calcola_cammino_ricorsivo(self, parziale: list[Sighting], successivi: list[Sighting]):
        if len(successivi) == 0:
            score = Model._calcola_score(parziale)
            if score > self._score_ottimo:
                self._score_ottimo = score
                self._cammino_ottimo = copy.deepcopy(parziale)
        else:
            for nodo in successivi:
                # aggiungo il nodo in parziale ed aggiorno le occorrenze del mese corrispondente
                parziale.append(nodo)
                self._occorrenze_mese[nodo.datetime.month] += 1
                # nuovi successivi
                nuovi_successivi = self._calcola_successivi(nodo)
                # ricorsione
                self._calcola_cammino_ricorsivo(parziale, nuovi_successivi)
                # backtracking: visto che sto usando un dizionario nella classe per le occorrenze, quando faccio il
                # backtracking vado anche a togliere una visita dalle occorrenze del mese corrispondente al nodo che
                # vado a sottrarre
                self._occorrenze_mese[parziale[-1].datetime.month] -= 1
                parziale.pop()

    def _calcola_successivi(self, nodo: Sighting) -> list[Sighting]:
        """
        Calcola il sottoinsieme dei successivi ad un nodo che hanno durata superiore a quella del nodo, senza eccedere
        il numero ammissibile di occorrenze per un dato mese
        """
        successivi = self._grafo.successors(nodo)
        successivi_ammissibili = []
        for s in successivi:
            if s.duration > nodo.duration and self._occorrenze_mese[s.datetime.month] < 3:
                successivi_ammissibili.append(s)
        return successivi_ammissibili

    @staticmethod
    def _calcola_score(cammino: list[Sighting]) -> int:
        """
        Funzione che calcola il punteggio di un cammino.
        :param cammino: il cammino che si vuole valutare.
        :return: il punteggio
        """
        # parte del punteggio legata al numero di tappe
        score = 100 * len(cammino)
        # parte del punteggio legata al mese
        for i in range(1, len(cammino)):
            if cammino[i].datetime.month == cammino[i - 1].datetime.month:
                score += 200
        return score





