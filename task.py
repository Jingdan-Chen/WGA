from infoReadin import *
from configReadin import *
import joblib
import os

config = get_config()
conf_dir = config["config_dir"]
baoy_files = {"化学":read_lesson_dem(conf_dir+"保研化学.txt"),
              "应用化学":read_lesson_dem(conf_dir+"保研应化.txt"),
              "应用化学(化学生物学)":read_lesson_dem(conf_dir+"保研化生.txt")}
data_path = config["rawdata_dir"]+config["filename"]
assert config["task_idx"] in "01234"
task_id = int(config["task_idx"])
basename = config["filename"].split(".")[0]

cache_path = config["cache_dir"]+f"{basename}.joblib"

if os.path.isfile(cache_path) and config["use_cache"]=="1":
    all_dict = joblib.load(cache_path)
else:
    all_dict = readin(data_path,config)
    joblib.dump(all_dict, cache_path)

def output_single(filename,record,mod=None):
    with open(filename,"w",encoding="ANSI") as f:
        f.write("课程,学分,成绩,绩点,学分绩\n")
        rec_list = mod if mod else record.keys()
        for item in rec_list:
            temp = record.get(item)
            credit = str(mod[item]) if mod!=None else record[item].credit
            Gcredit = record[item].Gcredit if temp!=None else None
            cregra = record[item].cregra if temp!=None else None
            score = record[item].score if temp!=None else None
            f.write(f"{item},{credit},{score},{Gcredit},{cregra}\n")
    
def output_baoy(filename,res_dict):
    f = open(filename,"w")
    f.close()
    with open(filename,"a",encoding="ANSI") as f:
        f.write("学号,姓名,专业,保研绩点,备注\n")
        for item in res_dict:
            id = item
            name = res_dict[id][0]
            major = res_dict[id][1]
            temp = res_dict[id][2]
            res = temp[0]
            record = temp[1]
            num_aqu = len(baoy_files[major])
            note = f"应修{num_aqu};实修{len(record)}" if len(record)<num_aqu else ""
            output_single(f"personal/{name}.csv",{i.name:i for i in record},
                               mod=baoy_files[major])
            f.write(f"{id},{name},{major},{res},{note}\n")
    return

def output_ADE(filename,res_dict):
    f = open(filename,"w")
    f.close()
    with open(filename,"a",encoding="ANSI") as f:
        f.write("学号,姓名,专业,GPA\n")
        for item in res_dict:
            id = item
            name = res_dict[id][0]
            major = res_dict[id][1]
            temp = res_dict[id][2]
            res = temp[0]
            record = temp[1]

            output_single(f"personal/{name}.csv",{i.name:i for i in record})
            f.write(f"{id},{name},{major},{res}\n")
    return

def output_C(filename,res_dict):
    f = open(filename,"w")
    f.close()
    with open(filename,"a",encoding="ANSI") as f:
        temp0 = list(res_dict.values())[0][2]
        temp1 = [key for key in temp0]
        title = "学号,姓名,专业,"+",".join(temp1)
        f.write(title+"\n")
        for item in res_dict:
            id = item
            name = res_dict[id][0]
            major = res_dict[id][1]
            message = f"{id},{name},{major},"

            temp2 = [str(res_dict[id][2][key]) for key in res_dict[id][2]]
            message = message+",".join(temp2)+"\n"

            f.write(message)
    return res_dict

def taskB(filename="result.csv"):
    res_dict = {i:[all_dict[i].name,all_dict[i].major,all_dict[i].calculate(
        1,demand=baoy_files[all_dict[i].major],
        A_lis=config["B_Aclass"])] for i in all_dict}
    output_baoy(filename,res_dict)

def taskA(filename="result.csv"):
    res_dict = {i:[all_dict[i].name,all_dict[i].major,all_dict[i].calculate(0)] for i in all_dict}
    output_ADE(filename,res_dict)

def taskE(filename="result.csv"):
    res_dict = {i:[all_dict[i].name,all_dict[i].major,all_dict[i].calculate(4)] for i in all_dict}
    output_ADE(filename,res_dict)

def taskD(filename="result.csv"):
    res_dict = {i:[all_dict[i].name,all_dict[i].major,all_dict[i].calculate(
        3,demand=config["D_only"],
        A_lis=config["D_Aclass"])] for i in all_dict}
    output_ADE(filename,res_dict)

def  taskC(filename="result.csv"):
    demand_list = ["C_condition_line","C_zx_line","C_condition_keybm","C_condition_keyxz",
                   "C_condition_keyname","C_zb_line","C_zb_name"]
    res_dict = {i:[all_dict[i].name,all_dict[i].major,all_dict[i].calculate(
        2,demand=[config[j] for j in demand_list],major=all_dict[i].major)] for i in all_dict}
    return output_C(filename,res_dict)
    