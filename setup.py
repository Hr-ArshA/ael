import os

import wget
import time
import json
import platform
import subprocess
from colorama import Fore, init

def get_distro():
    os_release = open('/etc/os-release', 'r').read().split('\n')
    for i in os_release:
        i = i.split('=')
        if i[0] == 'ID':
            return i[-1]

if get_distro() == 'debian':
    os.system('pip install deb')
    import apt

if get_distro() == 'arch':
    os.system("pip install python-pacman")
    import pacman


init()

def clear():
    os.system('clear')

def qemuexists():
    distro = get_distro()
    if distro == 'debian':
        cache = apt.Cache()
        cache.open()
        pkg = cache['qemu-system-x86']
        clear()
        print(f'{Fore.YELLOW}Checking for Q.EMU...')
        time.sleep(2)
        is_installed = pkg.is_installed
    
    elif distro == 'arch':
        is_installed = pacman.is_installed("qemu-system-x86")

    if is_installed:
        clear()
        print(f'{Fore.GREEN}Q.EMU is already installed!')
        time.sleep(2)
    else:
        print(f'{Fore.RED}Q.EMU is not installed!')
        time.sleep(2)
        clear()
        print(f'{Fore.GREEN}Downloading Q.EMU...{Fore.RESET}')
        time.sleep(2)
        try:
            if distro == 'debian':
                os.system('sudo apt-get install qemu-system-x86 -y')
            elif distro == 'arch':
                os.system('sudo pacman -S qemu-system-x86 -y')

        except:
            print(f'{Fore.RED}Unable to install Q.EMU! Please try installing manually!')
            time.sleep(3)
            input()

def conf_img():
    if os.path.isfile('config.json') == True:
        try:
            with open('config.json') as config:
                data = json.load(config)
                ram = data['ram']
                imgsize = data['size']
                clear()
                print(f'{Fore.BLUE}Loaded config.json file succesfully!')
                time.sleep(3)
                print(f'{Fore.GREEN}Set RAM to: {ram}MB')
                time.sleep(1)
                print(f'{Fore.GREEN}Set Virtual Disk to: {imgsize}MB')
                time.sleep(2)
                clear()
        except:
            print(f'{Fore.RED}An error occured on config.json reading. Please open an issue!')
            time.sleep(2)
            input()
    else:
        print(f'{Fore.RED}config.json wasn\'t found in the directory. Please create/add one from repo template!')
        time.sleep(2)
        input()
    print(f'{Fore.YELLOW}Checking if .img Virtual Disk exists...')
    time.sleep(3)
    if os.path.isfile('disk.img') == True:
        directory = os.getcwd()+'/disk.img'
        disksize = subprocess.check_output('qemu-img info '+directory+' | grep \'virtual size: \'', shell=True).decode()
        disksize = disksize[14:len(disksize)]
        disksize = disksize.split('(')[0]
        print(f'{Fore.GREEN}Virtual Disk (disk.img) found with total of {disksize}!')
    else:
        try:
            directory = os.getcwd()
            disklocation = directory+'/disk.img'
            diskgb = str(data['size'])+'M'
            print(f'{Fore.YELLOW}Virtual Disk (disk.img) wasn\'t found, attempting to create one...{Fore.RESET}')
            time.sleep(2)
            os.system(f'qemu-img create -f qcow2 {disklocation} {diskgb}')
        except:
            print(f'{Fore.RED}Failed to create disk.img. Please download the default one from repo!')
            time.sleep(2)
            input()

def startandroid():
    directory = os.getcwd()
    with open('config.json') as config:
        data = json.load(config)
    if data['boot'] == 'live':
        print(f'{Fore.YELLOW}Selected boot method: {Fore.BLUE}LIVE{Fore.RESET}')
        time.sleep(2)
        os.system(f'sudo bash live.sh')
    elif data['boot'] == 'normal':
        print(f'{Fore.YELLOW}Selected boot method: {Fore.BLUE}NORMAL{Fore.RESET}')
        time.sleep(2)
        os.system(f'sudo bash normal.sh')

if 'Linux' in platform.platform():
    if not os.path.isfile('Android.iso') == True:
        clear()
        print(f'{Fore.RED}Android.iso was not found!\n')
        time.sleep(2)
        clear()
        url = 'https://sourceforge.net/projects/android-x86/files/latest/download'
        directory = os.getcwd()
        print(f'{Fore.YELLOW}Downloading Android.iso...{Fore.GREEN}')
        wget.download(url, out=directory+'/Android.iso')
        time.sleep(2)
        print(f'{Fore.GREEN}Android.iso downloaded successfully!')
        time.sleep(2)
        clear()
        qemuexists()
        conf_img()
        startandroid()
    else:
        print(f'\n{Fore.GREEN}Android.iso (v9.0-r2) exists!')
        time.sleep(2)
        qemuexists()
        conf_img()
        startandroid()