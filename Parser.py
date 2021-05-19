'''
 ## INPUT FORMAT ##
-Seed: <Seed>
-Initial_time: <Initial Time>
-Random: <n1> <n2> <n3> <n4> <n5>

-Queues

name: <name_queue>
capacity: <capacity>
minService: <min_service>
maxService: <max_service>
minArrival: <min_arrival>
maxArrival: <max_arrival>


name: <name_queue2>
capacity: <capacity>
minService: <min_service>
maxService: <max_service>
minArrival: <min_arrival>
maxArrival: <max_arrival>
...

-Topology

source: <name_queue>
target:  <name_queue>
probability: <prob>

source: <name_queue>
target:  <name_queue2>
probability: <prob>

source: <name_queue>
target:  <name_queue3>
probability: <prob>
...

'''


import os.path
def Parse(arg):
    filename = arg



    if not os.path.isfile(filename):
        print('File does not exist.')
    else:

        #queue order: name, number services, size queue, minService, maxService, minArrival = 0, maxArrival = 0

        is_queue = False
        is_topo = False

        with open(filename) as f:
            content = f.read().splitlines()

        randoms = []
        aux = {}
        queues = []
        topos = []
        seed = 0
        initial_time = 0
        for line in content:
            if not (line and line.strip()):
                continue
            elif "Initial_time" in line:
                line = line.strip('-Initial_time:')
                line = line.strip(' ')
                initial_time = float(line)
            elif "Seed" in line:
                line = line.strip('-Seed:')
                line = line.strip(' ')
                seed = float(line)
            elif "Random" in line:
                line = line.strip('-Random:')
                line = line.strip(' ')
                randoms = [float(i) for i in line.split(" ")]
            elif "Queue" in line:
                is_queue = True
                ia_topo = False
            elif "Topology" in line:
                queues.append(aux)
                aux = {}
                is_queue = False
                is_topo = True

            elif is_queue:
                if "name:" in line:
                    if not aux == {}:
                        queues.append(aux)
                    aux = {}
                    line = line.replace('name:', '')
                    line = line.strip(' ')
                    aux["name"] = line
                elif "capacity" in line:
                    line = line.replace('capacity:', '')
                    line = line.strip(' ')
                    aux["capacity"] = line
                elif "servers" in line:
                    line = line.replace('servers:', '')
                    line = line.strip(' ')
                    aux["servers"] = line
                elif "minService" in line:
                    line = line.replace('minService:', '')
                    line = line.strip(' ')
                    aux["minService"] = line
                elif "maxService" in line:
                    line = line.replace('maxService:', '')
                    line = line.strip(' ')
                    aux["maxService"] = line
                elif "minArrival" in line:
                    line = line.replace('minArrival:', '')
                    line = line.strip(' ')
                    aux["minArrival"] = line
                elif "maxArrival" in line:    
                    line = line.replace('maxArrival:', '')
                    line = line.strip(' ')
                    aux["maxArrival"] = line
                
            elif is_topo:
                if "source" in line:
                    if not aux == {}:
                        topos.append(aux)
                    aux = {}
                    line = line.replace('source:', '')
                    line = line.strip(' ')
                    aux["source"] = line

                elif "target:" in line:
                    line = line.replace('target:', '')
                    line = line.strip(' ')
                    aux["target"] = line
                elif "probability:" in line:
                    line = line.replace('probability:', '')
                    line = line.strip(' ')
                    aux["probability"] = line


        topos.append(aux) #ULTIMO TOPO SAI DO LAÇO

        '''
        for element in queues:
            for key in element:
                if key == 'name':
                    print(key + ' ' + str(element[key]))
                else:
                    print('\t' + str(key) + ' ' + str(element[key]))

        print(topos)
        
        for element in topos:
            for key in element:
                if key == 'source':
                    print(key + ' ' + str(element[key]))
                else:
                    print('\t' + str(key) + ' ' + str(element[key]))
        '''
        return queues, topos, seed, initial_time, randoms
