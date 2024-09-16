from enum import Enum

class ResultType(Enum):
    RESULT_OK = 1
    RESULT_ERROR_SYSTEM = 2
    RESULT_ERROR_EXCEPTION = 3
    RESULT_ERROR_PERMISSION = 4
    RESULT_ERROR_OVERTHINKTIME = 5
    RESULT_ERROR_FILENOTFOUND = 6

class ErrorUser(Enum):
    USER_OWN = 1
    USER_ENEMY = 2
    USER_NONE = 3

class ResultStatus(Enum):
    WON = 1
    LOST = 2
    DRAW = 3
        

class FightResult:
    def __init__(self, user1File, user2File):
        self.user = user1File
        self.enemy = user2File

    def systemError(self, errorUser):
        self.resultType = ResultType.RESULT_ERROR_SYSTEM
        self.errorUser = errorUser
        return self

    def exceptionError(self, errorUser):
        self.resultType = ResultType.RESULT_ERROR_EXCEPTION
        self.errorUser = errorUser
        return self

    def thinkTimeOverError(self, errorUser):
        self.resultType = ResultType.RESULT_ERROR_OVERTHINKTIME
        self.errorUser = errorUser
        return self

    def fileNotFoundError(self, errorUser):
        self.resultType = ResultType.RESULT_ERROR_FILENOTFOUND
        self.errorUser = errorUser
        return self

    def result(self, ownPoint, enemyPoint, draw):
        self.errorUser = ErrorUser.USER_NONE
        self.resultType = ResultType.RESULT_OK
        self.ownPoint = ownPoint
        self.enemyPoint = enemyPoint
        self.draw = draw
        if ownPoint == enemyPoint:
            self.resultStatus = ResultStatus.DRAW
        elif ownPoint > enemyPoint:
            self.resultStatus = ResultStatus.WON
        else: 
            self.resultStatus = ResultStatus.LOST

        return self

    def getEnemyResult(self):
        enemyResult = FightResult(self.enemy, self.user)
        enemyResult.resultType = self.resultType

        if self.errorUser == ErrorUser.USER_NONE:
            enemyResult.errorUser = ErrorUser.USER_NONE
        elif self.errorUser == ErrorUser.USER_OWN:
            enemyResult.errorUser = ErrorUser.USER_ENEMY
        else: 
            enemyResult.errorUser = ErrorUser.USER_OWN
        enemyResult.ownPoint = self.enemyPoint
        enemyResult.enemyPoint = self.ownPoint
        enemyResult.draw = self.draw

        if self.resultStatus == ResultStatus.DRAW:
            enemyResult.resultStatus = ResultStatus.DRAW
        elif self.resultStatus == ResultStatus.WON:
            enemyResult.resultStatus = ResultStatus.LOST
        else:
            enemyResult.resultStatus = ResultStatus.WON

        return enemyResult


    def printInfo(self):
        print("player pt [" + str(self.ownPoint)     + "]")
        print("enemy  pt [" + str(self.enemyPoint)   + "]")
        print("draw   pt [" + str(self.draw)         + "]")
        print("result    [" + str(self.resultStatus) + "]")





