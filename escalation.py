from process import Process

class Escalation():
    
    def __init__(self, in_file, out_file, opt):
        self.execLine = []
        self.readyLine = []
        self.waitingLine = []

        self.currTime = 0

        self.currPid = 0

        self.processes = self.load(in_file)
        self.out_file = out_file

        #Atributos para a escrita em arquivo
        self.previousProcess = None
        self.opt = opt
        #Limpando o arquivo
        archive = open(out_file, "w")
        archive.close()

        self.start()


    def load(self, in_file):
        processes = []

        loadFile = open(in_file, "r")

        line = loadFile.readline()
        while(line != ''):
            line = line.split()
            admTime = int(line[0])
            name = line[1]
            priority = int(line[2])

            bursts = []
            for c in range(3, line.__len__()):
                bursts.append(int(line[c]))

            new = Process(self.currPid, admTime, name, priority, bursts)
            
            if bursts.__len__() % 2 == 0:
                new.state = "IO"

            processes.append(new)

            self.currPid += 1
            line = loadFile.readline()

        loadFile.close()

        return processes


    def writeProcesses(self):
        outFile = open(self.out_file, "a")

        outFile.write("Tempo Corrente: " + str(self.currTime) + "\n")

        if self.execLine != []:
            execTxt = "Processo em Execucao - PID: {}, Nome: {}, Prioridade: {}, Tempo Restante: {}\n"
            outFile.write(execTxt.format(self.execLine[0].pid, self.execLine[0].name, self.execLine[0].priority, self.execLine[0].getRemainingTime()))

        outFile.write("Fila de Prontos\n")

        readyTxt = "PID: {}, Nome: {}, Tempo Admissao: {}, Prioridade: {}\n"
        for process in self.readyLine:
            outFile.write(readyTxt.format(process.pid, process.name, process.admTime, process.priority))


        outFile.write("Fila de Espera\n")

        waitingTxt = "PID: {}, Nome: {}, Tempo Admissao: {}, Prioridade: {}, Tempo Restante IO: {}\n"
        for process in self.waitingLine:
            outFile.write(waitingTxt.format(process.pid, process.name, process.admTime, process.priority, process.getRemainingIOTime()))

        outFile.write("_"*100 + "\n")

        outFile.close()

    
    def pick(self):
        pass


    def start(self):
        pass