from termcolor import colored
from ftplib import FTP
from socket import *
from struct import *
import argparse
import paramiko
import time
import sys
import os


parser = argparse.ArgumentParser(description="Options for AuthTester")

parser.add_argument('-g', '--generate', help="Ip range")
parser.add_argument('-o', '--output', help="Output file name")
parser.add_argument('-t', '--target', help="Target ip")
parser.add_argument('-T', '--targets', help="File with targets ip")
parser.add_argument('-l', '--login', help="Login")
parser.add_argument('-p', '--password', help="Password")
parser.add_argument('-f', '--fast', action="store_true", help="Fast mode")
parser.add_argument('-m', '--mode', help="Protocol type (SSH/FTP)")

args = parser.parse_args()
addr_success = []

def check_file(file_path):
    if os.path.isfile(file_path):
        print("> File: available")
    else:
        print(colored("> File not found!", "red"))
        sys.exit(0)

def generate(rang, file_name):
    try:
        first, second = rang.split("-")
    except:
        print(colored("> Wrong input!", "red"))
    else:
        with open(file_name, "w") as f:
            try:
                for ip in range(unpack('!I', inet_pton(AF_INET, first))[0], unpack('!I', inet_pton(AF_INET, second))[0]):
                    addr = inet_ntop(AF_INET, pack('!I', ip))
                    f.write(addr + "\n")
            except:
                print(colored("> Illegal IP!", "red"))
            else:
                print(colored("\nList was created and saved to " + file_name, "green"))

def ftp_check():
    print("--------- ---------------")
    if args.targets:

        with open(args.targets, "r") as f:
            for line in f:
                ip = line[:-1]
                try:
                    ftp = FTP(ip, timeout=timeout)
                    ftp.login(login, passwd)
                except:
                    print("[" + colored("FAILURE", "red") + "] " + ip)
                else:
                    print("[" + colored("SUCCESS", "green") + "] " + ip)
                    addr_success.append(ip)

    if args.target:
        ip = args.target

        try:
            ftp = FTP(ip, timeout=1)
            ftp.login(login, passwd)
        except:
            print("[" + colored("FAILURE", "red") + "] " + ip)
        else:
            print("[" + colored("SUCCESS", "green") + "] " + ip)
            addr_success.append(ip)

    print("--------- ---------------")

def ssh_check():
    if login and passwd:
        print("--------- ---------------")

        if args.targets:
            client    = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            with open(args.targets, "r") as f:
                for line in f:
                    ip = line[:-1]
                    try:
                        client.connect(hostname=ip, username=login, password=passwd, port=22, timeout=timeout)
                    except:
                        print("[" + colored("FAILURE", "red") + "] " + ip)
                    else:
                        print("[" + colored("SUCCESS", "green") + "] " + ip)
                        addr_success.append(ip)

        if args.target:
            ip = args.target

            try:
                client.connect(hostname=ip, username=login, password=passwd, port=22, timeout=timeout)
            except:
                print("[" + colored("FAILURE", "red") + "] " + ip)
            else:
                print("[" + colored("SUCCESS", "green") + "] " + ip)
                addr_success.append(ip)

        print("--------- ---------------")

    else:
        print(colored("> Login and password are required!", "red"))

if args.generate and args.output:
    generate(args.generate, args.output)
    sys.exit(0)
elif args.generate and not args.output:
    print(colored("> Output argument is required!", "red"))
    sys.exit(0)
elif not args.generate and args.output:
    print(colored("> Range is required!", "red"))
    sys.exit(0)

if args.targets:
    check_file(args.targets)

if args.fast:
    print("> Fast mode " + colored("enabled", "white", 'on_green'))
    timeout = 0.1
else:
    print("> Fast mode " + colored("disabled", "white", 'on_red'))
    timeout = 0.5

if args.login and args.password:
    login = args.login
    passwd = args.password
    print("> Login: " + login)
    print("> Password: " + passwd)
else:
    login = ""
    passwd = ""

if str(args.mode).lower() == "ssh":
    print("> Mode: SSH")
    time.sleep(2)
    ssh_check()
elif str(args.mode).lower() == "ftp":
    print("> Mode: FTP")
    time.sleep(2)
    ftp_check()
else:
    print(colored("> Wrong protocol!", "red"))
    sys.exit(0)

if len(addr_success) > 1:
    for addr in addr_success:
        print(colored(addr,"green"))
    print("-------------------------")
elif len(addr_success) == 0:
    print("Nothing:(")

if str(args.mode).lower() == "ftp" and len(addr_success) > 0 and not login and not passwd:
    print("login   : anonymous")
    print("password: keepme")

elif len(addr_success) > 0 and login and passwd:
    print("login   : " + login)
    print("password: " + passwd)

print()

