import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap, BoundaryNorm
import matplotlib.patches as patches

def visualizar_grid(ambiente, robo=None, caminho=None, titulo=""):
    pass


# NO ARQUIVO robo_explorer/visualization.py
# Substitua a classe VisualizacaoDinamica por esta:

class VisualizacaoDinamica:
    """
    Classe para gerenciar a visualização passo a passo (animação) do robô.
    Agora com suporte a todas as etapas.
    """
    def __init__(self, ambiente):
        plt.ion()
        self.fig, self.ax = plt.subplots(figsize=(8, 8))
        self.ambiente = ambiente

        # Prepara o mapa de cores uma única vez
        self.colors = ['#00008B', '#2E8B57', '#FFD700', '#DC143C']
        self.cmap = ListedColormap(self.colors)
        self.bounds = [0, 1, 2, 3, 4]
        self.norm = BoundaryNorm(self.bounds, self.cmap.N)

    # --- DEFINIÇÃO DA FUNÇÃO CORRIGIDA ---
    # Adicionado o argumento 'caminho_planejado=None'
    def atualizar(self, robo, caminho=None, mapa_visitados=None, titulo="", caminho_planejado=None):
        self.ax.clear()

        # Desenha o grid (terrenos e obstáculos)
        grid_visual = np.ones((self.ambiente.n, self.ambiente.n), dtype=int)
        for (x, y), custo in self.ambiente.terrenos.items():
            grid_visual[y, x] = custo
        for (x, y) in self.ambiente.obstaculos:
            grid_visual[y, x] = 0
        self.ax.imshow(grid_visual, cmap=self.cmap, norm=self.norm, interpolation='nearest', origin='upper')

        # Desenha o mapa de células visitadas (para a Etapa 2)
        if mapa_visitados:
            for (x, y) in mapa_visitados:
                rect = patches.Rectangle((x - 0.5, y - 0.5), 1, 1, linewidth=1, edgecolor='none', facecolor='cyan', alpha=0.2)
                self.ax.add_patch(rect)

        # Desenha o caminho percorrido pelo robô
        if caminho:
            caminho_y = [p[1] for p in caminho]
            caminho_x = [p[0] for p in caminho]
            self.ax.plot(caminho_x, caminho_y, color='cyan', linewidth=3, marker='o', markersize=6, label="Caminho Percorrido")

        # --- LÓGICA NOVA ---
        # Desenha o caminho que o robô está planejando fazer (com estilo diferente)
        if caminho_planejado:
            caminho_y = [p[1] for p in caminho_planejado]
            caminho_x = [p[0] for p in caminho_planejado]
            self.ax.plot(caminho_x, caminho_y, color='white', linestyle='--', linewidth=2, label="Caminho Planejado")

        # Desenha a posição atual do robô
        pos_atual = robo.get_posicao()
        self.ax.plot(pos_atual[0], pos_atual[1], 'o', color='magenta', markersize=12, label="Robô")

        # Desenha Fim (para Etapas 3 e 4)
        if hasattr(robo, 'fim'):
             self.ax.plot(robo.fim[0], robo.fim[1], 'rX', markersize=15, label='Fim')

        # Configurações do gráfico
        self.ax.set_title(titulo)
        self.ax.grid(which="minor", color="w", linestyle='-', linewidth=1)
        self.ax.tick_params(which="minor", size=0)
        self.ax.set_xticks(np.arange(0, self.ambiente.n, 1))
        self.ax.set_yticks(np.arange(0, self.ambiente.n, 1))
        self.ax.legend()
        
        plt.pause(0.05)

    def fechar(self, titulo=""):
        """Atualiza o título final e mantém a janela aberta."""
        self.ax.set_title(titulo)
        plt.ioff()
        plt.show()