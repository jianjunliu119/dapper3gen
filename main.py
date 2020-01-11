# -*- coding: utf-8 -*-
from db import DB
from config import Config
import os, datetime,shutil
import numpy as np
import pandas as pd
import configparser


def str2hump(text):
    """下划线转驼峰"""
    arr = filter(None, text.lower().split('_'))
    res = ''
    j = 0
    for i in arr:
        res = res + i[0].upper() + i[1:]
        j += 1
    return res


def strbegin2low(text):
    """字符串首字母转小写"""
    res = ''
    for i, v in enumerate(text):
        if i == 0:
            res += v.lower()
        else:
            res += v
    return res


def gencs(classname=''):
    """生成三层"""
    config = Config(classname=classname)
    print('%s开始生成三层 时间:%s' % (config._model_name, datetime.datetime.now()))
    module_dir_dal = 'gen\\dal\\%s' % config._dir
    module_dir_model = 'gen\\model\\%s' % config._dir
    module_dir_grid = 'gen\\datagrid\\%s' % config._dir
    module_dir_bll = 'gen\\bll\\%s' % config._dir
    # try:
    #     shutil.rmtree(os.getcwd() +'\\'+module_dir_grid)
    # except Exception as e:
    #     pass
    # try:
    #     shutil.rmtree(os.getcwd() +'\\'+module_dir_bll)
    # except Exception as e:
    #     pass
    # try:

    #     shutil.rmtree(os.getcwd() +'\\'+module_dir_dal)

    # except Exception as e:
    #     pass
    # try:
    #     shutil.rmtree(os.getcwd() +'\\'+module_dir_model)
    # except Exception as e:
    #     pass
    try:
        os.makedirs(module_dir_grid)
    except Exception as e:
        pass
    try:
        os.makedirs(module_dir_bll)
    except Exception as e:
        pass
    try:

        os.makedirs(module_dir_dal)

    except Exception as e:
        pass
    try:

        os.makedirs(module_dir_model)

    except Exception as e:
        pass

    except Exception as e:
        print(e)
        pass
    db = DB(config._host, config._port, config._db, config._user,
            config._password)

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
    data_type,
    data_type
FROM
	INFORMATION_SCHEMA.COLUMNS 
WHERE
	table_name = '%s' 
	AND table_schema = '%s'
    ''' % (config._table_name, config._db))
    for index, filed in enumerate(data.values):
        if filed[2].count('char'):
            data.values[index][2] = 'string'

        # if filed[2].count('int'):
            # data.values[index][2] = 'int'
        if filed[2] == 'tinyint':
            data.values[index][2] = 'bool'

        if filed[2].count('time'):
            data.values[index][2] = 'DateTime'

        if filed[2] == 'float':
            data.values[index][2] = 'float'
        
    fileds = data.values
    model_params = ''
    mapper_params=''
    grid_colls = ''
    mec_type = 0

    for index,filed in enumerate(fileds):
        model_params += '\n'
        if filed[1] != '':
            model_params += '''        /// <summary>
        /// %s 
        /// </summary>\n''' % filed[1]

        model_params += '        public %s %s { get; set; }\n' % (
            filed[2], str2hump(filed[0]))
        if '_' in filed[0]:

            mapper_params += '\n'

            mapper_params += '            Map(f => f.%s).Column("%s");' % (str2hump(filed[0]),filed[0])


        has_add = 0
        if config._table_name == 'datapoint':
            if 'V' in filed[0]:
                ssql = 'select * from var_dict where var_code = "' + filed[0] +'"'
                data2 = db.execQuery(ssql)
                mec_type = int(data2['mec_type'][0])
                fileds[index][2] = mec_type
                # fileds[index].append(int(data2['date_type'][0]))
                print(fileds[index])
        binding_str = str2hump(filed[0])
        header_str = filed[1]
        col_datetype = filed[2]
        if filed[0] == 'id':
            header_str = '编号'
        
        if col_datetype == 'bool':
            binding_str += ',Converter={StaticResource cvtSwitch}'
        if binding_str == 'CreateTime':
            binding_str +=',Converter={StaticResource cvtDateTime}' 

        grid_colls +='''\n        <DataGridTextColumn Header="'''+ header_str +'''" Binding="{Binding '''+ binding_str +'''}"></DataGridTextColumn>'''




    if config._table_name == 'datapoint':
        arr = []
        for i in range(1,7):
            arr1 = []
            for j in fileds:
                if j[2] ==i:
                    arr1.append(j)
            arr.append(arr1)
            print( arr) 

        for i,v in enumerate(arr):
            file_names = ['MainHoist.xml','ViceHoist.xml','BigCar.xml','MainCar.xml','ViceCar.xml','PowerDistribution.xml']

            data_grid = '''<DataGrid x:Name=\"dataGrid\" Height=\"600\" ItemsSource=\"{Binding}\" CanUserAddRows=\"False\" AutoGenerateColumns=\"False\"> 
    <DataGrid.Columns>
        <DataGridTextColumn Header="编号" Binding="{Binding Id}"></DataGridTextColumn> '''
            for j in v:

                converter_str =''
                print(j[3])
                if j[3] == 'tinyint':
                    converter_str = ',Converter={StaticResource cvtSwitch}'
                data_grid +='''\n        <DataGridTextColumn Header="'''+ j[1] +'''" Binding="{Binding '''+ str2hump(j[0])+converter_str+'''}"></DataGridTextColumn>'''
            data_grid +='''\n        <DataGridTextColumn Header="创建时间" Binding="{Binding CreateTime,Converter={StaticResource cvtDateTime}}"></DataGridTextColumn>'''
            data_grid +='''
     </DataGrid.Columns> 
</DataGrid>'''
            with open('gen/datagrid/%s/%s.xml' % (config._dir, file_names[i]),
                          'w+',
                          encoding='utf-8') as f:
                f.write(data_grid)
                f.close()
        model_params += '''        public bool ConnectionState { get; set; }
        public string SystempDataTime { get; set; }
        public int ConnectionDelay { get; set; }'''




    with open('tpls/model.tpl', 'r', encoding='utf-8') as f:
        tpl = f.read()
        tpl = tpl.replace('$solution_name', config._solution_name)
        tpl = tpl.replace('$project_name', config._project_name)
        tpl = tpl.replace('$table_name', config._table_name)
        tpl = tpl.replace('$table_comment', table_comment)
        tpl = tpl.replace('$model_name', config._model_name)
        tpl = tpl.replace('$dir', config._dir)
        tpl = tpl.replace('$model_params', model_params)
        tpl = tpl.replace('$mapper_params', mapper_params)
        f.close()
        with open('gen/model/%s/%s.cs' % (config._dir, config._model_name),
                  'w+',
                  encoding='utf-8') as f:
            f.write(tpl)
            f.close()

    data_grid = '''
<DataGrid 
           Width="1680" 
           Height="580"
           HeadersVisibility="Column"
           ItemsSource="{Binding}" 
           CanUserAddRows="False" 
           AutoGenerateColumns="False" 
           Style="{DynamicResource DataGridStyle1}" 
           ColumnHeaderStyle="{DynamicResource DataGridColumnHeaderStyle2}" 
           RowStyle="{DynamicResource DataGridRowStyle1}" 
           CellStyle="{DynamicResource DataGridCellStyle1}" >
    <DataGrid.Columns>'''
    data_grid += grid_colls
    data_grid +='''
     </DataGrid.Columns> 
</DataGrid>'''

    data_grid +='''
    <Page.Resources>
        <cvt:SwitchConverter x:Key="SwitchConverter"/>
          <cvt:DateTimeConverter x:Key="dateTimeConverter"/>
    </Page.Resources>
      xmlns:cvt="clr-namespace:HDCraneCIMS.IPC.Desk.Converter"
    '''
    with open('gen/datagrid/%s/%s.xml' % (config._dir, config._model_name),
                  'w+',
                  encoding='utf-8') as f:
            f.write(data_grid)
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
    insert_sql = '''INSERT INTO `%s` (\n%s)  \n%sVALUES (\n%s)''' % (
        config._table_name, keys, spaces, values)
    update_sql = '''UPDATE `%s` SET 
%s 
%sWHERE `id` = @id''' % (config._table_name, update_ext, spaces)

    with open('tpls/dal.tpl', 'r', encoding='utf-8') as f:
        tpl = f.read()
        tpl = tpl.replace('$solution_name', config._solution_name)
        tpl = tpl.replace('$project_name', config._project_name)
        tpl = tpl.replace('$table_name', config._table_name)
        tpl = tpl.replace('$table_comment', table_comment)
        tpl = tpl.replace('$model_name_low', strbegin2low(config._model_name))
        tpl = tpl.replace('$model_name', config._model_name)
        tpl = tpl.replace('$dir', config._dir)
        tpl = tpl.replace('$insert_sql', insert_sql)
        tpl = tpl.replace('$update_sql', update_sql)
        f.close()
        with open('gen/dal/%s/%sDAL.cs' % (config._dir, config._model_name),
                  'w+',
                  encoding='utf-8') as f:
            f.write(tpl)
            f.close()
            '''生成bll'''

   

    with open('tpls/bll.tpl', 'r', encoding='utf-8') as f:
        tpl = f.read()
        tpl = tpl.replace('$solution_name', config._solution_name)
        tpl = tpl.replace('$project_name', config._project_name)
        tpl = tpl.replace('$model_name', config._model_name)
        tpl = tpl.replace('$dir', config._dir)
        f.close()
        with open('gen/bll/%s/%sBLL.cs' % (config._dir, config._model_name),
                  'w+',
                  encoding='utf-8') as f:
            f.write(tpl)
            f.close()
            '''生成factory'''
    with open('tpls/factory.tpl', 'r', encoding='utf-8') as f:
        tpl = f.read()
        tpl = tpl.replace('$solution_name', config._solution_name)
        tpl = tpl.replace('$project_name', config._project_name)
        tpl = tpl.replace('$host', config._host)
        tpl = tpl.replace('$user', config._user)
        tpl = tpl.replace('$password', config._password)
        tpl = tpl.replace('$db', config._db)
        f.close()
        with open('gen/ConnectionFactory.cs', 'w+', encoding='utf-8') as f:
            f.write(tpl)
            f.close()
    '''生成分分页对象'''
    with open('tpls/pagedata.tpl', 'r', encoding='utf-8') as f:
        tpl = f.read()
        tpl = tpl.replace('$solution_name', config._solution_name)
        tpl = tpl.replace('$project_name', config._project_name)
        f.close()
        with open('gen/PageData.cs', 'w+', encoding='utf-8') as f:
            f.write(tpl)
            f.close()

    print('%s生成三层完成 时间:%s' % (config._model_name, datetime.datetime.now()))


def gendb(classname='', xlsxpath=''):

    config = Config(classname=classname)
    if config._sheet == '':
        return
    db = DB(config._host, config._port, config._db, config._user,
            config._password)

    # 机构类型 1:起升机构 2:小车机构 3

    df = pd.read_excel(config._xlsxpath,
                       sheet_name=config._sheet,
                       keep_default_na=False)

    # print(df[2:].values)

    print('创建表：[%s] 时间 %s' % (config._table_name, datetime.datetime.now()))
    tablename = config._table_name

    sqlstr = 'CREATE TABLE `' + tablename + '`  ('

    fstr = ''
    fields =''
    field_types = []

    for index, row in df[3:].iterrows():
        if row[1] != 'id':
            fields += '`'+row[1] + '`,'
            field_types.append(row[2])
        co = ''
        de = ''
        at = ''
        if row[6] != '':
            co = row[6]

        if row[3] != '':
            de = 'DEFAULT ' + row[3]

        if row[5] != '':
            at = 'NOT NULL ' + row[5]

        fstr += '`' + row[1] + '` ' + row[
            2] + ' ' + de + ' ' + at + ' COMMENT "' + row[0] +' '+ co + '",'
    sqlstr += fstr + '  PRIMARY KEY (`id`)) COMMENT = "' + classname + '"'
    delstr = 'drop table if exists `' + tablename + '`;'

    try:
        db.exec(delstr)
    except Exception as e:
        print('删除表错误： %s \n %s' (e,delstr))
    try:

        db.exec(sqlstr)
    except Exception as e:
        print('创建表错误: %s \n %s' (e,sqlstr))
    fields = fields[:-1]
    if config._sheet == '变量名字典表':
        df1 = pd.read_excel(config._xlsxpath,
            sheet_name=config._data_sheet,
            keep_default_na=False)
        i = 0

        fields2 = []
        field2_types = []
        field2_comments = []
        field2_mec_types = []

        for index, row in df1.iterrows():
            values = ''
            for index1,col in enumerate(row):
                if index1 == 0:
                    fields2.append(col)

                if index1 == 1:
                    field2_comments.append(col)
                if index1 == 2:
                    field2_mec_types.append(col)


                if index1 == 3:
                    if col == 1:
                        field2_types.append('tinyint(1)')
                    else:
                        field2_types.append('varchar(50)')
                field_type = field_types[index1+1]
                if 'varchar' in field_type:
                    col = '"'+str(col)+'"'

                if str(col) == '' or str(col) == "":
                    col = 'NULL'
                values += str(col) +','
            values = values[:-1]
            print('#' * 10)
            insert_sql = 'INSERT INTO `crane_ipc`.`'+ tablename +'` (' + fields +') VALUES(now(),'+ values +')'
            db.exec(insert_sql)

        '''开始创建数据点数据表'''
        create_sql2_arr = []
        table_comments = ['主起升','副起升','大车','主小车','副小车','配电']

        for j in range(1,7):
            dp_table_name = config._datapoint_table_name+'_'+ str(j)
            delstr = 'drop table if exists `' + dp_table_name + '`;'
            create_sql2 = 'CREATE TABLE `' + dp_table_name + '`  (`id` int(11) NOT NULL AUTO_INCREMENT,`create_time` datetime(0) DEFAULT now() COMMENT "创建时间",'

            for i,f in enumerate(fields2):
                if field2_mec_types[i] == j:
                    create_sql2 += '`'+ f +'` '+ field2_types[i] + ' COMMENT "' + field2_comments[i] +'",\n'
            create_sql2 +=  '  PRIMARY KEY (`id`)) COMMENT = "'+ table_comments[j-1]+'"'
            print('#' * 20)
            print(create_sql2)

            db.exec(delstr)
            db.exec(create_sql2)
                

            

        delstr = 'drop table if exists `' + config._datapoint_table_name + '`;'

        create_sql2 = 'CREATE TABLE `' + config._datapoint_table_name + '`  (`id` int(11) NOT NULL AUTO_INCREMENT,`create_time` datetime(0) DEFAULT now() COMMENT "创建时间",'

        for i,f in enumerate(fields2):
            create_sql2 += '`'+ f +'` '+ field2_types[i] + ' COMMENT "' + field2_comments[i] +'",\n'

        create_sql2 +=  '  PRIMARY KEY (`id`)) COMMENT = "数据点总汇表"'
        create_sql2 = create_sql2

        db.exec(delstr)
        db.exec(create_sql2)

        


        

        pass

    print('%s表结构生成结束 时间:%s' % (config._table_name, datetime.datetime.now()))


if __name__ == "__main__":
    print('start')

    xlsxpath = 'E:\projects\HDCraneCIMS20191114\HDCraneCIMS2\document\数据库设计.xlsx'

    cf = configparser.ConfigParser()
    cf.read('config.ini', encoding='utf-8')
    i = 0
    for sl in cf._sections:
        i += 1
        if sl != 'pub':
            print("#" * 20)
            #gendb(classname=sl, xlsxpath=xlsxpath)
            gencs(sl)
            print("#" * 20)
