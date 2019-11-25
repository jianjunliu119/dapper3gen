# -*- coding: utf-8 -*-
import configparser,codecs,re
class Config:
    __configdir = False
    def __init__(self, configdir=''):
        if not configdir.strip():
            self.__configdir = 'config.ini'
        else:
            self.__configdir = configdir
        self.RemoveBOM()
        # self.auto = 1
        self._host = self.GetStr('pub','host')
        self._user = self.GetStr('pub','user')
        self._password = self.GetStr('pub','password')
        self._db = self.GetStr('pub','db')
        self._port = self.GetInt('pub','port')
        self._base_namespace = self.GetStr('pub','base_namespace')
        self._model_name = self.GetStr('pub','model_name')
        self._table_name = self.GetStr('pub','table_name')
        self._dir = self.GetStr('pub','dir')
        return 
    def GetStr(self, section, option):
        cf = configparser.ConfigParser()
        try:
            cf.read(self.__configdir,encoding='utf-8')
            Ret = cf.get(section, option)
            return Ret
        except Exception:
            return ""


    #int
    def GetInt(self, section, option):
        cf = configparser.ConfigParser()
        try:
            cf.read(self.__configdir,encoding='utf-8')
            Ret = cf.getint(section, option)
            return Ret
        except Exception as e:
            print(option,e)
            return 0


    #float
    def GetFloat(self, section, option):
        cf = configparser.ConfigParser()
        try:
            cf.read(self.__configdir)
            Ret = cf.getfloat(section, option)
            return Ret
        except Exception:
            return 0


    #bool
    def GetBool(self, section, option):
        cf = configparser.ConfigParser()
        try:
            cf.read(self.__configdir,encoding='utf-8')
            Ret = cf.getboolean(section, option)
            return Ret
        except Exception:
            return False

    #修改数据
    def Update(self, section, option, value):
        value = str(value)
        cf = configparser.ConfigParser()
        try:
            cf.read(self.__configdir,encoding='utf-8')
            cf.set(section, option, value)
            cf.write(open(self.__configdir, "r+",encoding='utf-8'))
            return True
        except Exception as e:
            print(option,e,value)
            return False


    #添加数据
    def Add(self, section, option, value):
        cf = configparser.ConfigParser()
        try:
            cf.read(self.__configdir)
            cf.add_section(section)
            cf.set(section, option, value)
            cf.write(open(self.__configdir, "r+"))
            return True
        except Exception:
            return False
    def RemoveBOM(self):
        content = open(self.__configdir,encoding='utf-8').read()
        content = re.sub(r'\ufeff','',content)
        open(self.__configdir,'w',encoding='utf-8').write(content)

    
if __name__ == "__main__":
    config = Config()
    print(config._account1)
    pass