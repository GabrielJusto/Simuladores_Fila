import random
import argparse

LOST = 0

'''
   o ---->  o===== 1 ----> o======2
                     '
                     '---> saída

FUNÇÃO 1
queue_1.counter -= 1
    if queue_1.counter >= queue_1.total_servers:
        if Sort((0,1)) >= psbl_events['SA1']: <---- saída
            scheduler.schedule('SA1')
        else:
            scheduler.scheduler('P12') <--- próxima entrada
    
                      --> saída (10%)
                     '
                     '
    o ---->  o===== 1 ----> o======== 2 (80%)
                     '
                     '-->   o======= 3 (10%)
                     

FUNÇÃO 2
queue_1.counter -= 1
    if queue_1.counter >= queue_1.total_servers:
        if Sort((0,1)) >= psbl_events['P12']: <---- entrada 1
            scheduler.schedule('SA1')
        elsif Sort((0,1)) >= psbl_events['P13']::
            scheduler.scheduler('P12') <--- entrada 2
        else:
            scheduler.scheduler('SA1') <--- saída

Q1:{(Q2, 0, 10), (Q3, 11,20),  20:Q3, 0:OUT}

 Q1 {(q2, 10%), () .. }--> 0 - 10
 Q1 (q3, 10%) --> 10 - 20
 Q1 (out, 80%) --> 20 - 100

 z > q2 > y > q3 > x > out
numero = 0.01
enquanto( element : dicionário)
    numero >= element.prob():
        return
'''

class Queue:
    #static
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

    def add_new(self, function, current_time, target = None):
        self.buffer.add_new(self.name, self.counter, current_time, function, target)

class Scheduler:
    s_buffer = []
    
    def schedule(self, queue_source, queue_target, global_time, sort):
        #print("new event:", (event_desc, float(global_time + sort), float(sort)))
        self.s_buffer.append((queue_source, queue_target, float(global_time + sort), float(sort)))
        
        #print(self.s_buffer[len(self.s_buffer)-1])

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
    
    def __str__(self):
        output = ''
        for i in self.s_buffer:
            output += str(i) + '\n'
        return output

'''
class Event:
    description =  ""
    min_time = 0
    max_time = 0
    prob_higher_then = 0

    def __init__(self, desc, min_t, max_t, p_h_t):
        self.description = desc
        self.min_time = min_t
        self.max_time = max_t
        self.prob_higher_then = p_h_t
    
    def probability(self):
        return self.prob_higher_then

    def range(self):
        return (self.min_time, self.max_time)
'''

class Hbuffer:
    buff = []
    last_register = ()
    def __init__(self, name, max_size, count):
        self.clean_buffer()
        states = [0] * (max_size + 1)
        self.last_register = (name, count, Queue.static_time, states, "-")
        self.buff.append(self.last_register)

    def add_new(self, name, queue_count, current_time, funtion, target):
        #print(event + ' queue count ', queue_count)
        print(funtion, target)
        print(Queue.static_time, type(Queue.static_time))
        Queue.static_time += (current_time) - Queue.static_time
        print(self.last_register)

        new_states =  self.last_register[3][:]
        print(new_states, type(new_states))

        print("\n")
        new_states[self.last_register[1]] = Queue.static_time

        description = ""

        if funtion == "tandem":
            description += name + " -> "+ target
        else:
            description += funtion + " " + name

        new_register = (name, queue_count, current_time, new_states, description)
        self.buff.append(new_register)
        self.last_register = new_register


    def print_Hbuffer(self):
        for i in self.buff:
            print("{0:^8} {1:>6} {2:>9,.3f}  [".format(i[4],i[1],i[2]), end="")
        #print(i[0] + " " + str(i[1]) + " " + str( round(i[2], 3) ), end = "")
            for j in i[3]:
                print(" {0:^6,.3f} ".format(j), end="")
            print("]")
    
    def return_answer(self):
        return self.last_register

    def last_buff_metric(self):
        l = self.buff[-1]
        return [l[2]] + [i for i in l[3]]
    
    def clean_buffer(self):
        self.buff = []
        self.last_register = ()


class RandomNumbers:
    lst = []
    def __init__(self, seed, size ,lst):
        if lst == None:
            self.generate_list(seed, size)
        else:
            self.lst = lst
        
    def generate_list(self, seed, size):
        a = 651
        m = 15619
        c = 4
        for i in range(size):
            seed = ((a*seed) + c) % m
            U = seed/m
            

            self.lst.append(U)
        
    def get_next(self, minArrival, maxArrival):
        return float(((maxArrival - minArrival) * self.lst.pop(0) + minArrival))

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
        
def GetNextDestiny(source_name, list_queues, randoms):
    random_number = randoms.get_next(0, 1)
    accumulator_1 = 0
    accumulator_2 = 0

    for t_queue in list_queues:
        name_queue, probability = t_queue
        accumulator_2 += probability
        if  accumulator_1 <= random_number and random_number < accumulator_2:
            return name_queue

        accumulator_1 += accumulator_2

    return 'exit ' + source_name


# def entrance(queue, events, scheduler, current_time, h_buffer, randoms):
#     #h_buffer.add_new('ENTRANCE', queue.counter, current_time)
#     global LOST
#     try:
#         if queue.counter < queue.max_size:
#             queue.counter += 1
#             if queue.counter <= queue.total_servers:
#                 event = events['EXIT']
#                 scheduler.schedule(event.description , current_time, randoms.get_next(event.range()))
#         else:
#             LOST += 1
#         event = events['ENTRANCE']
#         scheduler.schedule(event.description, current_time, randoms.get_next(event.range()))
#         h_buffer.add_new('ENTRANCE', queue.counter, current_time)
#     except:
#         print("Acabaram os números aleatórios, fim da execução!")

# ###Adicionei Esse método
# def tandem(queue_1, queue_2, events, scheduler, current_time, h_buffer, randoms):
#     global DIC
#     queue_1.counter-=1
#     if queue_1.counter >= queue_1.total_servers:
#         if randoms.get_next(event.range()) < DIC[(queue_1,queue_2)]:
#             event = events["TANDEM"]
#             scheduler.schedule(event.description, current_time, randoms.get_next(event.range()))
#         else:
#             event = events["EXIT"]
#             scheduler.schedule(event.description, current_time, randoms.get_next(event.range()))


#     if queue_2.counter < queue_2.max_size:
#         queue_2.counter += 1
#         if queue_2.counter <= queue_2.total_servers:
#             event = events['EXIT']
#             scheduler.schedule(event.description , current_time, randoms.get_next(event.range()))
#     else:
#         LOST += 1

#      h_buffer.add_new('TANDEM', queue_2.counter, current_time)
    
    
# ### Não alterei Para 
# def out(queue, events, scheduler, current_time, h_buffer, randoms):
#     #h_buffer.add_new('EXIT', queue.counter, current_time)

#     queue.counter-=1
#     if queue.counter >= queue.total_servers:
#         event = events['EXIT']
#         scheduler.schedule(event.description, current_time, randoms.get_next(event.range()))
    
#     h_buffer.add_new('EXIT', queue.counter, current_time)

def Entrance(queue, Scheduler, current_time, randoms, topo):

    try:
        if queue.counter < queue.max_size:
            queue.counter += 1
            if queue.counter <= queue.total_servers:
                destiny = GetNextDestiny(queue.name, topo.GetTargets(queue.name), randoms)
                Scheduler.schedule(queue.name, destiny, current_time, randoms.get_next(queue.minService, queue.maxService))
        Scheduler.schedule(None , queue.name, current_time,  randoms.get_next(queue.minArrival, queue.maxArrival))
                
        queue.add_new("entrance", current_time)
    except:
        print("Terminou a lista de aleatórios!")

    


def Exit(queue, Scheduler, current_time ,randoms, topo):
    try:
        queue.counter-=1
        if queue.counter >= queue.total_servers:
            destiny = GetNextDestiny(queue.name, topo.GetTargets(queue.name), randoms) 
            Scheduler.schedule(queue.name, destiny, current_time,  randoms.get_next(queue.minService, queue.maxService))

        queue.add_new("exit",current_time)
    except:
        print("Terminou a lista de aleatórios!")

def Tandem(queue_source, queue_target, Scheduler, current_time, randoms, topo):
    try:
        queue_source.counter -=1

        if queue_source.counter >= queue_source.total_servers:
            destiny = GetNextDestiny(queue_source.name, topo.GetTargets(queue_source.name), randoms)
            Scheduler.schedule(queue_source.name, destiny, current_time,  randoms.get_next(queue_source.minService, queue_source.maxService))
        
        if queue_target.counter < queue_target.max_size:
            queue_target.counter += 1
            if queue_target.counter <= queue_target.total_servers:
                destiny = GetNextDestiny(queue_target.name, topo.GetTargets(queue_target.name), randoms)
                Scheduler.schedule(queue_target.name, destiny, current_time,  randoms.get_next(queue_target.minService, queue_target.maxService))

        queue_source.add_new("tandem",current_time, queue_target.name)
    except:
        print("Terminou os Aleatórios!")

    #entrada
    #Saida
    #Q1 -> Q2

def search_entrances(queues):
    entrances = []

    for key in queues:
        if queues[key].minArrival > 0:
            entrances.append(queues[key])

    return entrances


def Simulate(initial_time, queues, topo, seed = 0, size = 100, lst = None, prt = False):

    scheduler = Scheduler()
    
    #h_buffer = Hbuffer('-', queue, 0)
    
    randoms = RandomNumbers(seed, size, lst)
    entrances  = search_entrances(queues)
    for entrance in entrances:
        scheduler.schedule(None, entrance.name, initial_time, 0)
    while(len(randoms.lst) > 0):
        n_action = scheduler.next_action()
        time = n_action[2]
        #if tempo > tempo_lim: 
        #    break

        if n_action[0] == None and "exit" not in n_action[1]:
            Entrance(queues[n_action[1]], scheduler, time, randoms, topo)
            
        elif not "exit" in n_action[1] and not "exit" in n_action[0]:
            Tandem(queues[n_action[0]], queues[n_action[1]], scheduler, time, randoms, topo)
        
        else:
            Exit(queues[n_action[0]], scheduler, time, randoms, topo)

    for key in queues:
        queues[key].buffer.print_Hbuffer()
        print("\n")

    if prt:
        h_buffer.print_Hbuffer()

    #return h_buffer.last_buff_metric()
    


queues = {}

queues["Ticket"] = Queue('Ticket', 4, 2, 2, 5, 3, 4)
queues["Student Service"] = Queue('Student Service', 3, 1, 5, 7)
queues["Finance"] = Queue('Finance', 3, 1, 2, 3)


topology = Topology()
topology.Append(queues["Ticket"].name, queues["Student Service"].name, 0.8)
topology.Append(queues["Student Service"].name, queues["Finance"].name, 0.5)
topology.Append(queues["Finance"].name, queues["Student Service"].name, 0.3)

Simulate(2.0, queues, topology)

#random.seed(10)
'''
parser = argparse.ArgumentParser(description = "Simulador Simples Primeira Entrega")

parser.add_argument('-arrived', type=str, required = True, help = "O intervalo de tempo para a chegada de clientes na fila. Recebe dois inteiros separados por ','.EX.: 1,2;")
parser.add_argument('-service', type=str, required = True, help = "o intervalo de tempo de atendimento de um cliente na fila. Recebe dois inteiros separados por ','.EX.: 1,2;")
parser.add_argument('-servers', type=int, required = True, help = "Quantidade de servidores;")
parser.add_argument('-capacity', type=int, required = True, help = "Capacidade da fila;")
parser.add_argument('-initial', type=int, required = True, help = "Tempo de chegada do primeiro na fila;")
parser.add_argument('-exec_times', type=int, required = True, help = "Quantidade de vezes que irá executar com diferente seeds;")
parser.add_argument('-seed', type=int, required = False, help = "A semente geradora dos números aleatórios;")
parser.add_argument('-size', type=int, required = False, help = "Quantidade de numeros aleatórios gerados;")
parser.add_argument('-list', type=str, required = False, help = "Lista pré-setada de numeros aleatórios;")
parser.add_argument('-print', help = "Mostrar tabela interia de execução.", action="store_true")



args = parser.parse_args()

arrived = args.arrived.split(",")
service = args.service.split(",")

lst = None
if args.list is not None:
    lst = [float(i) for i in args.list.split(",")]

seed = 56
if args.seed is not None:
    seed = args.seed

size = 100
if args.size is not None:
    size = args.size

psbl_events = {}
psbl_events['ENTRANCE'] = Event('ENTRANCE', float(arrived[0]), float(arrived[1]), 0)
psbl_events['EXIT'] = Event('EXIT', float(service[0]), float(service[1]), 0)

queue = Queue(args.servers, args.capacity)
initial_time = args.initial


l = [0] * (queue.max_size+2)
avg_LOST = 0
# print("{0:^4} {1:<4} {2:^14}".format("I", "Seed", "Time"), end = "")
# for i in range(queue.max_size+1):
#     print("{0:^14}".format(i), end = "")
# print("Lost")
for i in range(args.exec_times):
    queue = Queue(args.servers, args.capacity)
    last_buff = simulate(initial_time, queue, psbl_events, seed, size, lst, args.print)
    #print("{0:^4} {1:<4}".format(str(i)+"º",seed), end="")
    for j in range(len(last_buff)):
        l[j] = last_buff[j] + l[j]
        #print("{0:^14.5f}".format(last_buff[j]), end="")  
    #print("  "+str(LOST), end="")
    print(f"Lost: {LOST}")
    avg_LOST +=LOST 
    LOST = 0
    seed = seed + (random.randint((-1)*seed, 100))

    print("")

print("\nAverage:")
print("{0:^8} {1:^14}".format("Lost", "Time"), end = "")
for i in range(len(l)-1):
    print("{0:^14}".format(i), end = "")
print("\n{0:^8} {1:^14.5f}".format(avg_LOST/args.exec_times, l[0]/args.exec_times), end = "")
for i in range(1,len(l)):
    print("{0:^14.5f}".format(l[i]/args.exec_times), end = "")
'''
