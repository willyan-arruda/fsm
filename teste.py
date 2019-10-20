import _thread
import threading
import time

def worker(message, x):
    for i in range(5):
       print (message, x)
       time.sleep(1)


for i in range(5):
	variavel = 'processo'+ str(i)
	teste = "thread em execu"
	variavel = threading.Thread(target=worker,args=(teste, i))
	variavel.start()




while variavel.isAlive():
    print ("Aguardando thread")
    time.sleep(5)
 
print ("Thread morreu")
print ("Finalizando programa")