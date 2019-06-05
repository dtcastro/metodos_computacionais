# -*- coding: utf-8 -*-
"""
Descrição do modelo do El Farol

"""

import random
import numpy
from mesa import Agent, Model
from mesa.time import BaseScheduler
#from mesa.time import RandomActivation
#from mesa.time import StagedActivation # talvez seja o staged se primeiro tomar a decisão e depois reavaliar
#from mesa.datacollection import DataCollector

# ver se as variáveis podem ser globais ou precisam ser de instância mesmo;
# acho que precisam ser das classes para que as simulações possam ser feitas

#history = []

class Strategy():
    def __init__(self, memory_size):
        self.weights = numpy.random.uniform(low = -1.0, high = 1.0, size = memory_size)
        #print(self)
    
    def __str__(self):
        strategy_str = "Strategy "
        for i in range(len(self.weights)):
            strategy_str += "weight[%d]: %f " % (i, self.weights[i])
        return strategy_str
        
class Person(Agent):
    """Uma Pessoa que gosta de música irlandesa em Santa Fe
    """
    def __init__(self, unique_id, model, strategy):
        super().__init__(unique_id, model)
        self.strategy = strategy
        
    def __init__(self, unique_id, model, number_strategies, memory_size, history):
        super().__init__(unique_id, model)
        self.strategies = [Strategy(memory_size) for _ in range(number_strategies)]
        self.best_strategy = self.strategies[0]
        # aqui não precisa ser de instância pq vai ser a mesma pra todos os objetos
        self.history = history # ver desempenho, se não está duplicando tudo mesmo; se é passagem por referência ou por valor
        
    def __str__(self):
        return "Pessoa %d" % (self.unique_id)
     
    def update_stragegy(memory_size):
        best_score = memory_size * 100 + 1
#        for i in range(len(self.strategies)):
 
    def predict_attendance(self, strategy):
        print("predict_attendance")
        print(strategy)
        prediction = strategy.weights[0] # isso é o que está no artigo do Fogel 1999
        #prediction = strategy.weights[0] * 100 # isso é o que está no código do netlogo
        for i in range(len(strategy.weights) - 1):
            print(i)
            # i + 1 pq i começa em zero e o peso zero foi usado acima como 
            # constante; conferir se é sub_history i ou i + 1 mesmo pq o zero é o attendance
            prediction += strategy.weights[i + 1] * self.history[i]
        
        # está  no artigo do Fogel 1999, mas não tem no código do NetLogo
        prediction = round(abs(prediction))
        
        # esse if está no Fogel 1999, mas não tem no código do NetLogo
        if prediction > 100:
            prediction = 100
        
        return prediction
        
    def step(self):
        """ Decides if goes to the bar or not"""
        prediction = self.predict_attendance(self.strategies[0])
        print(prediction)
        
class ElFarolModel(Model):
    """A model with some number of agents."""
    def __init__(self, memory_size, number_strategies):
        # precisa ser variável de instância pq é esse instância com esses valores; outro modelo tem outros valores; não é o mesmo valor para qualquer objeto
        self.memory_size = memory_size
        self.number_strategies = number_strategies
        self.history = random.sample(range(1, 100), self.memory_size * 2)
        print(self.history)
        self.attendance = self.history[0]

        #self.schedule = RandomActivation(self)
        self.schedule = BaseScheduler(self)
        #self.schedule = StagedActivation(self, ["period1", "period2"])
        
        # Create people
        for i in range(5):
            people = Person(i, self, self.number_strategies, self.memory_size,
                            self.history) # ver a questão de passar a history como parametro pq tem que ser igual pra todo mundo
#            people = Person(i, self, Strategy(self.memory_size))
            self.schedule.add(people)
            
          
    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()
        