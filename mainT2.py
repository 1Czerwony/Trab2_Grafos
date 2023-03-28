import math

class Grafo:
    def __init__(self, n):
        self.matriz = [[0 for i in range(n)] for j in range(n)]
        self.vertices = [[None,math.inf] for i in range(n)]
        self.arestas = {}
    
    def add_aresta(self,i,j,x):
        if i in range(len(self.matriz)) and j in range(len(self.matriz)):
            self.matriz[i][j] = x
            self.arestas[(i,j)] = 0
    
    def __str__(self):
        return "vertices:"+str(self.matriz)
    
#------------------------------------------------------------------------------------------------------

def Initialize_Single_Source(g, s):
    for v in g.vertices:
        v = {None,math.inf}
    g.vertices[s][1] = 0

#------------------------------------------------------------------------------------------------------

def Relax(g,u,v):
    #print(g.vertices[v][1],g.vertices[u][1],g.matriz[u][v])
    if g.vertices[v][1] > (g.vertices[u][1] + g.matriz[u][v]):
        g.vertices[v][1] = (g.vertices[u][1] + g.matriz[u][v])
        g.vertices[v][0] = u

#------------------------------------------------------------------------------------------------------

def Bellman_Ford(g,s):
    Initialize_Single_Source(g,s)
    for i in range(len(g.vertices)-1):
        for aresta in g.arestas:
            Relax(g,aresta[0],aresta[1])
    for aresta in g.arestas:
        if g.vertices[aresta[0]][1] > g.vertices[aresta[1]][1] + g.matriz[aresta[0]][aresta[1]]:
            return False
    return True

#------------------------------------------------------------------------------------------------------

g = Grafo(5)
g.add_aresta(0,1,6)
g.add_aresta(0,3,7)
g.add_aresta(1,2,5)
g.add_aresta(1,3,8)
g.add_aresta(1,4,-4)
g.add_aresta(2,1,-2)
g.add_aresta(3,2,-3)
g.add_aresta(3,4,9)
g.add_aresta(4,1,2)
g.add_aresta(4,2,7)

Bellman_Ford(g,0)
print(g.vertices)