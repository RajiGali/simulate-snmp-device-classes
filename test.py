import argparse 

# Initialize parser 
parser = argparse.ArgumentParser() 
  
# Adding optional argument 
parser.add_argument("-d", "--Output", nargs='+' , help = "Enter the template/templates") 
  
# Read arguments from command line 
args = parser.parse_args() 
  
if args.Output: 
    print("Diplaying Output as: % s" % args.Output) 
