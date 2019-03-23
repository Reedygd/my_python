import functions
import time
import config
import re
import os

def creat_alarm (year=0,month=0,day=0,hour=0,minute=5,second=0):
    #获取本地时间
    curtime=time.localtime(time.time())
    year=year+curtime.tm_year
    month=month+curtime.tm_mon
    day=day+curtime.tm_mday
    hour=hour+curtime.tm_hour
    minute=minute+curtime.tm_min
    second=second+curtime.tm_sec

    #转化为时间戳并下发命令并获取返回值
    timestap=time.mktime((year,month,day,hour,minute,second,curtime.tm_wday,curtime.tm_yday,curtime.tm_isdst))
    commond="ubus call alarm alarm_create '{\"type\":\"alarm\",\"timestamp\":%d,\"circle\":0,\"volume\":60,\"event\":\"testfun\"}' " % timestap
    if 0 == functions.check_serial():
        res=functions.serial_dev(commond)
        if res:
            res_new=[]
            for i in res:
                res_new.append(i.decode().replace('\r','').replace('\n','').replace('\t',''))
            #print(res_new)
            for line in res_new:
                if re.findall("code",line):
                    lis=line.split(":")
                    lis_new=[]
                    for j in lis:
                        lis_new.append(j.replace('\t','').replace('\n','').replace('\r','').strip())
            if int(lis_new[1])==0:
                print("Creat alarm success")
                return 0
            else:
                print("Creat alarm fail")
                return 1
        else:
            print("Error！No response return")
            return 1
    else:
        res = os.popen("adb shell %s" % commond).readlines()
        if res:
            res_new = []
            for i in res:
                res_new.append(i.replace('\r', '').replace('\n', '').replace('\t', ''))
            print(res_new)
            for line in res_new:
                if re.findall("code", line):
                    lis = line.split(":")
                    lis_new = []
                    for j in lis:
                        lis_new.append(j.replace('\t', '').replace('\n', '').replace('\r', '').strip())
            if int(lis_new[1]) == 0:
                print("Creat alarm success")
                return 0
            else:
                print("Creat alarm fail")
                return 1
        else:
            print("Error！No response return")
            return 1
    return None


def stop_micmute(min=0):
    command= "ubus call alarm micmute '{\"minute\":%d}' " % min
    if 0 == functions.check_serial():
        if min == 0:
            res=functions.serial_dev(command)
            if res:
                new_res=[]
                for i in res:
                    new_res.append(''.join(i.decode()).replace('\n','').replace('\t','').replace('\r',''))
            if '"code": 0'in new_res:
                print("stop micmute success")
                return 0
            else:
                print("stop micmute fail")
                return 1
        else:
            res=functions.serial_dev("ubus call alarm micmute '{\"minute\":%d}' " % min)
            if res:
                new_res = []
                for i in res:
                    new_res.append(''.join(i.decode()).replace('\n', '').replace('\t', '').replace('\r', ''))
            if  '"code": 0' in res:
                print("stop micmute %s minute success" % min)
                return 0
    else:
        if min == 0:
            res=os.popen("adb shell %s" % command).readlines()
            if res:
                new_res=[]
                for i in res:
                    new_res.append(i.replace('\t','').replace('\n',''))
            if '"code": 0'in new_res:
                print("stop micmute success")
                return 0
            else:
                print("stop micmute fail")
                return 1
        else:
            res = os.popen("adb shell %s" % command).readlines()
            if res:
                new_res=[]
                for i in res:
                    new_res.append(i.replace('\t','').replace('\n',''))
            if '"code": 0'in new_res:
                print("stop micmute %s minute success" % min)
                return 0
            else:
                print("stop micmute %s minute success" % min)
                return 1
    return None

def start_micmute():
    command='/etc/init.d/pns mic_on'
    if 0 == functions.check_serial():
        res=functions.serial_dev(command)
        if res:
            res_new=[]
            for i in res:
                res_new.append(i.decode().replace('\r', '').replace('\n', ''))
            for line in res_new:
                if re.findall("code",line):
                    lis=line.split(":")
                    lis_new=[]
                    for j in lis:
                        lis_new.append(j.replace('\n','').replace('\r','').strip())
                    if int(lis_new[1])==0:
                        print("Start micmute success")
                        return 0
                    else:
                        print("Start micmute fail")
                        return 1
    else:
        res=os.popen("adb shell %s" % command).readlines()
        if res:
            new_res = []
            for i in res:
                new_res.append(i.replace('\t', '').replace('\n', ''))
        if '"code": 0' in new_res:
            print("start micmute success")
            return 0
        else:
            print("start micmute fail")
            return 1

def config_mode():
    command='/etc/init.d/wireless config_mode'
    if 0== functions.check_serial():
        res = functions.serial_dev(command)
        res_new=[]
        for i in res:
            res_new.append(i.decode().replace('\r','').replace('\n','').replace('\t',''))
        if '"code": 0' in res_new:
            print("entter config mode success")
            return 0
        else:
            print("enter config mode fail")
            return 1
    else:
        res= os.popen("adb shell %s" % command)
        res_new = []
        for i in res:
            res_new.append(i.decode().replace('\r','').replace('\n','').replace('\t',''))
        if '"code": 0' in res_new:
            print("entter config mode success")
            return 0
        else:
            print("enter config mode fail")
            return 1

def set_mico_wifi(ssid='ygd_r3p',passwd='12345678'):
    command = '/etc/init.d/wireless internet "30" "%s" "%s"' % (ssid, passwd)
    if 0 == functions.check_serial():
        functions.serial_dev(command)
        time.sleep(15)
        res=functions.serial_dev("ifconfig")
        for i in res:
            i=str(i)
            ip = re.search('.+inet addr:(1[^2][^7]\.\d+\.\d+\.\d+)', i)
            if ip:
                print("set wifi success,ip is:", ip.group(1))
                break
        else:
            print("set wifi fail")
            return 1
    else:
        res = os.popen("adb shell %s" % command).readlines()
        time.sleep(15)
        res2 = os.popen("adb shell ifconfig").readlines()
        for i in res2:
            i = str(i)
            ip = re.search('.+inet addr:(1[^2][^7]\.\d+\.\d+\.\d+)', i)
            if ip:
                print("set wifi success,ip is:", ip.group(1))
                break
        else:
            print("set wifi fail")
            return 1

def query_alarm():
    command = "ubus call alarm alarm_query '{\"type\":\"alarm\"}'"
    if 0 == functions.check_serial():
        res = functions.serial_dev(command)
        #print(res)
        res_new=[]
        for i in res:
            res_new.append(i.decode().replace('\r','').replace('\n','').replace('\t','').replace('\\','').replace('\"',''))
        for j in res_new:
            id=re.findall('id: [0-9a-z]+-[0-9a-z]+-[0-9a-z]+-[0-9a-z]+-[0-9a-z]+',j)
            if id:
                break
        for k in range(len(id)):
            id[k]=id[k].replace('id:','').strip()
        if id and len(id) !=0:
            return id
        else:
            return list()
    else:
        res=os.popen('adb shell %s' % command).readlines()
        res_new=[]
        for i in res:
            res_new.append(i.replace('\r', '').replace('\n', '').replace('\t', '').replace('\\', '').replace('\"', ''))
        for j in res_new:
            id = re.findall('id: [0-9a-z]+-[0-9a-z]+-[0-9a-z]+-[0-9a-z]+-[0-9a-z]+', j)
            if id:
                break
        for k in range(len(id)):
            id[k] = id[k].replace('id:', '').strip()
        if len(id) !=0:
            return id
        else:
            return list()

def delete_alarm(num=0):
    alarm_id_list=query_alarm()
    num=int(num)
    if len(alarm_id_list) ==0:
        print("the alarm is null")
    else:
        if num == 0 and len(alarm_id_list) > 1:
            for lis in alarm_id_list:
                command = "ubus call alarm alarm_delete '{\"type\":\"alarm\",\"id\":\"%s\"}'" % lis
                if functions.check_serial==0:
                    res = functions.serial_dev(command)
                    res_new = []
                    for i in res:
                        res_new.append(i.decode().replace('\r', '').replace('\n', '').replace('\t', ''))
                    if '"code": 0' in res_new:
                        print("delete %s alarm success" % lis)
                        return 0
                    else:
                        print("delete %s alarm fail" % lis)
                        return 1
                else:
                    res=os.popen("adb shell %s" % command).readlines()
                    res_new = []
                    for i in res:
                        res_new.append(i.replace('\r', '').replace('\n', '').replace('\t', ''))
                    if '"code": 0' in res_new:
                        print("delete %s alarm success" % lis)
                        return 0
                    else:
                        print("delete %s alarm fail" % lis)
                        return 1
            #del res_new, res
        elif num == 0 and len(alarm_id_list) == 1:
            command = "ubus call alarm alarm_delete '{\"type\":\"alarm\",\"id\":\"%s\"}'" % alarm_id_list[0]
            # print(command)
            if functions.check_serial ==0:
                res = functions.serial_dev(command)
                # print(res)
                res_new = []
                for i in res:
                    res_new.append(i.decode().replace('\r', '').replace('\n', '').replace('\t', ''))
                # print(res_new)
                if '"code": 0' in res_new:
                    print("delete alarm success")
                    return 0
                else:
                    print("delete alarm fail")
                    return 1
            else:
                res = os.popen("adb shell %s" % command).readlines()
                res_new = []
                for i in res:
                    res_new.append(i.replace('\r', '').replace('\n', '').replace('\t', ''))
                if '"code": 0' in res_new:
                    print("delete %s alarm success" % lis)
                    return 0
                else:
                    print("delete %s alarm fail" % lis)
                    return 1
        elif num != 0 and num < len(alarm_id_list):
            command = "ubus call alarm alarm_delete '{\"type\":\"alarm\",\"id\":\"%s\"}'" % alarm_id_list[num - 1]
            print(command)
            if functions.check_serial ==0:
                res = functions.serial_dev(command)
                res_new = []
                for i in res:
                    res_new.append(i.decode().replace('\r', '').replace('\n', '').replace('\t', ''))
                # print(res_new)
                if '"code": 0' in res_new:
                    print("delete alarm success")
                    return 0
                else:
                    print("delete alarm fail")
                    return 1
            else:
                res = os.popen("adb shell %s" % command).readlines()
                res_new = []
                for i in res:
                    res_new.append(i.replace('\r', '').replace('\n', '').replace('\t', ''))
                if '"code": 0' in res_new:
                    print("delete alarm success" )
                    return 0
                else:
                    print("delete alarm fail" )
                    return 1
        elif num > len(alarm_id_list):
            print("the alarm is not exist")
            return 1

def set_classic_bluetooth(connect=1,discover=1):
    command="ubus call mibt enable '{\"btmode\":\"classic\",\"connect\":%d,\"discover\":%d}'" % (connect,discover)
    if 0 == functions.check_serial():
        res = functions.serial_dev(command)
        res_new=[]
        for i in res:
            res_new.append(i.decode().replace('\t','').replace('\n','').replace('\r','').replace(',',''))
        print(res_new)
        if '"code": 0' in res_new:
            print("set bluetooth success")
            return 0
        else:
            print("set bluetooth fail")
            return 1
    else:
        res=os.popen("adb shell %s" % command).readlines()
        for i in res:
            res_new.append(i.replace('\t','').replace('\n','').replace('\r','').replace(',',''))
        if '"code": 0' in res_new:
            print("set bluetooth success")
            return 0
        else:
            print("set bluetooth fail")
            return 1

def disconnect_bluetooth():
    command = "ubus call mibt disconnect"
    if 0==functions.check_serial():
        res=functions.serial_dev(command)
        res_new=[]
        for i in res:
            res_new.append(i.decode().replace('\t','').replace('\n','').replace('\r',''))
        if '"code": 0' in res_new:
            print("disconnect bluetooth success")
            return 0
        else:
            print("disconnect bluetooth fail")
            return 1
    else:
        res=os.popen("adb shell %s" % command).readlines()
        res_new = []
        for i in res:
            res_new.append(i.replace('\t', '').replace('\n', '').replace('\r', ''))
        if '"code": 0' in res_new:
            print("disconnect bluetooth success")
            return 0
        else:
            print("disconnect bluetooth fail")
            return 1

def connect_bluetooth(mac):
    command="ubus call mibt connect '{\"mac\":\"%s\"}' " % mac
    if 0==functions.check_serial():
        res=functions.serial_dev(command)
        res_new=[]
        for i in res:
            res_new.append(i.decode().replace('\t','').replace('\n','').replace('\r',''))
        if '"code": 0' in res_new:
            print("connect bluetooth success")
            return 0
        else:
            print("connect bluetooth fail")
            return 1
    else:
        res = os.popen("adb shell %s" % command).readlines()
        res_new = []
        for i in res:
            res_new.append(i.replace('\t', '').replace('\n', '').replace('\r', ''))
        if '"code": 0' in res_new:
            print("connect bluetooth success")
            return 0
        else:
            print("connect bluetooth fail")
            return 1

def set_mediaplayer_volume(volume=12):
    cmd=r"ubus call mediaplayer player_set_volume '{\"volume\":%d,\"media\":\"\"}'" % volume
    if 0 == functions.check_serial():
        res=functions.serial_dev(cmd)
        res_new=[]
        for i in res:
            res_new.append(i.decode().replace('\t','').replace('\n','').replace('\r','').replace(',',''))
        if '"code": 0' in res_new:
            print("set volume success")
            return 0
        else:
            print("set volume fail")
            return 1
    else:
        res = os.popen(r"adb shell %s" % cmd).readlines()
        res_new = []
        for i in res:
            res_new.append(i.replace('\t', '').replace('\n', '').replace('\r', '').replace(',', ''))
        if '"code": 0' in res_new:
            print("set volume success")
            return 0
        else:
            print("set volume fail")
            return 1







if __name__ == '__main__':
    #stop_micmute()
    # start_micmute()
    #creat_alarm()
    #config_mode()
    #set_mico_wifi()
    #query_alarm()
    #delete_alarm()
    #set_classic_bluetooth()
    #functions.close_serial()
    set_mediaplayer_volume(20)
