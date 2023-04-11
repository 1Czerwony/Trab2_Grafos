# Algoritmos em Grafos | Trabalho 2 Parte III
# João Augusto da Silva Gomes | RA:120114
# Vitor Felipe de Souza Siqueira | RA:122907
# Professor: Marco Aurélio Lopes Barbosa
#------------------------------------------------------------------------------------------------------
import math
from collections import deque
#------------------------------------------------------------------------------------------------------

class Grafo:     # Classe que representa um Grafo
    def __init__(self, n):                                                      # Para cada vértice i, guarda uma lista com 4 informações:
        self.vertices = [[[],None,None,math.inf] for i in range(n)]             # [lista de adjacências, cor, pai, distancia] 
        self.c = {}                                                             # Alfabeto com os pesos/capacidades de cada aresta
        self.f = {}                                                             # Alfabeto com as fontes de cada aresta

    def add_aresta(self, u, v, c):     # Adiciona uma aresta (u,v) de peso/capacidade 'c' no grafo
        if u in range(len(self.vertices)) and v in range(len(self.vertices)) and (u,v) not in self.c :
            self.vertices[u][0].append(v)
            self.c[(u,v)] = c
        else:
            print(f'A aresta ({u},{v}) é inválida')
    
#------------------------------------------------------------------------------------------------------

# Retorna True se um grafo é uma rede (não possui arestas antiparalelas) e False, caso contrário
def verifica_rede(r):
    for aresta in r.c:
        if (aresta[1], aresta[0]) in r.c:
            return False
    return True

#------------------------------------------------------------------------------------------------------

# Busca em largura em um grafo
def BFS(g, s): 
    for u in range(len(g.vertices)):
        g.vertices[u][1] = 'B'
        g.vertices[u][2] = None
        g.vertices[u][3] = math.inf
    g.vertices[s][1] = 'C'
    g.vertices[s][2] = None
    g.vertices[s][3] = 0                   
    q = deque()
    q.append(s)                                                 # Fila 'q' onde o primeiro vértice será visitado e eliminado da fila e seus vértices filhos serão adicionados ao final da fila
    while q != deque([]):                             
        u = q.popleft()                            
        for v in g.vertices[u][0]:
            if g.vertices[v][1] == 'B':                                      
                g.vertices[v][1] = 'C'                  
                g.vertices[v][3] = g.vertices[u][3] + 1         # Vértices descobertos recebem a distância de seu pai + 1
                g.vertices[v][2] = u                    
                q.append(v)                     
        g.vertices[u][1] = 'P'                                  # Define cor de u como PRETO
        
#------------------------------------------------------------------------------------------------------

# Retorna True se um fluxo f é válido na rede r ou False, caso contrário
def verifica_fluxo(r, f):
    if verifica_rede(r) == False:
        return False
    for aresta in f:
        if aresta not in r.c or f[aresta] > r.c[aresta]:        # O fluxo é INVÁLIDO se existir alguma aresta (u,v) do fluxo que não existe na rede
            return False                                        # ou se para alguma aresta (u,v) da rede: f(u,v) > c(u,v)
    return True

#------------------------------------------------------------------------------------------------------

# Gera uma rede residual a partir de uma rede original r e um fluxo f
def gera_rede_residual(r, f):
    if verifica_fluxo(r,f) == False or f == {}:                             # Se o fluxo for inválido, retorna None
        return None
    Gf = Grafo(len(r.vertices))                                              
    for aresta in r.c:
            if r.c[aresta] - f[aresta] > 0:                                     # Se f(u,v) < c(u,v), adiciona a aresta (u,v) na rede residual com valor c(u,v) - f(u,v).
                Gf.add_aresta(aresta[0],aresta[1],r.c[aresta] - f[aresta])
            Gf.add_aresta(aresta[1],aresta[0],f[aresta])                        # Para cada aresta (u,v), adiciona aresta a aresta (v,u) com valor de f(u,v)
    return Gf

#------------------------------------------------------------------------------------------------------

# Encontra e retorna as arestas de um caminho entre s e t em uma rede r
def encontra_caminho(r, s, t):
    if r.c == {} or r.vertices == []:       # Retorna None se a rede for vazia
        return None
    BFS(r, s)
    if r.vertices[t][3] == math.inf:        # Retorna None se não existir caminho entre s e t
        return None
    else:
        v = t
        u = r.vertices[t][2]                
        path = {}
        while u != None:                    # Cria um dicionário com as arestas presentes num caminho entre s e t
            path[(u,v)] = r.c[(u,v)]        # Para cada aresta do caminho, guarda o fluxo da aresta
            u = r.vertices[u][2]
            v = r.vertices[v][2]
    return path

#------------------------------------------------------------------------------------------------------

def Edmonds_Karp(g,s,t):
    if verifica_rede(g) == False:
        return None
    f = {}                                  # Dicionário que armazena o fluxo f(u,v) de cada aresta (u,v)
    for aresta in g.c:
        f[aresta] = 0
    Gf = gera_rede_residual(g,f)            # Gera a rede residual a partir da rede original e do fluxo f
    while True:
        p = encontra_caminho(Gf,s,t)        # Encontra um caminho entre s e t
        if p == None:                       # Se não existir caminho entre s e t, retorna o fluxo f
            return f
        cf = min(p.values())                # cf é o valor do fluxo máximo que pode ser adicionado ao fluxo f
        for aresta in p:
            if aresta in g.c:               # Se a aresta (u,v) está na rede original, adiciona cf ao fluxo f(u,v)
                f[aresta] += cf
            else:                           # Se a aresta (u,v) não está na rede original, subtrai cf do fluxo f(v,u)
                f[(aresta[1],aresta[0])] -= cf
        Gf = gera_rede_residual(Gf,f)        # Gera a rede residual a partir da rede original e do fluxo f
        if Gf == None:                      # Se a rede residual for inválida, retorna None
            return None
        


#TESTES------------------------------------------------------------------------------------------------------

# Rede inválida (arestas antiparalelas)
g = Grafo(2)
g.add_aresta(0,1,1)
g.add_aresta(1,0,2)

assert verifica_rede(g) == False

# Rede da figura 26.1 do livro
s,v1,v2,v3,v4,t = 0,1,2,3,4,5
r = Grafo(6)
r.add_aresta(s,v1,16)
r.add_aresta(s,v2,13)
r.add_aresta(v1,v3,12)
r.add_aresta(v2,v1,4)
r.add_aresta(v2,v4,14)
r.add_aresta(v3,v2,9)
r.add_aresta(v3,t,20)
r.add_aresta(v4,v3,7)
r.add_aresta(v4,t,4)

assert verifica_rede(r) == True

# Fluxo da figura 26.1 do livro (válido na rede r)
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

# Fluxo inválido na rede r
f2 = {}
f2[(s,v1)] = 17

assert verifica_fluxo(r,f) == True
assert verifica_fluxo(r,f2) == False

# Rede residual inválida
assert gera_rede_residual(r, f2) == None

# Rede residual da figura 26.4(b) do livro
rf = gera_rede_residual(r, f)
assert rf != None
assert rf.c[(s,v1)] == 5
assert rf.c[(v1,s)] == 11
assert rf.c[(s,v2)] == 5
assert rf.c[(v2,s)] == 8
assert rf.c[(v3,v1)] == 12
assert rf.c[(s,v2)] == 5
assert rf.c[(v2,v3)] == 4
assert rf.c[(v3,v2)] == 5
assert rf.c[(v3,v4)] == 7
assert rf.c[(v2,v4)] == 3
assert rf.c[(v4,v2)] == 11
assert rf.c[(v3,t)] == 5
assert rf.c[(t,v3)] == 15
assert rf.c[(t,v4)] == 4

# Caminho entre s e t da figura 26.4(b) do livro
path = encontra_caminho(rf, s, t)
assert (s,v2) in path
assert (v2,v3) in path
assert (v3,t) in path
#print(Edmonds_Karp(r,s,t))