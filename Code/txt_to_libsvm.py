# coding=utf-8
"""
created on:2017/9/7
author:DilicelSten
target:将txt文件转换成libsvm数据格式的文件
finished:2017/9/7
"""
name_list = ['boxoffice', 'weibo_score', 'douban_score', 'mtime_score']
for a in range(4):
    for i in range(2017, 2018):
        print i
        readin = open('/home/lhn/PycharmProjects/DMSteps/Datas/new_model_training/'+str(i)+'/'+name_list[a]+'.txt', 'r')

        output = open('/home/lhn/PycharmProjects/DMSteps/Datas/libsvm/'+str(i)+'/'+name_list[a]+'_libsvm.txt', 'w')
        try:
            the_line = readin.readline()
            while the_line:
                # delete the \n
                the_line = the_line.strip('\n')
                index = 0
                output_line = ''
                for sub_line in the_line.split(','):
                    #the label col
                    if index == 0:
                        output_line = sub_line
                    #the features cols
                    if sub_line != 'NULL' and index != 0:
                        the_text = ' ' + str(index) + ':' + sub_line
                        output_line = output_line + the_text
                    index = index + 1
                output_line = output_line + '\n'
                output.write(output_line)
                the_line = readin.readline()
        finally:
            readin.close()