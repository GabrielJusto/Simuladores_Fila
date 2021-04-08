Simulador realizado pelos alunos da Escola Politécnica da Pontifícia Universidade Católica do Rio Grande do Sul:
Gabriel Bonatto Justo
Gabriel Pereira Paiz
Victor Scherer Putrich

Turma: 128

run: python.exe filasTandem.py 'comandos'
Ex: python.exe filaTandem.py -arrived 2,4 -service 3,5 -servers 2 -exec_times 5 -capacity 5 -initial 3 -seed 63 -size 10 -print

Comandos:
-h -> Help, tudo isso está escrito lá;
-arrived -> O intervalo de tempo para a chegada de clientes na fila. Recebe dois inteiros separados por ','.EX.: 1,2;
-service -> O intervalo de tempo de atendimento de um cliente na fila. Recebe dois inteiros separados por ','.EX.: 1,2;
-servers -> Quantidade de servidores;
-capacity -> Capacidade da fila;
-initial -> Tempo de chegada do primeiro na fila;
-exec_times -> Quantidade de vezes que irá executar com diferente seeds;
-seed -> A semente geradora dos números aleatórios;
-size -> Quantidade de numeros aleatórios gerados;
-list -> Lista pré-setada de numeros aleatórios;
-print -> Mostrar tabela interia de execução.

-seed, -size e -list não são obrigatórios