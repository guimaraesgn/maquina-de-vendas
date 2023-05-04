from tkgpio import TkCircuit

from os import path
from json import load

def rodar (programa):
    pasta_atual = path.dirname(__file__)
    caminho_das_configuracoes = path.join(pasta_atual, "configuracoes.json")
    with open(caminho_das_configuracoes, encoding="UTF-8") as arquivo:
        configuracoes = load(arquivo)
    
    circuito = TkCircuit(configuracoes)
    circuito.run(programa)