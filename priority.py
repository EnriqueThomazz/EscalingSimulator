from escalation import Escalation

class Priority(Escalation):
    def pick(self):
        if self.readyLine == []:
            return
        chosen = self.readyLine[0]
        for process in self.readyLine:
            #Menor prioridade é o com mais prioridade
            if process.priority < chosen.priority:
                chosen = process

        self.readyLine.remove(chosen)
        self.execLine.append(chosen)


    def start(self):
        #Enquanto existirem processos a serem admitidos, em execucao, prontos ou em espera
        while self.processes != [] or self.execLine != [] or self.readyLine != [] or self.waitingLine != []:
        
            #Admitindo novos processos
            for process in self.processes:
                if process.admTime == self.currTime:
                    if process.state == "IO":
                        self.waitingLine.append(process)
                    else:
                        self.readyLine.append(process)

            for process in self.readyLine:
                if process in self.processes:
                    self.processes.remove(process)
            for process in self.waitingLine:
                if process in self.processes:
                    self.processes.remove(process)


            #Se nao houver processo em execucao, entao escolhe um da fila de prontos
            if self.execLine == []:
                self.pick()


            #Escrevendo no arquivo de saida
            if self.opt == "S":
                if self.execLine != [] and self.execLine[0] != self.previousProcess:
                    self.previousProcess = self.execLine[0]
                    self.writeProcesses()
            else:
                self.writeProcesses()

   
            #Se há um processo em execucao
            if self.execLine != []:                
                #Executando o processo em Execucao
                self.execLine[0].exec()
                #Se o processo terminou a execucao
                if self.execLine[0].state == "TERMINATED":
                    self.execLine.pop(0)                 

            
            #Atualizando os processos na fila de espera
            for process in self.waitingLine:
                #Se ele ainda tiver IO pra fazer
                if process.state == "IO":
                    process.exec()
                #Se ele ja tiver concluido o IO, move pra fila de prontos
                if process.state == "CPU":
                    self.readyLine.append(process)
            for process in self.readyLine:
                if process in self.waitingLine:
                    self.waitingLine.remove(process)

            #Tirando os processos que estao fazendo IO da fila de prontos e colocando em espera
            for process in self.readyLine:
                if process.state == "IO":
                    self.waitingLine.append(process)
            for process in self.waitingLine:
                if process in self.readyLine:
                    self.readyLine.remove(process)


            #Se o processo em execucao estiver em IO entao move ele pra lista de espera
            if self.execLine != []:
                if self.execLine[0].state == "IO":
                        self.waitingLine.append(self.execLine[0])
                        self.execLine.pop(0)


            self.currTime += 1

        self.writeProcesses()


opt = str(input("Voce gostaria de um resultado simplificado(S) ou completo(C)? ")).upper()
Priority("entrada.txt", "saida.txt", opt)