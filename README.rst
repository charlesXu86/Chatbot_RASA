一、Chatbot_RASA
==========================

Chatbot_RASA是一个基于 `RASA <https://rasa.com>`_ 的多轮任务型对话系统，该项目支持不同场景的任务型对话快速接入，具有泛化能力好，多轮对话质量高的特点
现在RASA的新版本已经支持基于知识库（knowledge base）的问答和检索（retrieve）的问答。我在RASA的基础上做了一些二次开发，比如在nlu阶段引入了 **bert**，在policy
中引入 **强化学习** 等


二、项目架构
============

1、RASA总体架构：

|image0|

2、执行流程：

    1、接收到用户信息后，rasa会将其送进Interpreter，送进解释器的数据格式为一个字典，其中包含：原文、识别到的Intent、Slot、Sentiment等等信息

    2、Interpreter会把数据传送到Traker，Tracker的作用是记录对话状态，并且跟踪对话进度

    3、Policy会从Tracker中获取当前对话状态，并且确定一个最佳的Action

    4、机器人根据Action确定一个response发送给用户，并且此时将当前的状态反馈给Tracker，更新对话状态，循环往复，直到对话结束



三、使用说明
==============

1、在成功运行项目之前，需要安装一些外部pip包：

    pip install chatbot_nlu

    pip install chatbot_dm

2、安装bert as service

3、数据验证

    rasa data validate --domain domain/cuishou_domain.yml

4、Train NLU & Core

    rasa train --domain domain/cuishou_domain.yml --data data --config config/config_with_components.yml --out models

5、Evaluating Models

6、启动Action

    python -m rasa_sdk.endpoint --actions actions

7、启动对话服务

    1、交互模式 Interactive Learning： # --skip-visualization

        rasa run actions --actions actions& rasa interactive -m models/20200107-105951.tar.gz --endpoints endpoints.yml

    2、Debug模式

        rasa run --endpoints config/endpoints.yml --enable-api --m models/20191011-175206.tar.gz --log-file bot.out.log --debug

    3、shell模式

        rasa shell --debug


具体的使用说明，可以参考`RASA的官方说明文档 <https://rasa.com/docs/rasa/user-guide/evaluating-models/>`_



四、REST接口模式
======================
将Action和对话模型启动后，RASA便可以以REST形式提供服务，为工程调用，或者接入微信公众号、钉钉群等。在这里我要安利一下我的另外一个项目：

 **`Chatbot_Help <https://github.com/charlesXu86/Chatbot_Help>`_ **


四、Update News
======================

    * 2020.1.7  接入钉钉群，支持主动推送消息、outgoing交互

    * 2020.1.9  接入微信





五、Resources
======================

.. _`Dingtalk_README`: https://github.com/charlesXu86/Chatbot_Help/blob/master/Dingtalk_README.rst



.. |image0| image:: https://github.com/charlesXu86/Chatbot_RASA/blob/master/image/rasa_architecture.png
