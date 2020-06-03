import argparse,os,fnmatch
my_dir= ".//data"
device=['xp.snmprec','ubuntu.snmprec']
for root_dir_path, sub_dirs, files in os.walk(my_dir):

        if files:
            tag = os.path.relpath(root_dir_path, my_dir)
            for dev in device:
                for file in files:
                    tag_parent = os.path.dirname(tag)
                    sub_folder = os.path.basename(tag)
                    if fnmatch.fnmatch(file,dev):
                        print(os.path.normpath(os.path.join(my_dir,tag_parent,sub_folder)))
                #print(sub_folder if sub_folder else "","--->",(file))
                #print (tag_parent)
                #print( "File:",file,"belongs in",tag_parent, sub_folder if sub_folder else "")
                    
