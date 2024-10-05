import os
import sys
def kill_port(port):
    try:
        port = int(port)
        cmd = f"kill -9 $(lsof -t -i:{port})"
        status = os.system(cmd)
        if status == 0:
            return True
        else:
            return False
            
            
    except:
        return False
        
try:
   port = sys.argv[1]
except:
    port = None 

if port != None:
    if kill_port(port):
        print("done")
    else:
        os.system("clear")
        print(f"Can't kill port {port}")
        

   
else:
    print("Usage: killPort `PORT`")