class Ambiente:
    """
    Representa o ambiente de grid n x n.
    Contém informações sobre o tamanho, obstáculos e custos de terreno.
    """
    def __init__(self, n=10, obstaculos=None, terrenos=None):
        self.n = n
        self.obstaculos = set(obstaculos) if obstaculos else set()
        self.terrenos = terrenos if terrenos else {} 

    def is_valido(self, x, y):
        """
        Verifica se uma posição (x, y) está dentro dos limites E NÃO É UM OBSTÁCULO.
        Esta é a verificação crucial que estava falhando.
        """
        # 1. Verifica se está dentro dos limites do grid
        if not (0 <= x < self.n and 0 <= y < self.n):
            return False
        
        # 2. VERIFICA SE A POSIÇÃO É UM OBSTÁCULO
        if (x, y) in self.obstaculos:
            return False
            
        # Se passou nas duas verificações, a célula é válida
        return True

    def get_custo(self, x, y):
        """Retorna o custo de movimento para uma célula, com padrão 1 (Normal)."""
        return self.terrenos.get((x, y), 1)