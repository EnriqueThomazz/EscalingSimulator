
class Process():
    def __init__(self, pid, admTime, name, priority, bursts):
        self.admTime = admTime
        self.name = name
        self.priority = priority
        self.bursts = bursts

        self.pid = pid

        self.state = "CPU"


    def getRemainingTime(self, override=False):
        remTime = 0   

        index = 0
        #Se quiser saber o tempo restante de CPU
        if not override:
            if self.state == "IO":
                index = 1
        #Se quiser saber o tempo restante de IO ele deixa como 0

        for c in range(index, self.bursts.__len__(), 2):
            remTime += self.bursts[c]

        return remTime
        

    def getRemainingIOTime(self):
        return self.getRemainingTime(True)

    def exec(self):
        #Reduz em 1 ciclo o que quer q seja q ele esteja fazendo
        self.bursts[0] -= 1

        # Atualiza o estado do processo
        if self.bursts[0] == 0:
            self.bursts.pop(0)

            if self.bursts == []:
                self.state = "TERMINATED"

            elif self.state == "CPU":
                self.state = "IO"

            else:
                self.state = "CPU"
        
        

