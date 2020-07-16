"""The script is used to run snmp agent for multiple device templates chosen by the user."""

# -*- coding: utf-8 -*-
import os
import argparse
import fnmatch
import socket
import subprocess
from utils import Utils
from faker import Faker

class DeviceSimulator():
    "Class to simulate snmp devices."
    def __init__(self):
        "initialize"
        utils = Utils()
        self.config = utils.read_conf('device.conf')

    def parse_args():
        "This function is used to input the templates chosen by the user."
        # Initialize parser
        parser = argparse.ArgumentParser(description='SNMP Simulator.')
        group = parser.add_mutually_exclusive_group(required=True)

        # Adding optional argument
        group.add_argument('-d', '--devices', required=False, nargs='+',
                            help="Enter single or multiple file names using '-d' option Ex:- -d xp.snmprec ubuntu.snmprec", default=False, metavar="")
        group.add_argument('-p', '--print', required=False, action='store_true',
                            help=" use '-p' for listing down available device templates to use")
        # Read arguments from command line
        args = parser.parse_args()
        return args

    def available_templates(data_dir):
        """ Check for available device templates."""
        try:
            print('************Available device templates to use found in data directory********')
            for (root_dir_path, _, files) in os.walk(data_dir):
                if files:
                    tag = os.path.relpath(root_dir_path, data_dir)

                    for file in files:

                        sub_folder = os.path.basename(tag)

                        print((sub_folder if sub_folder else ''), '--->', file)

            print('************End********')
        except:
            raise("Error in reading available device templates ")

    def find_dev_templates(data_dir, dev_templates):
        """To find the device template path in data directory."""
        templates_path = []

        for (root_dir_path , _, files) in os.walk(data_dir):

            if files:
                tag = os.path.relpath(root_dir_path, data_dir)
                for device in dev_templates:
                    for file in files:
                        tag_parent = os.path.dirname(tag)
                        sub_folder = os.path.basename(tag)
                        if fnmatch.fnmatch(file, device):
                            templates_path.append(os.path.normpath(
                                os.path.join(data_dir, tag_parent, sub_folder)))

        return templates_path

    def get_open_port(self,host):
        """To find open port."""
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, 0))
        s.listen(1)
        port = s.getsockname()[1]
        s.close()
        return port

    def create_snmp(self,templates_path,host):
        """check response by snmpget for the chosen device templates."""
        num_devices = len(templates_path)
        ports = []
        dev_dirs = []
        for i in range(num_devices):
            try:
                port = self.get_open_port(host)
                ports.append(port)
                dev_dirs.append(templates_path[i])
                print("snmpsim run: %d." %(i + 1), templates_path[i].split('/')[-1], port)
                subprocess.run(("snmpsimd.py --v3-engine-id=010203040505060880 --v3-user=qxf2 --data-dir=%s --agent-udpv4-endpoint=127.0.0.1:%s --logging-method=file:./data/snmp_logs.txt:10m --log-level=debug &" %(templates_path[i], port)),shell=True)
            except OSError:
                raise ValueError(
                    "error in running the snmp device 'snmpsimd.py' command")

        return ports, dev_dirs

    def check_snmp_response(self,ports,dirs):
        "check if simulated devices are up and running on the aligned ports."
        active_devices = []
        active_ports = []
        try:
            for (port,dir) in zip(ports,dirs):
                device = dir.split('\\')[-1].split('/')[-1]
                response = subprocess.call("snmpget -v2c -c %s 127.0.0.1:%s 1.3.6.1.2.1.1.1.0" %(device, port),shell=True)
                if response == 0:
                    print("\n %s is up and running on the port:%s \n"%(device,port))
                    active_ports.append(port)
                    active_devices.append(device)
                else:
                    print("\n %s is not running as expected on the port:%s \n"%(device,port))
        except OSError:
            raise("Error in checking snmp response for the given device")

        return active_ports,active_devices
    
    def update_iptables(self,port_list,active_devices_val):
        "re-routing the active ports traffic to some fake ips."
        active_ips = []
        mapped_devices = []
        for port,device in zip(port_list,active_devices_val):
            faker = Faker()
            ip = faker.ipv4()
            try:
                subprocess.run(("sudo iptables -t nat -A OUTPUT -p udp -d %s --dport 1:65535 -j DNAT --to-destination 127.0.0.1:%s"%(ip,port),shell=True))
                subprocess.run(("sudo iptables -t nat -A OUTPUT -p icmp -d %s  --icmp-type echo-request -j DNAT --to-destination 127.0.0.1:%s"%(ip,port),shell=True))
                subprocess.run(("sudo iptables -t nat -A OUTPUT -p tcp -d %s  --dport 22 -j DNAT --to-destination 127.0.0.1:%s"%(ip,port),shell=True))
                active_ips.append(ip)
                mapped_devices.append(device)
            except OSError:
                raise ValueError('error in running the iptable update commands')
        return active_ips,mapped_devices

if __name__ == '__main__':
    devices = DeviceSimulator()
    args = DeviceSimulator.parse_args()
    data_dir = devices.config.get('data','dir')
    host = devices.config.get('data','host')

    if args.print is True:
        DeviceSimulator.available_templates(data_dir)
    elif args.devices is not False:
        templates = DeviceSimulator.find_dev_templates(data_dir, args.devices)
        if templates is not None:
            print("\n Running SNMP simulated devices....\n")
            ports_val,dev_dir_val = devices.create_snmp(templates,host)
            if ports_val is not None:
                print("\n Checking SNMP simulated devices response....\n ")
                active_ports_val,active_devices_val = devices.check_snmp_response(ports_val,dev_dir_val)
                print("\n Updating iptables with fake ip's re-routing traffic to active ports\n")
                simulated_ip_val,mapped_devices_val = devices.update_iptables(active_ports_val,active_devices_val)
                print("\n Here are the list of mapped ip's - %s and simulated devices - %s\n"%(simulated_ip_val,mapped_devices_val))

