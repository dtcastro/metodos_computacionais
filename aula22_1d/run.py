# -*- coding: utf-8 -*-
"""
Created on Sat Sep  1 10:40:37 2018

@author: dtcas
"""

from model import ElFarolModel, Person

################# pra rodar sem o batch runner ##############
memory_size = 3
number_strategies = 3
number_persons = 8
overcrowding_threshold = 5
model = ElFarolModel(memory_size, number_strategies, number_persons, 
                     overcrowding_threshold)

for i in range(20):
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
#model_data = model.datacollector.get_model_vars_dataframe()

# TODO
# 2 COLOCAR O ESPAÇO 
# 3 colocar o custo para sacar o dinheiro
# ver os total de instrumentos favoritos de cada grupo

