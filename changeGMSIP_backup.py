import MySQLdb #Use this to talk to MySQL datbase
import os #Use this to talk to GMS services on Linux OS
import subprocess #Run Linux commands using subprocess modules


def main():
    #Stop GMS Services
    stop_gms_services()

    print("Enter the GMS database credentials...")
    gms_db_name = input("What is the database name? (Default is 'sgmsdb')")
    gms_db_ip = input("What is the database IP address? ")
    gms_db_username = input("What is the datbase username? ")
    gms_db_password = input("What is the database password? ")


    try:
        db = db_connection(gms_db_ip, gms_db_username,
                            gms_db_password, gms_db_name)
        # you must create a Cursor object. It will let
        #  you execute all the queries you need
        cur = db.cursor()
        print("Successfully created database connection.")
    except:
        print("Unable to establish database connection. Verify you have the correct username and/or password.")
    

    old_gms_ip = input("What is the old GMS server IP address? ")
    new_gms_ip = input("What is the new GMS server IP address? ")

    try:
        update_wsexternalhome(cur, new_gms_ip, old_gms_ip)
        db.commit()
    except:
        print("Failed to execute SQL query.")
    
    #db.close()

    #Start GMS Services
    start_gms_services()





###################################DB CONNECTION########################################
def db_connection(db_ip, db_username, db_password, db_name):
    connection = MySQLdb.connect(host=db_ip,    # your host, usually localhost
                                 user=db_username,         # your username
                                 passwd=db_password,  # your password
                                 db=db_name)        # name of the data base                           
    return connection
########################################################################################


"""
=============================================================================================================
============================================MySQL QUERY FUNCTIONS==============================================
=============================================================================================================
"""
#Change the scheduler IP
def update_schedulers(handle, new_ip, old_ip):
    handle.execute("""UPDATE schedulers set ipAddress = %s where ipAddress = %s""", (new_ip, old_ip))

#Change the IP in the sgms_config table
def update_sgms_config(handle, new_ip, old_ip):
    handle.execute("""UPDATE sgms_config set paramValue = %s where paramValue = %s""",(new_ip, old_ip))

#Change the summarizer IP    
def update_summarizers(handle, new_ip, old_ip):
    handle.execute("""UPDATE summarizers set ipAddress = %s where ipAddress = %s""", (new_ip, old_ip))

#Change the monitor IP
def update_monitors(handle, new_ip, old_ip):
    handle.execute("""UPDATE monitors set ipAddress = %s where ipAddress = %s""", (new_ip, old_ip))

#Change the perf_summarizer_thread IP
def update_perf_summarizer_thread(handle, new_ip, old_ip):
    handle.execute("""UPDATE perf_summarizer_thread set summarizer_ID = %s where summarizer_ID = %s""", (new_ip, old_ip))

#Change the perf_syslog_collector IP
def update_perf_syslog_collector(handle, new_ip, old_ip):
    handle.execute("""UPDATE perf_syslog_collector set scheduler_IP  = %s where scheduler_IP = %s""", (new_ip, old_ip))

#Change perf_viewpoint_summarizer IP
def update_perf_viewpoint_summarizer(handle, new_ip, old_ip):
    handle.execute("""UPDATE perf_viewpoint_summarizer set summarizer_IP = %s where summarizer_IP = %s""", (new_ip, old_ip))

#Change perf_syslog_files IP
def update_perf_syslog_files(handle, new_ip, old_ip):
    handle.execute("""UPDATE perf_syslog_files set summarizer_IP = %s where summarizer_IP = %s""", (new_ip, old_ip))

#Change trapmgrs IP
def update_trapmgrs(handle, new_ip, old_ip):
    handle.execute("""UPDATE trapmgrs set listenip = %s where listenip = %s""", (new_ip, old_ip))

#Change gmsvpinstances IP
def update_gmsvpinstances(handle, new_ip, old_ip):
    handle.execute("""
    UPDATE gmsvpinstances set ipAddress=%s where ipAddress=%s
    """, (new_ip, old_ip))

#Change externalhome for gmsvpinstances
def update_wsexternalhome(handle, new_ip, old_ip):
    handle.execute("""UPDATE gmsvpinstances set wsExternalHostname = %s where wsExternalHostname = %s""",
                   ('https://'+new_ip, 'https://'+old_ip))

#Change vpng_databases IP
def update_vpng_databases(handle, new_ip, old_ip):
    handle.execute("""UPDATE vpng_databases set ipAddress = %s where ipAddress = %s""", (new_ip, old_ip))


"""
=============================================================================================================
========================================END MySQL QUERY FUNCTIONS==============================================
=============================================================================================================
"""


###################################################################

def change_ip(connection, service_name, handle, new_ip, old_ip):
    handle.execute(
        """UPDATE %s set ipAddress = %s where ipAddress = %s""", (service_name, new_ip, old_ip))
    connection.commit()    
###################################################################


"""
=============================================================================================================
========================================STOP GMS Services in Linux==============================================
=============================================================================================================
"""
#Stop all GMS services
def stop_gms_services():
    subprocess.run(["/opt/GMSVP/bin/sgms", "all", "stop"], check=True)

#Start all GMS services
def start_gms_services():
    subprocess.run(["nohup","/opt/GMSVP/bin/sgms", "all", "start",">","/dev/null"], check=True)

"""
=============================================================================================================
========================================END STOP GMS Services in Linux==============================================
=============================================================================================================
"""


if __name__ == '__main__':
    main()
