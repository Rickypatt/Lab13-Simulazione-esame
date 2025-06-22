import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._bestScore = None
        self._bestPath = None
        self._graph = nx.DiGraph()
        self._idMap = {}

    def buildGraph(self,anno):
        self._graph.clear()

        nodi = self.getDrivers(anno)
        for n in nodi:
            self._idMap[n.driverId] = n
        self._graph.add_nodes_from(nodi)
        archi = self.getEdges(anno)
        for a in archi:
            self._graph.add_edge(self._idMap[a[0]], self._idMap[a[1]], weight=a[2])


        dictPesi = {}
        for n in self._graph.nodes:
            pesoU = self._graph.out_degree(n, weight="weight")
            pesoE = self._graph.in_degree(n, weight="weight")
            dictPesi[n] = pesoU - pesoE

        best = max(dictPesi, key=dictPesi.get)
        return dictPesi, best

    def getGraphDetails(self):
        return self._graph.number_of_nodes(), self._graph.number_of_edges()

    def getAllYears(self):
        return DAO.getYears()

    def getDrivers(self,year):
        return DAO.getDrivers(year)

    def getEdges(self,year):
        return DAO.getEdges(year)

    def getDreamTeam(self, k):
        self._bestPath = []
        self._bestScore = 10000

        parziale = []
        self.ricorsione(parziale,k)
        parziale.pop()

        return self._bestPath, self._bestScore

    def ricorsione(self, parziale, k):
        if len(parziale) == k and self.getScore(parziale) < self._bestScore:
            self._bestPath = copy.deepcopy(parziale)
            self._bestScore = self.getScore(parziale)
            return

        for n in self._graph.nodes():
            if n not in parziale:
                parziale.append(n)
                self.ricorsione(parziale,k)
                parziale.pop()

    def getScore(self, parziale):
        tasso = 0
        for n in self._graph.edges(data = True):
            if n[0] not in parziale and n[1] in parziale:
                tasso += n[2]["weight"]
        return tasso



