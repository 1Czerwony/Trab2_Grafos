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

    def add_aresta(self, u, v, c):     # Adiciona uma aresta (u,v) de peso/capacidade 'c' no grafo
        if u in range(len(self.vertices)) and v in range(len(self.vertices)) and (u,v) not in self.c :
            self.vertices[u][0].append(v)
            self.c[(u,v)] = c
        else:
            print(f'A aresta ({u},{v}) é inválida')
            
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

# Retorna True se um grafo é uma rede (não possui arestas antiparalelas) e False, caso contrário
def verifica_rede(r):
    for aresta in r.c:
        if (aresta[1], aresta[0]) in r.c:
            return False
    return True
        
#------------------------------------------------------------------------------------------------------

# Retorna True se um fluxo f é válido na rede r ou False, caso contrário
def verifica_fluxo(r, f):
    if verifica_rede(r) == False:
        return False
    for aresta in r.c:
        if f[aresta] > r.c[aresta] or f[aresta] < 0:            # Se o fluxo de uma aresta for maior que sua capacidade ou menor que 0, retorna False
            return False
    return True

#------------------------------------------------------------------------------------------------------

# Gera uma rede residual a partir de uma rede original r e um fluxo f
def gera_rede_residual(r, f):
    if verifica_fluxo(r,f) == False:                             # Se o fluxo for inválido, retorna None
        return None
    Gf = Grafo(len(r.vertices))                                              
    for aresta in r.c:
        if f[aresta] == 0:                                                      # Se f(u,v) = 0, adiciona a aresta (u,v) na rede residual com valor c(u,v).
            Gf.add_aresta(aresta[0],aresta[1],r.c[aresta])
        elif r.c[aresta] - f[aresta] > 0:                                       # Se f(u,v) < c(u,v), adiciona a aresta (u,v) na rede residual com valor c(u,v) - f(u,v).
            Gf.add_aresta(aresta[0],aresta[1],r.c[aresta] - f[aresta])
            Gf.add_aresta(aresta[1],aresta[0],f[aresta])                        # Para cada aresta (u,v), adiciona a aresta (v,u) com valor de f(u,v)
        else:
            Gf.add_aresta(aresta[1],aresta[0],r.c[aresta])                        
    return Gf

#------------------------------------------------------------------------------------------------------

# Encontra e retorna as arestas de um caminho entre s e t em uma rede r
# s e t devem ser os vértices de origem e destino, respectivamente, caso contrário, o algoritmo não funcionará corretamente
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

# Algoritmo de Edmonds-Karp para encontrar o fluxo máximo em uma rede
# s e t devem ser os vértices de origem e destino, respectivamente, caso contrário, o algoritmo não funcionará corretamente
def Edmonds_Karp(g,s,t):
    if verifica_rede(g) == False:                       # Se a rede não for válida, retorna None
        return None
    f={}
    for aresta in g.c:
        f[aresta] = 0
    while True:
        Gf = gera_rede_residual(g,f)    
        p = encontra_caminho(Gf,s,t)                    # p é um caminho encontrado entre s e t na rede residual
        if p == None:                                   # Se não existir caminho entre s e t, retorna o fluxo f
            return f
        cf = min(p.values())                            # cf é o valor de fluxo máximo que pode ser adicionado ao fluxo f
        for aresta in p:
            if aresta in g.c:                           # Se uma aresta (u,v) de p pertence à rede original, incrementa o fluxo f(u,v) em cf
                f[aresta] += cf
            else:                                       # Se a aresta (u,v) de p não pertence à rede original, decrementa o fluxo f(v,u) em cf
                f[(aresta[1],aresta[0])] -= cf
            
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

# Teestes de fluxo na rede r
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

# Fluxo máximo da figura 26.6(e) do livro 
f3 = Edmonds_Karp(r,s,t)
assert f3[(s,v1)] == 12
assert f3[(s,v2)] == 11
assert f3[(v1,v3)] == 12
assert f3[(v2,v1)] == 0
assert f3[(v2,v4)] == 11
assert f3[(v3,v2)] == 0
assert f3[(v3,t)] == 19
assert f3[(v4,v3)] == 7
assert f3[(v4,t)] == 4
assert verifica_fluxo(r,f3) == True

# -----------------------------------------------------------------------------------------------

# Exemplo de rede com 7 vértices e 12 arestas
s1,a,b,c,d,e,t1 = 0,1,2,3,4,5,6
h = Grafo(7)
h.add_aresta(s1,a,5)
h.add_aresta(s1,b,7)
h.add_aresta(s1,c,4)
h.add_aresta(a,b,1)
h.add_aresta(a,d,3)
h.add_aresta(b,c,2)
h.add_aresta(b,e,5)
h.add_aresta(b,d,4)
h.add_aresta(c,e,4)
h.add_aresta(d,t1,9)
h.add_aresta(e,d,1)
h.add_aresta(e,t1,6)
assert verifica_rede(h) == True

# Verifica fluxo máximo da rede h gerado pelo algoritmo Edmonds_Karp
f4 = Edmonds_Karp(h,s1,t1)
assert verifica_fluxo(h,f4) == True
assert f4[(s1,a)] == 4
assert f4[(s1,b)] == 7
assert f4[(s1,c)] == 3
assert f4[(a,b)] == 1
assert f4[(a,d)] == 3
assert f4[(b,d)] == 4
assert f4[(b,e)] == 4
assert f4[(b,c)] == 0
assert f4[(c,e)] == 3
assert f4[(d,t1)] == 8
assert f4[(e,d)] == 1
assert f4[(e,t1)] == 6