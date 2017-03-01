# -*- coding: utf-8 -*-

import os
import time
import socket
import subprocess
from wifi import Cell
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from .models import Info, Robot
from .robot_server import Server, find_local_ip, check_url, robot_logs
from .wpa_wifi import Network, Fileconf

# Create your views here.


#create context the first time
try :
    context
except NameError :
    context = {'valid' : False}

#function to load the global context    
def start():
    robot = Robot.objects.get(alive=True)
    context['server_snap'] = Server('snap',robot)
    context['server_jupyter'] = Server('jupyter',robot)
    context['server_rest'] = Server('http',robot)
    context.update({'info' : Info.objects.get(), 'robot' : robot ,  'url_for_index' : '/','valid' : True})
    

def index(request):
    if not context['valid'] : start()
    # Adding new context specific to the view here :
    rest = request.GET.get('rest','go')
    if rest=='stop' : 
        context['server_rest'].stop()
        context.update({ 'url_for_index' :  '/'})
    context['server_snap'].stop()
    context['server_jupyter'].stop()
    context.update({ 'message' : None})
    return render(request, 'app1/index.html',context)

def snap(request):
    # Adding new context specific to the view here :
    context['server_jupyter'].stop()
    context['server_snap'].start()
    for i in range(20):
        if check_url('http://localhost:6969') : 
            break
        time.sleep(1)
    iframe_src = '/static/snap/snap.html#open:http://'+socket.gethostname()+'.local:6969/snap-blocks.xml'
    context.update({'iframe_src' : iframe_src })
    return render(request, 'app1/base-iframe.html', context)
    
def jupyter(request):
    # Adding new context specific to the view here :
    context['server_snap'].stop()
    context['server_jupyter'].start()
    for i in range(10):
        if check_url('http://localhost:8888') : 
            break
        time.sleep(1)
    iframe_src = 'http://{}.local:8888'.format(socket.gethostname())
    context.update({'iframe_src' : iframe_src })
    return render(request, 'app1/base-iframe.html', context)
    
def monitor(request):
    context['server_rest'].start()
    for i in range(10):
        if check_url('http://localhost:8080') : 
            break
        time.sleep(1)
    iframe_src = '/static/monitor/'+context['robot'].brand.lower()+'-'+context['robot'].creature.lower()+'.html#open=http://'+find_local_ip()+':8080'
    context.update({'iframe_src' : iframe_src, 'url_for_index' : '/?rest=stop' })
    return render(request, 'app1/base-iframe.html', context)
    
def rest(request):
    rest_action = request.POST.get('rest_action',False)
    if rest_action=='stop': context['server_rest'].stop()
    else : context['server_rest'].start()
    context.update({ 'logs_rest' : '/rest/raw/', 'url_rest' : '/rest/state/'})
    return render(request, 'app1/rest.html', context)
    
def rest_state(request):
    return HttpResponse(context['server_rest'].state())
    
def rest_raw(request):
    raw=''
    if context['server_rest'].daemon.pid==-1 : return HttpResponse(raw)
    with open(os.path.join(settings.LOG_ROOT, context['server_rest'].daemon.logfile+
    context['server_rest'].daemon.type+'_'+context['robot'].creature+'_'+context['robot'].type+'.log'), 'r') as log:
        u = log.readlines()
    for l in u : 
        try : 
            raw += l+'<br>'
        except UnicodeDecodeError:
            pass
    return HttpResponse(raw)
    
    
    
    
def configuration(request):
    try:
        connect = subprocess.check_output(['iwgetid', '-r'])
    except :
        connect = 'none'
        pass
    try : 
    # works only on linux system
        wifi = list(Cell.all('wlan0'))
        conf = Fileconf.from_file('/etc/wpa_supplicant/wpa_supplicant.conf')
    except :
    # give fake values on windows platform
        context.update({'ip' : find_local_ip(),'hostname' : socket.gethostname(), 
        'wifi' : [{ 'ssid' : 'test network' , 'quality' : '0/70' , 'encrypted' : 'secure' },{ 'ssid' : 'reseau test2' , 'quality' : '0/70' , 'encrypted' : 'secure' }],  'conf' : [{'ssid' : 'reseau test', 'opts' : {'priority' : '1'}},{'ssid' : 'reseau test2', 'opts' : {'priority' : '5'}},], 'connect' : 'reseau test' })
        pass
    else : 
        # Adding new context specific to the view here :
        context.update({'ip' : find_local_ip(),'hostname' : socket.gethostname(), 
        'wifi' : wifi, 'conf' : conf.network_list, 'connect' : connect })
    return render(request, 'app1/settings.html', context)
    
def wifi_add(request):
    try : 
    # works only on linux system
        conf = Fileconf.from_file('/etc/wpa_supplicant/wpa_supplicant.conf')
    except :
    # give fake values on windows platform
        pass
        return HttpResponseRedirect('/settings')
    wifi_ssid = request.POST['wifi_ssid']
    wifi_psk = request.POST['wifi_psk']
    wifi_priority = request.POST['wifi_priority']
    opts = {}
    if wifi_psk != '' : opts = { 'psk' : wifi_psk, }
    if wifi_priority != 'Aucune' : opts.update({'priority' : wifi_priority})
    (res, msg) = conf.add(wifi_ssid, **opts)   
    if res : conf.make_new()
    message = { 'ok' : None, 'ssid' : "Wrong network name !", 'psk' : "Wrong password !"} 
    context.update({ 'message' : message[msg], 'category' : 'warning'})
    return HttpResponseRedirect('/settings')
    
def wifi_suppr(request):
    try : 
    # works only on linux system
        conf = Fileconf.from_file('/etc/wpa_supplicant/wpa_supplicant.conf')
    except :
    # give fake values on wondows platform
        pass
        return HttpResponseRedirect('/settings')
    wifi_ssid = request.POST['wifi_ssid']
    res = conf.suppr(wifi_ssid)
    if res : conf.make_new()
    message = { True : "Network deleted" , False : "Can't suppress the network !"} 
    context.update({ 'message' : message[res], 'category' : 'success'})
    return HttpResponseRedirect('/settings')
   
def wifi_restart(request):
    try : 
        res1 = subprocess.call(['sudo', 'ifdown', 'wlan0'])
        time.sleep(1)
        res2 = subprocess.call(['sudo', 'ifup', 'wlan0'])
    except :
    # return on fail (windows)
        pass
        return HttpResponseRedirect('/settings')
    if res1 == 0 and res2 == 0 : context.update({ 'message' : 'Wifi restarted', 'category' : 'success'})
    else :  context.update({ 'message' : 'Unable to restart wifi', 'category' : 'warning'})
    return HttpResponseRedirect('/settings')   
    
def logs(request):
    snap = context['server_snap'].state() 
    jupyter = context['server_jupyter'].state()
    rest = context['server_rest'].state() 
    context.update({'url_logs' : '/logs/raw/', 'snap' : snap, 'jupyter' : jupyter, 'rest' : rest}) 
    return render(request, 'app1/logs.html', context)
     
def rawlogs(request):
    raw = robot_logs(context['robot'])
    return HttpResponse(raw)
            
    
    
    
def reboot(request):
    try :
        command = '(sleep 2 ; sudo reboot) &'
        subprocess.call(command, shell=True)
    except :
    # return on fail (windows)
        pass
    return HttpResponseRedirect('/')    
    
def shutdown(request):
    try : 
        subprocess.call(['sudo', 'halt'])
    except :
    # return on fail (windows)
        pass
    return HttpResponseRedirect('/')    


