# 分布式客户端使用文档
使用此客户端, 您可以用自己的QQ号搭建一个Unibot

## 准备工作
::: warning 注意

部署本项目需要一定的电脑基础，会读文档

本教程不会提供`保姆级`的内容，因为`我为什么要牺牲打PJSK的时间来帮助你`

:::
### 获取一台服务器
你需要一台24h不关机的电脑，否则关机这段时间bot将无法工作

电脑需要运行 Windows 8 或 Windows server 2012 以上版本的系统（更低版本没有经过测试）


### 下载客户端和申请token
请加群467602419在群文件下载客户端，找群主申请token

## 配置客户端
你需要将客户端放在一个文件夹内，在这个文件夹下新建一个`token.yaml`，用你喜欢的编辑器打开，填上以下的设置
```yaml
token: xxxxxx
port: 2525
blacklist:
- 123456
- 234567
```
其中，`token` 填写申请的token，`port` 填写你要通信的端口号，不懂可直接填写`2525`，如果你有要关闭bot的群，则需要按照格式配置 `blacklist` 项，不需要可以删除只保留上面两行。

准备就绪后可尝试启动客户端，如果没有问题会显示如下日志
```text
[xxxx-xx-xx xx:xx:xx,xxx] Running on http://127.0.0.1:2525 (CTRL + C to quit)
```
::: tip

如果出现闪退，建议检查yaml文件是否包括了中文字符，缩进空格是否和上面一样，如果都没问题，可能是你用的编辑器换行问题，建议使用[Sublime Text](https://www.sublimetext.com/)进行编辑

:::


## 配置 GO-CQHTTP

### 下载 [GO-CQHTTP](https://github.com/Mrs4s/go-cqhttp/releases)

如果上面的链接无法打开，你也可以在群文件下载

>如果你不知道这是什么，善用搜索引擎.

### 使用反向 WebSocket
打开 cqhttp 按提示创建bat文件，打开后, 通信方式选择: 反向WS

在 CQHTTP 配置文件中，填写 `ws_reverse_url` 值为 `ws://127.0.0.1:你的端口/ws/`，这里 `你的端口` 应改为上面填的端口号。

然后，如果有的话，删掉 `ws_reverse_event_url` 和 `ws_reverse_api_url` 这两个配置项。

最后的连接服务列表应该是这样的格式
```yaml
# 连接服务列表
servers:
  # 添加方式，同一连接方式可添加多个，具体配置说明请查看文档
  #- http: # http 通信
  #- ws:   # 正向 Websocket
  #- ws-reverse: # 反向 Websocket
  #- pprof: #性能分析服务器
  # 反向WS设置
  - ws-reverse:
      # 反向WS Universal 地址
      # 注意 设置了此项地址后下面两项将会被忽略
      universal: ws://127.0.0.1:2525/ws/
      # 重连间隔 单位毫秒
      reconnect-interval: 3000
      middlewares:
        <<: *default # 引用默认中间件
```

之后，打开cqhttp，按提示登录qq后，客户端应该会出现一行这样的日志
```text
[xxxx-xx-xx xx:xx:xx,xxx] 127.0.0.1:xxxxx GET /ws/ 1.1 101 - 515
```

## 测试对话

在有机器人的群里发送命令，比如`sk`，如果一切正常，ta 应该会回复你。

如果没有回复，请检查客户端运行是否报错、cqhttp 日志是否报错。如果都没有报错，则可能是机器人账号被腾讯风控，需要在同一环境中多登录一段时间。