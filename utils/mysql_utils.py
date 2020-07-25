# -*- coding: utf-8 -*-

'''
@Author  :   Xu
 
@Software:   PyCharm
 
@File    :   mysql_utils.py
 
@Time    :   2019-10-05 14:22
 
@Desc    :   数据库连接工具类
 
'''

import pymysql
import logging

logger = logging.getLogger(__name__)


class SkillData():

    def __init__(self):

        # 本地
        self.database = 'renren_security'
        self.host = 'rm-uf6rv6pnfqsf649w92o.mysql.rds.aliyuncs.com'
        self.username = 'gpu'
        self.password = 'kvqpZxG6'
        # self.table_list = 'report_calculate_data_results'
        self.db = pymysql.connect(host=self.host, port=3306, user=self.username, passwd=self.password, db=self.database)

        # 线上
        # self.database = 'reports'
        # self.host = 'rm-bp1qu674tzv6x7379188.mysql.rds.aliyuncs.com'
        # self.username = 'reports_h_r2'
        # self.password = 'lUejZqzL9T8UuYDg'
        # self.table_list = 'report_calculate_data_results'
        # self.db = pymysql.connect(self.host, self.username, self.password, self.database)

    def get_data(self, skillId):
        """
        根据技能id获取训练机器人需要的数据
        :param skillId: 技能ID
        :return:
        """
        db = pymysql.connect(self.host, self.username, self.password, self.database)
        logger.info('Connect mysql {} successfully'.format(self.database))
        cursor = self.db.cursor()
        cursor.execute("select * from report_calculate_data_results where process_id = %s", speechId)
        res = cursor.fetchall()
        logger.info('All data length is {}'.format(len(res)))
        cursor.close()
        self.db.close()

        return res

    def get_no_intent_data(self, speechId):
        '''
        获取没有意图的数据（用户说话）
        :param speechId:
        :return:
        '''
        db = pymysql.connect(self.host, self.username, self.password, self.database)
        # db = pymysql.connect(host=self.host, port=3306, user=self.username, passwd=self.password, db=self.database)
        logger.info('Connect mysql {} successfully'.format(self.table_list))
        cursor = db.cursor()
        cursor.execute("select * from report_calculate_data_results where process_id = %s "
                       " and matched_status = 2 "
                       "and user_talk_text is not null", speechId)
        result = cursor.fetchall()
        logger.info('No intent data is {}'.format(len(result)))
        cursor.close()

        return result

    def get_intent_details_data(self, speechId):
        """
        根据话术Id获取对应的意图详情
        :param speechId:
        :return:
        """
        logger.info('Connect mysql {} successfully'.format(self.table_list))
        cursor = self.db.cursor()
        cursor.execute("select ti.intention_id, ti.talk_id, i.name from talk_intention ti inner join intention  i on i.id=ti.intention_id where ti.talk_id= %s", speechId)
        res = cursor.fetchall()
        logger.info('All data length is {}'.format(len(res)))
        cursor.close()
        self.db.close()

        return res



if __name__ == "__main__":
    skillid = '569353302990019129'
    SkillData().get_data(skillid)