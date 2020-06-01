'''
This python script is used to print the available templates

'''

import os
import argparse
from colored import fg, bg, attr

my_dir = ".//data"

def print_templates():
    #Print the templates
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

def print_arguments():
    #This function is used to print the templates chosen by the user

    # Initialize parser 
    parser = argparse.ArgumentParser() 
  
    # Adding optional argument 
    parser.add_argument("-d", "--Output", nargs='+' , help = "Show Output") 
    parser.add_argument("-p", "--Print",required=False,help = "enter 'display' to show the available templates" )
    # Read arguments from command line 
    args = parser.parse_args() 
  
    if args.Output: 
          #print(args.Output)
          for i in args.Output:
            try: 
              os.system("snmpsimd.py --v3-engine-id=010203040505060880 --v3-user=qxf2 --data-dir=./data/os/ubuntu --agent-udpv4-endpoint=127.0.0.1:6464 &")           
            except OSError:
                raise ValueError("error in running the snmp device 'snmpsimd.py' command")
            #snmpsimd.py --v3-engine-id=010203040505060809 --v3-user=qxf2 --v3-auth-key=testqxf2 --agent-udpv4-endpoint=127.0.0.1:6464 --data-dir=/home/ubuntu/data/


    elif args.Print.upper() == 'DISPLAY':
        print_templates()


    



    



if __name__ == "__main__":
    #print_templates()
    print_arguments()
    