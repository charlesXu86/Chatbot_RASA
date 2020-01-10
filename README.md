# Chatbot_CN 项目下的RASA模块
**将RASA模块从原项目里分离下来。**

## 技术架构
![pipeline][2]
[参考](https://rasa.com/docs/get_started_step1/)

### 模块化
Action - Rasa NLU - Rasa Core - Web Server（Django restful API）

### Context保存
将所需要的entities放入不同slot中(通过Rasa-core实现)

### 基于意图(Intent-based)的对话
这是当NLP算法使用intents和entities进行对话时，通过识别用户声明中的名词和动词，然后与它的dictionary交叉引用，让bot可以执行有效的操作。
### ...
## Rasa NLU
使用自然语言理解进行意图识别和实体提取


## run model
1、安装外部模块
   * pip install chatbot_nlu
   * pip install chatbot_dm

2、bert
   * 启动bert service

3、数据验证：
    
    rasa data validate --domain domain/cuishou_domain.yml

4、Train nlu & core

    rasa train --domain domain/cuishou_domain.yml --data data --config config/config_with_components.yml --out models

5、Evaluating Models


6、启动action

    python -m rasa_sdk.endpoint --actions actions


Interactive Learning： # --skip-visualization
    
    rasa run actions --actions actions& rasa interactive -m models/20200107-105951.tar.gz --endpoints endpoints.yml

Debug模式
local: 
    
    rasa run --endpoints config/endpoints.yml --enable-api --m models/20191011-175206.tar.gz --log-file bot.out.log --debug

server: 
   
    rasa run --endpoints config/endpoints.yml --enable-api --m models/20200107-105951.tar.gz --debug

rasa run --enable-api -m models --debug

shell模式
   * rasa shell --debug

### Example:





### Pipeline
假设我们在config文件中这样设置pipeline`"pipeline": ["Component A", "Component B", "Last Component"]`
那么其生命周期如下：
![LifeCircle][3]
在`Component A`调用开始之前， rasa nlu会首先根据nlu的训练集创建一个Context(no more than a python dict). Context用于在各个Component之间传递消息。 比如， 我们可以让`Component A`去根据训练集计算特征向量， 训练完成后将结果保存在Context中， 传递到下一个Component。 `Component B` 可以获取这些特征向量， 并根据其做意图分类。在所有Component完成后， 最后的Context中保存这个模型的元数据(metadata). 

```
MITIE是一个MIT信息提取库，该库使用了最先进的统计机器学习工具构建。它类似于word2vec中的word embedding。MITIE模型，在NLU（自然语言理解）系统中，完成实体识别和意图提示的任务。
”nlp_mitie”初始化MITIE
”tokenizer_jieba”用jieba来做分词
”ner_mitie”和”ner_synonyms”做实体识别
”intent_featurizer_mitie”为意图识别做特征提取”intent_classifier_sklearn”使用sklearn做意图识别的分类。

### Run as a service
``` bash

```


### add aditional modules



### Interactive Learning

在交互式学习模式下, 我们可以为Bot对话提供反馈. 这是一个非常强有力的方式去检测Bot能做什么, 同时也是修改错误最简单的方式. 基于机器学习的对话的有点就在于当bot不知道如何回答或者回答错误时, 我们可以及时的反馈给bot. 有些人称这种方式为[Software 2.0](https://medium.com/@karpathy/software-2-0-a64152b37c35)


### Action
进行数据校验, 和数据交互. 
采用Py2Neo与数据库(Neo4j)进行交互. 

  [1]: http://images.zshaopingb.cn/2018/12/3664281616.png
  [2]: http://images.zshaopingb.cn/2018/12/4005670685.png
  [3]: http://images.zshaopingb.cn/2018/12/4136964647.png
  [4]: http://images.zshaopingb.cn/2018/12/923236055.jpg
  [5]: http://images.zshaopingb.cn/2018/12/2537130720.jpg
  [6]: http://images.zshaopingb.cn/2018/12/1133622055.png
