import random
from robo_explorer.visualization import VisualizacaoDinamica
from robo_explorer.environment import Ambiente
from robo_explorer.agents import (RoboReativoSimples, RoboBaseadoModelo, 
                                 RoboBaseadoObjetivos, RoboBaseadoUtilidade, RoboUtilidadeParcial)

obstaculos_mapa = [ (4,0),(0,1),(3,1),(2,2),(2,3),(5,3),(1,4),(6,4),(3,5),(5,5),(6,5),(7,5),(8,5),(5,6),(8,6),(5,7),(8,7),(5,8),(7,8),(8,8),(5,9) ]

def gerar_pontos_aleatorios(n, obstaculos):
    obstaculos_set = set(obstaculos)
    while True:
        inicio = (random.randint(0, n - 1), random.randint(0, n - 1))
        if inicio not in obstaculos_set: break
    while True:
        fim = (random.randint(0, n - 1), random.randint(0, n - 1))
        if fim not in obstaculos_set and fim != inicio: break
    return inicio, fim
def gerar_terreno_aleatorio(n, inicio, fim, num_custo2=15, num_custo3=10):
    terrenos = {}
    coords = [(x, y) for x in range(n) for y in range(n)]; coords.remove(inicio); coords.remove(fim); random.shuffle(coords)
    for i in range(num_custo2): terrenos[coords.pop(0)] = 2
    for i in range(num_custo3): terrenos[coords.pop(0)] = 3
    return terrenos


def executar_etapa1():
    ambiente = Ambiente(n=10, obstaculos=[])
    visualizador = VisualizacaoDinamica(ambiente)
    robo = RoboReativoSimples(ambiente, visualizador=visualizador)
    robo.explorar()
    visualizador.fechar("Etapa 1: Concluída")

def executar_etapa2():
    ambiente = Ambiente(n=10, obstaculos=obstaculos_mapa)
    visualizador = VisualizacaoDinamica(ambiente)
    robo = RoboBaseadoModelo(ambiente, visualizador=visualizador)
    robo.explorar()
    visualizador.fechar("Etapa 2: Concluída")

def executar_etapa3():
    ambiente = Ambiente(n=10, obstaculos=obstaculos_mapa)
    inicio, fim = gerar_pontos_aleatorios(10, obstaculos_mapa)
    visualizador = VisualizacaoDinamica(ambiente)
    robo = RoboBaseadoObjetivos(ambiente, inicio, fim, visualizador=visualizador)
    robo.executar()
    visualizador.fechar("Etapa 3: Concluída")

def executar_etapa4():
    inicio, fim = (5, 0), (5, 9)
    # terrenos = gerar_terreno_aleatorio(10, inicio, fim)

    # Mapa de terrenos extraído da imagem (custos 2 e 3)
    terrenos = {
        # Custo 3 (Vermelho)
        (5, 2): 3, (5, 3): 3, (6, 3): 3, (4, 4): 3, (5, 4): 3,
        (6, 4): 3, (4, 5): 3, (5, 5): 3, (6, 5): 3, (5, 7): 3,
        # Custo 2 (Amarelo)
        (2, 3): 2, (3, 3): 2, (7, 3): 2, (2, 4): 2, (2, 5): 2,
        (3, 5): 2, (7, 5): 2, (8, 5): 2, (3, 6): 2, (6, 6): 2,
        (7, 6): 2, (4, 7): 2
    }
    ambiente = Ambiente(n=10, obstaculos=[], terrenos=terrenos)
    visualizador = VisualizacaoDinamica(ambiente)
    robo = RoboBaseadoUtilidade(ambiente, inicio, fim, visualizador=visualizador)
    robo.executar_e_avaliar()
    visualizador.fechar("Etapa 4: Concluída")

def executar_etapa4_parcialmente_observavel():
    print("\n--- EXECUTANDO ETAPA 4: AMBIENTE PARCIALMENTE OBSERVÁVEL ---")
    
    inicio, fim = (5, 0), (5, 9)
    
    terrenos_mapa = {
        (5, 2): 3, (5, 3): 3, (6, 3): 3, (4, 4): 3, (5, 4): 3,
        (6, 4): 3, (4, 5): 3, (5, 5): 3, (6, 5): 3, (5, 7): 3,
        (2, 3): 2, (3, 3): 2, (7, 3): 2, (2, 4): 2, (2, 5): 2,
        (3, 5): 2, (7, 5): 2, (8, 5): 2, (3, 6): 2, (6, 6): 2,
        (7, 6): 2, (4, 7): 2
    }

    custo_nucleo = 3
    custo_borda = 2

    terrenos_mapa_dificil = {
        # Núcleo da "Cordilheira" (Custo x - Vermelho)
        (3, 4): custo_nucleo, (4, 4): custo_nucleo, (5, 4): custo_nucleo, (6, 4): custo_nucleo, (7, 4): custo_nucleo,
        (3, 5): custo_nucleo, (7, 5): custo_nucleo,
        (3, 6): custo_nucleo, (4, 6): custo_nucleo, (5, 6): custo_nucleo, (6, 6): custo_nucleo, (7, 6): custo_nucleo,
        
        # Bordas da "Cordilheira" (Custo y - Amarelo)
        (2, 5): custo_borda, (8, 5): custo_borda,
        (2, 6): custo_borda, (8, 6): custo_borda,
        (3, 3): custo_borda, (4, 3): custo_borda, (5, 3): custo_borda, (6, 3): custo_borda, (7, 3): custo_borda,
        (3, 7): custo_borda, (4, 7): custo_borda, (5, 7): custo_borda, (6, 7): custo_borda, (7, 7): custo_borda,
    }
    
    ambiente = Ambiente(n=10, obstaculos=[], terrenos=terrenos_mapa_dificil)
    
    visualizador = VisualizacaoDinamica(ambiente)
    robo = RoboUtilidadeParcial(ambiente, inicio, fim, visualizador=visualizador)
    
    robo.executar_ciclo_planejamento()
    
    visualizador.fechar("Etapa 4 (Parcial): Concluída")

# --- PONTO DE ENTRADA ---
if __name__ == "__main__":
    # Escolha qual etapa você quer visualizar de forma animada
    # executar_etapa1()
    # executar_etapa2()
    # executar_etapa3()
    # executar_etapa4()
    executar_etapa4_parcialmente_observavel()