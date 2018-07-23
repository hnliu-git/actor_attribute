# ActorAttribute
Judge an actor according to nine attribute
## Operation Environment
 - scikit-learn
 - pymongo
 - MySQLdb
## Operation Instruction
  Run `training_model` to get the coef <br>
  Then Using the coef to run `movie_input_cal`
## Data Structure
>Input Data<br>
- actor_price
```
{
   "_id" : 663419,
   "actor_list" : [
      {
         "actor_name" : "妻夫木聪",
         "price_num" : 3,
         "nomination_num" : 5
      },
}
```
- actor_weibo
```
{
   "_id" : 663419,
   "actor_list" : [
      {
         "follow_num" : 472,
         "actor_name" : "王宝强",
         "weibo_num" : 2151,
         "fans_num" : 29010000
      },
}
```
- actor_baiduindex
```
{
   "_id" : 655823,
   "actor_baidu_index" : {
      "黄景瑜" : 550660,
      "张译" : 446376,
      "麦亨利" : 76797,
      "霍思燕" : 354866,
      "尹昉" : 78355,
      "任达华" : 207328,
      "海清" : 224923,
   }
}
```
- actor_boxoffice
```
{
   "_id" : 655823,
   "actor_boxoffice" : {
      "霍思燕" : [748,13657,7700,454,2921,413,1783,180,897,679,10739,12297,12996],
      "杜江" : [...]
   }
}
```
- actor_fans_love
```
{
   "_id" : 663419,
   "actor_fans_love" : {
      "刘承羽" : 74,
   }
}
```
- actor_newpercentage
```
{
    “_id”: 电影的 id(中国票房网),
    “actor_newpercentages”:{
    吴京:0.8,
    ......
}
```
- actor_baiduindex
```
{
    “_id”: 电影的 id(中国票房网),
    “actor_baidu_index”:{
    ”吴京”:493852,
    ......
    }
}
```
- actor_doubanScore
```
{
  “_id”: 电影的 id(中国票房网),
  “actor_douban_score”:{
  "吴京" : 7.122,
  ......
  }
}
```
>Output Data
- actor_totalist 
```
{
  “_id”: 电影的 id(中国票房网),
  “coef”(每种变量的权重占比):{
  “emotion_score”:0.1,(评论涉及率)
  “boxOffice”:0.1,(历史票房影响力)
  “price”:0.1,(提名及获奖情况)
  “baiduIndex”:0.1,(百度搜索指数)
  “doubanScore”:0.1,(豆瓣评分)
  “weibo”:0.1,(微博影响力)
  “match_type”:0.1,(电影匹配程度)
  “newpercentages”:0.1,(新闻曝光率)
  “fans_love”:0.1,(影迷喜好度)
},
  “emotion_score”:{吴京:0.8,......},
  “price”:{吴京:0.8,......},
  “baiduIndex”:{吴京:0.8,......},
  “doubanScore”: {吴京:0.8,......},
  “weibo”: {吴京:0.8,......},
  “match_type”: {吴京:0.8,......},
  “newpercentages”: {吴京:0.8,......},
  “fans_love”: {吴京:0.8,......}
}
```
- actor_attribute
```
{
  “_id”: 电影的 id(中国票房网),
  “actor_attribute”:{
  吴京:0.8,
  ......
  }
}
```
## File Introduction
- factor_analysis <br>
因子分析，在求解coef中未用到
- linear_models <br>
三个模型类，用于比较模型好坏
- mongo_data_extract <br>
提取mongo数据库的数据
- movie_input_cal <br>
获取输入数据，转换为输出数据（根据算法得出的coef)
- new_model<br>
意义不明
- training_model<br>
算法主函数
- txt_to_libsvm
转换 txt 为libsvm格式

## Key Points
- 不会有样例
- 必须先看LinearRegression才能看这份代码
- 输入和输出并不唯一，仅仅只是此处采用如此的输入输出格式
- Github 中已包含部分先前数据的libsvm 可用来做测试
