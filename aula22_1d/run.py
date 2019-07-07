"""
Roda a simulação do modelo, mas sem exibir os agentes em um grid no browser.
"""

from model import ElFarolModel

################# pra rodar sem o batch runner ##############
memory_size = 5
number_strategies = 10
number_persons = 100
overcrowding_threshold = 60
model = ElFarolModel(memory_size, number_strategies, number_persons, 
                     overcrowding_threshold)

for i in range(50):
    """ 
    Roda n passos na simulação.
    """
    print('Rodada ' + str(i))
    model.step()

# Recupera os valores finais do coletor de dados
model_data = model.datacollector.get_model_vars_dataframe()