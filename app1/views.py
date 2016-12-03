import os
import time
import socket
import subprocess
from wifi import Cell
from django.shortcuts import render
from .models import Info, Robot
from .robot_server import Server, find_local_ip, check_url
from .wpa_wifi import Network, Fileconf

# Create your views here.

# Load the context for all the views here :
robot = Robot.objects.get(alive=True)
server_snap = Server('snap',robot)
server_jupyter = Server('jupyter',robot, simulator='no')
context = {'info' : Info.objects.get(), 'robot' : robot ,  'url_for_index' : '/'}

def index(request):
    server_snap.stop()
    server_jupyter.stop()
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
        wifi = list(Cell.all('wlan0'))
    except :
        wifi = False
        pass
    conf = Fileconf.from_file('/etc/wpa_supplicant/wpa_supplicant.conf')
    connect = subprocess.check_output(['iwgetid', '-r'])
    # Adding new context specific to the view here :
    context.update({'ip' : find_local_ip(),'hostname' : socket.gethostname(), 'wifi' : wifi, 'conf' : conf.network_list, 'connect' : connect })
    
    
               
    return render(request, 'app1/settings.html', context)


def juju(request):
    
    context = {'scheme' : request.scheme, 'host' : request.get_host(), 'path' : request.path, 'full' : request.get_full_path(), 'get' : request.GET, 'post' : request.POST }
   
    return render(request, 'app1/juju.html', context)

def juju2(request):
    
    context = {'scheme' : request.scheme, 'host' : request.get_host(), 'path' : request.path, 'full' : request.get_full_path(), 'get' : request.GET, 'post' : request.POST, 'configfile' : configfile }
   
    return render(request, './static-snap/snap.html', context)