import random
import argparse

class Queue:
    total_servers = 0
    max_size = 0
    counter = 0

    def __init__(self, t_serv, s_queue):
        self.total_servers = t_serv
        self.max_size = s_queue
    

class Scheduler:
    s_buffer = []
    
    def schedule(self, event_desc, global_time, sort):
        #print("new event:", (event_desc, float(global_time + sort), float(sort)))
        self.s_buffer.append( (event_desc, float(global_time + sort), float(sort)))
        
        print(self.s_buffer[len(self.s_buffer)-1])

    def next_action(self):
        min_time = float("inf")
        min_index = -1

        for index in range(len(self.s_buffer)):
            if self.s_buffer[index][1] < min_time:
                min_index = index
                min_time = self.s_buffer[index][1]
        
        try:
            next_action = self.s_buffer[min_index]
            del self.s_buffer[min_index]
            return next_action
        except:
            print("Erro index not found:", min_index)
            return None
    

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

class Hbuffer:
    buff = []
    last_register = ()
    def __init__(self, event, queue, initial_time):
        states = [0] * (queue.max_size + 1)
        self.last_register = (event, queue.counter, initial_time, states )
        self.buff.append(self.last_register)

    def add_new(self, event, queue_count, current_time):
        #print(event + ' queue count ', queue_count)
        
        new_states =  self.last_register[3][:]
        new_states[self.last_register[1]]+= (current_time) - self.last_register[2]

        new_register = (event, queue_count, current_time, new_states)
        self.buff.append(new_register)
        self.last_register = new_register

    def print_Hbuffer(self):
        for i in self.buff:
            print("{0:^8} {1:>6} {2:>9,.3f}  [".format(i[0],i[1],i[2]), end="")
        #print(i[0] + " " + str(i[1]) + " " + str( round(i[2], 3) ), end = "")
            for j in i[3]:
                print(" {0:^6,.3f} ".format(j), end="")
            print("]")
    
    def return_answer(self):
        return self.last_register

class RandomNumbers:
    lst = []
    def __init__(self, seed,lst = None):
        if lst == None:
            self.generate_list(seed)
        else:
            self.lst = lst
        


    def generate_list(self, seed, size = 1000):
        a = 651
        m = 15619
        c = 4
        for i in range(size):
            seed = ((a*seed) + c) % m
            U = seed/m
            

            self.lst.append(U)
        

    def get_next(self, range_lim):
        return float(((range_lim[1] - range_lim[0]) * self.lst.pop(0) + range_lim[0]))
        

def entrance(queue, events, scheduler, current_time, h_buffer, randoms):
    #h_buffer.add_new('ENTRANCE', queue.counter, current_time)

    try:
        if queue.counter < queue.max_size:
            queue.counter += 1
            if queue.counter <= queue.total_servers:
                event = events['EXIT']
                scheduler.schedule(event.description , current_time, randoms.get_next(event.range()))
        
        event = events['ENTRANCE']
        scheduler.schedule(event.description, current_time, randoms.get_next(event.range()))
        h_buffer.add_new('ENTRANCE', queue.counter, current_time)
    except:
        print("Acabaram os números aleatórios, fim da execução!")

def out(queue, events, scheduler, current_time, h_buffer, randoms):
    #h_buffer.add_new('EXIT', queue.counter, current_time)

    queue.counter-=1
    if queue.counter >= queue.total_servers:
        event = events['EXIT']
        scheduler.schedule(event.description, current_time, randoms.get_next(event.range()))
    
    h_buffer.add_new('EXIT', queue.counter, current_time)

def simulate(initial_time, queue, events, seed, lst = None):
    
    scheduler = Scheduler()
    
    h_buffer = Hbuffer('-', queue, 0)
    
    event = events['ENTRANCE']
    randoms = RandomNumbers(seed, lst)
    
    scheduler.schedule( event.description, initial_time, 0)
    
    while(len(randoms.lst) > 0):
        n_action = scheduler.next_action()
        time = n_action[1]
        #if tempo > tempo_lim: 
        #    break

        if n_action[0] == 'ENTRANCE':
            entrance(queue, events, scheduler, time, h_buffer, randoms)
            
        elif n_action[0] == 'EXIT':
            out(queue, events, scheduler, time, h_buffer, randoms)

    h_buffer.print_Hbuffer()
    


'''
def ch_1(queue_1, scheduler, current_time):
    
    last_register = h_buffer

    if queue_1.counter < queue_1.max_size:
        queue_1.counter+=1
        if queue_1.counter <= queue_1.total_servers:
            if Sort((0, 1)) >= psbl_events['SA1'].probability():
                scheduler.schedule('SA1')
            else:
                scheduler.schedule('P12')
        
    scheduler.schedule('CH1')

def  sa_1(queue_1, scheduler, current_time):
    queue_1.counter -= 1
    if queue_1.counter >= queue_1.total_servers:
        if Sort((0,1)) >= psbl_events['SA1']:
            scheduler.schedule('SA1')
        else:
            scheduler.scheduler('P12')

def p_1_2(queue_1, queue_2, scheduler, current_time):

    queue_1.counter -= 1
    if queue_1.counter >= queue_1.max_size:
        if Sort((0,1)) >= psbl_events['SA1'].probability():
            scheduler.schedule('SA1')
        else:
            scheduler.schedule('P12')
    queue_2.counter += 1

    if queue_2.counter <= queue_2.total_servers:
        scheduler.scheduler('SA2')

def sa_2(queue_2, scheduler, current_time):
    queue_2.counter -= 1
    if queue_2.counter >= queue_2.total_servers:
        scheduler.schedule('SA2')

'''

#random.seed(10)

parser = argparse.ArgumentParser(description = "Simulador Simples Primeira Entrega")

parser.add_argument('-arrived', type=str, required = True, help = "O intervalo de tempo para a chegada de clientes na fila. Recebe dois inteiros separados por ','.EX.: 1,2;")
parser.add_argument('-service', type=str, required = True, help = "o intervalo de tempo de atendimento de um cliente na fila. Recebe dois inteiros separados por ','.EX.: 1,2;")
parser.add_argument('-servers', type=int, required = True, help = "Quantidade de servidores;")
parser.add_argument('-capacity', type=int, required = True, help = "Capacidade da fila;")
parser.add_argument('-seed', type=int, required = False, help = "A semente geradora dos números aleatórios;")
parser.add_argument('-initial', type=int, required = True, help = "Tempo de chegada do primeiro na fila;")
parser.add_argument('-list', type=str, required = False, help = "Lista pré-setada de numeros aleatórios.")


args = parser.parse_args()

arrived = args.arrived.split(",")
service = args.service.split(",")

lst = None
if args.list is not None:
    lst = [float(i) for i in args.list.split(",")]

seed = 56
if args.seed is not None:
    seed = args.seed

psbl_events = {}
psbl_events['ENTRANCE'] = Event('ENTRANCE', float(arrived[0]), float(arrived[1]), 0)
psbl_events['EXIT'] = Event('EXIT', float(service[0]), float(service[1]), 0)

queue = Queue(args.servers, args.capacity)

initial_time = args.initial
simulate(initial_time, queue, psbl_events, seed, lst)
#simulate(initial_time, queue, limit_counter, psbl_events)
#[0.3276, 0.8851, 0.1643, 0.5542, 0.6813, 0.7221, 0.9881]
