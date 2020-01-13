一、Chatbot_RASA
==========================

1、Chatbot_RASA是一个基于 `RASA <https://rasa.com>`_ 的多轮任务型对话系统，该项目支持不同场景的任务型对话快速接入，具有泛化能力好，多轮对话质量高的特点
现在RASA的新版本已经支持基于知识库（knowledge base）的问答和检索（retrieve）的问答。我在RASA的基础上做了一些二次开发，比如在nlu阶段引入了 **bert**，在policy
中引入 **强化学习** 等

2、这个项目将会陆续提供查天气、查快递、查机票、闲聊等等对话，同时你也可以使用本项目对算法模型在对话系统中的应用进行快速验证


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

        rasa run --endpoints config/endpoints.yml --enable-api --m models/20200113-162316.tar.gz --log-file bot.out.log --debug

    3、shell模式

        rasa shell --debug


具体的使用说明，可以参考 `RASA的官方说明文档 <https://rasa.com/docs/rasa/user-guide/evaluating-models/>`_



四、REST接口模式
======================
1、将Action和对话模型启动后，RASA便可以以REST形式提供服务，为工程调用，或者接入微信公众号、钉钉群等。在这里我要安利一下我的另外一个项目：

`Chatbot_Help <https://github.com/charlesXu86/Chatbot_Help>`_

这个项目可以轻松的将你的机器人接入到第三方平台，轻松又快速的实现交互

2、服务启动后，就可以在postman中对服务进行测试：

接口列表：

.. code:: python

    /conversations/<conversation_id>/messages          POST      add_message
    /conversations/<conversation_id>/tracker/events    POST      append_events
    /webhooks/rest                                     GET       custom_webhook_RestInput.health
    /webhooks/rest/webhook                             POST      custom_webhook_RestInput.receive
    /model/test/intents                                POST      evaluate_intents
    /model/test/stories                                POST      evaluate_stories
    /conversations/<conversation_id>/execute           POST      execute_action
    /domain                                            GET       get_domain
    /socket.io                                         GET       handle_request
    /                                                  GET       hello
    /model                                             PUT       load_model
    /model/parse                                       POST      parse
    /conversations/<conversation_id>/predict           POST      predict
    /conversations/<conversation_id>/tracker/events    PUT       replace_events
    /conversations/<conversation_id>/story             GET       retrieve_story
    /conversations/<conversation_id>/tracker           GET       retrieve_tracker
    /webhooks/socketio                                 GET       socketio_webhook.health
    /status                                            GET       status
    /model/predict                                     POST      tracker_predict
    /model/train                                       POST      train
    /model                                             DELETE    unload_model
    /version                                           GET       version

接口说明

.. code:: python

    a、获取版本接口   GET方法
        url：http://172.18.103.43:5005/version

    b、获取服务的状态  GET方法
        url: http://172.18.103.43:5005/status

        {
            "model_file": "models/20200109-103803.tar.gz",
            "fingerprint": {
                "config": "99914b932bd37a50b983c5e7c90ae93b",
                "core-config": "506804ad89d3db9175b94c8752ca7537",
                "nlu-config": "45f827a042c25a6605b8a868d95d2299",
                "domain": 2088252815302883506,
                "messages": 2270465547977701800,
                "stories": 1278721284179639569,
                "trained_at": 1578537378.2885341644,
                "version": "1.4.1"
            },
            "num_active_training_jobs": 0
        }

    c、会话接口
        url：http://172.18.103.43:5005/webhooks/rest/webhook

        参数：{
                "sender": "000001",
                "message": "你好"
              }

    b、 button接口


四、Update News
======================

    * 2020.1.7  接入钉钉群，支持主动推送消息、outgoing交互

    * 2020.1.9  接入微信





五、Resources
======================

.. _`Dingtalk_README`: https://github.com/charlesXu86/Chatbot_Help/blob/master/Dingtalk_README.rst



.. |image0| image:: https://github.com/charlesXu86/Chatbot_RASA/blob/master/image/rasa_architecture.png
