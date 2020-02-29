#!/usr/bin/env python3

def strCall(command):
    with open('bashcall.sh','w') as f:
        f.write("#!/bin/bash\n\n")
        f.write(command + '\n')
    execute()

def lstCall(command_list):
    with open('bashcall.sh','w') as f:
        f.write("#!/bin/bash\n\n")
        for command in command_list:
            f.write(command + '\n')
    execute()

def call(command):
    strCall(command)

def listCall(command_list):
    lstCall(command_list)


def execute():
    from subprocess import call
    import os
    call(['bash', 'bashcall.sh'])
    os.remove('bashcall.sh')