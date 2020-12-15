# id3_decisiontree
Simple id3 decision tree program.GUI base on pyqt5.</br>
基于id3算法的决策树实现，图形界面利用pyqt5实现。</br>

# 使用介绍
程序入口为main_program.py。</br>
使用前首先读入或生成决策树，即左侧大框中需要有决策树示意。</br>

读取决策树需要两个文件，决策树文件和属性文件，
示例里为sex_tree.txt与columns_sex_tree.txt与columns_sex_txt
在左上角填入文件名后点击读取决策树。</br>

生成决策树需要在训练决策树栏中填写训练文件名，示例中为train.txt。</br>
测试集在示例中为test.txt，点击读取测试集后，若已经读取或生成过决策树，直接点击分类进行分类测试。</br>

存储决策树输入文件名后生成一个该文件名的文件和一个columns_前缀的文件，用于下次读取决策树。</br>
![image](https://github.com/huiluczP/id3_decisiontree/blob/master/sample.png)
