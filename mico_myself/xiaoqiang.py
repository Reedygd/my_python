import time
import json
import sys
import re
import requests
import random
from Crypto.Hash import SHA

def login(host,passwd):
    #host = '192.168.31.1'
    homeRequest = requests.get('http://' + host + '/cgi-bin/luci/web/home')
    key = re.findall(r'key: \'(.*)\',', homeRequest.text)[0]
    mac = re.findall(r'deviceId = \'(.*)\';', homeRequest.text)[0]
    nonce = "0_" + mac + "_" + str(int(time.time())) + "_" + str(random.randint(1000, 10000))
    pwdtext = passwd

    pwd = SHA.new()
    pwd.update((pwdtext + key).encode('utf-8'))
    hexpwd1 = pwd.hexdigest()
    pwd2 = SHA.new()
    pwd2.update((nonce + str(hexpwd1)).encode('utf-8'))
    hexpwd2 = pwd2.hexdigest()

    data = {
        "logtype": 2,
        "nonce": nonce,
        "password": hexpwd2,
        "username": "admin"
    }
    response = requests.post(url='http://192.168.31.1/cgi-bin/luci/api/xqsystem/login', data=data, timeout=5)
    #print(type(response))
    resjson = json.loads(response.content.decode('utf-8'))
    return resjson

def get_status(baseurl):
    #获取小米路由器的状态信息，如CPU负载，内存，设备列表等信息；
    try:
        statusInfo = json.loads(requests.get(baseurl,timeout=5).content.decode('utf-8'))
        devList = statusInfo['dev']
        print('\n--------------------[Status]-----------------\n')
        print('[CPU]: ' + str(statusInfo['cpu']['core']) + '核   ' + statusInfo['cpu']['hz'] + '   系统负载 ' + str(statusInfo['cpu']['load']))
        print('[MAC]: ' + statusInfo['hardware']['mac'])
        print('[MEM]: Type: ' + statusInfo['mem']['type'] + '   Total: ' + statusInfo['mem']['total'] + '   Usage: ' + str(statusInfo['mem']['usage'] * 100) + '% \n')
        print('--------------------[DEV]----------------------\n')
        for dev in devList:
            print(dev['mac'] + ' ' + dev['devname'])
    except Exception as e:
        print(e)

def get_waninfo(wanurl):
    '''the api is:/api/xqnetwork/wan_info'''
    try:
        wanInfo = json.loads(requests.get(wanurl,timeout=5).content.decode('utf-8'))
        print(wanInfo)
        if wanInfo['info']['details']['wanType'] == 'dhcp':
            print('\n--------------------[WAN]----------------------\n')
            print('连接类型： '+ wanInfo['info']['details']['wanType'])
            print('IP地址： '+ wanInfo['info']['ipv4'][0]['ip'])
            print('子网掩码：'+ wanInfo['info']['ipv4'][0]['mask'])
            print('默认网关：'+ wanInfo['info']['gateWay'])
            print('DNS: '+ wanInfo['info']['dnsAddrs'] + ' '+ wanInfo['info']['dnsAddrs1'] )
        if wanInfo['info']['details']['wanType'] == 'pppoe':
            print('\n--------------------[WAN]----------------------\n')
            print('用户: ' + wanInfo['info']['details']['username'])
            print('密码: ' + wanInfo['info']['details']['password'])
            print('类型: ' + wanInfo['info']['details']['wanType'])
            print('IP地址: ' + wanInfo['info']['ipv4'][0]['ip'])
            print('网关: ' + wanInfo['info']['gateWay'])
            print('DNS: ' + wanInfo['info']['dnsAddrs'] + ',' + wanInfo['info']['dnsAddrs1'])

    except Exception as e:
        print(e)

def set_wifi(wifiurl,wifiindex='1',status='0',ssid='Xiaomi_6DDE',pwd='12345678',encryption='mixed-psk',channel='0',bandwidth='0',hidden='0',txpower='mid'):
    '''the api is /api/xqnetwork/set_wifi. And wifiindex='1' is 2.4G,wifiindex='2' is 5G,wifiindex='3' is share wifi.'''
    wifidata={'wifiIndex':wifiindex,'on':status,'ssid':ssid,'pwd':pwd,'encryption':encryption,'channel':channel,'bandwidth':bandwidth,'hidden':hidden,'txpwr':txpower}
    try:
        response=requests.post(wifiurl,data=wifidata)
        if response.status_code == 200:
            print('Set Wifi Success!')
    except Exception as e:
        print('Set Wifi faild!')

def get_dhcpinfo(dhcpurl):
    '''the api interface is:/api/xqnetwork/lan_dhcp'''
    try:
        dhcpinfo=json.loads(requests.get(dhcpurl).content.decode('utf-8'))
        if dhcpinfo:
            print('局域网IP地址：'+dhcpinfo['info']['lanIp'][0]['ip'])
            if int(dhcpinfo['info']['ignore']) ==0:
                print('DHCP状态 ：'+' enable')
            else:
                print('DHCP状态 ：' + ' disable')
            print('租约(分) ：'+dhcpinfo['info']['leasetime'])
            print('开始 IP  ：'+dhcpinfo['info']['start'])
            print('结束 IP  ：'+str(int(int(dhcpinfo['info']['limit'])+int(dhcpinfo['info']['start'])-1)))
        else:
            print('dhcp info is null')
    except Exception as e:
        print("get dhcp info fail")


def set_dhcp(dhcpurl,ignore='0',start='5',end='100',leasetime='3m'):
    '''the api is /api/xqnetwork/set_lan_dhcp,and the ignore value is 0 dhcp is enable,is 1 dhcp is disable'''
    if ignore == 1:
        dhcpparams={'ignore':ignore}
    else:
        dhcpparams={'leasetime':leasetime,'start':start,'end':end,'ignore':ignore}
    try:
        response=requests.get(dhcpurl,params=dhcpparams)
        if response.status_code == 200:
            print('set dhcp success')
    except Exception as e:
        print('set dhcp fail')

def change_lanip(url,lanip):
    '''the api is /api/xqnetwork/set_lan_ip'''
    ipparams={'ip':lanip}
    try:
        response=requests.get(url,params=ipparams)
        if response.status_code==200:
            print('set lan ip success,wait device reboot')
        else:
            print('set lan ip fail')
    except Exception as e:
        print('error')

def set_wan_type(set_wan_url,wantype):
    if wantype=="pppoe":
        wandata = {"pppoeNmae" :"admin","pppoePwd" :"12345678","autoset" :0}
        res=requests.post(set_wan_url,data=wandata)
        if res.status_code == 200:
            print("set pppoe success!")
        else:
            print("set pppoe fail!")
    elif wantype == "dhcp":
        wandata = {"wanType":"dhcp","autoset":0}
        res = requests.post(set_wan_url, data=wandata)
        if res.status_code == 200:
            print("set dhcp success!")
        else:
            print("set dhcp fail!")
    else:
        wandata={"wanType":"static","statisIp":"10.231.38.237","staticMask":"255.255.255.0","staticGateway":"10.231.38.254","dns1":"10.237.8.8","dns2":"10.236.8.8"}
        res = requests.post(set_wan_url, data=wandata)
        if res.status_code == 200:
            print("set static ip success!")
        else:
            print("set static ip fail!")



if __name__ == '__main__':
    host = '192.168.31.1'
    passwd = '12345678'
    resjson=login(host,passwd)
    if resjson['code'] == 0:
        print('Login Success! Token is ' + resjson['token'])
    else:
        print('Login Failed! Code is ' + str(resjson['code']))
    url='http://'+host+'/cgi-bin/luci/;stok='+resjson['token']+'/api/xqnetwork/set_wifi'
    dhcpurl='http://'+host+'/cgi-bin/luci/;stok='+resjson['token']+'/api/xqnetwork/set_lan_dhcp'
    dhcpinfourl='http://'+host+'/cgi-bin/luci/;stok='+resjson['token']+'/api/xqnetwork/lan_dhcp'
    #setdhcpstate('http://' + host + '/cgi-bin/luci/;stok=' + resjson['token'] + '/api/xqnetwork/set_lan_dhcp')
    set_wan_url='http://'+host+'/cgi-bin/luci/;stok='+resjson['token']+'/api/xqnetwork/set_wan'
    channelList_1=[1,2,3,4,5,6,7,8,9,10,11,12,13]
    channelList_2=[36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136,140,149,153,157,161,165]
    while 1:
        #getStatus('http://'+ host + '/cgi-bin/luci/;stok='+ resjson['token'] + '/api/misystem/status')
        #getWanInfo('http://'+ host + '/cgi-bin/luci/;stok='+ resjson['token'] + '/api/xqnetwork/wan_info')
        for chan in channelList_1:
            #set_wifi(wifiurl=url,status=0,wifiindex=1,ssid='ygd_r3p',pwd='12345678',encryption='mixed-psk',channel='13',bandwidth='0',hidden='0',txpower='min')
            #print("close 2.4G wifi")
            #time.sleep(10)
            #set_wifi(wifiurl=url, status=1,wifiindex=1,ssid='ygd_r3p', pwd='12345678', encryption='mixed-psk', channel='13',bandwidth='0', hidden='0', txpower='min')
            #print("open 2.4G wifi")
            #time.sleep(180)
            set_wifi(wifiurl=url, status=1, wifiindex=1, ssid='ygd_r3p', pwd='12345678', encryption='mixed-psk',channel=chan, bandwidth='0', hidden='0', txpower='min')
            print("current channel is :",chan)
            time.sleep(180)
            #setdhcp(dhcpurl,ignore=1)




        #setdhcpstate('http://'+host+'/cgi-bin/luci/;stok='+resjson['token']+'/api/xqnetwork/set_lan_dhcp')
