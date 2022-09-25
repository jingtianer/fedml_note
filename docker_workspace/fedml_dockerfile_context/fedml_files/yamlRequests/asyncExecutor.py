import asyncio
import threading

def exeTaskAsync(task, callBack):
    threading.Thread(target = lambda :exeTask(task, callBack)).start()

def exeTask(task, callBack = None):
    ret = asyncio.run(task())
    if callBack is not None:
        callBack(ret)
    return ret
