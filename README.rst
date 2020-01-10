一、Chatbot_RASA
==========================

Chatbot_RASA是一个基于 `RASA <https://rasa.com>`_ 的多轮任务型对话系统，该项目支持不同场景的任务型对话快速接入，具有泛化能力好，多轮对话质量高的特点


二、项目架构
============

RASA总体架构：

|image0|



三、使用说明
==============

1、在成功运行项目之前，需要安装一些外部pip包：

    pip install chatbot_nlu

    pip install chatbot_dm

2、安装bert as service



三、各消息类型使用示例
======================

1、dingtalk

.. code:: python

    import chatbot_help as ch
    from chatbot_help import DingtalkChatbot

    print(ch.__version__)                # 打印版本信息
    dtalk = DingtalkChatbot(webhook)     # 你设置群机器人的时候生成的webhook

详情请参考：`Dingtalk_README <https://github.com/charlesXu86/Chatbot_Help/blob/master/Dingtalk_README.rst>`_

2、wetalk

.. code:: python



四、Update News
======================

    * 2020.1.7  接入钉钉群，支持主动推送消息、outgoing交互

    * 2020.1.9  接入微信





五、Resources
======================

.. _`Dingtalk_README`: https://github.com/charlesXu86/Chatbot_Help/blob/master/Dingtalk_README.rst



.. |image0| image:: https://github.com/charlesXu86/Chatbot_RASA/blob/master/image/rasa_architecture.png
