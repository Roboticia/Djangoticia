import os
import time
from django.shortcuts import render
from .models import Info, Robot
from .robot_server import Server, find_local_ip

# Create your views here.

# Load the context for all the views here :
robot = Robot.objects.get(alive=True)
server_snap = Server('snap',robot, simulator='vrep')
context = {'info' : Info.objects.get(), 'robot' : robot ,  'url_for_index' : '/'}

def index(request):
    server_snap.stop()
    return render(request, 'app1/index.html',context)

def snap(request):
    # Adding new context specific to the view here :
    server_snap.start()
    time.sleep(5)
    iframe_src = '/static/snap/snap.html#open:http://'+find_local_ip()+':6969/snap-blocks.xml'
    context.update({'iframe_src' : iframe_src })
    return render(request, 'app1/base-iframe.html', context)


def juju(request):
    
    context = {'scheme' : request.scheme, 'host' : request.get_host(), 'path' : request.path, 'full' : request.get_full_path(), 'get' : request.GET, 'post' : request.POST }
   
    return render(request, 'app1/juju.html', context)

def juju2(request):
    
    context = {'scheme' : request.scheme, 'host' : request.get_host(), 'path' : request.path, 'full' : request.get_full_path(), 'get' : request.GET, 'post' : request.POST, 'configfile' : configfile }
   
    return render(request, './static-snap/snap.html', context)