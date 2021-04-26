'''i
PSEUDO ALGORITMOS FILAS

func CHEGADA(fila):
    incrementa fila
    se cliente pode ser atendido:
        destino = sortear(fila.targets)
        agenda destino
    agenda chegada de novo cliente na fila

func SAIDA(fila):
    descrementa fila
    se a fila não tem servidor disponível (>=):
        destino = sortear(fila.targets ++ saída)
        agenda destino

func TANDEM(fila_source, fila_targe):
    decrementa fila_source
    se não tem servidor disponível em fila_source(>=):
        destino = sortear(fila.targets ++ saída)
        agenda destino

    incrementa fila_target
    se fila_target tem servidor disponível
        destino = sortear(fila_target.targets ++ saída)
        agenda destino

'''

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
        print(size)
        for i in range(size):
            seed = ((a*seed) + c) % m
            U = seed/m
            

            self.lst.append(U)
        
        
    def get_next(self, left, right):
        return float(((right - left) * self.lst.pop(0) + left))
   


class Queue:
    name = ""
    servers = 0
    capacity = 0
    minArrival = 0
    maxArrival = 0
    minService = 0
    maxService = 0
    counter = 0 
    
    def __init__(self, name, capacity, servers, minArrival, maxArrival, minService, maxService):
        self.name = name
        self.servers = servers
        self.capacity = capacity
        self.minArrival = minArrival
        self.maxArrival = maxArrival
        self.minService = minService
        self.maxService = maxService

    def __str__(self):
        return 'name: ' + self.name + '\ncapacity: ' + str(self.capacity) + '\nsize queue: ' + str(self.counter)+ '\nservers: ' + str(self.servers) + '\narrival time: ' + str(self.minArrival) + '-' + str(self.maxArrival) + 's' + '\nservice time: ' + str(self.minService) + '-' + str(self.maxService) + 's\n'
        
#estrutura para guardar a topologia das filas, 
#     a saída da fila representa o resto das probabilidades
class Topology:
    topo = {} #source: list (target, probability)

    def Append(self, source, target, prob):
        if not source in self.topo:
            self.topo[source] = []

        self.topo[source].append( (target, prob) )
    def GetTargets(self, source):
        return self.topo[source]

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


class Scheduler:
    s_buffer = []
    
    def schedule(self, queue_source, queue_target, global_time, sort):
        self.s_buffer.append( (queue_source, queue_target, float(global_time + sort), float(sort)))
        
    '''
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
    '''
    def __str__(self):
        output = ''
        for i in self.s_buffer:
            output += str(i) + '\n'
        return output
    
#pega a próxima fila ou saída de acordo com a probabilidade
def GetNextDestiny(source_name, list_queues):
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



#SCHEDULER DEVE TER UM SOURCE E UM TARGET PARA AVALIAR QUAL DAS 3 FUNÇÕES CHAMAR
# se source == None e target == queue -> entrance()
# se source == queue e target == exit -> exit()
# se source == queue e target == queue -> tandem()


def Entrance(queue, Scheduler, randoms, topo):
    current_time = 0 #APAGAR

    if queue.counter <= queue.capacity:
        queue.counter += 1
        if queue.counter >= queue.servers:
            destiny = GetNextDestiny(queue.name, topo.GetTargets(queue.name))
            Scheduler.schedule(queue.name, destiny, current_time, randoms.get_next(queue.minService, queue.maxService))
    Scheduler.schedule(None , queue.name, current_time,  randoms.get_next(queue.minArrival, queue.maxArrival))

def Exit(queue, Scheduler, randoms, topo):
    current_time = 0
    queue.counter-=1
    if queue.counter >= queue.servers:
        destiny = GetNextDestiny(queue.name, topo.GetTargets(queue.name)) 
        Scheduler.schedule(queue.name, destiny, current_time,  randoms.get_next(queue.minService, queue.maxService))

def Tandem(queue_source, queue_target, Scheduler, randoms, topo):
    current_time = 0
    queue_source.counter -=1

    if queue_source.counter <= queue_source.servers:
        destiny = GetNextDestiny(queue_source.name, topo.GetTargets(queue_source.name))
        Scheduler.schedule(queue_source.name, destiny, current_time,  randoms.get_next(queue_source.minService, queue_source.maxService))
        

    queue_target.counter += 1
    if queue_target.counter >= queue_target.servers:
        destiny = GetNextDestiny(queue_target.name, topo.GetTargets(queue_target.name))
        Scheduler.schedule(queue_target.name, destiny, current_time,  randoms.get_next(queue_target.minService, queue_target.maxService))



## how to define a queue ##
# queue:  name, servers, capacity, minArrival, maxArrival, minService, maxService #

ticket = Queue('Ticket', 4, 2, 2, 5, 3, 4)
student_service = Queue('Student Service', 3, 1, 0, 0, 5, 7)
finance = Queue('Finance', 3, 1, 0, 0, 2, 3)

## how to define a topology ##
topology = Topology()
topology.Append(ticket.name, student_service.name, 0.8)
topology.Append(student_service.name, finance.name, 0.5)
topology.Append(finance.name, student_service.name, 0.3)

Scheduler = Scheduler()
randoms = RandomNumbers(40, 40, None)


Entrance(ticket, Scheduler, randoms, topology)
Entrance(ticket, Scheduler, randoms, topology)
Entrance(ticket, Scheduler, randoms, topology)
Entrance(ticket, Scheduler, randoms, topology)
Tandem(ticket, student_service, Scheduler, randoms, topology)
Tandem(ticket, student_service, Scheduler, randoms, topology)
Tandem(ticket, student_service, Scheduler, randoms, topology)
Tandem(ticket, student_service, Scheduler, randoms, topology)
Tandem(ticket, student_service, Scheduler, randoms, topology)
Entrance(ticket, Scheduler, randoms, topology)
Entrance(ticket, Scheduler, randoms, topology)
Entrance(ticket, Scheduler, randoms, topology)
Exit(student_service, Scheduler, randoms, topology)

print(ticket)
print(student_service)


print(Scheduler)