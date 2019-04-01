# AuthTester

**Dependencies:**</br>
- paramiko</br>
- termcolor</br>

**Usage:**</br>
-h, --help &nbsp;&nbsp;&nbsp;&nbsp;*Show help message*</br>
-t, --target &nbsp;&nbsp;*Target ip*</br>
-T, --targets *File with targets ip*</br>
-l, --login &nbsp;&nbsp;&nbsp;&nbsp;*Login*</br>
-p, --password *Password*</br>
-f, --fast &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Fast mode*</br>
-m, --mode &nbsp;&nbsp;&nbsp;*Protocol type (SSH/FTP)*</br>
  
**Generator:**</br>
-g, --generate Ip range</br>
-o, --output Output file name</br>

**Examples:**</br>
```$ python3 auther.py -g 192.168.1.0-192.168.1.255 -o example.txt```</br>
```$ python3 auther.py -T example.txt -m ftp --fast```</br>
```$ python3 auther.py -t 192.168.1.54 -m ftp```</br>
```$ python3 auther.py -T example.txt -m ssh -l admin -p admin -f```</br>
  
**GUI version:**&nbsp;[click](https://yadi.sk/d/EjkbDmvR-xJY_A) 
