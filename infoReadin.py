import pandas as pd
from copy import deepcopy

def read_lesson_dem(path): # read lesson demands
    res_dict = dict()
    with open(path,"r",encoding="utf-8") as f:
        cont = f.readlines()
    for item in cont:
        name = item.strip("\n").split()[0]
        credit = int(item.split()[1])
        res_dict[name] = credit
    return res_dict

def judge_condition(obj):
    res=None
    assert type(obj)==list
    cont = obj[0]
    if type(obj[1]) in {set,list,tuple}:
        res= True if cont in obj[1] else False
    else:
        res= True if cont in {obj[1]} else False
    return res


def help1(obj): # correct worksheet["成绩"]
    try:
        return float(obj)
    except:
        return 0.
    
class record:
    def __init__(self,row):
        self.name = row["课程名称"]
        self.score = row["成绩"]
        self.scoreMark = row["成绩备注"]
        self.credit = row["学分"]
        self.Gcredit = row["绩点"]
        self.teacher = row["任课教师"]
        self.lectureCode = row["课程代码"]
        self.classCode = row["教学班"]
        self.lessonMark = row["课程标记"]
        self.lessonNat = row["课程性质"]
        self.cregra = row["学分绩点"]
        self.testNat = row["考试性质"]
        self._class = row["学生类别"]
        self.major = row["专业"]
        self.year = row["学年"]
        self.kkxy = row["开课学院"]


        # add all attributes to the find_dict dictionary
        self.find_dict = {
            "学分":self.credit,
            "课程名称": self.name,
            "成绩": self.score,
            "成绩备注": self.scoreMark,
            "绩点": self.Gcredit,
            "任课教师": self.teacher,
            "课程代码": self.lectureCode,
            "教学班": self.classCode,
            "课程标记": self.lessonMark,
            "课程性质": self.lessonNat,
            "学分绩点": self.cregra,
            "考试性质": self.testNat,
            "学生类别": self._class,
            "专业": self.major,
            "学年": self.year,
            "开课学院": self.kkxy
        }

    def find_label(self, string):
        return self.find_dict.get(string)

class student:
    def __init__(self,row):
        self.id = row["学号"]
        self.name = row["姓名"]
        self.classno = row["班级"]
        self.grade = row["年级"]
        self.major = row["专业"]
        self._class = row["学生类别"]
        self.gender = row["性别"]
        self.record = dict()

    def add_record(self,row_obj):
        self.record[row_obj.name] = row_obj
        return

    def __str__(self):
        return f"学号:{self.id},姓名:{self.name},专业:{self.major},年级:{self.grade},记录课程数:{len(self.record)}"

    def calculate(self,taskid,demand=None,A_lis=None,major=None):
        collection = []
        if taskid==0:
            sum_cre = 0
            sum_valscore = 0
            for item in self.record.values():
                sum_cre += item.credit
                sum_valscore += item.credit*item.Gcredit
                collection.append(item)
            return sum_valscore/sum_cre,collection
        elif taskid==1:
            assert demand!=None and A_lis!=None
            sum_cre = 0
            sum_valscore = 0

            for item in self.record.values():
                if item.name in demand.keys():
                    frag=1.25 if [item.name,item.teacher] in A_lis else 1.0
                    sum_cre += demand[item.name]
                    sum_valscore += demand[item.name]*item.Gcredit*frag
                    temp = deepcopy(item)
                    temp.Gcredit = temp.Gcredit * frag
                    temp.cregra = temp.cregra * frag
                    collection.append(temp)
            return sum_valscore/sum_cre,collection
        
        elif taskid==2:
            # demand_list = ["C_condition_line","C_zx_line","C_condition_keybm","C_condition_keyxz",
            #        "C_condition_keyname"]
            assert type(demand)==list and major!=None
            condition_line = demand[0]
            [condition_keybm,condition_keyxz,condition_keyname] = demand[2:5]
            if major=="应用化学(化学生物学)":
                condition_line["专选"] = demand[1][1]
                condition_line["专必"] = demand[5][2] 
                condition_keyname["专必"] = demand[6][2]
            elif major=="应用化学":
                condition_line["专选"] = demand[1][0]
                condition_line["专必"] = demand[5][1] 
                condition_keyname["专必"] = demand[6][1]
            elif major=="化学":
                condition_line["专选"] = demand[1][0]
                condition_line["专必"] = demand[5][0] 
                condition_keyname["专必"] = demand[6][0]
            else:
                condition_line["专选"] = 0
                condition_line["专必"] = []
                condition_keyname["专必"] = []


            condition_dict = {"开课学院":condition_keybm,"课程性质":condition_keyxz,
                              "课程名称":condition_keyname}
            sum_demand = {key:0 for key in condition_line}

            def judge_belong(obj,lis):
                if type(obj)!=str:
                    return False
                for item in lis:
                    if item in obj:
                        return True
                return False
            
            for item in self.record.values():
                for cri in condition_dict:
                    for label in condition_dict[cri]:
                        # print(cri,item.find_label(cri),condition_dict[cri],label)
                        if judge_belong(item.find_label(cri),condition_dict[cri][label]) and item.score>=60:
                            sum_demand[label] += item.credit
            
            res_dict = {key:"" for key in condition_line}
            for key in res_dict:
                if sum_demand[key] < float(condition_line[key]):
                    res_dict[key] = f"应修{condition_line[key]}学分;实修{sum_demand[key]}学分"
            return res_dict
        
        elif taskid==3:
            assert demand!=None and A_lis!=None
            sum_compcre = 0
            sum_compvalscore = 0
            sum_optcre = 0
            sum_optvalscore = 0

            for item in self.record.values():
                if [demand[0],item.find_label(demand[0])] == demand:
                    if "必修" in item.find_label("课程性质"):
                        frag=1.25 if [item.name,item.teacher] in A_lis else 1.0
                        sum_compcre += item.credit
                        sum_compvalscore += item.credit*(60+(item.score-60)*frag)
                    else:
                        sum_optcre += item.credit
                        sum_optvalscore += item.credit*(item.score*0.002)
                    collection.append(item)
            temp = sum_compvalscore/sum_compcre if sum_compcre!=0 else 0
            return temp+sum_optvalscore,collection
        
        elif taskid==4:
            sum_cre = 0
            sum_valscore = 0
            for item in self.record.values():
                sum_cre += item.credit
                sum_valscore += item.credit*item.score
                collection.append(item)
            return sum_valscore/sum_cre,collection
        

    def print_self(self):
        print(self)
        pass

def judge_condition(obj):
    res=None
    assert type(obj)==list
    cont = obj[0]
    if type(obj[1]) in {set,list,tuple}:
        res= True if cont in obj[1] else False
    else:
        res= True if cont in {obj[1]} else False
    return res

def check_row(row_obj,config):
    for item in config["lesson_expel"]:
        temp = deepcopy(item)
        key = temp[0]

        temp[0] = row_obj.find_label(key)
        

        if judge_condition(temp):
            return False
        else:
            continue
        
    for item in config["stu_doit"]:
        temp = deepcopy(item)
        key = temp[0]
        temp[0] = row_obj.find_label(key)

        if judge_condition(temp):
            continue
        else:
            return False
    return True
        

def readin(filepath,config):
    worksheet = pd.read_excel(filepath)
    # type correction
    worksheet["学号"] = worksheet["学号"].apply(str)
    worksheet["成绩"] = worksheet["成绩"].apply(help1)
    worksheet["课程代码"] = worksheet["课程代码"].apply(str)

    # strip()
    for col in worksheet.columns:
        if worksheet[col].dtype == "object":
            try:
                worksheet[col] = worksheet[col].apply(lambda a:a.strip())
            except:
                pass

    res_dict = dict()
    for idx in range(worksheet.shape[0]):
        row = worksheet.loc[idx]
        row_stu = row["学号"]
        row_obj = record(row)
        if not check_row(row_obj,config):
            continue
        if row_stu not in res_dict:
            res_dict[row_stu] = student(row)
        res_dict[row_stu].add_record(row_obj)
    return res_dict


