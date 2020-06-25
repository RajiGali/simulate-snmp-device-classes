"""utilities"""
import os,configparser

class Utils():
    """utilities"""
    
    def read_conf(self,conf_file):
        try:
            config = configparser.ConfigParser()
            conf_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),'.','conf'))
            config.read(os.path.join(conf_dir,conf_file))
        except FileNotFoundError:
            raise("Error in reading conf file")  
        
        return config