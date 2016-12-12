# -*- coding: utf-8 -*-

import os
import time
import socket
import subprocess
from wifi import Cell
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Info, Robot
from .robot_server import Server, find_local_ip, check_url
from .wpa_wifi import Network, Fileconf

# Create your views here.

# Load the context for all the views here :
robot = Robot.objects.get(alive=True)
server_snap = Server('snap',robot,simulator='vrep')
server_jupyter = Server('jupyter',robot, simulator='no')
context = {'info' : Info.objects.get(), 'robot' : robot ,  'url_for_index' : '/'}

def index(request):
    server_snap.stop()
    server_jupyter.stop()
    context.update({ 'message' : None})
    return render(request, 'app1/index.html',context)

def snap(request):
    # Adding new context specific to the view here :
    server_jupyter.stop()
    server_snap.start()
    for i in range(5):
        if check_url('http://localhost:6969') : 
            break
        time.sleep(1)
    iframe_src = '/static/snap/snap.html#open:http://'+find_local_ip()+':6969/snap-blocks.xml'
    context.update({'iframe_src' : iframe_src })
    return render(request, 'app1/base-iframe.html', context)
    
def jupyter(request):
    # Adding new context specific to the view here :
    server_snap.stop()
    server_jupyter.start()
    for i in range(5):
        if check_url('http://localhost:8888') : 
            break
        time.sleep(1)
    iframe_src = 'http://{}:8888'.format(find_local_ip())
    context.update({'iframe_src' : iframe_src })
    return render(request, 'app1/base-iframe.html', context)
    
    
def settings(request):
    try : 
    # works only on linux system
        wifi = list(Cell.all('wlan0'))
        conf = Fileconf.from_file('/etc/wpa_supplicant/wpa_supplicant.conf')
        connect = subprocess.check_output(['iwgetid', '-r'])
    except :
    # give fake values on wondows platform
        context.update({'ip' : find_local_ip(),'hostname' : socket.gethostname(), 
        'wifi' : [{ 'ssid' : 'reseau test' , 'quality' : '0/70' , 'encrypted' : 'sécurisé' },{ 'ssid' : 'reseau test2' , 'quality' : '0/70' , 'encrypted' : 'sécurisé' }],  'conf' : [{'ssid' : 'reseau test', 'opts' : {'priority' : '1'}},{'ssid' : 'reseau test2', 'opts' : {'priority' : '5'}},], 'connect' : 'reseau test' })
        pass
    else : 
        # Adding new context specific to the view here :
        context.update({'ip' : find_local_ip(),'hostname' : socket.gethostname(), 
        'wifi' : wifi, 'conf' : conf.network_list, 'connect' : connect })
    
    
               
    return render(request, 'app1/settings.html', context)
    
def change(request):
    try : 
    # works only on linux system
        conf = Fileconf.from_file('/etc/wpa_supplicant/wpa_supplicant.conf')
    except :
    # give fake values on wondows platform
        conf = False
    wifi_ssid = request.POST['wifi_ssid']
    wifi_psk = request.POST['wifi_psk']
    opts = {}
    if wifi_psk != '' : opts = { 'psk' : wifi_psk }
    (res, msg) = conf.add(wifi_ssid, **opts)   
    if res : conf.make_new()
    message = { 'ok' : None, 'ssid' : "Le nom de réseau fourni n'est pas valide", 'psk' : "le mot de passe fourni n'est pas valide"} 
    context.update({ 'message' : message[msg], 'category' : 'warning'})
    return HttpResponseRedirect('/settings')
   
    
    


def juju(request):
    
    wifi_ssid = request.POST.get('wifi_ssid',False)    
    
    context = {'scheme' : request.scheme, 'host' : request.get_host(), 'path' : request.path, 'full' : request.get_full_path(), 'get' : request.GET, 'post' : request.POST, 'wifi_ssid' : wifi_ssid }
    context.update({'ip' : find_local_ip(),'hostname' : socket.gethostname(), 'wifi' : [{ 'ssid' : 'reseau test' , 'quality' : '0/70' , 'encrypted' : 'sécurisé' },{ 'ssid' : 'reseau test2' , 'quality' : '0/70' , 'encrypted' : 'sécurisé' }],  'conf' : [{'ssid' : 'reseau test', 'opts' : {'priority' : '1'}},], 'connect' : 'reseau test' })
    context.update({ 'message' : False})
   
    return render(request, 'app1/juju.html', context)

def juju2(request):
    messages.warning(request, 'Profile details updated.')
    context.update({ 'message' : "Le mot de passe n'est pas valide (au moins 8 caractères, uniquement lettres et nombres)", 'category' : 'warning'})
    return render(request, 'app1/base.html', context)