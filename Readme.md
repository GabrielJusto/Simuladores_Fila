Simulador realizado pelos alunos da Escola Politécnica da Pontifícia Universidade Católica do Rio Grande do Sul:
Gabriel Bonatto Justo
Gabriel Pereira Paiz
Victor Scherer Putrich

Turma: 128

* Compilação: python3 filasTandem.py input_file.txt 

* Vídeo de Explicação: https://www.youtube.com/watch?v=yfislhBn-NQ

* Resumo Exemplo Criado: Modelo de um posto de gasolina com 4 filas: Bomba, Lavagem, Pneu, Loja.
	
	-Bomba: Para que um cliente entre no posto e use todos os serviços disponíveis é necessário que abasteça em uma das 3 bombas, com tempo de chagada de 1-3 minutos e tempo de serviço de 1-3 minutos e fila de tamanho infinita. Apos ser atendindo, o cliente tem 20% de probabilidade de ir para a fila de Lavagem, 50% de ir para a Loja e 30% para encher os seu Pneu.
	
	-Lavagem: A capacidade da fila de lavagem tem tamanho 3 com apenas 1 servidor e tempo de atendimento entre 10 a 20 minutos. Da lavagem existe 30% de chance de ir a fila Pneu e 70% Loja.
	
	-Pneu: A fila pneu tem capacidade máxima 3 com 1 servidor e tempo de atendimento entre 5 a 7 minutos. Pode ir tanto para a Lavagem com 15% ou para a loja com 85%.
	
	-Loja: Na Loja existe uma capacidade máxima de 7 clientes com 3 servidores disponíveis e um tempo de serviço entre 5 a 15 minutos. O único destino para a loja é a saída.
	
* Formato de Entrada do Simulador:

Exemplo Input.txt
	
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
 


