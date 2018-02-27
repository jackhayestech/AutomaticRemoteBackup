from fabric.api import *
import datetime
import json
from pprint import pprint

sites = json.load(open('sites.json'))

hosts = []
passwords = {}
site_settings = {}

for site in sites:
    user = sites[site]['user']
    host = sites[site]['host']
    password = sites[site]['password']
    tmp_back_name = sites[site]['back_name']
    tmp_back_dir = sites[site]['back_dir']
    tmp_local_dir = sites[site]['local_dir']

    hosts.append(user + '@' + host)
    passwords[user + '@' + host + ":22"] = password

    tmp_settings = {"back_name" : tmp_back_name, "back_dir" : tmp_back_dir, "local_dir" : tmp_local_dir}
    site_settings[user + '@' + host] = tmp_settings

env.hosts = hosts
env.passwords = passwords
def create_file_backup():
    site_settings[env.host_string]

    back_name = site_settings[env.host_string]["back_name"]
    back_dir = site_settings[env.host_string]["back_dir"]
    local_dir = site_settings[env.host_string]["local_dir"]

    now = datetime.datetime.now()
    name = back_name + now.strftime("%Y-%m-%d")
    run('tar -zcvf ' + name + '.tar.gz ' + back_dir)
    curr_dir = run('pwd')
    get(curr_dir + '/' + name + '.tar.gz', local_dir)
    run('rm ' + name + '.tar.gz')