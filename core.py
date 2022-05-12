import os,sys
import requests, re, base64, json
from bs4 import BeautifulSoup
global token
token="3s6v9y$B&E)H@McQfThWmZq4t7w!z%C*F-JaNdRgUkXn2r5u8x/A?D(G+KbPeSha"

if getattr(sys, 'frozen', False):
    program_directory = os.path.dirname(os.path.abspath(sys.executable))
else:
    program_directory = os.path.dirname(os.path.abspath(__file__))


def enctry(s):
    k = token
    encry_str = ""
    for i,j in zip(s,k):
        temp = str(ord(i)+ord(j))+'_'
        encry_str = encry_str + temp
    s1 = base64.b64encode(encry_str.encode("utf-8"))
    strs1 = bytes.decode(s1)
    return strs1
def dectry(s2str):
    s2 = str.encode(s2str)
    p = base64.b64decode(s2).decode("utf-8")
    k = token
    dec_str = ""
    for i,j in zip(p.split("_")[:-1],k):
        temp = chr(int(i) - ord(j))
        dec_str = dec_str+temp
    return dec_str

def getCurrentSession():
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36 OPR/79.0.4143.72'
    }

    session = requests.Session()
    a = session.get('http://192.168.242.254/login_online_detail.php', headers=headers)

    soup = BeautifulSoup(a.text, 'html.parser')
    ls =[i.text for i in soup.find_all("label")]
    data = soup.find("span", {"class": "topF"}).text.split(', 登入成功')[0]
    status = {
        'total': ls[8],
        'download': ls[9],
        'upload': ls[10],
        'LoginTime': ls[2]
    }
    return {'data':data,"status":status}

def login(account,password):
    login_data={
        'username':account,
        'userpwd':password
    }
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36 OPR/79.0.4143.72'
    }

    session = requests.Session()
    a = session.post('http://192.168.242.254/cgi-bin/ace_web_auth.cgi?web_jumpto=&orig_referer=', headers=headers, data = login_data)

    soup = BeautifulSoup(a.text, 'html.parser')
    redirMatch = re.match(r'.*?window\.location\s*=\s*\"([^"]+)\"', str(soup), re.M|re.S)
    if 'login_online_detail.php' in redirMatch.group(1):
        print('登入成功')
        return '登入成功'
    else:
        print('登入失敗')
        return '登入失敗'

def addUser(username,password):
    with open(F'{program_directory}\data.json',"r") as jsave:   
        data = json.load(jsave)
        user_exists = False
        for item in data["users"]:
            if username == item['username']:
                user_exists = True
                break
        if not user_exists:
            password_encrypted=enctry(password)
            user={"username": username, "password_encrypted": password_encrypted}
            data["users"].append(user)
        else:
            return "user already exists"
        print(data["users"])
    with open(F'{program_directory}\data.json',"w") as jsave:    
        json.dump(data, jsave)
def setDefault(index):
    with open(F'{program_directory}\data.json',"r") as jsave:   
        data = json.load(jsave)
        data["settings"]["selected_user"]=index
    with open(F'{program_directory}\data.json',"w") as jsave:    
        json.dump(data, jsave)
def rmUser(username):
    with open(F'{program_directory}\data.json',"r") as jsave:   
        data = json.load(jsave)
        for item in data["users"]:
            if username == item['username']:
                data["users"].remove(item)
                break
        print(data["users"])
    with open(F'{program_directory}\data.json',"w") as jsave:    
        json.dump(data, jsave)
def getUser(username):
    with open(F'{program_directory}\data.json',"r") as jsave:
        data = json.load(jsave)
        user={}
        for item in data["users"]:
            if username == item['username']:
                user={'username':item['username'],'password':dectry(item['password_encrypted'])}
                break
        return user
def getUsers():
    with open(F'{program_directory}\data.json',"r") as jsave:
        data = json.load(jsave)
        print(data["users"])
        return {'users':data["users"],'select':data["settings"]["selected_user"],'LoginOnBoot':data["settings"]["login_on_startup"]}

def onBoot():
    with open(F'{program_directory}\data.json',"r") as jsave:
        data = json.load(jsave)
        select = data["settings"]["selected_user"]
        if select == None:
            return "unselect"
    user=getUser(data['users'][select]['username'])
    login(user["username"],user["password"])

