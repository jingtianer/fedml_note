from yaml import MarkedYAMLError, safe_load, safe_dump 

def read_yaml(yamlfile):
    return yaml_load(yamlfile)
    
def has_value(key, data):
    return key in data

def get_value(key, data):                                                                                                                                                                                     
    if key in data:                                                                                                                                                                                      
        return data[key]
    else:
        raise Exception("The key:%s does not exist in the dictionary.", key)

def set_value(key, data, val):                                                                                                                                                                                     
    if key in data:                                                                                                                                                                                   
        data[key] = val
    else:
        raise Exception("The key:%s does not exist in the dictionary.", key)

def yaml_load(yamlfile):                                                                                                                                                                                
    try:                                                                                                                                                                                                      
        with open(yamlfile,'r') as f:                                                                                                                                                                         
            data = safe_load(f)                                                                                                                                                                               
    except MarkedYAMLError as e:                                                                                                                                                                              
        raise Exception("YAML Error: %s" % str(e))                                                                                                                                                        
    return data                                                                                                                                                                                               
                                                                                                                                                                                                            
def yaml_dump(yamlfile, data):                                                                                                                                                                                
    try:                                                                                                                                                                                                      
        with open(yamlfile, 'w') as f:                                                                                                                                                                        
            safe_dump(data, f)
    except Exception as e:
        raise Exception("YAML data dump err %s" % str(e))
        