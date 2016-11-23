#this file is used to test robot_server.py absolutely no need in production

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "projet.settings")
import django
django.setup()

from app1.robot_server import Server, find_local_ip

from app1.models import *

robot = Robot.objects.get(alive=True)

server = Server('snap',robot, simulator='vrep')

