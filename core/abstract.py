from abc import ABCMeta, abstractmethod

import logging
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


class BaseDB(object):
    __metaclass__ = ABCMeta

    def __init__(self, data):
        # self.config = jsoncfg.load_config('configs.txt')
        self.df = data
        self.file_FD = open("output.csv", "w")
        self.result = pd.DataFrame()
        self.attribute = []
        self.list_probabilityOfAB = []
        self.list_probability = []
        # self.df = pd.DataFrame.from_csv(filename)

    def preprocessing(self):
        #self.df = self.df.drop(['Address2', 'Address3'], axis=1)
        for idx in range(0, len(self.df.columns)):
            self.df[self.df.columns[idx]].replace("empty", np.nan, inplace=True)
        self.df = self.df.dropna(axis=1, how='all')

    def groupattributes(self):
        self.attribute = []
        self.list_probabilityOfAB = [[]]
        self.list_probability = []
        tuple_cnt = self.df.shape[0]
        threshold = (0.015*tuple_cnt)
        col_list = len(self.df.columns)
        for idx in range(0, col_list - 1):
            probabilityList = []
            for inner_idx in range(idx+1, col_list):
                df_t = self.df.groupby([self.df.columns[idx], self.df.columns[inner_idx]]).size().reset_index(name='count')
                df_t.loc[df_t['count'] <= threshold, 'count'] = 0
                probabilityList.append(float(df_t['count'].sum())/tuple_cnt)
                #print probabilityList
            # Calculate probability of occurrence of 2 individual independent events P(A and B)
            self.list_probabilityOfAB.append(probabilityList)
        #print self.list_probabilityOfAB

    def probability_columns(self):
        tuple_ct = self.df.shape[0]
        for idx, col in enumerate(self.df.columns):
            df_temp = pd.DataFrame(self.df[col].value_counts())
            df_temp.columns = ['count']
            self.list_probability.append([y / tuple_ct for y in df_temp['count']])
        # print(self.list_probability)

    # @abstractmethod
    # def createMRFs(self):
    #     pass
    #
    # @abstractmethod
    # def createBNs(self):
    #     pass
    #
    # @abstractmethod
    # def factorGraphs(self):
    #     pass

    # @abstractmethod
    # def insert_json(self, jObject):
    #     pass
    #
    # @abstractmethod
    # def update_json(self, key, value):
    #     pass

    # def get_connection(self):
    #     db_config = self.config['db']
    #     connection = psycopg2.connect(database=db_config.name(),
    #                                   user=db_config.user(),
    #                                   password=db_config.password(),
    #                                   host=db_config.host(),
    #                                   port=db_config.port_num())
    #     return connection
    #
    # def execute(self, command, params=None, returnsResult=False):
    #     connection = None
    #     try:
    #         logger.info("About to execute command: {0}".format(command))
    #         # start_time_1 = timeit.default_timer()
    #         connection = self.get_connection()
    #         cursor = connection.cursor()
    #
    #         cursor.execute(command, params)
    #         # cursor.close()
    #         connection.commit()
    #         # elapsed_1 = timeit.default_timer() - start_time_1
    #
    #         # logger.info("Time taken to Execute command {0}: {1}".format(command, elapsed_1))
    #
    #         result = []
    #         if returnsResult:
    #             result = cursor.fetchall()
    #         cursor.close()
    #         return result
    #
    #     except (Exception, psycopg2.DatabaseError) as error:
    #         logger.error("Error during DB operation {0}".format(error))
    #         raise
    #
    #     finally:
    #         if connection is not None:
    #             connection.close()
    #
    # @abstractmethod
    # def drop_table(self):
    #     pass
    #
    # @abstractmethod
    # def create_index(self):
    #     pass

    # def __str__(self):
    #     return ""