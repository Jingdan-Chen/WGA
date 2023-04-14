import re

def de_comment(my_string)->str:

    # 定义正则表达式
    pattern = r'^(.*?)(?=#)'

    # 使用正则表达式匹配
    match = re.search(pattern, my_string)

    # 获取匹配结果
    if match:
        result = match.group(1)
        return(result)  # 输出 "hello world "
    else:
        return my_string
    
def read_config(filename,value_type=str,name_idx=0,value_idx=1)->dict:
    res = {}
    with open(filename,"r",encoding="utf-8") as f:
        cont = f.readlines()
    for item in cont:
        item = de_comment(item.strip())
        if len(item)==0:
            continue
        for obj in ["=",",","，"]: #judge segment
            if obj in item:
                seg = obj
                break
            seg = " "
        item_ = item.split(seg)
        name = item_[name_idx].strip()
        value = value_type(item_[value_idx]) if value_type!=str else item_[1].strip()
        res[name] = value
    return res

def get_config():
    config = read_config("./config.txt")
    eval_list = ['stu_doit','B_Aclass',"D_only",'lesson_expel','D_Aclass']
    for item in config:
        if item in eval_list:
            config[item] = eval(config[item])
    return config