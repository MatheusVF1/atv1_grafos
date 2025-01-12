import numpy as np
from shapely import geometry
import matplotlib.pyplot as plt
from math import dist
from descartes.patch import PolygonPatch
from matplotlib import Path
import random

def lerVertices(arquivo):
    entrada = arquivo.readlines() 
    aux = 0
    V = []

    for i in range(0, 2):
        divi = entrada[i]
        if i == 0:
            divi = divi.split(",")
            pontoInicial = (float(divi[0]), float(divi[1]))
            V.append(pontoInicial)
        else:
            divi = divi.split(",")
            pontoFinal = (float(divi[0]), float(divi[1]))
            V.append(pontoFinal)

    quantObstaculos = int(entrada[2])
    aux = 3
    quantPontos = 0
    polV = []

    for i in range(quantObstaculos):
        quantPontos = int(entrada[aux])
        polG = []
        for j in range(quantPontos):
            aux += 1
            divi = entrada[aux]

            divi = divi.split(", ")
            V.append((float(divi[0]), float(divi[1])))
            polG.append((float(divi[0]), float(divi[1])))
        polV.append(polG)
        aux += 1
    return pontoInicial, pontoFinal, polV, V

#Indo pegar os dados do arquivo txt
f = open("mapa.txt", "r")
comeco, final, Vertices, allVertices = lerVertices(f)

# fazendo o mapa e plotando ele
armazenPoligono = []
fig, gp = plt.subplots()

for polig in Vertices:
    poliC = geometry.Polygon(shell=polig)
    armazenPoligono.append(poliC)

    x, y = poliC.exterior.xy
    gp.fill(x, y, alpha=0.5, fc='black')
    plt.plot(x, y)

pontos = []
i = 0

for p in allVertices:
    cponto = geometry.Point(p)
    pontos.append(cponto)
    x, y = cponto.xy
    plt.plot(x, y, 'o')
    gp.annotate(str(i), (x[0], y[0]))
    i += 1

    
    
    

lines =[]
fig,gp = plt.subplots()

for i in allVertices:
    for j in allVertices:
      if i!=j:
        vaiProximo = False
        line = geometry.LineString([i,j])
        for poliC in armazenPoligono:
          if line.crosses(poliC) or poliC.contains(line) or poliC.covers(line):
            vaiProximo = True
        if vaiProximo == False:

          lines.append(line)
          x,y = line.xy
          plt.plot(x,y)

for polig in armazenPoligono:
  x,y = polig.exterior.xy
  gp.fill(x, y, alpha=1, fc='black')


    
    
    

class Graph:
    def __init__(self, vertices):
        self.quantVertices = vertices
        self.graph = []

    def gprint(self):
        print(self.graph)

    def add_edge(self, u, v, w):
        self.graph.append([u, v, w])

def grafoVisibilidade(Poligonos, V):
    G = Graph(15)
    fig, gp = plt.subplots()

    for i in V:
        for j in V:
            if i!=j:
                vaiProximo = False
                line = geometry.LineString([i,j])
                for poliC in Poligonos:
                    if line.crosses(poliC) or poliC.contains(line) or poliC.covers(line):
                        vaiProximo = True
                if vaiProximo == False:
                    G.add_edge(allVertices.index(i),allVertices.index(j),line.length)
                    x,y = line.xy
                    plt.plot(x,y)
    for polig in Poligonos:
        x,y = polig.exterior.xy
        gp.fill(x, y, alpha=1, fc='black')
    return G

G = grafoVisibilidade(armazenPoligono, allVertices)





def mstKruskal(G):
    T = []
    indice = 0
    aresta = 0
    G.graph = sorted(G.graph, key=lambda vertice: vertice[2])
    vizinho = []
    classif = []

    for vertice in range(G.quantVertices):
        vizinho.append(vertice)
        classif.append(0)
    
    while aresta < G.quantVertices - 1:
        u, v, w = G.graph[indice]
        indice = indice + 1
        x = achar(vizinho, u)
        y = achar(vizinho, v)
        if x != y:
            aresta = aresta + 1
            T.append([u, v, w])
            juncao(vizinho, classif, x, y)

    custoMinimo = 0
    print("Arestas da árvore construída com Kruskal")

    for u, v, weight in T:
        custoMinimo += weight
        print("{} --- {} == {}".format(u, v, weight))
    
    print("\nMenor árvore vista:", custoMinimo)
    return T

def mstPrim(G):
    T = []
    matrizG = [[0 for coluna in range(G.quantVertices)] for fileira in range(G.quantVertices)]
    Vselecionado = [0] * G.quantVertices

    for aresta in G.graph:
        matrizG[aresta[0]][aresta[1]] = aresta[2]
    
    Vselecionado[0] = True
    quantArestas = 0

    while quantArestas < G.quantVertices - 1:
        minimo = np.Inf
        u = 0
        v = 0
        for i in range(G.quantVertices):
            if Vselecionado[i]:
                for j in range(G.quantVertices):
                    if ((not Vselecionado[j]) and matrizG[i][j]):
                        if minimo > matrizG[i][j]:
                            minimo = matrizG[i][j]
                            u = i
                            v = j
        T.append([u, v, matrizG[u][v]])
        Vselecionado[v] = True
        quantArestas += 1
    
    T = sorted(T, key=lambda vertice: vertice[2])
    custoMinimo = 0
    print("\nArestas da árvore construída com Prim")

    for u, v, weight in T:
        custoMinimo += weight
        print("{} --- {} == {}".format(u, v, weight))
    
    print("\nMenor árvore vista:", custoMinimo)
    return T

def menorChave(key, mst, G):
    minimo = np.Int
    for v in range(G.quantVertices):
        if key[v] < minimo and mst[v] == False:
            minimo = key[v]
            indiceMin = v
    return indiceMin

def juncao(vizinho, classif, x, y):
    if classif[x] < classif[y]:
        vizinho[x] = y
    elif classif[x] > classif[y]:
        vizinho[y] = x
    else:
        vizinho[y] = x
        classif[x] += 1

def achar(vizinho, i):
    if vizinho[i] == i:
        return i
    return achar(vizinho, vizinho[i])

kruskal = mstKruskal(G)
prim = mstPrim(G)




def verticeMaisProximo(T, posicao, pontos):
    novoVert = geometry.Point((posicao[0],posicao[1]))
    menorDist = float(123456)
    vertice = -100

    for i in range(len(pontos)):
        if novoVert.distance(pontos[i]) < menorDist:
            menorDist = novoVert.distance(pontos[i])
            vertice = i
    if menorDist == 0.0:
        print(f"Local escolhido já estava no trajeto dos vértices: {vertice}")
    else:
        T = T.append([len(pontos)-1, vertice, menorDist])
        pontos.append(novoVert)
    return vertice

posic = np.array([1,10])  # Fazendo teste com ponto inicial
v = verticeMaisProximo(kruskal, posic, pontos)




def computarCaminho(T, start, end, pontos):
    verticeInicial = verticeMaisProximo(T, start, pontos)
    verficeFinal = verticeMaisProximo(T, end, pontos)
    matrizV = [[] for linha in range(len(pontos))]
    
    for u, v, w in T:
        matrizV[u].append(v)
        matrizV[v].append(u)

    for i in range(len(matrizV)):
        matrizV[i] = sorted(matrizV[i], key=lambda v: v)

    visitado = set()
    fila = []
    vizinho = [0] * 15
    fila.append(verticeInicial)
    visitado.add(verticeInicial)

    while fila:
        Vatual = fila.pop(0)

        if Vatual == verficeFinal:
            return calCaminho(vizinho, verticeInicial, verficeFinal)
        
        for k in matrizV[Vatual]:
            if k not in visitado:
                vizinho[k] = Vatual
                visitado.add(k)
                fila.append(k)

def calCaminho(pais, verticeInicial, verficeFinal):
    path = []
    path.append(verficeFinal)

    while path[-1] != verticeInicial:
        path.append(pais[path[-1]])
    
    path.reverse()
    return path

start = np.array([1, 10])
end = np.array([10, 1])
resultadoCaminho = computarCaminho(kruskal, start, end, pontos)
print(resultadoCaminho)



start = np.array([random.uniform(0,10), random.uniform(0,10)])
end = np.array([random.uniform(0,10), random.uniform(0,10)])
print("Pontos aleatórios obtidos:", start,end)

path = computarCaminho(kruskal, start, end,pontos)
print("Caminho obtido com os pontos aleatórios:", path)
