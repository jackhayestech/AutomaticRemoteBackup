#pip install requests
#pip install fabric
from fabric.api import *
from datetime import datetime
from functions import *
import json

# Loads the remote servers information required to create backups
sites = json.load(open('sites.json'))
# Loads the settings for the user running the script
settings = json.load(open('settings.json'))
# List of all the hosts to connect to
hosts = []
# Dictonary of the passwords
passwords = {}
# Dictonary of the settings needed to create the backups
site_settings = {}
# A list of errors that have occured during the back up
errors = []
# A list of the messages to display
messages = []

#Loops through all the sites in the sites.json file
for site in sites:
    #Gets the current site username
    user = sites[site]['user']
    #Gets the current site address
    host = sites[site]['host']
    #Gets the current sites password
    password = sites[site]['password']
    #What the back up will be saved as
    tmp_back_name = sites[site]['back_name']
    #The directory on the remote server to be backed up
    tmp_back_dir = sites[site]['back_dir']
    #The directory where the back is to be saved
    tmp_local_dir = sites[site]['local_dir']
    # The max number of backups to be stored for this site
    tmp_num_backs = sites[site]['number_of_backups']
    #Adds the host connection to the hosts list
    hosts.append(user + '@' + host)
    #Adds the password to the password dictonary
    passwords[user + '@' + host + ":22"] = password
    #Loads the settings into a temp dictonary
    tmp_settings = {"back_name" : tmp_back_name, 
        "back_dir" : tmp_back_dir, 
        "local_dir" : tmp_local_dir, 
        "number_of_backups" : tmp_num_backs}
    #Copies the dictonary into the site settings dictonary
    site_settings[user + '@' + host] = tmp_settings

# Sets the fabric env hosts to our loaded hosts list
env.hosts = hosts
# Sets the fabric env passwords to our loaded passwords dictonary
env.passwords = passwords

# Connects to the remote server and downloads a backup
def create_file_backup():
    try:
        # Gets the sites settings for the current site
        site_settings[env.host_string]
        # Loads individual settings into the appropriate variables
        back_name = site_settings[env.host_string]["back_name"]
        back_dir = site_settings[env.host_string]["back_dir"]
        local_dir = site_settings[env.host_string]["local_dir"]
        # Creates the backup name
        now = datetime.now()
        name = back_name + "-" + now.strftime("%Y-%m-%d")
        # Creates a backup
        run('tar -zcvf ' + name + '.tar.gz ' + back_dir)
        # Gets the absolute path to the backup
        curr_dir = run('pwd')
        # Downloads the backup to the local directory
        get(curr_dir + '/' + name + '.tar.gz', local_dir)
        # Removes the backup from the remote server
        run('rm ' + name + '.tar.gz')
        # Checks the remaining diskspace on the local directory
        diskspace_message = check_remaining_disk_space(local_dir)
        # Appends the new message to the message list
        messages.append(diskspace_message)
        # Manages the sites created backups deleting any copies if the max backup limit is reached
        manage_backups(back_name,local_dir,site_settings[env.host_string]["number_of_backups"])
    # An error has occured during the backup
    except SystemExit:
        error_with_execution(name)

# The full list of hosts has been run through
@runs_once
def finished():
    # If a confirmation email is to be sent
    if settings['confirm_backup'] == "true":
        # The results of this backup
        results_string = ""
        # Errors have occured
        if len(errors) > 0:
            results_string = results_string + "The following backups have completed with errors: \n\n"
            for error in errors: 
                results_string = results_string + error + "\n"
          # The backup ran without issue
        else:
            results_string = results_string + "The back up concluded with no issues \n\n"

        # There are messages
        if len(messages) > 0:
            results_string = results_string +  "The backups concluded with these messages: \n"
            for message in messages: 
                results_string = results_string + message + "\n"
        #Sends the confirmation request
        send_confirmation(results_string)
