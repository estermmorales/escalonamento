import threading
import matplotlib.pyplot as plt
import pandas as pd


# Classe que representa o processo
class Processo:

    def __init__(self, id, chegada, cpu, prioridade):
        self.id = id
        self.chegada = chegada
        self.cpu = cpu
        self.prioridade = prioridade

    def get_cpu(self):
        return self.cpu
    
    def get_chegada(self):
        return self.chegada

    def get_prioridade(self):
      return self.prioridade
    
    def get_id(self):
        return self.id
    
# Classe que representa a fila de aptos
class FilaAptos:

    listaProcessos = []

    def __init__(self):
        pass

    def insere_processo(self, processo):
        self.listaProcessos.append(processo)

    def mostra_dados_processo(self, posicao):
        print(f'Identificacao: {self.listaProcessos[posicao].get_id()}')
        print(f'Chegada......: {self.listaProcessos[posicao].get_chegada()}')
        print(f'CPU..........: {self.listaProcessos[posicao].get_cpu()}')
        print(f'Prioridade...: {self.listaProcessos[posicao].get_prioridade()}\n')

    def get_proximo_processo(self):
        return self.listaProcessos.pop(0)

    def mostra_processos_lista(self):
        for i in range(len(self.listaProcessos)):
            self.mostra_dados_processo(i)

    def tamanho_lista(self):
        return len(self.listaProcessos)

    def ordenar_por_cpu(self):
        self.listaProcessos = sorted(self.listaProcessos, key=lambda Processo:Processo.cpu)
    
    def ordenar_por_prioridade(self):
        self.listaProcessos = sorted(self.listaProcessos, key=lambda Processo:Processo.prioridade)

# Thread algoritmo FCFS
class threadFCFS(threading.Thread):

    tempo_relogio = 0
    media = 0.0

    def __init__(self, fila_aptos):
        self.fila_aptos = fila_aptos
        threading.Thread.__init__(self)

    def escalonar(self):
        qtd_processos = self.fila_aptos.tamanho_lista()
        
        for i in range(qtd_processos):
            proc = self.fila_aptos.get_proximo_processo()
            self.tempo_relogio += proc.get_cpu()

        self.media = (self.tempo_relogio - proc.get_cpu()) / qtd_processos

        media = (self.tempo_relogio - proc.get_cpu()) / qtd_processos
        return media

    def run(self):
        print('Algoritmo FCFS')
        self.media = self.escalonar()
        medias.append(self.media)
        print(f'Media de espera: {self.media:.2f}')

# Thread algoritmo SJF (SHORTEST JOB FIRST)
class threadSJF(threading.Thread):

    tempo_relogio = 0
    media = 0.0

    def __init__(self, fila_aptos):
        self.fila_aptos = fila_aptos
        threading.Thread.__init__(self)

    def escalonar(self):
        self.fila_aptos.ordenar_por_cpu()
        qtd_processos = self.fila_aptos.tamanho_lista()
        
        for i in range(qtd_processos):
            proc = self.fila_aptos.get_proximo_processo()
            self.tempo_relogio += proc.get_cpu()

        self.media = (self.tempo_relogio - proc.get_cpu()) / qtd_processos

        media = (self.tempo_relogio - proc.get_cpu()) / qtd_processos
        return media

    def run(self):
        print('\nAlgoritmo SJF')
        self.media = self.escalonar()
        medias.append(self.media)
        print(f'Media de espera: {self.media:.2f}')

# Thread algoritmo baseado em PRIORIDADE
class threadPrioridade(threading.Thread):

    tempo_relogio = 0
    media = 0.0

    def __init__(self, fila_aptos):
        self.fila_aptos = fila_aptos
        threading.Thread.__init__(self)

    def escalonar(self):
        self.fila_aptos.ordenar_por_prioridade()
        qtd_processos = self.fila_aptos.tamanho_lista()
        
        for i in range(qtd_processos):
            proc = self.fila_aptos.get_proximo_processo()
            self.tempo_relogio += proc.get_cpu()

        media = (self.tempo_relogio - proc.get_cpu()) / qtd_processos
        return media

    def run(self):
        print('\nAlgoritmo baseado em PRIORIDADE')
        self.media = self.escalonar()
        medias.append(self.media)
        print(f'Media de espera: {self.media:.2f}')

# Funcao principal
def main():

    global medias
    medias = []

    lista_processos = []

    processos = pd.read_csv('processo.csv')
    
    for i in range(len(processos.index)):
      #                                         Id                 Chegada              CPU                 Prioridade
      lista_processos.append(Processo(processos.iloc[i][0], processos.iloc[i][1], processos.iloc[i][2], processos.iloc[i][3]))
      
    f_aptos = FilaAptos()
    for i in lista_processos:
      f_aptos.insere_processo(i)
    
    f_aptos.mostra_processos_lista()

    fcfs = threadFCFS(f_aptos)
    fcfs.start()
    fcfs.join()

    f_aptos = FilaAptos()
    for i in lista_processos:
      f_aptos.insere_processo(i)
    
    sjf = threadSJF(f_aptos)
    sjf.start()
    sjf.join()

    f_aptos = FilaAptos()
    for i in lista_processos:
      f_aptos.insere_processo(i)

    prioridade = threadPrioridade(f_aptos)
    prioridade.start()
    prioridade.join()

    faixa = [medias[0], medias[1], medias[2]]
    algoritmos = ['FCFS', 'SJF', 'Prioridade']
    plt.bar(algoritmos, faixa, color="red")
    plt.show()

    main()