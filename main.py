print("Initializing program")
from infoReadin import *
from configReadin import *
from task import *

if __name__ == '__main__':
    print("Analyzing!")
    config = get_config()
    task_idx = int(config["task_idx"])
    task_func_lis = [taskA,taskB,taskC,taskD,taskE]

    task_func_lis[task_idx](filename=config["resname"])

    print("Finish!")