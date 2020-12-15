import decisionTreeGUI as dt_gui
import decision_tree as dt
from functools import partial

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

"""
ui.pushButton.clicked.connect(partial(convert, ui))
def convert(ui):
    input = ui.lineEdit.text()
    result = float(input) * 6.7
    ui.lineEdit_2.setText(str(result))
"""
# 防止出错直接崩溃
import cgitb
cgitb.enable(format='text')


def pushLoadTreeButton(ui):
    # 按下读取决策树按钮事件
    # 读取tree相关line中值并调用load方法
    # browser中显示决策树信息
    # 提示加载数据
    ui.tipBrowser.append("start loading tree data...")

    tree_file = str(ui.treeFileLine.text())
    columns_file = str(ui.columnsFileLine.text())
    dt_gui.tree, dt_gui.columns = dt.load_tree(tree_file, columns_file)

    # 显示决策树
    tree_content_list = []
    dt.tree_content(dt_gui.tree, dt_gui.columns, tree_content_list)
    ui.treeShow.setText("")  # 先清空
    tree_str = ""
    for l in tree_content_list:
        tree_str += (l + "\n")
    ui.treeShow.setText(tree_str)

    # 提示加载成功
    ui.tipBrowser.append("load tree success")
    print("完成决策树加载")


def pushTrainTreeButton(ui):
    # 按下创建决策树按钮
    # 提示加载数据
    ui.tipBrowser.append("start loading train data...")

    load_tree_file = str(ui.trainTreeLine.text())
    dt_gui.columns, data = dt.load_data(load_tree_file)
    train_columns = dt_gui.columns[:]
    dt_gui.tree = dt.build_tree(data, train_columns)

    # 显示决策树
    tree_content_list = []
    dt.tree_content(dt_gui.tree, dt_gui.columns, tree_content_list)
    ui.treeShow.setText("")  # 先清空
    tree_str = ""
    for l in tree_content_list:
        tree_str += (l + "\n")
    ui.treeShow.setText(tree_str)

    # 提示创建成功
    ui.tipBrowser.append("train tree success")
    print("完成决策树训练")


def pushLoadTestButton(ui):
    # 按下加载训练集地址
    # 提示加载数据
    ui.tipBrowser.append("start loading test data...")

    test_file = str(ui.testLine.text())
    dt_gui.test_matrix = dt.load_test_data(test_file)

    # 显示测试集信息
    test_str = ""
    for test_line in dt_gui.test_matrix:
        test_str += " ".join(test_line) + "\n"
    ui.testShow.setText(test_str)

    # 提示创建成功
    ui.tipBrowser.append("load test success")
    print("完成测试集加载")


def pushClassifyButton(ui):
    # 按下分类按钮
    # 提示开始
    ui.tipBrowser.append("start classifying...")
    if dt_gui.tree is None or dt_gui.columns is None:
        ui.tipBrowser.append("please load tree first")
        return
    # 开始训练
    classify_result = dt.whole_classify(dt_gui.tree, dt_gui.test_matrix, dt_gui.columns)
    # 显示信息
    result_str = ""
    for result_line in classify_result:
        result_str += " ".join(result_line) + "\n"
    ui.classifyShow.setText(result_str)
    # 提示分类成功
    ui.tipBrowser.append("classify success")
    print("完成分类")


def pushSaveButton(ui):
    # 按下存储按钮
    # 提示
    ui.tipBrowser.append("start saving...")
    if dt_gui.tree is None or dt_gui.columns is None:
        ui.tipBrowser.append("please load tree first")
        return
    # 开始存储
    save_file = str(ui.saveTrainLine.text()).strip()
    dt.save_tree(dt_gui.tree, dt_gui.columns, save_file)
    # 成功提示
    ui.tipBrowser.append("save tree success")
    print("存储完成")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = dt_gui.Ui_MainWindow()
    ui.setupUi(MainWindow=MainWindow)

    # 设置加载决策树按钮
    ui.loadTreeButton.clicked.connect(partial(pushLoadTreeButton, ui))
    ui.trainTreeButton.clicked.connect(partial(pushTrainTreeButton, ui))
    ui.testButton.clicked.connect(partial(pushLoadTestButton, ui))
    ui.pushButton.clicked.connect(partial(pushClassifyButton, ui))
    ui.saveTreeButton.clicked.connect(partial(pushSaveButton, ui))

    MainWindow.show()
    sys.exit(app.exec_())





