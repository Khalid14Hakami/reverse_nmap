from registrar import *
from cmd import Cmd
 
class MyPrompt(Cmd):
    def do_exit(self, inp):
        print("Bye")
        return True

    def do_add(self, inp):
        print("Adding '{}'".format(inp))

    def do_list(self, inp):
        print(reg.get_workers())
        

    def do_run_test(self, inp):
        print(reg.get_workers())
 



if __name__ == "__main__":
    print("firing up rigestrar")
    reg = Registrar()
    registrar_process = reg.start()

    MyPrompt().cmdloop()
    print("after")
    registrar_process.join()

#    print (reg.checkstatus()) 
