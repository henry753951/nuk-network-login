import eel,os,winshell,sys
import core,json
import argparse
parser = argparse.ArgumentParser(description='NUK網路自動登入')
parser.add_argument("--onBoot", type=int, default=0)
args = parser.parse_args()

if getattr(sys, 'frozen', False):
    program_directory = os.path.dirname(os.path.abspath(sys.executable))
else:
    program_directory = os.path.dirname(os.path.abspath(__file__))


def app():
    print(F'{os.getcwd()}\web')
    eel.init(F'{os.getcwd()}\web')
    @eel.expose
    def getUsers():
        return core.getUsers()
    @eel.expose
    def login(username):
        user=core.getUser(username)
        r = core.login(user["username"],user["password"])
        return {'msg':r}
    @eel.expose
    def setDefault(index):
        core.setDefault(index)
        return {'msg':'設定成功'}
    @eel.expose
    def addUser(username,password):
        core.addUser(username,password)
        return {'msg':'新增成功'}
    @eel.expose
    def rmUser(username):
        core.rmUser(username)
        return {'msg':'刪除成功'}
    @eel.expose
    def getCurrentSession():
        r = core.getCurrentSession()
        return r
    @eel.expose
    def switchRunOnBoot(sw):
        with open(F'{program_directory}\data.json',"r") as jsave:   
                data = json.load(jsave)
                data['settings']['login_on_startup']=sw
        with open(F'{program_directory}\data.json',"w") as jsave:    
            json.dump(data, jsave)

        def delete_shortcut_from_startup():  
            target = sys.argv[0]  
            s = os.path.basename(target)  
            fname = os.path.splitext(s)[0]  
            delfile = os.path.join(winshell.startup(), fname + '.lnk')  
            winshell.delete_file(delfile) 
        def create_shortcut_to_startup():  
            target = sys.argv[0]  
            title = 'nuk-net-auto-connect'
            s = os.path.basename(target)  
            fname = os.path.splitext(s)[0]  
            winshell.CreateShortcut(  
            Path = os.path.join(winshell.startup(),   
            fname + '.lnk'),  
            Target = target,
            Arguments = "--onBoot 1",
            Icon=(target, 0),  
            Description=title) 
        if sw :
            create_shortcut_to_startup()
        else:
            delete_shortcut_from_startup()



if __name__ == "__main__":
    if args.onBoot == 0:
        app()
        eel.start('',mode='chrome',size= (900, 700))
    else:
        core.onBoot()