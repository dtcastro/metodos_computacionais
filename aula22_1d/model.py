"""
Implementação em Python com o módulo Mesa do modelo El Farol do NetLogo:
    Wilensky, U.; Rand, W. (2015). NetLogo El Farol model.
    
Documentação do mesa: https://mesa.readthedocs.io/en/master/index.html
Código no GitHub do mesa: https://github.com/projectmesa/mesa

Correções pontuais para refletir o modelo de Fogel (1999), em que o modelo do 
NetLogo se baseou, mas parece ter implementado de forma ligeiramente incorreta
(correções destacadas ao longo dos comentários do código).
Comentários em inglês são de (Wilensky e Rand, 2015).
"""

import random
import numpy
import math
import sys
from mesa import Agent, Model
from mesa.time import BaseScheduler
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

# indica se exibe informações para debugar o código ou não
verbose = 0

class Strategy():
    """
    Comentário de Wilensky e Rand (2015):
    this reports a random strategy. a strategy is just a set of weights 
    from -1.0 to 1.0 which determines how much emphasis is put on each 
    previous time period when making an attendance prediction for the next 
    time period.
    """
    def __init__(self, memory_size):
        # cria uma estratégia atribuindo pesos aleatórios, mas imutáveis ao 
        # longo da simulação
        self.weights = numpy.random.uniform(low = -1.0, high = 1.0, 
                                            size = memory_size)
        if verbose:
            print(self)
    
    def __str__(self):
        """
        Imprime informações da estratégia.
        """
        strategy_str = "Strategy "
        for i in range(len(self.weights)):
            strategy_str += "weight[%d]: %f " % (i, self.weights[i])
        return strategy_str
        
class Person(Agent):
    """
    Um agente que representa uma pessoa que gosta de música irlandesa em
    Santa Fé. A cada passo, dependendo da previsão da melhor estratégia para a 
    lotação do bar, a pessoa decide ir ou não a o bar. A melhor estratégia é 
    aquela que, no passo corrente, teria fornecido as melhores previsões, com 
    base no histórico de frequência ao bar.
    Cada pessoa tem um conjunto de estratégias pré-definidas, mas a cada momento
    apenas a estratégia que apresentou o melhor desempenho é utilizada para 
    prever a lotação da noite, a partir da qual a pessoa decide se vai ou não 
    ao bar.
    As extensões do NetLogo pedem que, a cada passo que o agente escolhe ir ao
    bar e o bar não está lotado, ele seja recompensado; as recompensas são 
    acumuladas ao longo da simulação.
    """
    def __init__(self, unique_id, model, memory_size, number_strategies, 
                 number_persons, overcrowding_threshold, history):
        super().__init__(unique_id, model)
        self.memory_size = memory_size
        # cria as estratégias
        self.strategies = [Strategy(memory_size) for _ in range(number_strategies)]
        self.number_persons = number_persons
        self.overcrowding_threshold = overcrowding_threshold
        self.best_strategy = self.strategies[0]
        # como as listas não são replicáveis, o histórico de frequência ao bar
        # pode ser uma variável de instância; caso contrário, haveria um histórico
        # para cada agente, replicando de forma desnecessária e podendo ocasionar
        # problema de memória
        self.history = history 
        self.attend = 0 # 1 se o agente planeja ir ao bar na próxima noite
        
        # PRIMEIRA EXTENSÃO DO NETLOGO
        self.reward = 0 # recompensa acumulada por cada agente até o momento
        # recompensa relativa à máxima de todos os agentes; serve para 
        # definir o tamanho dos agentes, mas não ficou na solução final
        self.relative_reward = 0
        
        self.update_strategies()
        
    def __str__(self):
        return "Person %d; reward: %d" % (self.unique_id, self.reward)
     
    def update_strategies(self):
        """
        Comment from Wilensky and Rand (2015):
        Determines which strategy would have predicted the best results had it 
        been used this round. The best strategy is the one that has the sum of 
        smallest differences between the current attendance and the predicted 
        attendance for each of the preceding weeks (going back MEMORY-SIZE 
        weeks) this does not change the strategies at all, but it does 
        (potentially) change the one currently being used and updates the 
        performance of all strategies.
        """
        
        # Comment from Wilensky and Rand (2015): 
        # initialize best-score to a maximum, which is the lowest possible score
        best_score = self.memory_size * self.number_persons + 1
        
        if verbose:
            print("best_score :" + str(best_score))
        for i in range(len(self.strategies)):
            score = 0
            for week in range(self.memory_size):
                # previsão da estratégia para semanas passadas, com base nas 
                # informações históricas 
                prediction = self.predict_attendance(self.strategies[i], 
                                                     week + 1)
                
                if verbose:
                    print("Prediction " + str(i) + ": " + str(prediction))
                
                # A implementação incorreta do modelo do NetLogo em relação a 
                # Fogel (1999) não chegou a inviabilizar o modelo porque o
                # escore da estratégia era ruim; a consequência era apenas que
                # havia mais estratégias ruins do que o esperado
                # Quanto menor o escore, melhor a estratégia; assim, quanto mais
                # perto do observado for a previsão, menor o escore
                score += abs(self.history[week] - prediction)
                
                if verbose:
                    print("History[" + str(week) + "]: " + str(self.history[week]) + " score: " + str(score))

            if (score <= best_score):
                # atualizar a melhor estratégia corrente, com base no menor escore
                best_score = score # se tirar essa linha o modelo converge melhor; investigar
                self.best_strategy = self.strategies[i]
 
    def predict_attendance(self, strategy, week):
        """
        Comment from Wilensky and Rand (2015):
        This reports an agent's prediction of the current attendance using a 
        particular strategy and portion of the attendance history. More 
        specifically, the strategy is then described by the formula 
        p(t) = x(t - 1) * a(t - 1) + x(t - 2) * a(t -2) +.. 
            ... + x(t - MEMORY-SIZE) * a(t - MEMORY-SIZE) + c * 100,
        where p(t) is the prediction at time t, x(t) is the attendance of the 
        bar at time t, a(t) is the weight for time t, c is a constant, and 
        MEMORY-SIZE is an external parameter.
        """
        if verbose:
            print("predict_attendance week: " + str(week))

        # Comment from Wilensky and Rand (2015):
        # the first element of the strategy is the constant, c, in the 
        # prediction formula. one can think of it as the the agent's 
        # prediction of the bar's attendance in the absence of any other data 
        # then we multiply each week in the history by its respective weight

        # Correção para implementar apropriadamente o modelo de Fogel (1999).
        # O código do NetLogo multiplica o primeiro peso pelo número de 
        # pessoas, uma operação qe não existe no paper do Fogel (1999); isso 
        # faz com que os valores previstos sejam maiores do que seriam, fazendo
        # com que as estratégias sejam piores
        prediction = strategy.weights[0]
        # A linha abaixo replica o que está implementado no código do NetLogo,
        # que não é o que está no paper do Fogel (1999)
        #prediction = strategy.weights[0] * number_of_persons
       
        if verbose:
            print("prediction 0: " + str(prediction))

        for i in range(len(strategy.weights) - 1):
            # i+ 1 porque i começa em zero, mas o peso zero é a constante
            # usada acima
            prediction += strategy.weights[i + 1] * self.history[week + i]
            
            if verbose:
                print("iteracao " + str(i) + " " + str(strategy.weights[i + 1]) + " " + str(self.history[week + i]))

        # Correção para implementar apropriadamente o modelo do Fogel (1999).
        # O código do NetLogo não arredonda e não pega o valor absoluto da
        # previsão. Assim, a previsão assume incorretamente valores negativos 
        # e não inteiros. O código do NetLogo não tem linha correspondente à 
        # linha abaixo.
        prediction = round(abs(prediction))
        
        # Correção para implementar apropriadamente o modelo do Fogel (1999).
        # O código do NetLogo aceita valores da frequência superiores ao total
        # de pessoas, o que claramente é um erro. Isso não afeta os resultados
        # porque o método update_strategies calcula o valor absoluto da 
        # diferença entre o valor previsto e o valor efetivamente observado.
        # Assim, previsões negativas ou superiores ao total de pessoas 
        # simplesmente fazem com que as estratégias sejam piores. O código do
        # NetLogo não tem expressões correspondentes a essas.
        if prediction > self.number_persons:
            prediction = self.number_persons
        
        return prediction # previsão para a frequência ao bar
        
    def step(self):
        """ 
        Um passo da simulação.
        Nesse passo, o agente decide se vai ou não ao bar com base na previsão
        da melhor estratégia do momento.
        """
        if verbose:
            print("Person.step:")

        prediction = self.predict_attendance(self.best_strategy, week = 0)
        if verbose:
            print("prediction no step: " + str(prediction))

        # decide se vai ou não ao bar
        self.attend = (prediction <= self.overcrowding_threshold)

        if self.attend:
            # se o agente decidiu ir ao bar, coloca o agente no bar
            # TO DO: poderia ser uma função
            x = self.model.random.randrange(self.model.x_bar_init, 
                                            self.model.grid.width)
            y = self.model.random.randrange(self.model.y_bar_init, 
                                            self.model.grid.height)
        else:
            # se o agente decidiu não ir ao bar, coloca o agente em casa
            x = self.model.random.randrange(self.model.grid.width)
            if (x > (self.model.x_bar_init - 1)):
                y = self.model.random.randrange(self.model.y_bar_init - 1)
            else:
                y = self.model.random.randrange(self.model.grid.height)
            
        self.model.grid.move_agent(self, (x, y))

class ElFarolModel(Model):
    """
    Modelo El Farol como implementado no NetLogo.
    """
    def __init__(self, memory_size, number_strategies, number_persons, 
                 overcrowding_threshold):
        self.running = True # necessário para que o modelo seja chamado pelo servidor web
        self.memory_size = memory_size
        self.number_strategies = number_strategies
        self.number_persons = number_persons
        self.overcrowding_threshold = overcrowding_threshold
        
        # lista dos valores passados da frequência ao bar
        # history[0] é a frequência da semana mais recente
        self.history = random.sample(range(1, self.number_persons), 
                                     self.memory_size * 2)
        if verbose:
            print(self.history)
        self.attendance = self.history[0]

        self.schedule = BaseScheduler(self)

        # tamanho do grid definido em função do número de pessoas, como na 
        # visualização; pode ser um valor comum aos dois
        width = height = round(2 * round(math.sqrt(number_persons)))
        
        # mais que um agente pode estar na mesma célula; no modelo original do
        # NetLogo, há apenas um agente por célula; basta trocar por SigleGrid
        # aqui, mas tem que tratar para que, se for selecionada uma célula já
        # ocupada, colocar o agente em outra célula
        self.grid = MultiGrid(width, height, True)
        # define as coordenadas do bar, que está localizado no quadrante 
        # superior direito
        self.x_bar_init = round(width/2)
        self.y_bar_init = round(height/2)
        
        # Cria os agentes
        for i in range(self.number_persons):
            # history pode ser passada como parametro pq listas não são duplicadas
            # assim, garante-se que é uma history só, igual para todos os agentes
            person = Person(i, self, self.memory_size, self.number_strategies, 
                            self.number_persons, self.overcrowding_threshold, 
                            self.history)
            self.schedule.add(person)
            
            # Coloco as pessoas em casa inicialmente
            x = self.x_bar_init
            y = self.y_bar_init
            x = self.random.randrange(self.grid.width)
            # TO DO: pode ser função
            if (x >= (self.x_bar_init - 1)):
                # se o x foi maior que o limite do bar, o y tem que ser fora
                y = self.random.randrange(self.y_bar_init - 1)
            else:
                y = self.random.randrange(self.grid.height)
            
            self.grid.place_agent(person, (x, y))
            
        # variáveis que indicam os valores máximo, mínimo e médio para as 
        # recompensas de todos os agentes
        self.max_reward = 0 # PRIMEIRA EXTENSÃO
        self.min_reward = sys.maxsize # SEGUNDA EXTENSÃO
        self.mean_reward = 0 # SEGUNDA EXTENSÃO
        # TERCEIRA EXTENSÃO
        # Representam os valores do histograma da distribuição de recompensas
        # Não é a solução ideal porque o número de segmentos está fixo em 5
        # O modelo original do NetLogo mostra todos os valores de recompensa e 
        # número de agentes por cada um.
        self.bin0 = 0
        self.bin1 = 0
        self.bin2 = 0
        self.bin3 = 0
        self.bin4 = 0

        # Coleta a frequência em cada passo, os valores da distribuição de 
        # recompensas para exibição do histograma e o valor da recompensa de 
        # cada agente        
        self.datacollector = DataCollector(
                model_reporters={"Attendance": "attendance",
                                 "Bin0": "bin0",
                                 "Bin1": "bin1",
                                 "Bin2": "bin2",
                                 "Bin3": "bin3",
                                 "Bin4": "bin4"},
                agent_reporters={"Reward": lambda x: x.reward})
    
        self.datacollector.collect(self)
            
    def get_attendance(self):
        """
        Calcula a frequência corrente como a soma de todos os agentes que 
        decidiram ir ao bar.
        """
        # sum() retorna int64, que não é serializable e causa erro no módulo 
        # JSON usado pelo mesa para exibir as informações e o grid no browser
        # O erro é: "TypeError: Object of type 'int32' is not JSON serializable"
        return int(sum([person.attend for person in self.schedule.agents]))
    
    def update_history(self):
        """
        Atualiza a lista de frequêcias históricas com a frequência mais recente.
        Descarta o valor mais antigo.
        """
        self.history.pop() # remove o último elemento
        
        # Não cria umanova lista, mantendo válidas as referência à variável
        # history mantida pelos objetos da classe Person
        self.history.insert(0, self.attendance) 
        if verbose:
            print(self.history)
        
    def update_rewards_histogram(self):
        """
        TERCEIRA EXTENSÃO
        O mesa parece não ter suporte para histograma de distribuição de uma
        variável, como tem o NetLogo. O histograma do mesa é apropriado para 
        exibir determinado valor de todos os agentes.
        Assim, esse método não muito inteligente para exibir histograma das 
        recompensas, já que o número de segmentos é fixo em 5. Há uma variável
        por segmento.
        """
        self.bin0 = 0
        self.bin1 = 0
        self.bin2 = 0
        self.bin3 = 0
        self.bin4 = 0
        
        increment = self.max_reward / 5
        print(increment)
        for person in self.schedule.agents:
            if person.reward <= increment:
                self.bin0 += 1
            elif person.reward <= 2 * increment:
                self.bin1 += 1
            elif person.reward <= 3 * increment:
                self.bin2 += 1
            elif person.reward <= 4 * increment:
                self.bin3 += 1
            elif person.reward <= 5 * increment:
                self.bin4 += 1
   
    def step(self):
        """
        Avança o modelo por um passo. Atualiza a frequência, a lista de 
        frequências histórica e a melhor estratégia de cada agente.
        Atualiza também os valores máximo, mínimo e médio das recompensas,
        para exibição.
        """
        self.schedule.step()
        # atualiza o valor da última frequência
        self.attendance = self.get_attendance()
        if verbose:
            print("attendance")
            print(self.attendance)
        self.update_history()
        
        for person in self.schedule.agents:
            # atualiza a melhor estratégia de cada agente
            person.update_strategies()
            
            # PRIMEIRA EXTENSÃO
            # se o bar não está lotado, recompensa cada agente que foi ao bar
            if self.attendance <= self.overcrowding_threshold:
                if person.attend:
                    person.reward += 1
        
        # PRIMEIRA EXTENSÃO
        # atualiza as frequências relativas para exibir as pessoas mais bem 
        # sucedidas maiores, mas, como não era o que o modelo original do 
        # NetLogo fazia, optei por não exibir imagens, mas um quadrado
        # colorido mesmo
        if self.max_reward > 0:
            for person in self.schedule.agents:
                person.relative_reward = person.reward/self.max_reward
        
        # SEGUNDA EXTENSÃO
        # atualiza os valores máximo, médio e mínimo das recompensas
        self.max_reward = max([person.reward for person in 
                                       self.schedule.agents])

        self.mean_reward = numpy.mean([person.reward for person in 
                                       self.schedule.agents])

        self.min_reward = min([person.reward for person in 
                                       self.schedule.agents])

        # TERCEIRA EXTENSÃO    
        # atualiza os valores para exibição do histogram de recompensas
        self.update_rewards_histogram()
        self.datacollector.collect(self)
        