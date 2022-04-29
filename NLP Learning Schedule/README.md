![IEC](https://github.com/coder-yuzhiwei/iechub/blob/main/source/banner.jpg)



# IEC实验室自然语言处理学习大纲

本学习大纲为IEC实验室自然语言处理组的学习资料，学习时间为`5月1日-6月20日`，主要包括机器学习、自然语言处理、深度学习框架课程，NLP的实践任务以及最终的学习评测任务。

### 关于学习

- 请大家在[飞书文档](https://docs.feishu.cn/docs)的IEC共享文件夹内建立自己的目录，更新自己的学习进度。
- 【实践任务】需要在本大纲[实践任务](#NLP任务实践)发布的三个任务，或者[课程](#深度学习入门)中选择一项NLP任务进行实践，并将实践过程记录在飞书文档中。深度学习框架不限，推荐PyTorch或Paddle。
- 【学习评测任务】需要参加学习评测任务，至少提交一次自己的结果。

### 关于学习评测

学习评测在[CCKS2022通用信息抽取竞赛](https://aistudio.baidu.com/aistudio/competition/detail/161/0/introduction)上进行，实验室将在6月底对大家的学习成果进行评价，并对优秀者进行奖励。以下是评测说明：

- 以个人为单位报名，验证数据已于4月25日发布，大家可以直接在比赛界面提交结果，**每天至多提交三次结果**。
- 提交后需要在飞书文档上更新自己的提交记录，说明本次提交做了哪些工作（如模型调参、数据增强等），最终实验室会根据提交记录和打榜成绩综合评价大家的学习成果。
- 本次比赛赛题综合了多个抽取子任务，已公布的Seen Schema中6个抽取框架中，子任务难度各有不同，建议从“人生信息”和“影视情感”开始着手。

# 深度学习工具

#### PyTorch

PyTorch主要用于学术研究，易于上手，TensorFlow在工业落地方面更有修饰，建议大家使用PyTorch。

1. 【文档】[PyTorch中文文档](https://pytorch-cn.readthedocs.io/zh/latest/)
2. 【视频课程】[手动使用PyTorch实现简单的神经网络模型](https://space.bilibili.com/1413433465?spm_id_from=333.337.0.0)

# 深度学习入门

1. 【视频课程】[李沐 动手学深度学习 PyTorch版](https://space.bilibili.com/1567748478/channel/seriesdetail?sid=358497) 斯坦福公开课，由李沐老师中文讲述，从基础数学讲起，视频以及代码资料齐全，系统。
2. 【视频课程】[李宏毅 2021/2022春机器学习课程](https://www.bilibili.com/video/BV1Wv411h7kN?p=1)
3. 【视频课程】[斯坦福CS224N (2021|中英) 深度自然语言处理](https://www.bilibili.com/video/BV18Y411p79k/?spm_id_from=333.788.recommend_more_video.0)
4. 【在线教程】[零基础实践深度学习](https://www.paddlepaddle.org.cn/tutorials/projectdetail/3465990) 百度在线教程，代码资料都在线运行，不必安装环境，从简单到复杂写代码实践深度学习，采用百度自研的paddlepaddle深度学习框架。
5. 【书籍】[邱锡鹏 神经网络与深度学习](https://nndl.github.io/nndl-book.pdf) 复旦大学，全面介绍深度学习，配套资源均在Github，也有[课程视频](https://www.bilibili.com/video/BV13b4y1177W?spm_id_from=333.999.0.0)
6. 【书籍】[从零构建知识图谱：技术、方法与案例](https://weread.qq.com/web/reader/3b332a007260a5613b3feb6)
7. 【仓库】[东南大学《知识图谱》研究生课程](https://github.com/npubird/KnowledgeGraphCourse)

# NLP任务实践

1. ##### 知识图谱的构建

   见[知识图谱的构建](https://github.com/hejieshi/iechub/tree/main/NLP%20Learning%20Schedule/Knowledge%20Graph)，由廖攀负责。

2. ##### QAsystem

   见[基于RASA的问答系统](https://github.com/hejieshi/iechub/tree/main/NLP%20Learning%20Schedule/QA%20System)，由崔建民负责。

3. ##### 文本纠错

   见[文本纠错](https://github.com/hejieshi/iechub/tree/main/NLP%20Learning%20Schedule/Spell%20Error%20Correction)，由贺杰士负责。

   

# 其他实用工具

### Anaconda

##### 1. 创建环境

```sh
conda create -n env_name python=x.x
```

##### 2. 查看环境列表

```sh
conda env list
```

##### 3. 激活环境

```sh
conda activate env_name
```

##### 4. 删除环境

```sh
conda remove -n env_name --all
```

##### 5. 查看环境中的包

```sh
conda list
```

##### 6. 安装包

```sh
conda install package_name[=x.x.x]
pip install package_name[=x.x.x]
```

##### 7. 更新包

```sh
conda update package_name
pip update package_name
```

##### 8. 卸载包

```sh
conda uninstall package_name
pip uninstall package_name
```

