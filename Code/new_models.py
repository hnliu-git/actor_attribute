# coding=utf-8
"""
created on:2017/9/25
author:DilicelSten
target:使用多项式回归的方法测试数据
finished on:2017/9/25
"""
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_svmlight_file
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import numpy as np
from sklearn.metrics import mean_squared_error
name_list = ['boxoffice', 'weibo_score', 'douban_score', 'mtime_score']


def load_data(year):
    """
    读取数据并进行处理
    :return: 输入空间　输出空间
    """
    y_list = []
    for i in range(4):
        filename = '../Datas/libsvm/'+str(year)+'/'+name_list[i]+'_libsvm.txt'
        data = load_svmlight_file(filename)
        X = data[0]
        Y = data[1]
        for j in range(0, Y.__len__(), 1):
            if Y[j] > 10:
                Y[j] = Y[j] / 100000
        y_list.append(Y)
    # X为输入空间， y为输出空间
    X = X.toarray()
    scaler = StandardScaler().fit(X)
    features = scaler.transform(X)
    return features, y_list


def cal_eva(models, X, y):
    msr_score = np.mean((models.predict(X) - y) ** 2)
    mse_score = mean_squared_error(y, models.predict(X))
    f_measures = msr_score / mse_score
    return mse_score, f_measures


if __name__ == '__main__':
    year = 2011
    X = load_data(year)[0]
    y1 = load_data(year)[1][3]  # 票房
    regressor = LinearRegression()
    regressor.fit(X, y1)
    print regressor.coef_
    quadratic_featurizer = PolynomialFeatures(degree=2)
    X_quadratic = quadratic_featurizer.fit_transform(X)
    regressor_quadratic = LinearRegression()
    regressor_quadratic.fit(X_quadratic, y1)
    print regressor_quadratic.coef_
    print('1 r-squared', regressor.score(X, y1))
    # print('1 sse', cal_eva(regressor,X, y1)[0])
    # print('1 f_value', cal_eva(regressor,X, y1)[1])
    print('2 r-squared', regressor_quadratic.score(X_quadratic, y1))
    # print('2 sse', cal_eva(regressor_quadratic,X_quadratic, y1)[0])
    # print('2 f_value', cal_eva(regressor_quadratic,X_quadratic, y1)[1])
