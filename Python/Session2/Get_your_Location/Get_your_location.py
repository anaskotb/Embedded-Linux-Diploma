import requests

def getIP():
    response=requests.get("https://api.ipify.org/?format=json")
    jsonBody=response.json()
    ip=jsonBody['ip']
    print(ip)
    return ip

def getLoation():
    ip1=getIP()
    new_response=requests.get(f"https://ipinfo.io/{ip1}/geo")
   
    print(new_response.json())


getLoation()
