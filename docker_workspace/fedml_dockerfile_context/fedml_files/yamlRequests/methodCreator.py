from .baseFunc import *
from .contentType import ContentType, getContentType
import json
from .asyncExecutor import exeTask, exeTaskAsync
import logging
creator = locals()

var_list = ['path', 'type', 'res-type', 'async']
def checkMethod(method_para):
    for key in var_list:
        if key not in method_para:
            return False
    return True

class Methods():
    def __init__(self, methods):
        for method_name, method_para in methods.items():
            logging.info("generating method: %s" % method_name)
            if checkMethod(method_para):
                setattr(self,method_name, genMethod(method_para))
            else:
                logging.error("params check: %s not match the params check" % method_name)
        logging.info("method generation completed!")

def genMethod(method_para):
    path = method_para['path']
    resType = method_para['res-type']
    yaml_params = method_para['params'] if 'params' in method_para else {}
    save = method_para['save'] if 'save' in method_para else None
    contentType = getContentType(resType)
    if method_para['async']:
        return genAsyncMethod(method_para, path, yaml_params, save, contentType)
    else :
        return genSyncMethod(method_para, path, yaml_params, save, contentType)


def genConfigParas(data):
    for key, val in data.items():
        creator[key] = val


def genAsyncMethod(method_para, path, yaml_params, save, contentType):
    if method_para['type'] == "post":
        return lambda  req_params, body, callBack: exeTaskAsync(lambda :gen(method_para, req_params, body, path, yaml_params, contentType, save), callBack)
    elif method_para['type'] == "get":
        return lambda req_params, body, callBack: exeTaskAsync(lambda :gen(method_para, req_params, body, path, yaml_params, contentType, save), callBack)
    else :
        raise Exception("No Such type" + method_para['type'])


def genSyncMethod(method_para, path, yaml_params, save, contentType):
    if method_para['type'] == "post":
        return lambda req_params, body: exeTask(lambda :gen(method_para, req_params, body, path, yaml_params, contentType, save))
    elif method_para['type'] == "get":
        return lambda req_params, body: exeTask(lambda :gen(method_para, req_params, body, path, yaml_params, contentType, save))
    else :
        raise Exception("No Such type" + method_para['type'])

async def gen(method_para, req_params, body, path, yaml_params, contentType, save):
    if req_params is not None:
        yaml_params.update(req_params)
    req_params = yaml_params
    if 'body' in method_para:
        body_config = method_para['body']
        body,files = handle_body_config(body_config, body)
    if method_para['type'] == "post":
        res = basePost(url, port, path, body, files,req_params, contentType)
    elif method_para['type'] == "get":
        res = baseGet(url, port, path, body, files, req_params, contentType)
    else :
        raise Exception("No Such type" + method_para['type'])
    saveFile(save, res)
    return res

def handle_body_config(body_config, body):
    contentType = getContentType(body_config['content-type'])
    if contentType == ContentType.Text:
        if body is None:
            body = ''
        if 'content' in body_config:
            body = body_config['content']
        return body, None
    elif contentType == ContentType.Json:
        if body is None:
            body = {}
        if not isinstance(body, dict):
            raise Exception("josn body has to be a dict")
        if 'content' in body_config:
            yaml_body = body_config['content']
            body.update(yaml_body)
        body = json.dumps(body)
        return body, None
    elif contentType == ContentType.Binary:
        if body is None:
            body = {}
        files = None
        if 'files' in body_config:
            files = readFiles(body_config['files'])
            files.update(readFiles(body))
        return None, files
    else:
        raise Exception("content-type %s not supported!" % contentType)
    return None, None
def saveFile(save, res):
    if save is not None:
        with open(save, 'wb') as f:
            f.write(res)
    
def readFiles(files):
    return {file_name:open(file, "rb") for file_name,file in files.items()}

