import random
import argparse
import Parser
import sys

'''
Classe Queue guarda todos os atributos das filas
] 
'''
class Queue:
    #static_time é um valor statico da classe
    static_time = 0
     
    name = ""
    total_servers = 0
    max_size = 0
    minArrival = 0
    maxArrival = 0
    minService = 0
    maxService = 0
    counter = 0
    buffer = None 
    lost = 0

    def __init__(self, name,t_serv, s_queue, minService, maxService, minArrival = 0, maxArrival = 0):
        self.name = name
        self.total_servers = t_serv
        self.max_size = s_queue
        self.minArrival = minArrival
        self.maxArrival = maxArrival
        self.minService = minService
        self.maxService = maxService
        self.buffer = Hbuffer(self.name,self.max_size, self.counter) 

    def __str__(self):
        return 'name: ' + self.name + '\ncapacity: ' + str(self.max_size) +  '\nsize queue: ' +  str(self.counter)+'\nservers: ' + str(self.total_servers) +'\narrival time: ' + str(self.minArrival) + '-' + str(self.maxArrival) + 's' + '\nservice time: ' +  str(self.minService) + '-' +  str(self.maxService) + 's\n'

    def add_new(self, function, current_time, s_queue = None, order = True):
        self.buffer.add_new(self.name, self.counter, current_time, function,s_queue, order)
'''
Escalonador guarda registro dos eventos até serem executados
'''
class Scheduler:
    s_buffer = []
    str_buffer = []
    
    def schedule(self, queue_source, queue_target, global_time, sort):
        self.s_buffer.append((queue_source, queue_target, float(global_time + sort), float(sort)))
        self.str_buffer.append((queue_source, queue_target, float(global_time + sort), float(sort)))

    def next_action(self):
        min_time = float("inf")
        min_index = -1

        for index in range(len(self.s_buffer)):
            if self.s_buffer[index][2] < min_time:
                min_index = index
                min_time = self.s_buffer[index][2]
        
        try:
            next_action = self.s_buffer[min_index]
            del self.s_buffer[min_index]
            return next_action
        except:
            print("Erro index not found:", min_index)
            return None

    def print_scheduler(self):
        i = 1
        for action in self.str_buffer:
            if action[0] == None and "exit" not in action[1]:
                print("("+str(i)+")entr {0:<15} {1:>6,.4f} {2:>9,.4f}".format(action[1], action[2],action[3]))
                
            elif not "exit" in action[1] and not "exit" in action[0]:
                print("("+str(i)+"){0:<1}-> {1:<15} {2:>6,.4f} {3:>9,.4f}".format(action[0],action[1], action[2],action[3]))
            
            else:
                print("("+str(i)+"){0:<20} {1:>6,.4f} {2:>9,.4f}".format(action[1], action[2],action[3]))
            i+=1
    

'''
Guarda os registros executados de cada fila
'''
class Hbuffer:
    lst_ordem = []

    buff = []
    last_register = ()
    def __init__(self, name, max_size, count):
        self.clean_buffer()
        states = []
        #Se a fila for infinita inicializa com um vetor de apenas 1 posição
        if max_size != float('inf'):
            states = [0] * (max_size + 1)
        else:
            states = [0]

        self.last_register = (name, count, Queue.static_time, states, "-")
        self.buff.append(self.last_register)

    def add_new(self, name, queue_count, current_time, funtion, s_queue, order):

        diff = 0
        # Controle se a fila está execuntando o método tandem
        if order:
            if self.last_register[-1] == '-':
                diff = current_time
            else:    
                diff = current_time - Queue.static_time
            Queue.static_time += diff
        else:
            if self.last_register[-1] == '-':
                diff = current_time
            else:    
                diff = current_time - self.last_register[2]

        new_states =  self.last_register[3][:]
        index_state = self.last_register[1] 
        
        #Se a fila for infinita, aumenta o limite 
        if len(new_states) <= index_state:
            new_states.append(0)

        new_states[index_state] += diff

        description = ""

        #auxiliar de Log
        if funtion == "tandem":
            if order:
                description += name + " -> "+ s_queue
            else:
                description += s_queue + " -> "+ name
        else:
            description += funtion + " " + name

        new_register = (name, queue_count, current_time, new_states, description)
        self.buff.append(new_register)
        self.last_register = new_register

        Hbuffer.lst_ordem.append(description)
    

    def print_Hbuffer(self):
        for i in self.buff:
            print("{0:<35} {1:>6} {2:>9.3f}  [".format(i[4],i[1],i[2]), end="")
            for j in i[3]:
                print(" {0:^6,.3f} ".format(j), end="")
            print("]")
    
    def print_last_register(self):
        i = self.last_register
        print("|| {0:<8}|| {1:<5}|| {2:<12} |".format("Nome","Fila","Tempo"), end="")
        for j in range(len(i[3])):
            print("| {0:^12} |".format("Est."+str(j)), end="")
        print("| {0:<9}||".format("Perdidos"))
        print("|| {0:<8}|| {1:<5}|| {2:<12.3f} |".format(i[0],i[1],i[2]), end="")
        for j in i[3]:
            print("| {0:^12.3f} |".format(j), end="")
        print("|", end= "")

    def return_answer(self):
        return self.last_register

    def last_buff_metric(self):
        l = self.buff[-1]
        return [l[2]] + [i for i in l[3]]
    
    def clean_buffer(self):
        self.buff = []
        self.last_register = ()

'''
Gerador de numeros aleatórios
a = 651
M = 15619
C = 4
'''
class RandomNumbers:
    lst = []
    ast = False

    def __init__(self, seed, size, rand_lst):
        #Pode receber uma lista de aleatórios
        if rand_lst == []:
            self.generate_list(seed, size)
        else:
            self.lst = rand_lst.copy()
            self.ast = True
        
    def generate_list(self, seed, size):
        a = 651
        m = 15619
        c = 4
        for i in range(size):
            seed = ((a*seed) + c) % m
            U = seed/m
            

            self.lst.append(U)
        
    def get_next(self, minArrival, maxArrival, value):
        return float(((maxArrival - minArrival) * value + minArrival))
    
'''
Gera a topologia das filas
'''
class Topology:
    topo = {} #source: list (target, probability)

    def Append(self, source, target, prob):
        if not source in self.topo:
            self.topo[source] = []
        self.topo[source].append( (target, prob) )

    def GetTargets(self, source):
        return self.topo[source]

    #topo[source][]

    def __str__(self):
        output = '### Topology ###\n'
        for source in self.topo:
            output += 'SOURCE: ' + source + '\nTARGETS: '
            
            if source not in self.topo:
                output += 'exit ' + '100% | '
            else:
                sum_prob = 0
                for element in self.topo[source]:
                    target, prob = element
                    sum_prob += prob
                    output += target + ' ' + str(int(prob*100)) + '% | '
                if sum_prob < 1:
                    output += 'exit ' + str(int((1-sum_prob)*100)) + '% | '
            output += '\n'
        return output
'''
Calcula a probabilidade do proximo destino
'''
def GetNextDestiny(source_name, list_queues, random_number):
    accumulator_1 = 0
    accumulator_2 = 0

    for t_queue in list_queues:
        name_queue, probability = t_queue
        accumulator_2 += probability
        if  accumulator_1 <= random_number and random_number < accumulator_2:
            return name_queue

        accumulator_1 += accumulator_2

    return 'exit ' + source_name


'''
Método de entrada Fila
'''
def Entrance(queue, Scheduler, current_time, randoms, topo):
    try:
        if queue.counter < queue.max_size:
            queue.counter += 1
            if queue.counter <= queue.total_servers:                
                random_number = randoms.lst.pop(0)
                
                destiny = GetNextDestiny(queue.name, topo.GetTargets(queue.name), random_number)
                Scheduler.schedule(queue.name, destiny, current_time, randoms.get_next(queue.minService, queue.maxService, random_number))

        else:
            queue.lost += 1
                
        Scheduler.schedule(None , queue.name, current_time,  randoms.get_next(queue.minArrival, queue.maxArrival, randoms.lst.pop(0)))
    except:
        aux = None
        #print("Terminou a lista de aleatórios!")

    queue.add_new("entrance", current_time)

    

'''
Método de Saida da Fila
'''
def Exit(queue, Scheduler, current_time ,randoms, topo):
    try:
        queue.counter-=1
        if queue.counter >= queue.total_servers:
            random_number = randoms.lst.pop(0)
            destiny = GetNextDestiny(queue.name, topo.GetTargets(queue.name), random_number) 
            Scheduler.schedule(queue.name, destiny, current_time, randoms.get_next(queue.minService, queue.maxService, random_number))
    except:
        aux = None
        #print("Terminou a lista de aleatórios!")
    queue.add_new("exit",current_time)


'''
Método de transição entre filas
'''
def Tandem(queue_source, queue_target, Scheduler, current_time, randoms, topo):
    try:
        queue_source.counter -=1

        if queue_source.counter >= queue_source.total_servers:
            random_number = randoms.lst.pop(0)
            destiny = GetNextDestiny(queue_source.name, topo.GetTargets(queue_source.name), random_number)
            Scheduler.schedule(queue_source.name, destiny, current_time,  randoms.get_next(queue_source.minService, queue_source.maxService, random_number))

        if queue_target.counter < queue_target.max_size:
            queue_target.counter += 1
            if queue_target.counter <= queue_target.total_servers:
                random_number = randoms.lst.pop(0)
                destiny = GetNextDestiny(queue_target.name, topo.GetTargets(queue_target.name), random_number)
                Scheduler.schedule(queue_target.name, destiny, current_time, randoms.get_next(queue_target.minService, queue_target.maxService, random_number))
        else:
            queue_target.lost += 1
    except:
        aux = None

    queue_source.add_new("tandem",current_time, queue_target.name, order = True)
    queue_target.add_new("tandem",current_time, queue_source.name, order = False)

'''
Busca por entradas para inicializar a simulação
'''
def search_entrances(queues):
    entrances = []

    for key in queues:
        if queues[key].minArrival > 0:
            entrances.append(queues[key])

    return entrances

'''
Adiciona um "END" na final de todas as filas, ajustando o tempo em todas, quando termina a execução
'''
def last_resgister_buff(queues):
    higher = 0
    high_q = None
    for queue in queues:
        if queues[queue].buffer.last_register[2] > higher:
            higher = queues[queue].buffer.last_register[2]
            high_q = queues[queue]

    for queue in queues:
        if queues[queue] != high_q:
            queues[queue].add_new("END", higher, order= False)
        
'''
Onde ocorre a simulação
'''
def Simulate(initial_time, queues, topo, seed = 0, size = 100000, lst = []):
    scheduler = Scheduler()
    
    randoms = RandomNumbers(seed, size, lst)
    entrances  = search_entrances(queues)
    for entrance in entrances:
        scheduler.schedule(None, entrance.name, initial_time, 0)
    
    while(len(randoms.lst) > 0):   
        n_action = scheduler.next_action()
        time = n_action[2]


        if n_action[0] == None and "exit" not in n_action[1]:
            Entrance(queues[n_action[1]], scheduler, time, randoms, topo)
            
        elif not "exit" in n_action[1] and not "exit" in n_action[0]:
            Tandem(queues[n_action[0]], queues[n_action[1]], scheduler, time, randoms, topo)
        
        else:
            Exit(queues[n_action[0]], scheduler, time, randoms, topo)

    last_resgister_buff(queues)
    total_perdidos = 0
    for key in queues:
        #queues[key].buffer.print_Hbuffer()
        queues[key].buffer.print_last_register()
        total_perdidos += queues[key].lost
        print(" {0:^9}||\n".format(queues[key].lost))

    print(f"Total de processos perdidos: {total_perdidos}")
    #scheduler.print_scheduler()

if len(sys.argv) <= 1:
    print("ERROR!!!!! Precisa-se de argumento")
    quit()

arg = sys.argv[1]

randoms = []
queues = {}
topology = Topology()
seed = 0
initial_time = 0
queues_parsed, topo_parsed, seed, initial_time, randoms = Parser.Parse(arg)


############# FIZ AQUI UM PARSER QUE LE O INPUT.TXT E INSTANCIA AS FILAS E A TOPOLOGIA ##################

## name,t_serv, s_queue, minService, maxService, minArrival = 0, maxArrival = 0
for queue in queues_parsed:
    name = queue["name"]
    t_serv = int(queue["servers"])
    s_queue = int(queue["capacity"]) if "capacity" in queue else float('inf')
    minService = float(queue["minService"])
    maxService = float(queue["maxService"])

    
    if "minArrival" not in queue:
        queues[name] = Queue(name, t_serv, s_queue, minService, maxService)
    else:
        minArrival = float(queue["minArrival"])
        maxArrival = float(queue["maxArrival"])
        queues[name] = Queue(name, t_serv, s_queue, minService, maxService, minArrival, maxArrival)

for topo in topo_parsed:
    #for topo in element:
    
    topology.Append(topo["source"], topo["target"], float(topo["probability"]))     

for i in queues:
    print(queues[i])

print(topology)

for key in queues:
    if key not in topology.topo.keys():
        topology.Append(key, key, 0)


Simulate(initial_time, queues, topology, seed = seed, lst = randoms)


'''
n_queue = int(input("Numero de Filas:\n"))
serv = 0
cap = 0
minArr = 0
maxArr = 0
minServ = 0
maxServ = 0

for i in range(n_queue):
    print(f'Fila {i+1}:')
    serv = int(input("Numero de Servidores: "))
    cap = int(input("Capacidade: "))
    minServ = float(input("Min Serviço: "))
    minServ = float(input("Max Serviço: "))
    if i == 0:
        print("Como é a primeira fila:")
        minArr = float(input("Min Chegada: "))
        minArr = float(input("Max Chegada: "))
    queues["Q"+str(i+1)] = Queue("Q"+str(i+1),serv,cap,minServ, maxServ, minArr, maxArr)
    minArr = 0
    maxArr = 0
q_1 = ""
q_2 = ""
perc = 0
x = ""
control = True

if n_queue > 1:
    while(control):
        print("\nTopologia(Digite Apenas o numeros)")
        q_1 = input("De qual Fila Sai?\n")
        q_2 = input("Pra qual Fila entra?\n")
        perc = float(input("Qual a probabilidade?(numero entre 0 e 1)\n"))
        x = input("Terminou a Topologia!(reponder y ou n)\n")
        if x.upper() == "Y":
            control = False
        topology.Append(queues["Q"+q_1].name, queues["Q"+q_2].name, perc)

for q in queues:
     topology.Append(queues[q].name, "", 0)


seed = int(input("Qual a seed: "))

int_time = float(input("Tempo inicial para chegada: "))

Simulate(int_time, queues, topology, seed = seed)   
'''     

# queues["Ticket"] = Queue('Ticket', 4, 2, 2, 5, 3, 4)
# queues["Student Service"] = Queue('Student Service', 3, 1, 5, 7)
# queues["Finance"] = Queue('Finance', 3, 1, 2, 3)


# topology = Topology()
# topology.Append(queues["Ticket"].name, queues["Student Service"].name, 0.8)
# topology.Append(queues["Student Service"].name, queues["Finance"].name, 0.5)
# topology.Append(queues["Finance"].name, queues["Student Service"].name, 0.3)

# Simulate(2.0, queues, topology)

