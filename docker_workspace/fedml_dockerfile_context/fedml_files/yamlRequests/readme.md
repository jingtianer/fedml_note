# Yaml-Requests简介

- 对request库的封装，用于处理与chainCode http 接口的交互
- 方便对http api的使用
- 提供异步、同步两种方式
- 通过配置文件获取http请求的url，port等信息。调用者只需关注业务，请求的参数部分已经在配置文件中写好，调用者不必关注过多细节
    - async : true/false
    - content-type : json/file/none/...
    - url
    - port
    - path
- 处理文件读写
- 动态生成函数
- 并发任务

# 使用方法
## config的编写
编写yaml文件，包括：
- url: http服务的BaseUrl
- port: 服务端口
- methods: 定义方法

## yaml中method的定义
- 样例如下
```yaml
method_name:
    type: 'post'
    async: true
    res-type: 'json'
    path: '/invokeChaincode/json'
    save: './path/to/file'
    params:
        param1: 'val1'
        param2: 'val2'
        param3: 'val3'
    body:
        content-type: 'json/binary/text'
        content:
            xxx: 'xxx'
            xxx: 'xxx'
            xxx: 'xxx'
```

- type: 表示接口方法类型，可选`post/get`
- async: 是否异步调用，异步调用需要提供回调函数
- res-type: 返回值类型，可选`text/json/binary`
- path: 请求的path
- save: （可选）保存请求返回体的文件
- params: （可选）请求参数，（实际调用时的params优先，yaml中的params可以看作请求参数的缺省值）
- body: （可选）请求的body

## body的定义
- 定义1
```yaml
    body:
        content-type: 'json'
        content:
            xxx: 'xxx'
            xxx: 'xxx'
            xxx: 'xxx'
```
- 定义2
```yaml
    body:
        content-type: 'text'
        content: 'hello world'
```
- 定义3
```yaml
    body:
        content-type: 'binary'
        files:
            file1: 'path/to/file1/file1'
            file2: 'path/to/file2/file2'
            file3: 'path/to/file3/file3'
```
## 调用
- 以调用`sample_config.yaml`中的函数为例
```python
from configLoader import init
def callBack(ret, x):
    print("callBack %s : %s" % (x, ret))
methods = init("./sample_config.yaml")
print("invoke: %s" % methods.get(None, {"key":"a"}))
print("invoke: %s" % methods.set(None, {"key":"a", "val":"cc"}))
print("invoke: %s" % methods.get(None, {"key":"a"}))
print("invoke: %s" % methods.get_async(None, {"key":"a"}, lambda ret: callBack(ret, 'get_async1')))
print("invoke: %s" % methods.set_async(None, {"key":"a", "val":"bb"}, lambda ret: callBack(ret, 'get_async2')))
print("invoke: %s" % methods.get_async(None, {"key":"a"}, lambda ret: callBack(ret, 'get_async3')))

print("invoke: %s" % methods.get_file({'key':'a'}, None))
print("invoke: %s" % methods.set_file({'key':'a'}, {"sample_config.yaml":"./sample_config.yaml"}))
print("invoke: %s" % methods.get_file({'key':'a'}, None))
```

# 应用场景
1. 配合docker容器，不同容器使用同一套代码，根据不同的配置文件，进行不同参数的http请求
2. 作为requests库的封装，便于网络请求
3. 可以减少对fedml库代码的修改，减少bug的产生