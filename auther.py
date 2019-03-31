from termcolor import colored
from ftplib import FTP
import argparse
import paramiko
import sys
import os


parser = argparse.ArgumentParser(description="Options for FTPchecker")

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

    print("--------- ---------------")

    if len(addr_success) > 0:
        for addr in addr_success:
            print(colored(addr,"green"))

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

        print("--------- ---------------")

    else:
        print(colored("> Login and password are required!", "red"))

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
    ssh_check()
elif str(args.mode).lower() == "ftp":
    print("> Mode: FTP")
    ftp_check()
else:
    print(colored("> Wrong protocol!", "red"))
    sys.exit(0)