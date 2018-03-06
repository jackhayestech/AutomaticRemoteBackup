# AutomaticRemoteBackup
A tool to automatically create local backups of remote directories

# Required dependiecs
1. Requests, install with: pip install requests

2. Fabric, install with: pip install fabric or pip install fabric3 if running python version 3

# Instructions
1. Rename settings.json.example and sites.json.example removing the .example from the file name.

2. Fill out the settings.json and sites.json

3. Add "fab -f run_backup.py create_file_backup finished" to your cron 
