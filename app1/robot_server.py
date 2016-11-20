import os
import signal
import psutil
import time

from subprocess import Popen, STDOUT
from .models import Daemon

class Server(object):
    def __init__(self, type, robot, simulator='no'):
        self.robot = robot
        self.daemon = Daemon.objects.get(type=type, simulator=simulator )

    def get_command(self):
        cmd = [
            'poppy-services',
            (self.robot.brand+'-'+self.robot.creature).lower(),
            '--'+self.daemon.type,
            '--no-browser',
        ]

        if not self.robot.camera:
            cmd += ['--disable-camera']

        if not 'no' in self.daemon.simulator:
            cmd += ['--'+self.daemon.simulator]

        return cmd

    def start(self):
        if 'running' in self.state():
            self.daemon.log += (  '{} : pidfile {} already exist. '
                              'Daemon already running.<br>'.format(time.strftime(
                              "%y/%m/%d %H:%M", time.localtime()),self.daemon.pid))
            self.daemon.save()
            return False

        else :
            if self.daemon.logfile=='none':
                FNULL = open(os.devnull, 'w')
                p = Popen(self.get_command(), stdout=FNULL, stderr=STDOUT)
            else :
                with open(self.daemon.logfile+self.daemon.type+self.robot.creature, 'w') as log:
                    p = Popen(self.get_command(), stdout=log, stderr=STDOUT)
            self.daemon.pid = p.pid
            self.daemon.log += (  '{} : Daemon is now running with pid {}<br>'.
            format(time.strftime("%y/%m/%d %H:%M", time.localtime()),self.daemon.pid))
            self.daemon.save()
            return True

    def stop(self):
        if 'running' in self.state():
            try:
                p = psutil.Process(self.daemon.pid)
            except psutil.NoSuchProcess:
                return
            p_children = p.children(recursive=True)
            for process in p_children:
                process.send_signal(signal.SIGTERM)
                p.send_signal(signal.SIGTERM)
            
            time.sleep(1)
            
            if 'stopped' in self.state() :
                self.daemon.pid = -1
                self.daemon.log = ''
                self.daemon.save()
                return True
            else : 
                self.daemon.log += (  '{} : kill unsuccesfull. '
                                'Daemon always running.<br>'.format(time.strftime(
                                "%y/%m/%d %H:%M", time.localtime())))
                self.daemon.save()
                return False
        else :
            self.daemon.pid = -1
            self.daemon.log = ''
            self.daemon.save()
            return False
        
    def state(self):
        return 'Robot daemon is {}.'.format(
        'running' if psutil.pid_exists(self.daemon.pid) else'stopped')