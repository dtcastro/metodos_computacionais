"""
Descrição do modelo do El Farol

"""

import random
import numpy
import math
from mesa import Agent, Model
from mesa.time import BaseScheduler
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

# ver se as variáveis podem ser globais ou precisam ser de instância mesmo;
# acho que precisam ser das classes para que as simulações possam ser feitas

# history = [] # para evitar que todos os objetos Person tenham uma copia de history
# ver se passar history como parametro e armazenar como variavel de instancia duplica a history ou aponta pra mesma

verbose = 0

class Strategy():
    def __init__(self, memory_size):
        self.weights = numpy.random.uniform(low = -1.0, high = 1.0, 
                                            size = memory_size)
        if verbose:
            print(self)
    
    def __str__(self):
        strategy_str = "Strategy "
        for i in range(len(self.weights)):
            strategy_str += "weight[%d]: %f " % (i, self.weights[i])
        return strategy_str
        
class Person(Agent):
    """Uma Pessoa que gosta de música irlandesa em Santa Fe
    """
    def __init__(self, unique_id, model, memory_size, number_strategies, 
                 number_persons, overcrowding_threshold, history):
        if verbose:
            print("Person.__init__")
        super().__init__(unique_id, model)
        self.memory_size = memory_size
        self.strategies = [Strategy(memory_size) for _ in range(number_strategies)]
        self.number_persons = number_persons
        self.overcrowding_threshold = overcrowding_threshold
        self.best_strategy = self.strategies[0]
        # aqui não precisa ser de instância pq vai ser a mesma pra todos os objetos
        self.history = history # ver desempenho, se não está duplicando tudo mesmo; se é passagem por referência ou por valor
        self.attend = 0
        
        if verbose:
            print(self.history)
        self.update_strategies()
        if verbose:
            print("fim Person.__init__")
        
    def __str__(self):
        return "Pessoa %d" % (self.unique_id)
     
    def update_strategies(self):
        if verbose:
            print("update_strategies")
        best_score = self.memory_size * self.number_persons + 1
        
        if verbose:
            print("best_score :" + str(best_score))
        for i in range(len(self.strategies)):
            score = 0
            for week in range(self.memory_size):
                prediction = self.predict_attendance(self.strategies[i], 
                                                     week + 1)
                
                if verbose:
                    print("Prediction " + str(i) + ": " + str(prediction))
                score += abs(self.history[week] - prediction)
                
                if verbose:
                    print("History[" + str(week) + "]: " + str(self.history[week]) + " score: " + str(score))
            #print(score)
            if (score <= best_score):
                best_score = score # se tirar essa linha o modelo converge melhor
                self.best_strategy = self.strategies[i]
 
    def predict_attendance(self, strategy, week):
        if verbose:
            print("predict_attendance week: " + str(week))
        #print(strategy)
        prediction = strategy.weights[0] # isso é o que está no artigo do Fogel 1999
        #prediction = strategy.weights[0] * 100 # isso é o que está no código do netlogo
        #print("history")
        #print(self.history)
        if verbose:
            print("prediction 0: " + str(prediction))

        for i in range(len(strategy.weights) - 1):
            #print(i)
            # i + 1 pq i começa em zero e o peso zero foi usado acima como 
            # constante; conferir se é sub_history i ou i + 1 mesmo pq o zero é o attendance
            prediction += strategy.weights[i + 1] * self.history[week + i]
            
            if verbose:
                print("iteracao " + str(i) + " " + str(strategy.weights[i + 1]) + " " + str(self.history[week + i]))
            
        # está  no artigo do Fogel 1999, mas não tem no código do NetLogo
        prediction = round(abs(prediction))
        
        # esse if está no Fogel 1999, mas não tem no código do NetLogo
        if prediction > self.number_persons:
            prediction = self.number_persons
        
        return prediction
        
    def step(self):
        """ Decides if goes to the bar or not"""
        if verbose:
            print("Person.step:")
        #prediction = self.predict_attendance(self.strategies[0])
        prediction = self.predict_attendance(self.best_strategy, week = 0)
        if verbose:
            print("prediction no step: " + str(prediction))
        self.attend = (prediction <= self.overcrowding_threshold)
        #print(attend)
        #self.update_strategies()
        if self.attend:
            x = self.model.random.randrange(self.model.x_bar_init, 
                                            self.model.grid.width)
            y = self.model.random.randrange(self.model.y_bar_init, 
                                            self.model.grid.height)
        else:
            x = self.model.random.randrange(self.model.grid.width)
            if (x > self.model.x_bar_init):
                y = self.model.random.randrange(self.model.y_bar_init)
            else:
                y = self.model.random.randrange(self.model.grid.height)
            
        self.model.grid.move_agent(self, (x, y))

class ElFarolModel(Model):
    """A model with some number of agents."""
    def __init__(self, memory_size, number_strategies, number_persons, 
                 overcrowding_threshold):
        # precisa ser variável de instância pq é esse instância com esses valores; outro modelo tem outros valores; não é o mesmo valor para qualquer objeto
        self.running = True
        self.memory_size = memory_size
        self.number_strategies = number_strategies
        self.number_persons = number_persons
        self.overcrowding_threshold = overcrowding_threshold
        # indice zero é o mais recente
        self.history = random.sample(range(1, self.number_persons), 
                                     self.memory_size * 2)
        if verbose:
            print(self.history)
        self.attendance = self.history[0]

        #self.schedule = RandomActivation(self)
        self.schedule = BaseScheduler(self)
        #self.schedule = StagedActivation(self, ["period1", "period2"])

        width = height = round(2 * round(math.sqrt(number_persons)))
        self.grid = MultiGrid(width, height, True) # como está na configuração do NetLogo
        self.x_bar_init = round(width/2)
        self.y_bar_init = round(height/2)
        
        # Create people
        for i in range(self.number_persons):
            person = Person(i, self, self.memory_size, self.number_strategies, 
                            self.number_persons, self.overcrowding_threshold, 
                            self.history) # ver a questão de passar a history como parametro pq tem que ser igual pra todo mundo
#            people = Person(i, self, Strategy(self.memory_size))
            self.schedule.add(person)
            
            # Coloco as pessoas em casa

            x = self.x_bar_init
            y = self.y_bar_init
            
            #while(x >= x_bar_init & y <= y_bar_init): # origem estranha; ver se tem como mudar
                #x = self.random.randrange(0, x_bar_init - 2) # menos 2 pq tem a porta do bar
                #x = self.random.randrange(x_bar_init, self.grid.width)
                #x = self.random.randrange(self.grid.width)
                #y = self.random.randrange(0, y_bar_init - 2)
                #y = self.random.randrange(y_bar_init, self.grid.height)
                #y = self.random.randrange(self.grid.height)

            x = self.random.randrange(self.grid.width)
            #x = 2
            #y = self.random.randrange(self.grid.height)
            #y = 3
            # ver direito a questão da posição
            if (x >= self.x_bar_init):
                # se o x foi maior que o limite do bar, o y tem que ser fora
                y = self.random.randrange(self.y_bar_init)
            else:
                y = self.random.randrange(self.grid.height)
            
            self.grid.place_agent(person, (x, y))
            
        self.datacollector = DataCollector(
                model_reporters={"Attendance": "attendance"})
    
        self.datacollector.collect(self)
            
    def get_attendance(self):
        """calculate attendance"""
        return int(sum([person.attend for person in self.schedule.agents]))
        #return attendance
    
    def update_history(self):
        self.history.pop() # removes the last element
        #self.history = [self.attendance] + self.history # não funciona pq cria nova lista
        self.history.insert(0, self.attendance)
        if verbose:
            print(self.history)
        
    def step(self):
        '''Advance the model by one step.'''
        print("step")
        self.schedule.step()
        self.attendance = self.get_attendance()
        verbose = 1
        if verbose:
            print("attendance")
            print(self.attendance)
        self.update_history()
        for person in self.schedule.agents:
            person.update_strategies()
        self.datacollector.collect(self)
        