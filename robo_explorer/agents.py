import random
import heapq
import time

class Robo:
    def __init__(self, ambiente):
        self.ambiente = ambiente
        self.x = random.randint(0, self.ambiente.n - 1)
        self.y = random.randint(0, self.ambiente.n - 1)
        while (self.x, self.y) in self.ambiente.obstaculos:
            self.x = random.randint(0, self.ambiente.n - 1)
            self.y = random.randint(0, self.ambiente.n - 1)

    def get_posicao(self): return (self.x, self.y)

    def mover(self, dx, dy):
        novo_x, novo_y = self.x + dx, self.y + dy
        if self.ambiente.is_valido(novo_x, novo_y):
            self.x = novo_x; self.y = novo_y
            return True
        return False


class RoboReativoSimples(Robo):
    def __init__(self, ambiente, visualizador=None):
        super().__init__(ambiente)
        self.paredes_colididas = set()
        self.direcoes_map = {'Norte':(0,1),'Sul':(0,-1),'Leste':(1,0),'Oeste':(-1,0)}
        self.direcao_atual = random.choice(list(self.direcoes_map.keys()))
        self.caminho_percorrido = [self.get_posicao()]
        self.visualizador = visualizador

    def explorar(self):
        passos = 0
        while len(self.paredes_colididas) < 4 and passos < 500:
            if self.visualizador:
                self.visualizador.atualizar(robo=self, caminho=self.caminho_percorrido, titulo="Etapa 1: Explorando...")
            
            dx, dy = self.direcoes_map[self.direcao_atual]
            pos_antes = self.get_posicao(); self.mover(dx, dy); pos_depois = self.get_posicao()
            self.caminho_percorrido.append(pos_depois)
            if pos_antes == pos_depois:
                parede_atingida = None
                if dx == -1 and self.x == 0: parede_atingida = 'Oeste'
                elif dx == 1 and self.x == self.ambiente.n - 1: parede_atingida = 'Leste'
                elif dy == -1 and self.y == 0: parede_atingida = 'Sul'
                elif dy == 1 and self.y == self.ambiente.n - 1: parede_atingida = 'Norte'
                if parede_atingida and parede_atingida not in self.paredes_colididas:
                    self.paredes_colididas.add(parede_atingida)
                direcoes_disponiveis = list(self.direcoes_map.keys())
                if len(direcoes_disponiveis) > 1: direcoes_disponiveis.remove(self.direcao_atual)
                self.direcao_atual = random.choice(direcoes_disponiveis)
            passos += 1

class RoboBaseadoModelo(Robo):
    """
    Agente que usa um algoritmo de Busca em Profundidade (DFS) com uma pilha
    para explorar o mapa de forma completa e eficiente.
    """
    def __init__(self, ambiente, visualizador=None):
        super().__init__(ambiente)
        print(f"Robô Baseado em Modelo (Inteligente) iniciado em: {self.get_posicao()}")
        
        # O mapa de visitados garante que cada célula seja processada uma vez.
        self.mapa_visitados = {self.get_posicao()}
        
        # A pilha armazena o caminho atual para permitir o backtracking inteligente.
        self.caminho_pilha = [self.get_posicao()]
        
        self.passos_redundantes = 0
        self.caminho_percorrido_completo = [self.get_posicao()] # Para visualização
        self.visualizador = visualizador

    def explorar(self):
        """Executa o ciclo de exploração usando a lógica DFS."""
        
        # O loop continua enquanto a pilha não estiver vazia.
        while self.caminho_pilha:
            posicao_atual = self.caminho_pilha[-1] # Olha o topo da pilha
            self.x, self.y = posicao_atual
            
            # Atualiza a visualização a cada passo
            if self.visualizador:
                self.visualizador.atualizar(
                    robo=self,
                    caminho=self.caminho_percorrido_completo,
                    mapa_visitados=self.mapa_visitados,
                    titulo="Etapa 2: Mapeando com DFS..."
                )

            # Encontra vizinhos que ainda não foram visitados
            vizinhos_nao_visitados = [
                v for v in self._get_vizinhos_de_posicao(posicao_atual)
                if v not in self.mapa_visitados
            ]

            if vizinhos_nao_visitados:
                # Se encontrou um novo lugar para ir, avança
                proximo_passo = random.choice(vizinhos_nao_visitados)
                self.mapa_visitados.add(proximo_passo)
                self.caminho_pilha.append(proximo_passo)
                self.caminho_percorrido_completo.append(proximo_passo)
            else:
                # Se é um beco sem saída, faz o backtracking
                self.caminho_pilha.pop()
                if self.caminho_pilha: # Evita contar o último passo como redundante
                    self.caminho_percorrido_completo.append(self.caminho_pilha[-1])
                    self.passos_redundantes += 1
        
        self.avaliar_desempenho()

    def avaliar_desempenho(self):
        total_acessiveis = (self.ambiente.n * self.ambiente.n) - len(self.ambiente.obstaculos)
        percentual_visitado = (len(self.mapa_visitados) / total_acessiveis) * 100 if total_acessiveis > 0 else 0
        print("\n--- Resultado Etapa 2 (Inteligente) ---")
        print(f"Completude da Exploração: {percentual_visitado:.2f}%")
        print(f"Eficiência (passos de backtracking): {self.passos_redundantes}")

    def _get_vizinhos_de_posicao(self, pos):
        x, y = pos
        vizinhos = []
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            novo_x, novo_y = x + dx, y + dy
            if self.ambiente.is_valido(novo_x, novo_y):
                vizinhos.append((novo_x, novo_y))
        return vizinhos
    
class RoboBaseadoObjetivos(Robo):
    def __init__(self, ambiente, inicio, fim, visualizador=None):
        super().__init__(ambiente)
        self.x, self.y = inicio; self.inicio = inicio; self.fim = fim
        self.visualizador = visualizador

    def executar(self):
        caminho = self.encontrar_caminho()
        if caminho: self.executar_caminho_animado(caminho)
        print(f"Sucesso: {'Sim' if caminho else 'Não'}")
        if caminho: print(f"Comprimento: {len(caminho) - 1}")
        return caminho
    
    def executar_caminho_animado(self, caminho):
        caminho_parcial = []
        for passo in caminho:
            caminho_parcial.append(passo)
            self.x, self.y = passo
            if self.visualizador:
                self.visualizador.atualizar(robo=self, caminho=caminho_parcial, titulo=f"Etapa 3/4: Executando Caminho...")
            time.sleep(0.1)

    def encontrar_caminho(self):
        lista_aberta = [(0, self.inicio)]; veio_de = {}; g_score = {(x, y): float('inf') for x in range(self.ambiente.n) for y in range(self.ambiente.n)}; g_score[self.inicio] = 0; f_score = {(x, y): float('inf') for x in range(self.ambiente.n) for y in range(self.ambiente.n)}; f_score[self.inicio] = self._h_heuristica(self.inicio, self.fim); lista_aberta_set = {self.inicio}
        while lista_aberta:
            _, atual = heapq.heappop(lista_aberta); lista_aberta_set.remove(atual)
            if atual == self.fim: return self._reconstruir_caminho(veio_de, atual)
            x, y = atual
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                vizinho = (x + dx, y + dy)
                if self.ambiente.is_valido(vizinho[0], vizinho[1]):
                    tentativa_g_score = g_score[atual] + 1
                    if tentativa_g_score < g_score[vizinho]:
                        veio_de[vizinho] = atual; g_score[vizinho] = tentativa_g_score; f_score[vizinho] = g_score[vizinho] + self._h_heuristica(vizinho, self.fim)
                        if vizinho not in lista_aberta_set: heapq.heappush(lista_aberta, (f_score[vizinho], vizinho)); lista_aberta_set.add(vizinho)
        return None
    def _h_heuristica(self, a, b): return abs(a[0] - b[0]) + abs(a[1] - b[1])
    def _reconstruir_caminho(self, veio_de, atual):
        caminho_total = [atual]
        while atual in veio_de: atual = veio_de[atual]; caminho_total.insert(0, atual)
        return caminho_total



class RoboBaseadoUtilidade(RoboBaseadoObjetivos):
    def encontrar_caminho(self):
        # --- LÓGICA CORRIGIDA (DIJKSTRA) ---
        # A fila de prioridade agora usa apenas o g_score (custo real)
        lista_aberta = [(0, self.inicio)] 
        veio_de = {}
        g_score = {(x, y): float('inf') for x in range(self.ambiente.n) for y in range(self.ambiente.n)}
        g_score[self.inicio] = 0
        lista_aberta_set = {self.inicio}

        while lista_aberta:
            custo_atual, atual = heapq.heappop(lista_aberta)
            lista_aberta_set.remove(atual)

            if custo_atual > g_score[atual]:
                continue
            if atual == self.fim:
                return self._reconstruir_caminho(veio_de, atual)
            
            x, y = atual
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                vizinho = (x + dx, y + dy)
                if self.ambiente.is_valido(vizinho[0], vizinho[1]):
                    custo_movimento = self.ambiente.get_custo(vizinho[0], vizinho[1])
                    tentativa_g_score = g_score[atual] + custo_movimento
                    if tentativa_g_score < g_score[vizinho]:
                        veio_de[vizinho] = atual
                        g_score[vizinho] = tentativa_g_score
                        # A prioridade na fila é o custo real (g_score), não o f_score
                        if vizinho not in lista_aberta_set:
                            heapq.heappush(lista_aberta, (g_score[vizinho], vizinho))
                            lista_aberta_set.add(vizinho)
        return None

    def executar_e_avaliar(self):
        caminho = self.encontrar_caminho()
        if caminho: self.executar_caminho_animado(caminho)
        print(f"Sucesso: {'Sim' if caminho else 'Não'}")
        if caminho:
            custo_total = sum(self.ambiente.get_custo(x, y) for x, y in caminho[1:])
            print(f"Custo Total: {custo_total}")
        return caminho

class RoboUtilidadeParcial(RoboBaseadoUtilidade):
    def __init__(self, ambiente, inicio, fim, visualizador=None):
        super().__init__(ambiente, inicio, fim, visualizador)
        self.mapa_conhecido = {}
        self.caminho_percorrido = [inicio]

    def executar_ciclo_planejamento(self):
        passos = 0; limite_passos = (self.ambiente.n ** 2) * 2
        while self.get_posicao() != self.fim and passos < limite_passos:
            terrenos_visiveis = self.ambiente.observar_arredores(self.get_posicao(), raio=2)
            self.mapa_conhecido.update(terrenos_visiveis)
            caminho_planejado = self.encontrar_caminho_parcial()
            if not caminho_planejado or len(caminho_planejado) < 2:
                print("Não foi possível encontrar um caminho com o conhecimento atual. Falha."); break
            
            proximo_passo = caminho_planejado[1]
            self.x, self.y = proximo_passo
            self.caminho_percorrido.append(self.get_posicao())
            
            if self.visualizador:
                self.visualizador.atualizar(self, self.caminho_percorrido, titulo="Etapa 4: Parcialmente Observável", caminho_planejado=caminho_planejado)
            passos += 1
        
        if self.get_posicao() == self.fim:
            custo_total = sum(self.ambiente.get_custo(x, y) for x, y in self.caminho_percorrido[1:])
            print(f"\nSucesso: Sim! Custo Total: {custo_total}")
        else:
            print("\nSucesso: Não, não alcançou o destino no limite de passos.")

    def encontrar_caminho_parcial(self):
        # --- LÓGICA CORRIGIDA (DIJKSTRA) ---
        lista_aberta = [(0, self.get_posicao())]; veio_de = {}; g_score = {(x, y): float('inf') for x in range(self.ambiente.n) for y in range(self.ambiente.n)}; g_score[self.get_posicao()] = 0; lista_aberta_set = {self.get_posicao()}
        while lista_aberta:
            custo_atual, atual = heapq.heappop(lista_aberta); lista_aberta_set.remove(atual)
            if custo_atual > g_score[atual]: continue
            if atual == self.fim: return self._reconstruir_caminho(veio_de, atual)
            x, y = atual
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                vizinho = (x + dx, y + dy)
                if self.ambiente.is_valido(vizinho[0], vizinho[1]):
                    custo_movimento = self.mapa_conhecido.get(vizinho, 1)
                    tentativa_g_score = g_score[atual] + custo_movimento
                    if tentativa_g_score < g_score[vizinho]:
                        veio_de[vizinho] = atual; g_score[vizinho] = tentativa_g_score
                        if vizinho not in lista_aberta_set:
                            heapq.heappush(lista_aberta, (g_score[vizinho], vizinho)); lista_aberta_set.add(vizinho)
        return None