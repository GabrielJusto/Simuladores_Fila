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
    total_servers = 0
    max_size = 0
    counter = 0

    def __init__(self, t_serv, s_queue, topo_desc):
        self.total_servers = t_serv
        self.max_size = s_queue
        self.topo = self.create_topo(topo_desc)        
    
    def print_queue(self):
        print('total servers: ' + str(self.total_servers), end = '\n')
        print('maximum size: ' + str(self.max_size), end = '\n')
        print('queue topology: ', end = '')
        print(self.topo)



class Network:
    dic = {}
    


def entrance(queue,)




def entrance():
    
    number = random_number()
    
    for next_place in queue.topo:
        left_lim, right_lim = queue.topo[next_place]
        if left_lim  <= numero and numero > right_lim:
            #fazer algo aqui com next_place

    # key: descricao valor: fila

q1 = Queue(2,4)
q2 = Queue(1,5)

q.print_queue()

dic = {}
dic[(q1,q2)] = 0.7






'''
            --0.2--> O=== 3 --> Saida3
            '
            '
  O=== 1 --0.4--> O==== 2 --> Saida2
           '
           '
           '-> saida1

QUEUE
    fila1: atributos 
    fila2: atributos

NETWORK:
    fila1 : (fila2, 0.4)
    fila1 : (fila3, 0.4)

'''