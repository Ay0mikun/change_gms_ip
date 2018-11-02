import MySQLdb #Use this to talk to MySQL datbase
import os #Use this to talk to GMS services on Linux OS
import subprocess #Run Linux commands using subprocess modules


def main():
    sgmsdb_tables = ["schedulers","summarizers","monitors","gmsvpinstances","vpng_databases"]
    gms_db_name = "sgmsdb"
    #Stop GMS Services
    #stop_gms_services()

    print("Enter the GMS database credentials...")

    gms_db_ip = input("What is the database IP address? ")
    gms_db_username = input("What is the database username? ")
    gms_db_password = input("What is the database password? ")

    #Create database connection to GMS DB
    try:
        db = db_connection(gms_db_ip, gms_db_username,
                            gms_db_password, gms_db_name)
        # You must create a Cursor object. It will let you execute all the queries you need
        cur = db.cursor()
        print("Successfully created database connection.")
    except:
        print("ERROR: Unable to establish database connection. Verify you have the correct username and/or password.")
    

    old_gms_ip = input("\nWhat is the OLD GMS server IP address? ")
    new_gms_ip = input("What is the NEW GMS server IP address? ")

    print("\nChanging IP addresses, please wait...")

    for table in sgmsdb_tables:
        try:
            change_ip(db,table,cur,new_gms_ip,old_gms_ip)
        except:
            print("ERROR: Failed to update IP in {} table".format(table))    

   # update_sgms_config(db, cur, new_gms_ip, old_gms_ip)
   # update_perf_summarizer_thread(db, cur, new_gms_ip, old_gms_ip)
    #update_perf_syslog_collector(db, cur, new_gms_ip, old_gms_ip)
    #update_perf_syslog_files(db, cur, new_gms_ip, old_gms_ip)
    #update_trapmgrs(db, cur, new_gms_ip, old_gms_ip)
    #update_wsexternalhome(db, cur, new_gms_ip, old_gms_ip)
    #update_perf_viewpoint_summarizer(db, cur, new_gms_ip, old_gms_ip)
    
    #db.close()

    print("Successfully changed IP addresses. Done.")

    #Start GMS Services
    #start_gms_services()





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
import pdb
#Change IP addresses in SGMSDB tables list
def change_ip(connection, service_name, handle, new_ip, old_ip):
    pdb.set_trace()
    handle.execute(
        """UPDATE %s set ipAddress = %s where ipAddress = %s""", (service_name, new_ip, old_ip))
    connection.commit()

#Change the IP in the sgms_config table
def update_sgms_config(connection, handle, new_ip, old_ip):
    try:
        handle.execute(
            """UPDATE sgms_config set paramValue = %s where paramValue = %s""", (new_ip, old_ip))
        connection.commit()
    except:
        print("ERROR: Failed to change IP in 'sgms_config' table.")    

#Change the perf_summarizer_thread IP
def update_perf_summarizer_thread(connection, handle, new_ip, old_ip):
    try:
        handle.execute("""UPDATE perf_summarizer_thread set summarizer_ID = %s where summarizer_ID = %s""", (new_ip, old_ip))
        connection.commit()
    except:
        print("ERROR: Failed to change IP in 'perf_summarizer_thread' table.")

#Change the perf_syslog_collector IP
def update_perf_syslog_collector(connection, handle, new_ip, old_ip):
    try:
        handle.execute("""UPDATE perf_syslog_collector set scheduler_IP  = %s where scheduler_IP = %s""", (new_ip, old_ip))
        connection.commit()
    except:
        print("ERROR: Failed to change IP in 'perf_syslog_collector' table.")

#Change perf_viewpoint_summarizer IP
def update_perf_viewpoint_summarizer(connection, handle, new_ip, old_ip):
    try:
        handle.execute("""UPDATE perf_viewpoint_summarizer set summarizer_IP = %s where summarizer_IP = %s""", (new_ip, old_ip))
        connection.commit()
    except:
        print("ERROR: Failed to change IP in 'perf_viewpoint_summarizer' table.")

#Change perf_syslog_files IP
def update_perf_syslog_files(connection, handle, new_ip, old_ip):
    try:
        handle.execute("""UPDATE perf_syslog_files set summarizer_IP = %s where summarizer_IP = %s""", (new_ip, old_ip))
        connection.commit()
    except:
        print("ERROR: Failed to change IP in 'perf_syslog_files' table.")

#Change trapmgrs IP
def update_trapmgrs(connection, handle, new_ip, old_ip):
    try:
        handle.execute("""UPDATE trapmgrs set listenip = %s where listenip = %s""", (new_ip, old_ip))
        connection.commit()
    except:
        print("ERROR: Failed to change IP in 'trapmgrs' table.")

#Change externalhome for gmsvpinstances
def update_wsexternalhome(connection, handle, new_ip, old_ip):
    try:
        handle.execute("""UPDATE gmsvpinstances set wsExternalHostname = %s where wsExternalHostname = %s""",
                   ('https://'+new_ip, 'https://'+old_ip))
        connection.commit()
    except:
        print("ERROR: Failed to update 'wsexternalhome' in 'gmsvpinstances' table.")


"""
=============================================================================================================
========================================END MySQL QUERY FUNCTIONS==============================================
=============================================================================================================
"""



"""
=============================================================================================================
========================================GMS Services in Linux==============================================
=============================================================================================================
"""
#Stop all GMS services
#def stop_gms_services():
#    subprocess.run(["/opt/GMSVP/bin/sgms", "all", "stop"], check=True)

#Start all GMS services
#def start_gms_services():
#    subprocess.run(["nohup","/opt/GMSVP/bin/sgms", "all", "start",">","/dev/null"], check=True)

"""
=============================================================================================================
========================================END GMS Services in Linux==============================================
=============================================================================================================
"""


if __name__ == '__main__':
    main()
