import subprocess
import requests
import os

# Loads the settings for the user running the script
settings = json.load(open('settings.json'))

# Gets a date from a backups file name
def get_date(filename):
    split = filename.split('-')
    year = split[1]
    month = split[2]
    day = split[3].split('.')[0]
    return datetime(int(year),int(month),int(day))

# Manages the backups of the site
def manage_backups(name,local_dir,number_of_backups):
    files = os.listdir(local_dir)
    # The number of local backups exceed the limit
    if len(files) > number_of_backups: 
        # The oldest backup
        oldest_backup = ""
        oldest_backup_date = datetime.now()
        # Loops through the files
        for f in files:
            # Compares the files date to the current oldest found date
            if oldest_backup_date > get_date(f):
                # Updates the oldest backup variables
                oldest_backup_date = get_date(f)
                oldest_backup = f

        #Deletes the oldest backup
        subprocess.call(['rm',local_dir + '/' + oldest_backup])

#An error has been found
def error_with_execution(backName):
    errors.append(backName + '\n')

# Signals the remote server to send the email
def send_confirmation(results_string):
    url = settings['confirm_backup_address']
    payload = {'password': settings['confirm_backup_password'], 'email': settings['confirm_backup_email'],  'result': results_string}
    r = requests.post(url, data=payload)

# Checks the local backup device for remaining space
def check_remaining_disk_space(local_dir):
    # Gets the amount of space free on the local directory
    command = ['df -Ph ' + local_dir + " | tail -1 | awk '{print $4}'"]
    free = subprocess.check_output(command,shell=True).strip().decode('ascii')
    # Gets the total amount of space availiable on the directory
    command = ['df -Ph ' + local_dir + " | tail -1 | awk '{print $2}'"]
    total = subprocess.check_output(command,shell=True).strip().decode('ascii')
    # Constructs the message
    message = "Directory " + local_dir + " has " + str(free) + "/" + str(total) + " remaining disk space"
    return message