# coding=UTF-8
"""
代码查重，专用于数据结构机试，修改代码路径即可
"""
import os
import sys
import ssdeep

reload(sys)
sys.setdefaultencoding("utf-8")


class StudentItem:
    def __init__(self):
        self.id = 0
        self.item = 0
        self.num = 0
        self.hash = ""


def get_hash(path):
    f = open(path, 'r')
    lines = [l.strip() for l in f.readlines()]
    codes = ""
    for line in lines:
        codes += line
    return ssdeep.hash(codes)


def compare(path1, path2):
    hash1 = get_hash(path1)
    hash2 = get_hash(path2)
    return ssdeep.compare(hash1, hash2)


def get_stuid_item_num(mpath):
    path = os.path.basename(mpath).lower().replace(".cpp", "").replace(".c", "")
    items = path.split("_")
    stuid, item, num = (items[0], items[1], items[2])
    return int(stuid), int(item), int(num)


if __name__ == '__main__':
    # 代码的路径
    mpath = "/Users/sundiz/Desktop/1618011"
    # 判决门限，指代码的相似度，默认是80%就算是抄袭
    gate = 80
    mpaths = os.listdir(mpath)
    paths = [mpath + "/" + p for p in mpaths]
    stu_items = []
    for path in paths:
        stu_item = StudentItem()
        stuid, item, num = get_stuid_item_num(path)
        stu_item.id = stuid
        stu_item.item = item
        stu_item.num = num
        is_duplicate = False
        is_exist = False
        for m_stu_item in stu_items:
            if m_stu_item.id == stu_item.id and m_stu_item.item == stu_item.item:
                is_exist = True

            if m_stu_item.id == stu_item.id and m_stu_item.item == stu_item.item and m_stu_item.num > stu_item.num:
                is_duplicate = True
        if not is_exist:
            stu_item.hash = get_hash(path)
            stu_items.append(stu_item)
        else:
            stu_item.hash = get_hash(path)
            stu_items[len(stu_items) - 1] = stu_item

    # for stu_item in stu_items:
    #     print stu_item.id,stu_item.item
    # 作弊列表，每一项都包括了两个作弊者的学号和题目编号
    cheat_list = []
    for stu_item1 in stu_items:
        for stu_item2 in stu_items:
            if stu_item1.id != stu_item2.id and stu_item1.item == stu_item2.item and ssdeep.compare(stu_item1.hash, stu_item2.hash) > gate:
                cheat_list.append((stu_item1.id, stu_item2.id, stu_item1.item))
    # for cheat in cheat_list:
    #     print cheat
    # 整理后的作弊列表，每一项包括了作弊者的学号，作弊题目总数，所有作弊题目
    cheat_list2 = []
    for cheat1 in cheat_list:
        if cheat_list2 != [] and cheat1[0] == cheat_list2[len(cheat_list2) - 1][0]:
            num = cheat1[1]
            temp = list(cheat_list2[len(cheat_list2) - 1])
            if temp[len(temp) - 1] == cheat1[2]:
                continue
            temp[1] += 1
            temp.append(cheat1[2])
            cheat_list2.remove(cheat_list2[len(cheat_list2) - 1])
            cheat_list2.append(tuple(temp))
            continue
        else:
            cheat_list2.append((cheat1[0], 1, cheat1[2]))
    for cheat in cheat_list2:
        print cheat
