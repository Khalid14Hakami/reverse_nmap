from registrar import *

print("File one __name__ is set to: {}" .format(__name__))



if __name__ == "__main__":
   print("firing up rigestrar")
   reg = Registrar()
   reg.start()

#    print (reg.checkstatus())
