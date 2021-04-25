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


class Queue:
    name = ""
    servers = 0
    minArrival = 0
    maxArrival = 0
    minService = 0
    maxService = 0
    
    def Queue(name, servers, minArrival, maxArrival, minService, maxService):
        self.name = name
        self.servers = servers
        self.minArrival = minArrival
        self.maxArrival = maxArrival
        self.minService = minService
        self.maxService = maxService

#estrutura para guardar a topologia das filas, 
#     a saída da fila representa o resto das probabilidades
class Topology:
    topo = {} #source: list (target, probability)

    def AppendSource(source, target, prob):
        if not source in topo:
            topo[source] = []

        topo[source].append( (targe, prob) )
    def GetTargets(source):
        return topo[source]

#pega a próxima fila ou saída de acordo com a probabilidade
def GetNextDestiny(source_name, list_queues):
    random_number = sort(0,1)
    accumulator_1 = 0
    accumulator_2 = 0

    for t_queue in list_queues:
        name_queue, probability = t_queue
        accumulator_2 += probability

        if  accumulator_1 <= random_number < accumulator_2:
            return name_queue

        accumulator_1 += accumulator_2

    return 'exit ' + source_name

#SCHEDULER DEVE TER UM SOURCE E UM TARGET PARA AVALIAR QUAL DAS 3 FUNÇÕES CHAMAR
# se source == None e target == queue -> entrance()
# se source == queue e target == exit -> exit()
# se source == queue e target == queue -> tandem()

def Entrance(queue):
    if queue.counter <= queue.capacity:
        queue.counter += 1
        if queue.counter >= queue.servers:
            destiny = GetNextDestiny(queue.name, topo.GetTargets(queue.name))
            Scheduler.schedule(queue.name, destiny, current_time, sort(queue.minService, queue.maxService))
    Scheduler.schedule(None , queue.name, current_time, sort(queue.minArrival, queue.maxArrival))

def Exit(queue):
    queue.counter-=1
    if queue.counter >= queue.servers:
        destiny = GetNextDestiny(queue.name, topo.GetTargets(queue.name)) 
        Scheduler.schedule(queue.name, destiny, current_time, sort(queue.minService, queue.maxService))

def Tandem(queue_source, queue_target)
    queue_source.counter -=1

    if queue_source.counter <= queue_source.servers:
        destiny = GetNextDestiny(queue_source.name, topo.GetTargets(queue_source.name))
        Scheduler.schedule(queue_source.name, destiny, current_time, sort(queue_source.minService, queue_source.maxService))
        

    queue_target.counter += 1
    if queue_target.counter >= queue_target.servers
        destiny = GetNextDestiny(queue_target.name, topo.GetTargets(queue_target.name))
        Scheduler.schedule(queue_target.name, destiny, current_time, sort(queue_target.minService, queue_target.maxService))
