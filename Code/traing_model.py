# coding=utf-8
"""
created on:2017/9/5
author:DilicelSten
target:找出最好的模型
finished on:2017/9/5
"""
from sklearn.preprocessing import StandardScaler,MinMaxScaler
from sklearn.datasets import load_svmlight_file
from linear_models import *


name_list = ['boxoffice', 'weibo_score', 'douban_score', 'mtime_score']
model_list = ['my_linear_regression','my_lasso_lars','my_ridge']


# 到时针对具体数据再进行修改
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
            if Y[j] > 10 :
                Y[j] = Y[j] / 100000
        y_list.append(Y)
    # X为输入空间， y为输出空间
    X = X.toarray()
    # print "......................\n", Y

    scaler = StandardScaler().fit(X)
    features = scaler.transform(X)
    return features, y_list


def cal_avg(list1, list2, list3):
    """
    计算数值的平均值
    :param list1: 评分１的统计量列表
    :param list2: 评分２的统计量列表
    :param list3: 评分３的统计量列表
    :return:
    """
    avg = []
    v1 = list(map(lambda x: x[0] + x[1], zip(list1, list2)))
    v2 = list(map(lambda y: y[0] + y[1], zip(list3, v1)))
    for each in v2:
        avg.append(each/3.0)
    return avg


def cal_coef(final_list):
    result = []
    for i in range(len(final_list)):
        for j in range(len(final_list[i])):
            if final_list[i][j] < 0:
                final_list[i][j] = 0
    v1 = list(map(lambda x: x[0] + x[1], zip(final_list[0], final_list[1])))
    v2 = list(map(lambda y: y[0] + y[1], zip(final_list[2], final_list[3])))
    v3 = list(map(lambda z: z[0] + z[1], zip(v1, v2)))
    for each in v3:
        result.append(each/4.0)
    return result


def cal_one_model(box_office, all_score):
    """
    计算每个模型的各个统计量值
    :param box_office:
    :param all_score:
    :return: 模型的各个统计量值
    """
    # print box_office,"cal_one"
    # print all_score, "cal_one"

    w1 = 0.5
    w2 = 0.5
    # print box_office[0]
    # print all_score[0]
    v1 = [c * w1 for c in box_office]
    v2 = [d * w2 for d in all_score]
    result = list(map(lambda x: x[0] + x[1], zip(v1, v2)))
    return result


def cal_final_model(score_list):
    """
    计算最终模型的各统计量值总和
    :param score_list: [f统计量,R^2,SSE]
    :return: 三个因子的比例总和
    """
    result = []
    w3 = 1
    w4 = 1
    w5 = 1
    for i in range(len(score_list)):
        result.append(w3 * score_list[i][0] + w4 * score_list[i][1] - w5 * score_list[i][2])
    # result = w3 * score_list[0] + w4 * score_list[1] + w5 * score_list[2]
    return result


def cal_result(model,year):
    """
    计算１个模型的各个统计量
    :param model: 模型
    :return: 统计量列表
    """
    X = load_data(year)[0]
    y1 = load_data(year)[1][0]  # 票房
    y2= load_data(year)[1][1]  # 微博评分
    y3= load_data(year)[1][2]  # 豆瓣评分
    y4 = load_data(year)[1][3]  # 时光网评分
    # print X,y1,y2,y3,y4,"_________________"
    scaler = MinMaxScaler().fit(X)
    X = scaler.transform(X)
    # print model(X, y1)[0]
    # print model(X, y2)[0]
    # print model(X, y3)[0]
    # print model(X, y4)[0]
    result = cal_one_model(model(X, y1)[0], cal_avg(model(X, y2)[0], model(X, y3)[0], model(X, y4)[0]))
    result1 = []
    result1.append(model(X, y1)[1])
    result1.append(model(X, y2)[1])
    result1.append(model(X, y3)[1])
    result1.append(model(X, y4)[1])
    print result1
    # scaler = StandardScaler().fit(result1)
    # result1 = scaler.transform(result1)
    return result, result1



def cal_model_standard(year):
    """
    将多个模型集合并进行归一化
    :return:
    """
    p_list = []
    p_list.append(cal_result(my_linear_regression,year)[0])
    p_list.append(cal_result(my_lasso_lars,year)[0])
    p_list.append(cal_result(my_ridge,year)[0])
    # scaler = StandardScaler().fit(p_list)
    # features = scaler.transform(p_list)
    features = p_list
    return features


if __name__ == '__main__':
    # print cal_result(my_linear_regression,2010)
    for year in range(2017, 2018):
        print '---------------------------------'
        print year
        print '---------------------------------'
        print cal_result(my_linear_regression, year)
        print '---------------------------------'
        print cal_result(my_ridge, year)
        print '---------------------------------'
        print cal_result(my_lasso_lars, year)
        print '---------------------------------'
        # result = cal_final_model(cal_model_standard(year))
        # for i in range(len(result)):
        #     print model_list[i],
        #     print cal_model_standard(year)[i],
        #     print result[i]
        # print '---------------------------------'
        # print cal_result(my_linear_regression, year)[1]
        # print '---------------------------------'
        # print cal_coef(cal_result(my_linear_regression, year)[1])
        # print '---------------------------------'
    # print cal_result(my_linear_regression, 2010)[0]