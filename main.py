#!/usr/bin/env python2.7
#
# Author: Gowtham Sai
# Website: https://gowtham-sai.com
# Aritcle: blog.gowtham-sai.com (Will be updated soon)
# Date: 7th Aug, 2016.
# Purpose: BI Visualisation Tool Customisation & Configuration.
# What this script do?
#       -- This script will install superset and configures everything.
# Where do I need to modify the configuration?
#       -- There are few configuraiton files in this directory. Please go through the documentation.
#
# Sigstamp: 7h3 !n5|d3r

import os
import sys
import site
import json
import yaml
import mylog
import thread
import socket
import urllib
import urllib2
import getpass
import platform
import argparse
import subprocess


# Reading file from commandline.
parser = argparse.ArgumentParser()
parser.add_argument("-c", "--configFile", help="echo the string you use here")
args = parser.parse_args()

# Adding logger
log_file_name = urllib.urlopen('http://ip.42.pl/raw').read() + '.log'
logger = mylog.Log(to_file=True, filename=log_file_name)

# Setting up config file
config_file = args.configFile if args.configFile else "config.yaml"
sudo_pass = ''

# STASTIC CONF
ZK_CONFIG = ["tickTime=2000", "initLimit=10", "syncLimit=5", "dataDir=/tmp/zookeeper", "clientPort=2181",
             "clientPortAddress=INSIDERHOST", "maxClientCnxns=0", "autopurge.snapRetainCount=5", "autopurge.purgeInterval=1"]

SUPERVISOR_CONFIG_ZK = ['[supervisord]\n', 'nodaemon=true\n', 'loglevel=debug\n', '\n', '[program:zookeeper]\n', 'command=/var/lib/zookeeper/bin/zkServer.sh start-foreground\n',
                        'autostart=true\n', 'user=root\n', 'autorestart=true\n', 'stdout_logfile=/var/log/zookeeper/zookeeper.log\n', 'stdout_logfile_maxbytes=50MB\n', 'redirect_stderr=true\n', 'priority=0\n']



# SSH Preparation


def ssh_handler(host):
    filename = host + "_" + str(int(time.time())) + '.yaml'
    command_center("mkdir %s" % host)
    data = custom_json["hosts"][host]
    data['over_ssh'] = False
    with open(filename, 'w') as host_conf_file:
        yaml.dump(data, host_conf_file, default_flow_style=False)
    command_center("scp ./%s %s:/tmp/" % (host_conf_file, host))
    command_center("scp ./%s %s:/tmp/" % (__file__, host))
    command_center("ssh %s 'sudo su && cd /tmp && python %s --configFile %s'" %
                   (host, __file__, filename))
    command_center("mv %s %s/" % (filename, host))
    command_center("scp %s:/tmp/*.log ./%s" % (host,host))

# General configuraiton which installs supervisor, nginx, pm2, node


def general_config():
    command_center("apt-get update")
    command_center("apt-get install default-jre")
    command_center("apt-get install -y git")
    command_center("apt-get install -y supervisor")
    command_center("apt-get install -y python-software-properties")
    command_center("apt-get install -y nginx")
    command_center(
        "curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash -")
    command_center("apt-get install -y nodejs")

# Constructor for github repo cloning.
# https://github.com/airbnb/superset.git
# git@github.com:airbnb/superset.git


def git_resolver(host):
    is_ssh = True if '@' in host else False
    is_http = True if 'http' in host else False
    if is_ssh:
        url_split = host.split(':')[1].split('/')
        git_user = url_split[0]
        git_repo = url_split[1] if not '.git' in url_split[
            1] else url_split[1].split('.')[0]
    elif is_http:
        url_split = host.split('/')
        git_user = url_split[3]
        git_repo = url_split[-1] if not '.git' in url_split[-1] else url_split[-1].split('.')[
            0]
    else:
        url_split = host.split('/')
        git_user = url_split[1]
        git_repo = url_split[-1] if not '.git' in url_split[-1] else url_split[-1].split('.')[
            0]
    return git_user, git_repo


def git_constructor(git_user, git_repo):
    if '.git' in git_repo:
        return 'http://www.github.com/' + git_user + '/' + git_repo
    else:
        return 'http://www.github.com/' + git_user + '/' + git_repo + '.git'


# Static Dependency Functions.
def get_git_branches(host, requested_branch):
    git_user, git_repo = git_resolver(host)
    url = "http://api.github.com/repos/%s/%s/branches" % (git_user, git_repo)
    headers = {"Accept": "application/vnd.github.loki-preview+json"}
    req = urllib2.Request(url, headers=headers)
    res = urllib2.urlopen(req)
    jdata = res.readlines()[0]
    data = json.loads(jdata)
    branches = [v for b in data for k, v in b.iteritems() if k == 'name']
    return requested_branch in branches

# Command Center.


def command_center(install_cmd, exit_on_fail=False):
    # Executes the commands and return False if failed to execute
    install_cmd = "echo '%s' | sudo -S " % sudo_pass + install_cmd
    logger.info("Running command: %s"%install_cmd)
    exec_cmd = subprocess.Popen(
        install_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    exec_output, exec_error = exec_cmd.communicate()
    if exec_cmd.returncode != 0:
        logger.fatal("Error while installing. Check below and logs file:")
        logger.info(exec_error)
        return sys.exit(1) if exit_on_fail else (False, exec_error)
    return (True, exec_output)


def druid_install(data):
    node = data['node']
    github = data['github']
    version = data['branch'] if data['branch'] else 'master'
    if not get_git_branches(github, version):
        logger.fatal(
            "Unable to fetch druid from the %s repo. Skipping installation..!" % github)
    else:
        git_user, git_repo = git_resolver(github)
        command_center("apt-get install git")
        command_center("git clone %s -b %s /tmp/druid-%s" %
                       (git_constructor(git_user, git_repo), version, version))
        command_center("mv /tmp/druid-%s/ /var/lib/" %
                       (version))
        command_center("ln -s /var/lib/druid-%s /var/lib/druid" % (version))


def mysql_install(data):
    command_center("debconf-set-selections <<< 'mysql-server mysql-server/root_password password %s'"%data['password'])
    command_center("debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password %s'"%data['password'])
    command_center("apt-get install -y mysql-server")
    command_center("service mysql start")
    command_center("mysql -u root -p'%s' -e 'create database %s'"%(data['password'], data['database']))
    command_center("mysql -u root -p'%s' -e 'create user \"%s\"@\"%\" IDENTIFIED BY \"%s\"'"%(data['password'],data['dbuser'], data['dbpassword']))
    command_center("mysql -u root -p'%s' -e 'grant all on druid.* to \"%s\"@\"%\" IDENTIFIED BY \"%s\"'"%(data['password'],data['dbuser'], data['dbpassword']))

def kafka_install(data):
    command_center("curl http://redrockdigimark.com/apachemirror/kafka/0.9.0.0/kafka_2.11-0.9.0.0.tgz > /tmp/kafka_2.11-0.9.0.0.tgz")
    command_center("tar -xvzf /tmp/kafka_2.11-0.9.0.0.tgz -C /tmp/")
    command_center("mv /tmp/kafka_2.11-0.9.0.0 /var/lib/")
    command_center("ln -s /var/lib/kafka_2.11-0.9.0.0 /var/lib/kafaka")

def zookeeper_install(data):
    command_center("curl http://www-us.apache.org/dist/zookeeper/zookeeper-3.4.6/zookeeper-3.4.6.tar.gz > /tmp/zookeeper-3.4.6.tgz")
    command_center("tar -xvzf /tmp/zookeeper-3.4.6.tgz -C /tmp/")
    command_center("mv /tmp/zookeeper-3.4.6 /var/lib/")
    command_center("ln -s /var/lib/zookeeper-3.4.6 /var/lib/zookeeper")
    command_center("touch /var/lib/zookeeper/conf/zoo.cfg")
    private_ip = command_center("hostname -I")[1]
    with open("/var/lib/zookeeper/zoo.cfg", "w") as zf_file:
        for line in ZK_CONFIG:
            line = line.replace("INSIDERHOST", command_center("hostname -I")[1]) if "INSIDERHOST" in line else line
    command_center("supervisor reread")
    command_center("supervisor update")
    command_center("supervisor status all")
    command_center("touch /etc/supervisor/conf.d/zookeeper.conf")
    with open("/etc/supervisor/conf.d/zookeeper.conf", "w") as zk_sup:
        for line in SUPERVISOR_CONFIG_ZK:
            zk_sup.write(line)

def nodejs_install(data):
    command_center("touch /etc/profile.d/node_vars.sh")
    command_center('echo PM2_HOME="/etc/pm2"')
    github = data['github']
    version = data['branch'] if data['branch'] else 'master'
    if not get_git_branches(github, version):
        logger.fatal(
            "Unable to fetch capeve from the %s repo. Skipping installation..!" % github)
    else:
        git_user, git_repo = git_resolver(github)
        command_center("git clone %s -b %s /tmp/capeve-%s" %
                       (git_constructor(git_user, git_repo), version, version))
        command_center("mv /tmp/capeve-%s/ /var/lib/" %
                       (version))
        command_center("ln -s /var/lib/capeve-%s /var/lib/capeve" % (version))

    command_center("npm install pm2 -g")
    command_center("pm2 install pm2-logrotate")
    command_center("pm2 set pm2-logrotate:max_size 100M")
    command_center("pm2 set pm2-logrotate:compress true")
    command_center("pm2 set logrotate:rotateInterval '* * */1 * *'")
    command_center("pm2 save")

def memcahched_install(data):
    command_center("apt-get install -y memcahched")

with open(config_file, 'r') as stream:
        try:
            custom_json = yaml.load(stream)
            if not custom_json['over_ssh']:
                general_config()
                services = custom_json['services']
                for request in services.keys():
                    logger.info("Going to install %s"%request)
                    exec(request + "_install(%s)" % services[request])
                    logger.info("%s Installation Done.!"%request)
            else:
                for host in custom_json['hosts'].keys():
                    s(host)
            
        except yaml.YAMLError as exc:
            print exc

