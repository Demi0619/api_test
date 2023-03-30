import requests
import allure
import json
import jsonpath
import pymysql

class Keycap:
    @allure.step('get info')
    def get(self,url,params=None,**kwargs):
        res = requests.get(url=url,params=params,**kwargs)
        return res
    @allure.step('post info')
    def post(self,url,data=None,**kwargs):
        res = requests.post(url=url,json=data,**kwargs)
        return res
    @allure.step('extract info')
    def get_field(self,data,json_path):
        data = json.loads(data)
        fields_list = jsonpath.jsonpath(data,json_path)
        field =fields_list[0]
        return field

    def get_vars(self,data,name_list_sting,value_list_string):
        var_dict = {}
        name_list = name_list_sting.split(';')
        value_list = value_list_string.split(';')
        for i in range(len(name_list)):
            value = self.get_field(data,value_list[i])
            var_dict[name_list[i]]=value
        return var_dict

    @allure.step('get data from db')
    def dbCheck(self, sql):
        conn = pymysql.connect(
            host='shop-xo.hctestedu.com',
            port=3306,
            user='api_test',
            passwd='Aa9999!',
            database='shopxo_hctested',
            charset='utf8')
        curs = conn.cursor(pymysql.cursors.DictCursor)  # return data in dict instead of tuple
        curs.execute(query=sql)
        result = curs.fetchone()
        return result

