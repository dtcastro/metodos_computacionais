# -*- coding: utf-8 -*-
"""
Descrição do modelo do El Farol

"""

#import random
import numpy
from mesa import Agent, Model
from mesa.time import BaseScheduler
#from mesa.time import RandomActivation
#from mesa.time import StagedActivation # talvez seja o staged se primeiro tomar a decisão e depois reavaliar
#from mesa.datacollection import DataCollector

memory_size = 5

class Strategy():
    def __init__(self):
        self.pesos = numpy.random.uniform(low = -1.0, high = 1.0, size = memory_size)
        print(self.pesos[0])
        
class Person(Agent):
    """Uma Pessoa que gosta de música irlandesa em Santa Fe
    """
    def __init__(self, unique_id, model, strategy):
        super().__init__(unique_id, model)
        self.strategy = strategy
        
    def __str__(self):
        return "Pessoa %d" % (self.unique_id)
      
    def step(self):
        """ Decides if goes to the bar or not"""
        return 0

class ElFarolModel(Model):
    """A model with some number of agents."""
    def __init__(self):
        #self.schedule = RandomActivation(self)
        self.schedule = BaseScheduler(self)
        #self.schedule = StagedActivation(self, ["period1", "period2"])
        #total_sales = 0
        
     
        # Create people
        for i in range(5):
            people = Person(i, self, Strategy())
            self.schedule.add(people)
            
          
    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()
        