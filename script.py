import os
import time
from absl import app
from absl import flags

FLAGS = flags.FLAGS

flags.DEFINE_enum('task', None, ['start', 'stop','create','remove','list', 'destroy'], 'Task to do')
flags.DEFINE_integer('number', None, 'Number of instance')

def getIP(id):
    cmd = f"pct exec {id}"+" -- ip addr | grep eth0 | grep inet | awk '{print $2}'"
    ip = os.popen(cmd).read()
    return ip

def startLxc(id):
    cmd = f"pct start {id}"
    out = os.system(cmd)
    return out

def stopLxc(id):
    cmd = f"pct stop {id}"
    out = os.system(cmd)
    return out

def clone(id, newId):
    cmd = f"pct clone {id} {newId} --full --storage LXC"
    out = os.popen(cmd).read()
    return out

def list():
    cmd = 'pct list | grep "[2-9][0-9]"'
    out = os.popen(cmd).read()
    return out

def remove(id):
    cmd = f"pct destroy {id}"
    out = os.system(cmd)
    return out

def banner():
    TGREEN =  '\033[33m'
    TBLUE = '\033[36m'
    ENDC = '\033[m'
    print(TGREEN + """\

    ~         ~~          __
           _T      .,,.    ~--~ ^^
     ^^   // \                    ~
          ][O]    ^^      ,-~ ~
       /''-I_I         _II____
    __/_  /   \ ______/ ''   /'\_,__
      | II--'''' \,--:--..,_/,.-{ },
    ; '/__\,.--';|   |[] .-.| O{ _ }
    :' |  | []  -|   ''--:.;[,.'\,/
    '  |[]|,.--'' '',   ''-,.    |
      ..    ..-''    ;       ''. '

  """, ENDC)

    print(TBLUE + """\
  ____       _
 |  _ \ ___ | |_ ___ _ __  _ __ ___   _____  __
 | |_) / _ \| __/ _ \ '_ \| '_ ` _ \ / _ \ \/ /
 |  _ < (_) | ||  __/ | | | | | | | | (_) >  <
 |_| \_\___/ \__\___|_| |_|_| |_| |_|\___/_/\_\\\


 A python tool to manage lxc container on Proxmox

    """, ENDC)

def main(ARGV):
    pentesterlab = 103
    attacking = 102

    banner()


    if FLAGS.task == None:
        print("Invalid argument. Use --help to show help")
        return
    if FLAGS.task == "list":
        print("Listing all containers :")
        out = list()
        print(out)
        return
    if FLAGS.number == None:
        print("Invalid argument")
        return
    if FLAGS.task == "start":
        print("\n==Start some pentesterlabs==")
        for x in range(200,200+FLAGS.number):
            out = startLxc(x)
            #Wait for dhcp
            time.sleep(7)
            ip = getIP(x)
            if out == 0:
                print(f"ID : {x} IP : {ip}".rstrip())
                print("Username: root   Password: Pa$$w0rd")
            else:
                print(f'Error starting container {x}')


        print("\n==Start some attacking machines==")
        for x in range(300,300+FLAGS.number):
            out = startLxc(x)
            #Wait for dhcp
            time.sleep(7)
            ip = getIP(x)
            if out == 0:
                print(f"ID : {x} IP : {ip}".rstrip())
                print("Username: root   Password: Pa$$w0rd")
            else:
                print(f'Error starting container {x}')
        return
    if FLAGS.task == "stop":
        print("\n==Stop some pentesterlabs==")
        for x in range(200,200+FLAGS.number):
            out = stopLxc(x)
            if out == 0:
                print(f"ID : {x} Stopped")
            else:
                print(f'Error stopping container {x}')

        print("\n==Stop some attacking machines==")
        for x in range(300,300+FLAGS.number):
            out = stopLxc(x)
            if out == 0:
                print(f"ID : {x} Stopped")
            else:
                print(f'Error stopping container {x}')
        return
    if FLAGS.task == "create":
        print("\n==Creating some pentesterlabs==")
        for x in range(200,200+FLAGS.number):
            out = clone(pentesterlab,x)
            print(f"ID : {x} Created")

        print("\n==Start some pentesterlabs==")
        for x in range(200,200+FLAGS.number):
            out = startLxc(x)
            #Wait for dhcp
            time.sleep(7)
            ip = getIP(x)
            if out == 0:
                print(f"ID : {x} IP : {ip}".rstrip())
                print("Username: root   Password: Pa$$w0rd")
            else:
                print(f'Error starting container {x}')

        print("\n==Creating some attacking machines==")
        for x in range(300,300+FLAGS.number):
            out = clone(attacking,x)
            print(f"ID : {x} Created")

        print("\n==Start some attacking machines==")
        for x in range(300,300+FLAGS.number):
            out = startLxc(x)
            #Wait for dhcp
            time.sleep(7)
            ip = getIP(x)
            if out == 0:
                print(f"ID : {x} IP : {ip}".rstrip())
                print("Username: root   Password: Pa$$w0rd")
            else:
                print(f'Error starting container {x}')
        return
    if FLAGS.task == "remove":
        print("\n==Remove some pentesterlabs==")
        for x in range(200,200+FLAGS.number):
            out = remove(x)
            print(f"ID : {x} Removed")

        print("\n==Remove some attacking machines==")
        for x in range(300,300+FLAGS.number):
            out = remove(x)
            print(f"ID : {x} Removed")
        return

    if FLAGS.task == "destroy":
        print("\n==Destroy some pentesterlabs==")
        for x in range(200,200+FLAGS.number):
            out = stopLxc(x)
            print(f"ID : {x} Stopped")
        for x in range(200,200+FLAGS.number):
            out = remove(x)
            print(f"ID : {x} Removed")

        print("\n==Destroy some attacking machines==")
        for x in range(300, 300+FLAGS.number):
            out = stopLxc(x)
            print(f"ID : {x} Stopped")
        for x in range(300, 300+FLAGS.number):
            out = remove(x)
            print(f"ID : {x} Removed")


if __name__ == "__main__":
    app.run(main)