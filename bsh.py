#!/bin/python3.8
import os
def bsh_loop():
    print("bsh: bloated shell, written by null during study hall")
    status = 1
    while(status):
        print("bsh_lite?> ", end="")
        args = input().split()
        status = bsh_exec(args)
def bsh_start(args):
    pid = os.fork()
    if(pid == 0): os.execvp(args[0], args)
    else: os.waitpid(0, 0)
    return 1
def bsh_exec(args):
    if(args[0] == "cd"):
        os.chdir(args[1])
        return 1
    elif(args[0] == "info"):
        print("why yes, bsh is a 30 LOC shell written in python, what of it?")
        print("ctoddlers eternally BTFO, all I had to do was: import shell, shell.run()")
        return 1
    elif (args == []): return 1
    elif (args[0] == "exit"): return 0
    try: return bsh_start(args)
    except:
        print("error, idk what you tried to do but it din work lol")
        return 1
bsh_loop()
