# Algoritmos em Grafos | Trabalho 2 Parte I
# João Augusto da Silva Gomes | RA:120114
# Vitor Felipe de Souza Siqueira | RA:122907
# Professor: Marco Aurélio Lopes Barbosa
#------------------------------------------------------------------------------------------------------
import math
#------------------------------------------------------------------------------------------------------

class Rede:     # Classe que representa uma Rede
    def __init__(self, n):                                                      # Para cada vértice i, guarda uma lista com 4 informações:
        self.vertices = [[[],None,None,math.inf] for i in range(n)]             # [lista de adjacências, cor, pai, distancia] 
        self.c = {}                                                             # Alfabeto com as capacidades de cada aresta
    
    def add_aresta(self, u, v, c):     # Adiciona uma aresta (u,v) de capacidade 'c' na rede
        if u in range(len(self.vertices)) and v in range(len(self.vertices)) and v not in self.vertices[u][0]:
            self.vertices[u][0].append(v)
            self.c[(u,v)] = c
        else:
            print(f'A aresta ({u},{v}) é inválida')
    
#------------------------------------------------------------------------------------------------------

# Verifica se um fluxo f é válido na rede r
def verifica_fluxo(r, f):
    for aresta in f:
        if aresta not in r.c or f[aresta] > r.c[aresta]:        # O fluxo é INVÁLIDO se existir alguma aresta (u,v) do fluxo que não existe na rede
            return False                                        # ou se para alguma aresta (u,v) da rede: f(u,v) > c(u,v)
    return True

#------------------------------------------------------------------------------------------------------

# Rede da figura 26.1 do livro
s,v1,v2,v3,v4,t = 0,1,2,3,4,5
r = Rede(6)
r.add_aresta(s,v1,16)
r.add_aresta(s,v2,13)
r.add_aresta(v1,v3,12)
r.add_aresta(v2,v1,4)
r.add_aresta(v2,v4,14)
r.add_aresta(v3,v2,9)
r.add_aresta(v3,t,20)
r.add_aresta(v4,v3,7)
r.add_aresta(v4,t,4)

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