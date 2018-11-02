"""
Connect to GMS VA and execute queries to stop and start services
"""

from fabric import tasks
from fabric.api import *


env.hosts = [
    '10.61.242.95'
]

env.user="root"
env.password="sonicssh"

#Stop all GMS services
def stop_gms_services():
    result = run('/opt/GMSVP/bin/sgms all stop')
    print(result)

#Start all GMS services
def start_gms_services():
    result = run('nohup /opt/GMSVP/bin/sgms all start > /dev/null')
    print(result)


def main():
    tasks.execute(stop_gms_services)
    tasks.execute(start_gms_services)
    disconnect_all()

if __name__=='__main__':
    main()    
