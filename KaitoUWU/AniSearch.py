import requests, json
import urllib.parse as parse
from saucenao_api import SauceNao

API = "https://api.trace.moe/search?anilistInfo&url={}"
class ConvertError(Exception):
    pass
class InputError(Exception):
    pass
class SearchError(Exception):
    pass

def pathtl(path:str) -> str:
    forbiden = '?|/\<>"*:'
    for f in forbiden:
        if f in path: path = path.replace(f, "-")
    return path

class TraceMoe():
    class Syncro():
        def __init__(self, link=None, debug=False):
            self.link = link
            self.dbug = debug
            self.result = None
            self.raw = None

        def checkerror(self, item:dict):
            if len(item["error"]) >= 1:
                raise SearchError(item["error"])
            
        def search(self, link=None) -> dict:
            if link == None:
                if self.link != None:
                    link = self.link
                else: raise InputError("No input link.")
            if self.dbug: print("search")
            conv = parse.quote_plus(link)
            search = requests.get(API.format(conv)).json()
            self.checkerror(search)
            self.raw = search
            self.result = self.Filter(search)
            if self.dbug: print("done")
            return self.result

        def Filter(self, result):
            raw = result.copy()
            ids = []
            cache = []
            res = raw["result"]
            for r in res:
                if r["anilist"]["id"] not in ids:
                    cache.append(r)
                    ids.append(r["anilist"]["id"])
            raw["result"] = cache
            return raw
            

        def JSON(self, link=None, item:dict=None):
            target = None
            if item != None: target = item
            else: target = self.result
            if self.result != None:
                conv = json.dumps(target, ensure_ascii=False, indent=3)
                return conv
            else: raise ConvertError("search has not been called")

        def DUMP(self, path, item:dict=None):
            target = None
            if item != None: target = item
            else: target = self.result
            if self.result != None:
                with open(path, "w", encoding="utf8") as F:
                    conv = json.dump(target, F, ensure_ascii=False, indent=3)
                return path
            else: raise ConvertError("search has not been called")
                
    class Asyncro():
        def __init__(self, link=None, debug=False):
            self.link = link
            self.dbug = debug
            self.result = None
            self.raw = None

        def checkerror(self, item:dict):
            if len(item["error"]) >= 1:
                raise SearchError(item["error"])
            
        async def search(self, link=None) -> dict:
            if link == None:
                if self.link != None:
                    link = self.link
                else: raise InputError("No input link.")
            if self.dbug: print("search")
            conv = parse.quote_plus(link)
            search = requests.get(API.format(conv)).json()
            self.checkerror(search)
            self.raw = search
            self.result = self.Filter(search)
            if self.dbug: print("done")
            return self.result

        def Filter(self, result):
            raw = result.copy()
            ids = []
            cache = []
            res = raw["result"]
            for r in res:
                if r["anilist"]["id"] not in ids:
                    cache.append(r)
                    ids.append(r["anilist"]["id"])
            raw["result"] = cache
            return raw
            

        def JSON(self, link=None, item:dict=None):
            target = None
            if item != None: target = item
            else: target = self.result
            if self.result != None:
                conv = json.dumps(target, ensure_ascii=False, indent=3)
                return conv
            else: raise ConvertError("search has not been called")

        def DUMP(self, path, item:dict=None):
            target = None
            if item != None: target = item
            else: target = self.result
            if self.result != None:
                with open(path, "w", encoding="utf8") as F:
                    conv = json.dump(target, F, ensure_ascii=False, indent=3)
                return path
            else: raise ConvertError("search has not been called")        
        
if __name__ == "__main__":
    engine = TraceMoe.Syncro()
    find = engine.search("https://cdn.discordapp.com/attachments/922500802566844447/963314849276899338/vlcsnap-2022-04-02-00h53m00s493.png")
    print(len(engine.result["result"]), len(engine.raw["result"]))
    print(engine.DUMP("sample.json"))
    
