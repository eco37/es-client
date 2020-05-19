#!/usr/bin/python3 -tt
# -*- coding: utf-8 -*-
# File   : es-client.py
# Created: 19-05-31
#
# sudo apt-get install python-cmd2 python-requests python-argparse
# sudo apt-get install python3 python3-pip
## pip3 install -U cmd2

import argparse
import cmd2
import requests
from requests.exceptions import HTTPError
import signal
import os, sys

# FIXME: Set a value on a variable and check that variable on functions that is running
def sigint_handler(signum, frame):
    pass
 
signal.signal(signal.SIGINT, sigint_handler)

class MyPrompt(cmd2.Cmd):
    prompt = 'ES-Client (NONE)> '
    intro = "Welcome! Type ? to list commands"
    
    def preloop(self):
        self.cmdqueue = [];

    def init(self, host, port):
        self.host = host
        self.port = port
        self.prompt = 'ES-Client ({}:{})> '.format(self.host, self.port)

    def do_exit(self, inp):
        "Exit the application. Shorthand Ctrl-D"
        print("Exits...")
        return True
    
    def do_shell(self, line):
        "Run a shell command"
        output = os.popen(line).read()
        print(output)

    host_parser = argparse.ArgumentParser()
    host_parser.add_argument('host', help='Host/IP')
    host_parser.add_argument('port', help='Port')

    @cmd2.with_argparser(host_parser)
    def do_set_host(self, args):
        "Set new target host and port"
        self.host = args.host
        self.port = args.port
        self.prompt = 'ES-Client ({}:{})> '.format(self.host, self.port)

    
    def do_nodes(self, inp):
        "List connected nodes to cluster."
        headers = {
            'Content-Type': 'application/json',
        }

        params = (
            ('v', ''),
        )
        
        try:
            response = requests.get('http://{}:{}/_cat/nodes'.format(self.host, self.port), headers=headers, params=params)
            if not response:
                print(response.status_code)
                sys.stdout.buffer.write(response.content)
            else:
                sys.stdout.buffer.write(response.content)
        
        except HTTPError as http_err:
            print('HTTP error occurred: {}'.format(http_err))
        except Exception as err:
            print("Other error occurred: {}".format(err))

    def do_indices(self, inp):
        "Show indices information"
        headers = {
            'Content-Type': 'application/json',
        }

        params = (
            ('v', ''),
        )
        
        try:
            response = requests.get('http://{}:{}/_cat/indices'.format(self.host, self.port), headers=headers, params=params)
            if not response:
                print(response.status_code)
                sys.stdout.buffer.write(response.content)
            else:
                sys.stdout.buffer.write(response.content)
        
        except HTTPError as http_err:
            print('HTTP error occurred: {}'.format(http_err))
        except Exception as err:
            print("Other error occurred: {}".format(err))
    
    def do_cluster_health(self, args):
        "Show cluster health"
        params = (
            ('pretty', ''),
        )

        try:
            response = requests.get('http://{}:{}/_cluster/health'.format(self.host, self.port), params=params)
            if not response:
                print(response.status_code)
                sys.stdout.buffer.write(response.content)
            else:
                sys.stdout.buffer.write(response.content)
        
        except HTTPError as http_err:
            print('HTTP error occurred: {}'.format(http_err))
        except Exception as err:
            print("Other error occurred: {}".format(err))
    
    def do_cluster_state(self, args):
        "Show cluster state"
        params = (
            ('pretty', ''),
        )

        try:
            response = requests.get('http://{}:{}/_cluster/state'.format(self.host, self.port), params=params)
            if not response:
                print(response.status_code)
                sys.stdout.buffer.write(response.content)
            else:
                sys.stdout.buffer.write(response.content)
        
        except HTTPError as http_err:
            print('HTTP error occurred: {}'.format(http_err))
        except Exception as err:
            print("Other error occurred: {}".format(err))

    settings_parser = argparse.ArgumentParser()
    settings_parser.add_argument('index', help='Index to show settings from')

    @cmd2.with_argparser(settings_parser)
    def do_settings(self, args):
        "Show settings from Index"
        params = (
            ('pretty', ''),
        )

        try:
            response = requests.get('http://{}:{}/{}/_settings'.format(self.host, self.port, args.index), params=params)
            if not response:
                print(response.status_code)
                sys.stdout.buffer.write(response.content)
            else:
                sys.stdout.buffer.write(response.content)
        
        except HTTPError as http_err:
            print('HTTP error occurred: {}'.format(http_err))
        except Exception as err:
            print("Other error occurred: {}".format(err))

    set_settings_parser = argparse.ArgumentParser()
    set_settings_parser.add_argument('index', help='Index to change settings in')
    set_settings_parser.add_argument('field', help='Settings field')
    set_settings_parser.add_argument('value', help='Settings value')

    @cmd2.with_argparser(set_settings_parser)
    def do_set_settings(self, args):
        "Change a settings value"
        headers = {
            'Content-Type': 'application/json',
        }
        
        params = (
            ('pretty', ''),
        )

        if args.value == "null":
            data = '{{"{}":null}}'.format(args.field)
        else:
            data = '{{"{}":"{}"}}'.format(args.field, args.value)

        try:
            response = requests.put('http://{}:{}/{}/_settings'.format(self.host, self.port, args.index), headers=headers, data=data, params=params)
            if not response:
                print(response.status_code)
                sys.stdout.buffer.write(response.content)
            else:
                sys.stdout.buffer.write(response.content)
        
        except HTTPError as http_err:
            print('HTTP error occurred: {}'.format(http_err))
        except Exception as err:
            print("Other error occurred: {}".format(err))
    
    do_EOF = do_exit

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-H", "--hostname", dest='hostname', default='localhost', help='IP or Hostname (default: localhost)')
    parser.add_argument("-p", "--port", dest='port', default=9200, help='Port (default: 9200)')
    parser.add_argument("-c", "--commands", dest='commands', nargs="+", help='Commands')

    args = parser.parse_args()

    prompt = MyPrompt()
    prompt.init(args.hostname, args.port)
    
    if args.commands:
        print("Commands: ", end='')
        print(args.commands)
        print("")
        for command in args.commands:
            prompt.onecmd(command)
            print("")
    else:
        prompt.cmdloop()

