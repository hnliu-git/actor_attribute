# coding=utf-8
"""
created on:2017/9/5
author:DilicelSten
target:调出所有的线性模型并计算除相关的统计量
finished on:2017/9/5
"""

from sklearn import linear_model
import numpy as np
from sklearn.metrics import mean_squared_error


def cal_evaluation(models, X, y):
    """
    计算模型的评估数据
    :param models: 模型类型
    :param X: 自变量
    :param y: 因变量
    :return:　[f统计量,R^2,SSE]
    """
    result = []
    y_avg = 0
    for yi in y:
        y_avg += yi
    y_avg = y_avg * 1.0 / y.__len__()
    y_avg_list = [ y_avg for i in range(0,y.__len__(),1)]
    msr_score = np.mean((models.predict(X) - y_avg_list) ** 2)
    mse_score = mean_squared_error(y, models.predict(X))
    f_measures = msr_score / mse_score
    r2_score = models.score(X, y, sample_weight=None)
    result.append(f_measures)
    result.append(r2_score)
    result.append(mse_score)
    return result


def my_linear_regression(X, y):
    """
    普通的线性模型
    :param X: 输入空间
    :param y: 输出空间
    :return: F统计量,SSE,R^2_score
    """
    # print X
    clf = linear_model.LinearRegression()
    clf.fit(X, y)
    # print 'my_linear_regression',clf.coef_
    evaluate_value = cal_evaluation(clf, X, y)
    return evaluate_value,clf.coef_


def my_ridge(X, y):
    """
    岭回归
    :param X: 输入空间
    :param y: 输出空间
    :return: F统计量,SSE,R^2_score
    """
    clf = linear_model.Ridge()
    clf.fit(X, y)
    # print 'my_ridge' , clf.coef_
    evaluate_value = cal_evaluation(clf, X, y)
    return evaluate_value,clf.coef_


def my_lasso_lars(X, y):
    """
    LassoLars模型
    :param X: 输入空间
    :param y: 输出空间
    :return: F统计量,SSE,R^2_score
    """
    clf = linear_model.LassoLars(positive=True)
    clf.fit(X, y)
    # print 'my_lasso_lars',clf.coef_
    evaluate_value = cal_evaluation(clf, X, y)
    return evaluate_value,clf.coef_

