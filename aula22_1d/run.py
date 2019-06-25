# -*- coding: utf-8 -*-
"""
Created on Sat Sep  1 10:40:37 2018

@author: dtcas
"""

from model import ElFarolModel, Person
import numpy as np
import matplotlib.pyplot as plt

################# pra rodar sem o batch runner ##############
memory_size = 5
number_strategies = 10
number_persons = 100
overcrowding_threshold = 60
model = ElFarolModel(memory_size, number_strategies, number_persons, 
                     overcrowding_threshold)

for i in range(2):
    """ Calls step n times"""
    print('rodada ' + str(i))
    model.step()
    #for obj in model.schedule.agents:
        #if isinstance(obj, Person):
            #print('Lojista ' + str(obj.unique_id) + ' sales: ' + str(obj.sales) + ' lost sales: ' + str(obj.lost_sales))
            #print(obj.history)
#        if isinstance(obj, Portador):
#            print('Portador ' + str(obj.unique_id) + 'recursos: ' + str(obj.recursos))

#merchants_data = model.datacollector.get_agent_vars_dataframe()
#print(merchants_data.tail())
#
model_data = model.datacollector.get_model_vars_dataframe()

# TODO
# 2 COLOCAR O ESPAÇO 
# 3 colocar o custo para sacar o dinheiro
# ver os total de instrumentos favoritos de cada grupo

agent_counts = np.zeros((model.grid.width, model.grid.height))
for cell in model.grid.coord_iter():
    cell_content, x, y = cell
    agent_count = len(cell_content)
    agent_counts[x][y] = agent_count
plt.imshow(agent_counts, interpolation='nearest')
plt.colorbar()

# If running from a text editor or IDE, remember you'll need the following:
# plt.show()