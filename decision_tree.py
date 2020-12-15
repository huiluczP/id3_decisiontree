"""
实现id3算法决策树
包括读取，存储等
"""
import math
import pickle


def label_sort(element):
    # 设置排序方法
    return element[1]


def load_data(save_path):
    # 读取训练集信息，包括第一行的属性和数据矩阵
    # 由于id3都为离散，所以全部用字符串读取
    matrix = []
    try:
        sf = open(save_path, "r+")
        lines = sf.readlines()
        for line in lines:
            line = line.strip()
            simple_line_list = line.split(" ")
            matrix.append(simple_line_list)
    except IOError:
        print("读取训练文件失败")
    columns = matrix[0]
    data = matrix[1:]
    return columns, data


def load_test_data(save_path):
    # 读取待分类信息
    matrix = []
    try:
        sf = open(save_path, "r+")
        lines = sf.readlines()
        for line in lines:
            line = line.strip()
            simple_line_list = line.split(" ")
            matrix.append(simple_line_list)
    except IOError:
        print("读取测试文件失败")
    return matrix


def divide_set(data, column, value):
    # 根据属性切割数据行，切除目标属性，保留value相同行
    # 由于id3，只考虑离散数据
    data_after = []
    for d in data:
        if d[column] == value:
            left = d[0:column]
            right = d[column+1:]
            data_after.append(left + right)
    return data_after


def cal_entropy(data):
    # 计算熵，评价决策质量
    label_num = {}
    for d in data:
        label = d[-1]  # 分类在最后一列
        label_num.setdefault(label, 0)
        label_num[label] += 1
    entropy = 0
    for k in label_num:
        p = label_num[k] / len(data)
        e = - p * math.log(p, 2)
        entropy += e
    return entropy


def choose_divide_column(data):
    # 根据熵，计算最好的切分属性，返回属性序号
    max_change_entropy = 0
    column = 0
    former_entropy = cal_entropy(data)
    for i in range(len(data[0]) - 1):  # 最后一列为分类
        value_set = set([d[i] for d in data])
        e = 0
        for value in value_set:
            #  对每个值进行处理，计算熵总值
            data_after = divide_set(data, i, value)
            e += cal_entropy(data_after) * (len(data_after) / len(data))
        change_entropy = former_entropy - e
        if change_entropy > max_change_entropy:
            max_change_entropy = change_entropy
            column = i
    return column


def decide_label(data):
    # 当所有属性都完事后还是有不同分类，则按照最多的分类结果来
    label_num = {}
    for d in data:
        label = d[-1]  # 分类在最后一列
        label_num.setdefault(label, 0)
        label_num[label] += 1

    # (label，num)组合
    label_and_num = zip([k for k in label_num], [label_num[k] for k in label_num])
    label_num_list = [element for element in label_and_num]
    label_num_list.sort(key=label_sort)
    return label_num_list[-1][0]


def build_tree(data, columns):
    # 创建决策树，columns为属性名称，方便可视化
    label_list = [d[-1] for d in data]
    if label_list.count(label_list[0]) == len(label_list):
        # 全部为同一分类，停止
        return label_list[0]
    if len(data[0]) == 1:
        return decide_label(data)
    # 获取决策标签
    column = choose_divide_column(data)
    column_name = columns[column]
    tree = {column_name: {}}
    del(columns[column])
    # 对每个值做一次决策
    values = [d[column] for d in data]
    for v in values:
        columns_after = columns[:]
        data_after = divide_set(data, column, v)
        tree[column_name][v] = build_tree(data_after, columns_after)
    return tree


def print_tree(tree, columns, content=""):
    # 根据结构，简单输出决策树，content为前方缩进
    for k in tree:
        if k in columns:
            print(content + "column:" + str(k), end="")
            content += "      "
        else:
            print(content + str(k), end="")
        if str(type(tree[k])) == str(type({})):
            print()
            print_tree(tree[k], columns, content+"   ")
        else:
            print(" " + str(tree[k]))


def tree_content(tree, columns, tree_list, content=""):
    # 根据结构，简单输出决策树，content为前方缩进
    for k in tree:
        simple_tree_line = ""
        if k in columns:
            simple_tree_line += content + "column:" + str(k)
            content += "      "
        else:
            simple_tree_line += content + str(k)
        if str(type(tree[k])) == str(type({})):
            tree_list.append(simple_tree_line)
            tree_content(tree[k], columns, tree_list, content+"   ")
        else:
            simple_tree_line += " " + str(tree[k])
            tree_list.append(simple_tree_line)
    return tree_list


def classify(tree, input_data, columns):
    # 利用决策树分类
    column = list(dict(tree).keys())[0]
    column_index = columns.index(column)
    for k in tree[column]:
        # 找到相同值分支
        if k == input_data[column_index]:
            if str(type(tree[column][k])) == str(type({})):
                return classify(tree[column][k], input_data, columns)
            else:
                # 为分类结果，递归结束
                return tree[column][k]


def whole_classify(tree, matrix, columns):
    # 矩阵测试集分类，返回原数据+分类信息
    result_matrix = []
    for m in matrix:
        result = classify(tree, m, columns)
        simple_m = list(m[:])
        simple_m.append(result)
        result_matrix.append(simple_m)
    return result_matrix


def save_tree(tree, columns, save_name):
    # 存储决策树训练结果, 同时存储同前缀名的属性名信息
    fw = open(save_name, 'wb+')
    pickle.dump(tree, fw)
    fw.close()
    print("{} is saved".format(save_name))
    fw = open("columns_" + save_name, 'wb+')
    pickle.dump(columns, fw)
    fw.close()
    print("{} is saved".format("columns_" + save_name))


def load_tree(save_path, columns_save_path):
    # 读取tree信息和属性名信息
    fw = open(save_path, "rb+")
    tree = pickle.load(fw)
    fwc = open(columns_save_path, "rb+")
    columns = pickle.load(fwc)
    return tree, columns


if __name__ == "__main__":
    """
    t_columns, t_data = load_data("train.txt")
    whole_columns = t_columns[:]
    t_tree = build_tree(t_data, t_columns)
    print(t_tree)
    print_tree(t_tree, whole_columns, content="")
    save_tree(t_tree, whole_columns, "tree.txt")
    """
    t_tree, t_columns = load_tree("tree.txt", "columns_tree.txt")
    print(t_tree)
    print(t_columns)
    t_test = load_test_data("test.txt")
    print(t_test)
    c_result = whole_classify(t_tree, t_test, t_columns)
    print(c_result)




