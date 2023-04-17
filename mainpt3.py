# Algoritmos em Grafos | Trabalho 2 Parte III
# João Augusto da Silva Gomes | RA:120114
# Vitor Felipe de Souza Siqueira | RA:122907
# Professor: Marco Aurélio Lopes Barbosa
#------------------------------------------------------------------------------------------------------
import math, random, time
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
            
#------------------------------------------------------------------------------------------------------

# Busca em largura em um grafo
def BFS(g, s): # Argumentos: g é um grafo, s é o vértice de origem da busca
    for u in range(len(g.vertices)):                            # Para cada vértice u do grafo, define cor como BRANCO, pai como None e distância como infinito
        g.vertices[u][1] = 'B'
        g.vertices[u][2] = None
        g.vertices[u][3] = math.inf
    g.vertices[s][1] = 'C'                                      # Define cor de s como CINZA, pai como None e distância como 0
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

# Retorna True se um grafo é uma rede e False, caso contrário
def verifica_rede(r,s,t): # Argumentos: r é uma rede, s é o vértice de origem e t é o vértice de destino
    if s not in range(len(r.vertices)) or t not in range(len(r.vertices)):      # Se s ou t não forem vértices do grafo, retorna False
        return False
    for aresta in r.c:                       
        if aresta[1] == s or aresta[0] == t:                                    # Se existir aresta (v,s) ou (t,u), retorna False                                          
            return False                                                        
        if (aresta[1], aresta[0]) in r.c:                                       # Se existir arestas antiparalelas, retorna False
            return False
    for v in range(len(r.vertices)):                                            # Para todo vértice v deve existir um caminho de s para t que passe por v.
        if encontra_caminho(r,s,v) == None or encontra_caminho(r,v,t) == None:
            return False
    return True
        
#------------------------------------------------------------------------------------------------------

# Retorna True se um fluxo f é válido na rede r ou False, caso contrário
# Este algoritmo assume que a rede r é válida
def verifica_fluxo(r,f): # Argumentos: r é uma rede, f é um fluxo
    for aresta in r.c:
        if f[aresta] > r.c[aresta] or f[aresta] < 0:            # Se o fluxo de uma aresta for maior que sua capacidade ou menor que 0, retorna False
            return False
    return True

#------------------------------------------------------------------------------------------------------

# Gera uma rede residual a partir de uma rede original r e um fluxo 
# Este algoritmo assume que a rede r é válida
def gera_rede_residual(r,f): # Argumentos: r é uma rede, f é um fluxo
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
def encontra_caminho(r, s, t): # Argumentos: r é uma rede, s e t são vértices da rede r
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
# Este algoritmo assume que a rede g é válida
def Edmonds_Karp(g,s,t): # Argumentos: g é uma rede, s é o vértice de origem e t é o vértice de destino
    f={}
    for aresta in g.c:
        f[aresta] = 0
    while True:
        Gf = gera_rede_residual(g,f)    
        p = encontra_caminho(Gf,s,t)                    # p é um caminho encontrado usando BFS entre s e t na rede residual
        if p == None:                                   # Se não existir caminho entre s e t, retorna o fluxo f
            return f
        cf = min(p.values())                            # cf é o valor de fluxo máximo que pode ser adicionado ao fluxo f
        for aresta in p:
            if aresta in g.c:                           # Se uma aresta (u,v) de p pertence à rede original, incrementa o fluxo f(u,v) em cf
                f[aresta] += cf
            else:                                       # Se a aresta (u,v) de p não pertence à rede original, decrementa o fluxo f(v,u) em cf
                f[(aresta[1],aresta[0])] -= cf
            
#------------------------------------------------------------------------------------------------------
            
# Gera uma rede aleatória válida com n vértices
# A rede gerada possui s = 0 e t = n-1
# A probabilidade de uma aresta ser adicionada é 0.5
# O valor de cada aresta é um inteiro aleatório entre 1 e 50
def gera_rede_aleatória(n): # Argumentos: n é o número de vértices da rede
    if n < 2:                                               # Se n < 2, não é possível gerar uma rede válida
        return None
    p = 0.5
    g = Grafo(n)
    while verifica_rede(g,0,n-1) == False:                  # Sorteia novas arestas até que a rede seja válida
        for i in range(n):
            for j in range(i+1,n):                          
                if random.random() <= p:                    # Para cada par de vértices, sorteia uma aresta com probabilidade p
                    g.add_aresta(i,j,random.randint(1,50))
    return g,0,n-1

#TESTES BFS------------------------------------------------------------------------------------------------------

grafo = Grafo(6)
grafo.add_aresta(0,1,4)
grafo.add_aresta(0,2,2)
grafo.add_aresta(1,3,5)
grafo.add_aresta(2,3,1)
grafo.add_aresta(2,4,6)
grafo.add_aresta(3,5,3)
grafo.add_aresta(4,5,1)
BFS(grafo,0)

# Testa se os vértices estão sendo visitados na ordem correta
                           #[vizinhos, cor, pai, distancia]
assert grafo.vertices[0] == [[1,2], 'P', None, 0]
assert grafo.vertices[1] == [[3], 'P', 0, 1]
assert grafo.vertices[2] == [[3,4], 'P', 0, 1]
assert grafo.vertices[3] == [[5], 'P', 1, 2]
assert grafo.vertices[4] == [[5], 'P', 2, 2]
assert grafo.vertices[5] == [[], 'P', 3, 3]

#TESTES REDES------------------------------------------------------------------------------------------------------

# Rede inválida (arestas antiparalelas)
g = Grafo(2)
g.add_aresta(0,1,1)
g.add_aresta(1,0,2)
assert verifica_rede(g,0,1) == False

# Rede inválida (não existe caminho entre 0 e 3 que passe pelo vértice 2)
k = Grafo(4)
k.add_aresta(0,1,1)
k.add_aresta(1,3,1)
k.add_aresta(2,3,1)
assert verifica_rede(k,0,3) == False

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
assert verifica_rede(r,s,t) == True

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
assert verifica_rede(h,s1,t1) == True

#TESTES FLUXO------------------------------------------------------------------------------------------------------

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
assert verifica_fluxo(r,f) == True

# Fluxo inválido na rede r
f2 = {}
f2[(s,v1)] = 17
assert verifica_fluxo(r,f2) == False

#TESTES REDES RESIDUAIS------------------------------------------------------------------------------------------

# Rede residual inválida
assert gera_rede_residual(r,f2) == None

# Rede residual da figura 26.4(b) do livro
rf = gera_rede_residual(r,f)
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

#TESTES CAMINHOS---------------------------------------------------------------------------------------------------

# Caminho entre s e t da figura 26.4(b) do livro
path = encontra_caminho(rf, s, t)
assert (s, v2) in path
assert (v2, v3) in path
assert (v3, t) in path
for aresta in rf.c:
    if aresta != (v3, t) and aresta != (s, v2) and aresta != (v2, v3):
        assert aresta not in path

# Caminho entre s1 e t1 da rede h
path2 = encontra_caminho(h, s1, t1)
assert (s1, a) in path2
assert (a, d) in path2
assert (d, t1) in path2
for aresta in h.c:
    if aresta != (s1, a) and aresta != (a, d) and aresta != (d, t1):
        assert aresta not in path2

#TESTES ALGORITMO EDMONDS-KARP------------------------------------------------------------------------------------

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

#TESTES REDES ALEATÓRIAS-----------------------------------------------------------------------------------------------

# Redes aleatórias inválidas (menos de 2 vértices)
assert gera_rede_aleatória(1) == None
assert gera_rede_aleatória(0) == None
assert gera_rede_aleatória(-1) == None
 
print('Testando Redes Aleatórias...')

# Gera 100 redes aleatórias com 100 vértices e verifica se são válidas
for i in range(100):
    #n = random.randint(2,200)
    rede,s2,t2 = gera_rede_aleatória(100)
    assert verifica_rede(rede,0,99) == True

# Gera 100 redes aleatórias com 100 vértices e verifica se o fluxo máximo é válido
for i in range(100):
    #n = random.randint(2,200)
    rede,s2,t2 = gera_rede_aleatória(100)
    fluxo = Edmonds_Karp(rede,s2,t2)
    assert verifica_fluxo(rede,fluxo) == True
    
print('Testes concluídos com sucesso!')