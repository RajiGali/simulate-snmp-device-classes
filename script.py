'''
This python script is used to print the available templates
Get the user input for available device templates.

'''

import os
import argparse
from colored import fg, bg, attr
import fnmatch,itertools
#from faker import Faker

my_dir = ".//data"

class simulate_snmp_devices():
    'Class to simulate snmp devices' 

    

    def available_templates(self,*args):
        #Print the templates
        
        #if args == 'True':
            print("************Available device templates to use in data directory********")

            for root_dir_path, sub_dirs, files in os.walk(my_dir):
                
                color = fg('orchid') + attr('bold')
                reset = attr('reset')
                        
                if files:
                    tag = os.path.relpath(root_dir_path, my_dir)

                    for file in files:
                        tag_parent = os.path.dirname(tag)
                        sub_folder = os.path.basename(tag)

                        print(sub_folder if sub_folder else "","--->",(color+(file)+reset))
                
            print("************End********")
        

    def parse_args(self):
        #This function is used to print the templates chosen by the user

        # Initialize parser 
        parser = argparse.ArgumentParser() 
    
        # Adding optional argument 
        parser.add_argument('-d',"--devices",required=False,nargs='+',help = "Enter the file names ",action="count",default=False) 
        parser.add_argument("-p", "--Print",required=False,action="store_true",help = " type '-p' and hit 'Enter' to show available device templates." )
        
        # Read arguments from command line 
        
        args = parser.parse_args() 

        return args        

    def find_dev_template(self,*args):
        #To find the device template path in data directory.
        my_dir = ".//data"
        dev_templates = list(itertools.chain(*args)) 
        for root_dir_path, sub_dirs, files in os.walk(my_dir):
            
                if files:
                    tag = os.path.relpath(root_dir_path, my_dir)
                    for device in dev_templates:
                        for file in files:                    
                            tag_parent = os.path.dirname(tag)
                            sub_folder = os.path.basename(tag)
                            if fnmatch.fnmatch(file,device):
                                  print(os.path.normpath(os.path.join(my_dir,tag_parent,sub_folder)))
        
    
    
            
    



if __name__ == "__main__":
    devices = simulate_snmp_devices()
    args = devices.parse_args()    
    if args.Print is True:
        devices.available_templates(args.Print)
    elif args.devices is not False:
        devices.find_dev_template(args.devices)
    
    
    