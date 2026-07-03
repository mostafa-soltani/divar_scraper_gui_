import json


class save_and_load_json:

    def save(self,database,data,type = 'a',encoding = 'utf-8'):
        with open(database,type,newline='',encoding=encoding) as handle:
            json.dump(data,handle,ensure_ascii=False,indent=3)

    def load(self,database,encoding = 'utf-8') :
        with open(database,'r',newline='',encoding=encoding) as handle:
            data = json.load(handle)

        return data