import sys
import importlib
from fight import Fight
from fight_result import FightResult, ResultStatus, ErrorUser

DIRECTORY_NAME = "challenger"
SYOUBU_KAISUU = 10000

print("------------------------")
print("player is [" + sys.argv[1] + "]") # prints user1
print("enemy  is [" + sys.argv[2] + "]") # prints user2

userFile = sys.argv[1]
enemyFile = sys.argv[2]

user1Logic = importlib.import_module("."+userFile, package=DIRECTORY_NAME)

user2Logic = importlib.import_module("."+enemyFile, package=DIRECTORY_NAME)

thisFight = Fight(FightResult(userFile, enemyFile)) #dependency injection
    #print("user1 is ", userFile)
    #print("enemy is ", enemyFile)
fightResult = thisFight.fight(user1Logic.Logic, user2Logic.Logic, SYOUBU_KAISUU)

fightResult.printInfo()