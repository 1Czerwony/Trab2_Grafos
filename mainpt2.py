import math
from collections import deque

#------------------------------------------------------------------------------------------------------

class Rede:
    def __init__(self, n):
        #self.adj = [[] for i in range(n)]
        self.vertices = [[[],None,None,math.inf] for i in range(n)]
        self.c = {}
    
    def add_aresta(self,i,j,x):
        if i in range(len(self.vertices)) and j in range(len(self.vertices)):
            self.vertices[i][0].append(j)
            self.c[(i,j)] = x

    def __str__(self):
        return "Vertices:"+str(self.vertices)+"\nArestas:"+str(self.c)
    
#------------------------------------------------------------------------------------------------------

def BFS(g, s): 
    for u in range(len(g.vertices)):
        g.vertices[u][1] = 'B'
        g.vertices[u][2] = None
        g.vertices[u][3] = math.inf
    g.vertices[s][1] = 'C'
    g.vertices[s][2] = None
    g.vertices[s][3] = 0                   
    q = deque()
    q.append(s)                                             # Fila 'q' onde o primeiro vértice será visitado e eliminado da fila e seus vértices filhos serão adicionados ao final da fila
    while q != deque([]):                             
        u = q.popleft()                            
        for v in g.vertices[u][0]:
            if g.vertices[v][1] == 'B':                                      
                g.vertices[v][1] = 'C'                  
                g.vertices[v][3] = g.vertices[u][3] + 1     # Vértices descobertos recebem a distância de seu pai + 1
                g.vertices[v][2] = u                    
                q.append(v)                     
        g.vertices[u][1] = 'P'                              # Define cor de u como PRETO

#------------------------------------------------------------------------------------------------------

def verifica_fluxo(rede,f):
    for aresta in f:
        if aresta not in rede.c or f[aresta] > rede.c[aresta]:
            return False
    return True

#------------------------------------------------------------------------------------------------------

s,v1,v2,v3,v4,t = 0,1,2,3,4,5
g = Rede(6)
g.add_aresta(s,v1,16)
g.add_aresta(s,v2,13)
g.add_aresta(v1,v3,12)
g.add_aresta(v2,v1,4)
g.add_aresta(v2,v4,14)
g.add_aresta(v3,v2,9)
g.add_aresta(v3,t,20)
g.add_aresta(v4,v3,7)
g.add_aresta(v4,t,4)

f = {}
f[(s,v1)] = 11
f[(s,v2)] = 8
f[(v1,v3)] = 12
f[(v2,v1)] = 1
f[(v2,v4)] = 11
f[(v3,v2)] = 4
f[(v3,t)] = 15
f[(v4,v3)] = 7
f[(v4,t)] = 4

f2 = {}
f[(s,v1)] = 17

assert verifica_fluxo(g,f) == True
assert verifica_fluxo(g,f2) == True

print(g)