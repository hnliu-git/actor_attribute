# coding=utf-8
"""
created on:2017/11/5
author:DilicelSten
target:对电影主创贡献力进行因子分析
finished on:2017/11/5
"""

from sklearn.preprocessing import MinMaxScaler,StandardScaler
from sklearn.datasets import load_svmlight_file
from sklearn.decomposition import FactorAnalysis



name_list = ['boxoffice', 'weibo_score', 'douban_score', 'mtime_score']


def load_data(year):
    """
    读取数据并进行处理
    :return: 输入空间　输出空间
    """
    y_list = []
    for i in range(4):
        filename = '/home/lhn/PycharmProjects/DMSteps/Datas/libsvm/'+str(year)+'/'+name_list[i]+'_libsvm.txt'
        data = load_svmlight_file(filename)
        X = data[0]
        Y = data[1]
        for j in range(0, Y.__len__(), 1):
            if Y[j] > 10:
                Y[j] = Y[j] / 100000
        y_list.append(Y)
    # X为输入空间， y为输出空间
    X = X.toarray()
    scaler = MinMaxScaler().fit(X)
    features = scaler.transform(X)
    return features, y_list


def model_process(X, y):
    """
    调用训练模型进行数据处理
    :param X: 自变量
    :param y: 因变量
    :return: result
    """
    fa = FactorAnalysis()
    fa.fit_transform(X, y)
    # print fa.get_covariance()
    print fa.components_


def factor_analyze(year):
    """
    进行因子分析
    :param year:年份
    :return:
    """
    X = load_data(year)[0]
    y1 = load_data(year)[1][0]  # 票房
    y2= load_data(year)[1][1]  # 微博评分
    y3= load_data(year)[1][2]  # 豆瓣评分
    y4 = load_data(year)[1][3]  # 时光网评分
    # print X
    print '票房'
    model_process(X, y1)
    print '微博评分'
    model_process(X, y2)
    print '豆瓣评分'
    model_process(X, y3)
    print '时光网评分'
    model_process(X, y4)


if __name__ == '__main__':
    for i in range(2011,2012):
        print i
        print '------------------------------------------'
        factor_analyze(i)
        print '------------------------------------------'