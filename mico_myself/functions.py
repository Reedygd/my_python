import Crypto
import paramiko
import telnetlib
import paramiko
import re
import os
import time
import serial
import config
import json

#创建serial 对象
try:
    ser=serial.Serial(config.com, 115200, timeout=0.5)
except:
    print("the serial is not available")

#monitor_list=["mediaplayer","mipns","alarmd","messagingagent"]
def loginMicoBySSH(host,cmd):
    private_key = paramiko.RSAKey.from_private_key_file(config.rsa)
    # 创建SSH对象
    ssh = paramiko.SSHClient()
    # 允许连接不在know_hosts文件中的主机
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 连接服务器
    ssh.connect(hostname=host, port=22, username='root')
    # 执行命令
    stdin, stdout, stderr = ssh.exec_command(cmd)
    # 获取命令结果
    result = stdout.read().decode()
    # 关闭连接
    ssh.close()

def tel_dev(tel_host,tel_user,tel_passwd,command):
    try:
        tel_con = telnetlib.Telnet(tel_host, port=23, timeout=10)
        tel_con.read_until(b"XiaoQiang login: ", 10)
        tel_con.write(tel_user + b'\n')
        tel_con.read_until(b"Password: ", 10)
        tel_con.write(tel_passwd + b"\n")
        tel_con.read_until(b'root@XiaoQiang:~#', 10)
        print("telnet success")
        tel_con.write(command.encode('utf-8')+b'\n')
        time.sleep(10)
        res = tel_con.read_very_eager().decode()
        return res
        tel_con.write(b"exit\n")
    except:
        print("Error:telnet failed")


def serial_dev(command):
    try:
        if ser.is_open:
            # print("connect devices by serial success")
            ser.flushInput()
            ser.write(command.encode('utf-8') + b'\n')
            time.sleep(10)
            n = ser.in_waiting
            if n != 0:
                res = ser.readlines()
                # res = ser.read(11).decode()
                return res
            else:
                print("no result return")
            ser.close()
        else:
            print("serial is not open")
    except:
        print("serial connect failed")


def check_serial():
    try:
        if ser.is_open:
            return 0
        else:
            return 1
    except:
        #print("serial connect failed")
        return 1

def close_serial():
    if ser.is_open:
        ser.close()
    else:
        ser.close()




if __name__ == '__main__':
    res=loginMicoBySSH('192.168.31.145','ubus call miio renew ')
    print(res)