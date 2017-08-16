# -*- coding: utf-8 -*-
# @Time    : 17-8-14 上午11:28
# @Author  : Jimersy Lee
# @Site    : 
# @File    : bayes.py
# @Software: PyCharm
# @Desc    :

from numpy import *


def loadDataSet():
    """
    定义一些数据,返回言论单词,以及言论性质
    :return:
    """
    postingList = [
        ['my', 'dog', 'has', 'flea', 'problem', 'help', 'please'],
        ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
        ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
        ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
        ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
        ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']
    ]
    classVec = [0, 1, 0, 1, 0, 1]  # 1代表侮辱性文字 0代表正常言论
    return postingList, classVec


def createVocabList(dataSet):
    """
    创建一个包含所有文档中出现的不重复单词的列表,为此使用了set数据类型
    :param dataSet:
    :return:
    """
    vocabSet = set([])  # 创建一个空集
    for document in dataSet:
        vocabSet = vocabSet | set(document)  # 创建两个集合的并集
    return list(vocabSet)


def setOfWords2Vec(vocabList, inputSet):
    returnVec = [0] * len(vocabList)  # 创建一个其中所含元素都为0的向量
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
        else:
            print "the word:%s is not in my Vocabulary!" % word
    return returnVec


def trainNormalBayes0(trainMatrix, trainCategory):
    """
    朴素贝叶斯分类器训练函数
    :param trainMatrix: 每篇文档中词是否出现的向量组成的矩阵 [[0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0], [1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1], [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1], [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0]]
    0代表在所有单词中没有出现,1代表在所有单词中出现
    :param trainCategory:每篇文档列表类别标签所构成的向量 [0,1,0,1,0,1] 0代表非侮辱性 1代表侮辱性
    :return:
    """
    numTrainDocs = len(trainMatrix)  # 训练的文档数
    numWords = len(trainMatrix[0])  # 单词表中总的单词个数32个
    pAbusive = sum(trainCategory) / float(numTrainDocs)  # 3/6=0.5
    # p0Num = zeros(numWords)
    # p1Num = zeros(numWords)
    # 利用贝叶斯分类器进行分类时,要计算多个概率的乘积,如果其中一个概率值为0,那么最后的乘积也是0.为降低这种影响,可以将所有的词的出现数初始化为1,并将分母初始化为2
    p0Num = ones(numWords)  # 初始化numWords个元素的的数组,每个元素都是1
    # print p0Num
    p1Num = ones(numWords)
    p0Denom = 2.0  # 初始化类别0的计数值 分母初始化为2,消除概率为0的影响
    p1Denom = 2.0  # 初始化类别1的计数值 侮辱性言论类别
    for i in range(numTrainDocs):
        if trainCategory[i] == 1:
            p1Num += trainMatrix[i]  # 对数组中的每个元素都进行加操作
            p1Denom += sum(trainMatrix[i])  # 计数器=计数器+测试矩阵中的元素和
        else:
            p0Num += trainMatrix[i]  # 对数组中的每个元素都进行加操作
            p0Denom += sum(trainMatrix[i])  # 计数器=计数器+测试矩阵中的元素和
    p1Vect = p1Num / p1Denom  # 对每个元素除以该类别中的总词数,利用numpy可以直接实现
    p0Vect = p0Num / p0Denom
    return p0Vect, p1Vect, pAbusive


# 测试代码
listOfPosts, listClasses = loadDataSet()
myVocabList = createVocabList(listOfPosts)
print myVocabList  # 输出的list没有重复的单词

# 检测每篇文章中哪些词条在字典中出现过

print setOfWords2Vec(myVocabList, listOfPosts[0])  # 第1篇文章哪些单词出现过
print setOfWords2Vec(myVocabList, listOfPosts[3])  # 第4篇文章哪些单词出现过

# 测试朴素贝叶斯分类器训练函数
# 构建训练矩阵
trainMat = []  # 每篇文档中词是否出现的向量组成的矩阵
for postInDoc in listOfPosts:
    trainMat.append(setOfWords2Vec(myVocabList, postInDoc))
# 计算属于侮辱性文档的概率以及两个类别的概率向量
p0V, p1V, pAbusive = trainNormalBayes0(trainMat, listClasses)
print "trainMat=" + str(trainMat)
print "p0V=" + str(p0V)
print "p1V=" + str(p1V)
print "pAbusive=" + str(pAbusive)
