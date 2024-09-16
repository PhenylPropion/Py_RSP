from syouhai import Syouhai
from dashite import Dashite
from fight_result import FightResult
import janken_interface


class Fight:

    def __init__(self, fightResult):
        self.fightResult = fightResult

    def user1syoubu(self, user1Dashite, user2Dashite):
        if user1Dashite == user2Dashite:
            return Syouhai.AIKO

        if (user1Dashite == Dashite.PA and user2Dashite == Dashite.GU) or \
           (user1Dashite == Dashite.GU and user2Dashite == Dashite.CYOKI) or \
           (user1Dashite == Dashite.CYOKI and user2Dashite == Dashite.PA):
            return Syouhai.KACHI
        else:
            return Syouhai.MAKE

    def fight(self, user1LogicClass, user2LogicClass, syoubuKaisuu):
        #try:
            # CHECK IF logic is of type janken interface??

             # TODO differentiate which player logic throws an execption

        user1Logic = user1LogicClass()
        user2Logic = user2LogicClass()

        user1Logic.init(syoubuKaisuu)
        user2Logic.init(syoubuKaisuu)

        user1Kachisuu = 0
        user2Kachisuu = 0

        for i in range(0, syoubuKaisuu):
            user1Dashite = user1Logic.jankenpon()
            user2Dashite = user2Logic.jankenpon()

            user1kekka = self.user1syoubu(user1Dashite, user2Dashite)
            user2kekka = self.user1syoubu(user2Dashite, user1Dashite)

            user1Logic.kekka(user1kekka)
            user2Logic.kekka(user2kekka)

            if user1kekka == Syouhai.KACHI:
                user1Kachisuu += 1
            elif user2kekka == Syouhai.KACHI:
                user2Kachisuu += 1


            #print(user1kekka)

        draw = syoubuKaisuu - user1Kachisuu - user2Kachisuu

        self.fightResult.result(user1Kachisuu, user2Kachisuu, draw)

        return self.fightResult

        #except:
            #print("error while fighting")
        



