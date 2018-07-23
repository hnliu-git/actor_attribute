#coding=utf-8
'''
计算演员贡献力
'''
from pymongo import MongoClient
import numpy as np
import MySQLdb
from sklearn.preprocessing import StandardScaler,MinMaxScaler
from sklearn.datasets import load_svmlight_file
from mongo_data_extract import *
import sys
if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')

# conn=MySQLdb.Connect("localhost","root","123","Movie_2018",charset="utf8")
conn=MySQLdb.Connect("localhost","root","123","Movie_Data_Collect",charset="utf8")
cur=conn.cursor()

def connect_mongodb():
    """
    连接mongodb
    :return:数据库
    """
    # 建立mongodb数据库连接
    client = MongoClient('192.168.235.55', 27017)
    # 用户验证
    db = client.admin
    db.authenticate("admin", "123456")
    db = client.Seeing_future
    print ("报告!数据库连接成功!")
    return db





def find_actor_price(db,m_id):
    price_dict={}
    collection=db.actor_price
    if not collection.find_one({'_id': m_id}):
        pass
    else:
        actor_list=collection.find_one({'_id': m_id})['actor_list']
        if len(actor_list) == 0:
            pass
        else:
            for actor in actor_list:
                price_dict[actor['actor_name']]=actor['price_num']+actor['nomination_num']
    return price_dict

def find_actor_fans_love(db,m_id):
    fans_love_dict={}
    collection = db.actor_fans_love
    if not collection.find_one({'_id': m_id}):
        pass
    else:
        actor_list = collection.find_one({'_id': m_id})['actor_fans_love']
        fans_love_dict=actor_list
    return fans_love_dict

def find_actor_weibo(db,m_id):
    weibo_dict={}
    collection = db.actor_weibo
    if not collection.find_one({'_id': m_id}):
        pass
    else:
        actor_list = collection.find_one({'_id': m_id})['actor_list']
        if len(actor_list) == 0:
            pass
        else:
            for actor in actor_list:
                weibo_dict[actor['actor_name']] = actor['follow_num'] + actor['weibo_num']+ actor['fans_num']
    return weibo_dict

def find_actor_match_type(db,m_id):
    match_type_dict = {}
    collection = db.actor_match_type
    if not collection.find_one({'_id': m_id}):
        pass
    else:
        actor_list = collection.find_one({'_id': m_id})['actor_match_type']
        match_type_dict = actor_list
    return match_type_dict

def find_boxOffice(db,m_id):
    boxOffice_dict = {}
    collection = db.actor_boxOffice
    if not collection.find_one({'_id': m_id}):
        pass
    else:
        actor_list = collection.find_one({'_    id': m_id})['actor_boxoffice']
        for key in actor_list.keys():
            n=len(key)
            sum=0
            for v in actor_list[key]:
                sum+=v
            boxOffice_dict[key]=sum/n
    return boxOffice_dict

def find_actor_newspercentages(db,m_id):
    newspercentages_dict = {}
    collection = db.actor_newpercentages
    if not collection.find_one({'_id': m_id}):
        pass
    else:
        actor_list = collection.find_one({'_id': m_id})['actor_percentages']
        newspercentages_dict = actor_list
    return newspercentages_dict

def find_actor_emotion_score(db,m_id):
    emotion_score_dict={}
    collection=db.actor_emotion_score
    if not collection.find_one({'_id': m_id}):
        pass
    else:
        actor_list = collection.find_one({'_id': m_id})['actor_emotion_score']
        emotion_score_dict = actor_list
    return emotion_score_dict

def find_actor_baiduIndex(db,m_id):
    baiduIndex_dict = {}
    collection = db.actor_baiduIndex
    if not collection.find_one({'_id': m_id}):
        pass
    else:
        actor_list = collection.find_one({'_id': m_id})['actor_baidu_index']
        baiduIndex_dict = actor_list
    return baiduIndex_dict


def find_actor_doubanScore(db,m_id):
    doubanScore_dict = {}
    collection = db.actor_doubanScore
    if not collection.find_one({'id': m_id}):
        pass
    else:
        actor_list = collection.find_one({'id': m_id})['actor_douban_score']
        doubanScore_dict = actor_list
    return doubanScore_dict


def getActorList(cur,m_id):
    # cur.execute("select actor_name from charc_info where movie_id=%d"%m_id)
    print "select actor_name from mtime_movie,mtime_movie_actors where mtime_movie.m_id=mtime_movie_actors.m_id and cbo_id=%s;"%m_id
    cur.execute("select actor_name from mtime_movie,mtime_movie_actors where mtime_movie.m_id=mtime_movie_actors.m_id and cbo_id=%s;"%m_id)
    return cur.fetchall()

#-------------------------------下面的代码不必看了，重写就好-----------------------------------------

db=connect_mongodb()
MovieList=[663419,655823]
coef=[0.073,0,0.055,0,1.531,0.161,0.241,0.498,1.652]


NameList=['price','fans_love','weibo','match_type','boxOffice','newpercentages','emotion_score','baiduIndex','doubanScore']
for m_id in MovieList:
    print "-----------------------------------------------------------"
    # mongo_string="{\"_id\":"+str(m_id)+"," \
    #                                    "\"coef\":{"
    # for i in range(len(NameList)):
    #     mongo_string+="\""+NameList[i]+"\":"+str(float(coef[i]))+","
    # mongo_string+="},"
    # mongo_string=mongo_string.replace(",}","}")
    ActorContributeDict = {}
    MovieActorDict={}
    MovieActorDict['price']=find_actor_price(db,m_id)
    MovieActorDict['fans_love'] =find_actor_fans_love(db,m_id)
    MovieActorDict['weibo'] =find_actor_weibo(db,m_id)
    MovieActorDict['match_type'] =find_actor_match_type(db,m_id)
    MovieActorDict['boxOffice'] =find_boxOffice(db,m_id)
    MovieActorDict['newpercentages'] =find_actor_newspercentages(db,m_id)
    MovieActorDict['emotion_score'] =find_actor_emotion_score(db,m_id)
    MovieActorDict['baiduIndex'] = find_actor_baiduIndex(db, m_id)
    MovieActorDict['doubanScore'] =find_actor_doubanScore(db,m_id)
    actor_num=len(getActorList(cur,m_id))
    a=np.zeros(shape=(actor_num,9))
    cot=0
    actor_list=getActorList(cur,m_id)
    for actor in actor_list:
        for i in range(len(NameList)):
            if MovieActorDict[NameList[i]].has_key(actor[0]):
                print actor[0],NameList[i],MovieActorDict[NameList[i]][actor[0]]
                a[cot][i]=MovieActorDict[NameList[i]][actor[0]]
            else:
                a[cot][i]=0
        cot+=1
    scaler=StandardScaler().fit(a)
    a=scaler.transform(a)
    #加2操作去除负值
    a = np.array([[a[i][j] + 2 for j in range(len(a[i]))] for i in range(len(a))])

    '''
    存每个因子的值
    '''
    # ActorDict={}
    # for i in range(actor_num):
    #     if actor_list[i][0] in (u"妻夫木聪", u"黄西"):
    #         continue
    #     ActorDict[actor_list[i][0]] = {}
    #     cot=0
    #     contri=0
    #     for v in a[i]:
    #         # a[i][cot]=a[i][cot]*coef[cot]
    #         ActorDict[actor_list[i][0]][NameList[cot]]=a[i][cot]
    #         # print actor_list[i][0],NameList[cot],a[i][cot]*coef[cot]
    #         cot+=1
    # for i in range(len(NameList)):
    #     mongo_string += "\"" + NameList[i] + "\":{"
    #     for key in ActorDict.keys():
    #         mongo_string+="\""+key+"\":"+str(float(ActorDict[key][NameList[i]]))+","
    #     mongo_string+="},"
    # mongo_string+="}"
    # mongo_string=mongo_string.replace(",}","}")
    # print mongo_string
    # collection=db.actor_totallist
    # collection.insert_one(eval(mongo_string))




    '''
    存贡献力
    '''
    mongo_string="{\"_id\":"+str(m_id)+",\"actor_attribute\":{"
    for i in range(actor_num):
        cot=0
        contri=0
        for v in a[i]:
            if a[i][cot]*coef[cot]>0:
                contri+=a[i][cot]*coef[cot]
            cot+=1
        if contri<22:
            if actor_list[i][0] in (u"妻夫木聪",u"黄西"):
                continue
            print actor_list[i][0], contri
            mongo_string+="\""+actor_list[i][0]+"\":"+str(contri)+","
    mongo_string+="}}"
    mongo_string=mongo_string.replace(",}","}")
    print mongo_string
    collection=db.actor_attribute
    # collection.insert_one(eval(mongo_string))
