import os
import time
def child(name, indent):
   for i in range(10):
      print(f'{indent} {name} i={i}')
      time.sleep(0.1)
   os._exit(0)

def parent():
   indent = ""
   for name in ["proc1", "proc2", "proc3", "proc4"]:
      print(f'***> Starting {name}')
      newpid = os.fork()
      if newpid == 0:
         child(name, indent)
      indent += " "*15

   os.wait()

parent()
