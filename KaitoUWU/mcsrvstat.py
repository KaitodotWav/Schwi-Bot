import requests, json
from mcstatus import MinecraftServer as MCjava
from mcstatus import MinecraftBedrockServer as MCbe

jlink = "https://api.mcsrvstat.us/2/<address>"
blink = "https://api.mcsrvstat.us/bedrock/2/<address>"

class FetchError(Exception):
    pass

class AMCstat():
    def __init__(self, platform=None):
        self.plat = platform

    async def Jping(self, ip, mode="json"):
        server = MCjava.lookup(ip)
        res = server.query()
        return res

class Mcsrv():
    def __init__(self, platform):
        self.plat = str(platform)
        self.link = None
        if self.plat == "java":
            self.link = jlink
        elif self.plat == "bedrock":
            self.link = blink
        self.respond = None
        self.result = None

    def ping(self, ip):
        try:
            sent = requests.get(self.link.replace("<address>", str(ip)))
            self.respond = sent.text
            self.result = json.loads(sent.text)
            return sent.text
        
        except json.decoder.JSONDecodeError as e:
            raise FetchError(self.respond)
        

    def dump(self, Dir):
        with open(f"{Dir}", "w", encoding="utf8") as F:
            json.dump(self.result, F, ensure_ascii=False, indent=4)

    
        
if __name__ == "__main__":
    a = Mcsrv("java")
    try:
        a.ping("aaternoo.aternos.me")
    except FetchError as e:
        print(e)
    print(a.result)
    
    
    
