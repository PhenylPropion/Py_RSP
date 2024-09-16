import abc

class JankenInterface(abc.ABC):
    @abc.abstractmethod
    def init(self, syoubuKaisuu):
        pass

    @abc.abstractmethod
    def jankenpon(self):
        pass

    @abc.abstractmethod
    def kekka(self, syohai):
        pass