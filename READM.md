# Robô Explorador Inteligente


## Sobre o Projeto

Este projeto, desenvolvido como parte da disciplina de Inteligência Artificial, simula o comportamento de um robô autônomo em um ambiente de grid. O objetivo principal é demonstrar e solidificar a compreensão sobre as diferentes tipologias de agentes inteligentes.

A complexidade do agente evolui progressivamente através de quatro etapas, começando com um agente reativo simples e sem memória, e avançando até um agente sofisticado baseado em utilidade que otimiza rotas com base em custos de terreno.

## Estrutura de Arquivos

O projeto está organizado da seguinte maneira para garantir modularidade e clareza:

```
PROJETO_ROBO_IA/
├── robo_explorer/
│   ├── __init__.py         # Torna o diretório um pacote Python
│   ├── agents.py           # Contém as classes de todos os agentes (Robôs)
│   ├── environment.py      # Contém a classe que gerencia o ambiente (grid, obstáculos, etc.)
│   └── visualization.py    # Contém a classe para a visualização dinâmica
├── main.py                 # Script principal para executar as simulações
└── requirements.txt        # Lista de dependências do projeto
```

## Tecnologias Utilizadas

  * **Python 3.x**
  * **Matplotlib:** Para a visualização gráfica do grid e do comportamento do agente.
  * **NumPy:** Como dependência do Matplotlib para manipulação de matrizes.

## Configuração do Ambiente

Siga os passos abaixo para configurar e executar o projeto em sua máquina local.

### Pré-requisitos

  * Certifique-se de ter o Python 3 instalado. Você pode baixá-lo em [python.org](https://www.python.org/).

### Instalação

1.  **Clone o repositório** (ou simplesmente baixe e descompacte os arquivos em uma pasta chamada `PROJETO_ROBO_IA`).

2.  **Crie o arquivo `requirements.txt`** na raiz do projeto (`PROJETO_ROBO_IA/`) com o seguinte conteúdo:

    ```
    matplotlib
    ```

3.  **Abra um terminal** na pasta raiz do projeto.

4.  **Crie um ambiente virtual** para isolar as dependências do projeto:

    ```bash
    python -m venv venv
    ```

5.  **Ative o ambiente virtual:**

      * **No Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
      * **No macOS / Linux:**
        ```bash
        source venv/bin/activate
        ```

6.  **Instale as bibliotecas necessárias** a partir do arquivo `requirements.txt`:

    ```bash
    pip install -r requirements.txt
    ```

## Como Executar

Toda a execução é controlada pelo arquivo `main.py`. Para escolher qual etapa da simulação você quer visualizar, edite o bloco final do arquivo.

1.  **Abra o arquivo `main.py`** em um editor de código.

2.  **Navegue até o final do arquivo**, no bloco `if __name__ == "__main__":`.

3.  **Descomente a função da etapa que deseja executar** e comente as outras. Por exemplo, para executar a Etapa 2:

    ```python
    if __name__ == "__main__":
        # Escolha qual etapa você quer visualizar de forma animada
        # executar_etapa1()
        executar_etapa2()
        # executar_etapa3()
        # executar_etapa4()
    ```

4.  **Execute o script** a partir do seu terminal (com o ambiente virtual ativado):

    ```bash
    python main.py
    ```

    Uma janela do Matplotlib aparecerá, mostrando a simulação passo a passo da etapa escolhida.

## Descrição das Etapas (Agentes)

### Etapa 1: Agente Reativo Simples

  * **Objetivo:** Encontrar as 4 paredes que delimitam o grid.
  * **Lógica:** O robô escolhe uma direção e se move em linha reta até colidir com um limite. Ao colidir, ele registra a parede encontrada e escolhe uma nova direção para continuar a exploração. O ambiente não possui obstáculos internos.

### Etapa 2: Agente Reativo Baseado em Modelo

  * **Objetivo:** Explorar o máximo possível de um mapa com obstáculos.
  * **Lógica:** O agente utiliza uma memória (`mapa_visitados`) para saber por onde já passou. Ele sempre prioriza se mover para células adjacentes que ainda não foram visitadas. Se todos os vizinhos já foram visitados, ele se move para uma célula aleatória adjacente para tentar "desbloquear" seu caminho.

### Etapa 3: Agente Baseado em Objetivos

  * **Objetivo:** Encontrar o caminho mais curto (em número de passos) entre um ponto de início e um ponto de fim aleatórios.
  * **Lógica:** O agente recebe o mapa completo com os obstáculos de antemão. Ele utiliza o algoritmo **A\* (A-Estrela)** para calcular a rota ótima antes de se mover. A animação mostra o robô executando o caminho que já foi planejado.

### Etapa 4: Agente Baseado em Utilidade

  * **Objetivo:** Encontrar o caminho de **menor custo total** entre um ponto de início e um de fim fixos, em um mapa com diferentes tipos de terreno.
  * **Lógica:** Similar à Etapa 3, o agente usa o algoritmo A\*, mas a função de custo é modificada. Cada passo não vale "1", mas sim o valor do custo do terreno da célula de destino (ex: 1 para normal, 2 para arenoso, 3 para rochoso). Isso pode fazer com que o robô escolha um caminho mais longo em passos para evitar terrenos caros.