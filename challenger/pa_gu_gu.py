from dashite import Dashite
import syouhai
import janken_interface

class Logic(janken_interface.JankenInterface):

    def init(self, syoubuKaisuu):
        self.i = 0


    def jankenpon(self):
        case = self.i % 3

        if case == 0:
            return Dashite.PA

        if case ==1:
            return Dashite.GU

        if case == 2:
            return Dashite.GU


    def kekka(self, syohai):
        self.i += 1