from db import DB
from config import Config
import os,datetime
import numpy as np
import pandas as pd
import configparser


#下划线转驼峰
def str2hump(text):
    arr = filter(None, text.lower().split('_'))
    res = ''
    j = 0
    for i in arr:
        res = res + i[0].upper() + i[1:]
        j += 1
    return res
def strbegin2low(text):
    res=''
    for i,v in enumerate(text):
        if i == 0:
            res += v.lower()
        else:
            res +=v
    return res
        
        


def gencs(classname=''):
    config = Config(classname=classname)
    print('%s开始生成三层 时间:%s' % (config._model_name,datetime.datetime.now()))
    module_dir_dal = 'gen/dal/%s' % config._dir
    module_dir_model = 'gen/model/%s' % config._dir
    module_dir_bll = 'gen/bll/%s' % config._dir
    try:
        os.makedirs(module_dir_bll)
        os.makedirs(module_dir_dal)
        os.makedirs(module_dir_model)
    except Exception:
        pass
        # print(e)
    db = DB(config._host,config._port,config._db,config._user,config._password)

    data = db.execQuery('''
    SELECT
	TABLE_COMMENT 
FROM
	information_schema.TABLES 
WHERE
	table_schema = '%s' 
	AND table_name = '%s'
    ''' % (config._db, config._table_name))

    table_comment = data.values[0][0]


    '''生成model'''
    data = db.execQuery('''
    SELECT
	COLUMN_NAME,
	column_comment ,
    data_type
FROM
	INFORMATION_SCHEMA.COLUMNS 
WHERE
	table_name = '%s' 
	AND table_schema = '%s'
    ''' % (config._table_name,config._db))
    for index,filed in enumerate(data.values):
        if filed[2].count('char'):
            data.values[index][2] = 'string'

        if filed[2].count('int'):
            data.values[index][2] = 'int'

        if filed[2].count('time'):
            data.values[index][2] = 'DateTime'
    fileds = data.values
    model_params = ''
    for filed in fileds:
        model_params += '\n'
        if filed[1] != '':
            model_params += '''        /// <summary>
        /// %s 
        /// </summary>\n''' % filed[1]
        
        model_params += '        public %s %s { get; set; }\n' % (filed[2],str2hump(filed[0]))
    
    with open('tpls/model.tpl','r',encoding='utf-8') as f:
        tpl = f.read()
        tpl = tpl.replace('$solution_name',config._solution_name)
        tpl = tpl.replace('$project_name',config._project_name)
        tpl = tpl.replace('$table_name',config._table_name)
        tpl = tpl.replace('$table_comment',table_comment)
        tpl = tpl.replace('$model_name',config._model_name)
        tpl = tpl.replace('$dir',config._dir)
        tpl = tpl.replace('$model_params',model_params)
        f.close()
        with open('gen/model/%s/%s.cs' % (config._dir,config._model_name),'w+',encoding='utf-8') as f:
            f.write(tpl)
            f.close()
    '''生成dal'''
    # fileds = get_table_fileds().values

    keys = ''
    values = ''
    update_ext = ''
    spaces = ''  

    for filed in fileds:
        keys += spaces
        values += spaces
        update_ext += spaces
        if config._isautonumid:
            if filed[0] == "id":
                continue
            
        keys += '`%s`,' % (filed[0])

        # if filed[2] == 'int':
        values += '@%s,' % str2hump(filed[0])
        update_ext += '`%s` = @%s,' % (filed[0], str2hump(filed[0]))
        # else:
            # values += ''''@%s',\n''' % str2hump(filed[0])
            # update_ext += '''`%s` = '@%s',\n''' % (filed[0],str2hump(filed[0]))
    keys = keys[:-1]
    values = values[:-1]
    update_ext = update_ext[:-1]
    insert_sql = '''INSERT INTO `%s` (\n%s)  \n%sVALUES (\n%s)''' % (config._table_name, keys, spaces, values)
    update_sql = '''UPDATE `%s` SET 
%s 
%sWHERE `id` = @id''' % (config._table_name,update_ext,spaces)

    with open('tpls/dal.tpl','r',encoding='utf-8') as f:
        tpl = f.read()
        tpl = tpl.replace('$solution_name',config._solution_name)
        tpl = tpl.replace('$project_name',config._project_name)
        tpl = tpl.replace('$table_name',config._table_name)
        tpl = tpl.replace('$table_comment',table_comment)
        tpl = tpl.replace('$model_name_low',strbegin2low(config._model_name))
        tpl = tpl.replace('$model_name',config._model_name)
        tpl = tpl.replace('$dir',config._dir)
        tpl = tpl.replace('$insert_sql',insert_sql)
        tpl = tpl.replace('$update_sql',update_sql)
        f.close()
        with open('gen/dal/%s/%sDAL.cs' % (config._dir,config._model_name),'w+',encoding='utf-8') as f:
            f.write(tpl)
            f.close()
            '''生成bll'''
    with open('tpls/bll.tpl','r',encoding='utf-8') as f:
        tpl = f.read()
        tpl = tpl.replace('$solution_name',config._solution_name)
        tpl = tpl.replace('$project_name',config._project_name)
        tpl = tpl.replace('$model_name',config._model_name)
        tpl = tpl.replace('$dir',config._dir)
        f.close()
        with open('gen/bll/%s/%sBLL.cs' % (config._dir,config._model_name),'w+',encoding='utf-8') as f:
            f.write(tpl)
            f.close()

            '''生成factory'''
    with open('tpls/factory.tpl','r',encoding='utf-8') as f:
        tpl = f.read()
        tpl = tpl.replace('$solution_name',config._solution_name)
        tpl = tpl.replace('$project_name',config._project_name)
        tpl = tpl.replace('$host',config._host)
        tpl = tpl.replace('$user',config._user)
        tpl = tpl.replace('$password',config._password)
        tpl = tpl.replace('$db',config._db)
        f.close()
        with open('gen/ConnectionFactory.cs','w+',encoding='utf-8') as f:
            f.write(tpl)
            f.close()

    '''生成分分页对象'''
    with open('tpls/pagedata.tpl','r',encoding='utf-8') as f:
        tpl = f.read()
        tpl = tpl.replace('$solution_name',config._solution_name)
        tpl = tpl.replace('$project_name',config._project_name)
        f.close()
        with open('gen/PageData.cs','w+',encoding='utf-8') as f:
            f.write(tpl)
            f.close()

    print('%s生成三层完成 时间:%s' % (config._model_name,datetime.datetime.now()))
    



def gendb(classname='',xlsxpath=''):

    config = Config(classname=classname)
    db = DB(config._host,config._port,config._db,config._user,config._password)
    
    # 机构类型 1:起升机构 2:小车机构 3
    
    df = pd.read_excel(config._xlsxpath,sheet_name=config._sheet,keep_default_na=False)

    # print(df[2:].values)

    print('%s表结构生成开始 时间:%s' % (config._table_name,datetime.datetime.now()))
    tablename = config._table_name
    
    sqlstr = 'CREATE TABLE `'+ tablename +'`  ('
    
    fstr = ''
    
    for index,row in df[3:].iterrows():
        co = ''
        de = ''
        at = ''
        if row[6] != '':
            co = row[6]
    
        if row[3] != '':
           de ='DEFAULT '+row[3]

    
        if row[5]!='':
           at = 'NOT NULL ' + row[5]
    
        fstr += '`'+row[1]+'` ' + row[2] +' '+ de +' '+ at +' COMMENT "'+ row[0] + co+'",'
    sqlstr += fstr+ '  PRIMARY KEY (`id`)) COMMENT = "'+ classname +'"'
    delstr = 'drop table if exists `'+tablename+'`;'
    # print(sqlstr)
    db.exec(delstr)
    db.exec(sqlstr)

    print('%s表结构生成结束 时间:%s' %(config._table_name,datetime.datetime.now()))










if __name__ == "__main__":

    xlsxpath = 'E:\项目\起重机管理系统20191114\HDCraneCIMS2\document\数据库设计.xlsx'
    
    cf = configparser.ConfigParser()
    cf.read('config.ini',encoding='utf-8')
    i = 0
    for sl in cf._sections:
        i += 1
        if sl != 'pub':
            print("#"*20)
            gendb(classname=sl,xlsxpath=xlsxpath)
            gencs(sl)
            print("#"*20)