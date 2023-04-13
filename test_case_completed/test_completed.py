'''
1. load data from excel --> common function read_excel
2. constant value
3. encapsulate functions (json extractor, db check)
4. parameter passing
5. clear report structure
'''
import pytest
from test_case_completed.common_func import read_excel,edit_excel_and_save
from VAR import *
from keyword_encap import Keycap
import allure


def setup_module():
    global kc, all_val
    kc = Keycap()
    all_val={}
@pytest.mark.parametrize('data',read_excel(EXCEL_PATH,'Sheet1'))
def test_complete(data):
    # analyze excel data
    domain_name = data[1]
    path = data[2]
    method = data[3]
    params = data[4]
    header = data[5]
    request_data = data[6]
    data_type = data[7]
    json_path = data[8]
    expected_result = data[9]
    case_name = data[11]
    vars_from_res = data[12]
    vars_json_path = data[13]
    story = data[16]
    feature = data[17]
    priority = data[19]
    sql_ex = data[20]
    sql_var = data[21]
    sql_expected = data[22]
    url = domain_name+path
    # send request
    res = getattr(kc,method)(url=url,params=eval(params),data=eval(request_data),headers=eval(header))
    # verify response and write back
    row = data[0]+1
    if json_path is not None:
        actual_result = kc.get_field(res.text,json_path)
        if expected_result is not None:
            if actual_result == expected_result:
                value = 'pass'
            else:
                value = 'failed'
            edit_excel_and_save(EXCEL_PATH,'Sheet1',row,11,value)
    # get data from response and save for later use
    if vars_from_res is not None and vars_json_path is not None:
        all_val_temp = kc.get_vars(res.text,vars_from_res,vars_json_path)
        all_val.update(all_val_temp)

    # verify database and write back
    if sql_ex is not None:
        if sql_var is not None:   #use variable in sql query
            var_list = sql_var.split(';')
            var_list = [eval(var) for var in var_list]
            sql_actual_result = kc.dbCheck(sql_ex.format(*var_list))
        else:
            sql_actual_result = kc.dbCheck(sql_ex)

        if sql_expected is not None:
            if sql_actual_result == sql_expected:
                value ='pass'
            else:
                value ='failed'
            edit_excel_and_save(EXCEL_PATH,'Sheet1',row,23,value)
    # structure report
    if case_name is not None:
        allure.dynamic.title(case_name)
    if story is not None:
        allure.dynamic.story(story)
    if feature is None:
        allure.dynamic.feature(feature)
    if priority is not None:
        allure.dynamic.severity(priority)

