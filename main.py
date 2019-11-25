from db import DB
from config import Config
import os,datetime

config = Config()

db = DB(config._host,config._port,config._db,config._user,config._password)

def get_table_comment():
    ''' 获取表注释 '''
    data = db.execQuery('''
    SELECT
	TABLE_COMMENT 
FROM
	information_schema.TABLES 
WHERE
	table_schema = '%s' 
	AND table_name = '%s'
    ''' % (config._db, config._table_name))
    return data.values[0][0]
    
table_comment = get_table_comment()


def get_table_fileds() :
    ''' 获取表字段 '''
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
    return(data)

#下划线转驼峰
def str2hump(text):
    arr = filter(None, text.lower().split('_'))
    res = ''
    j = 0
    for i in arr:
        res = res + i[0].upper() + i[1:]
        j += 1
    return res

def gen_model():
    fileds = get_table_fileds().values
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
        tpl = tpl.replace('$base_namespace',config._base_namespace)
        tpl = tpl.replace('$table_name',config._table_name)
        tpl = tpl.replace('$table_comment',table_comment)
        tpl = tpl.replace('$model_name',config._model_name)
        tpl = tpl.replace('$dir',config._dir)
        tpl = tpl.replace('$model_params',model_params)
        f.close()
        with open('gen/%s/%s.cs' % (config._dir,config._model_name),'w+',encoding='utf-8') as f:
            f.write(tpl)
            f.close()
def gen_dal():
    fileds = get_table_fileds().values

    keys = ''
    values = ''
    update_ext = ''
    spaces = ' ' * 38 

    for filed in fileds:
        keys += spaces
        values += spaces
        update_ext += spaces
        keys += '`%s`,\n' % (filed[0])

        if filed[2] == 'int':
            values += '@%s,\n' % filed[0]
            update_ext += '`%s` = @%s,\n' % (filed[0],filed[0])
        else:
            values += ''''@%s',\n''' % filed[0]
            update_ext += '''`%s` = '@%s',\n''' % (filed[0],filed[0])
    keys = keys[:-2]
    values = values[:-2]
    update_ext = update_ext[:-2]
    insert_sql = '''INSERT INTO `%s` (\n%s)  \n%sVALUES (\n%s)''' % (config._table_name, keys, spaces, values)
    update_sql = '''UPDATE `%s` SET 
%s 
%sWHERE `id` = @id''' % (config._table_name,update_ext,spaces)

    with open('tpls/dal.tpl','r',encoding='utf-8') as f:
        tpl = f.read()
        tpl = tpl.replace('$base_namespace',config._base_namespace)
        tpl = tpl.replace('$table_name',config._table_name)
        tpl = tpl.replace('$table_comment',table_comment)
        tpl = tpl.replace('$model_name',config._model_name)
        tpl = tpl.replace('$dir',config._dir)
        tpl = tpl.replace('$insert_sql',insert_sql)
        tpl = tpl.replace('$update_sql',update_sql)
        f.close()
        with open('gen/%s/%sDAL.cs' % (config._dir,config._model_name),'w+',encoding='utf-8') as f:
            f.write(tpl)
            f.close()
def gen_bll():
    with open('tpls/bll.tpl','r',encoding='utf-8') as f:
        tpl = f.read()
        tpl = tpl.replace('$base_namespace',config._base_namespace)
        tpl = tpl.replace('$model_name',config._model_name)
        tpl = tpl.replace('$dir',config._dir)
        f.close()
        with open('gen/%s/%sBLL.cs' % (config._dir,config._model_name),'w+',encoding='utf-8') as f:
            f.write(tpl)
            f.close()

def gen_factory():
    with open('tpls/factory.tpl','r',encoding='utf-8') as f:
        tpl = f.read()
        tpl = tpl.replace('$base_namespace',config._base_namespace)
        tpl = tpl.replace('$host',config._host)
        tpl = tpl.replace('$user',config._user)
        tpl = tpl.replace('$password',config._password)
        tpl = tpl.replace('$db',config._db)
        f.close()
        with open('gen/ConnectionFactory.cs','w+',encoding='utf-8') as f:
            f.write(tpl)
            f.close()









if __name__ == "__main__":
    module_dir = 'gen/%s' % config._dir
    try:
        os.makedirs(module_dir)
    except Exception as e:
        print(e)

    gen_model()
    print('model层生成完毕')
    gen_dal()
    print('dal层生成完毕')
    gen_bll()
    print('bll层生成完毕')
    gen_factory()
    print('factory生成完毕')
    print('success auther by luanshaofeng')

    pass