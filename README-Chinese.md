# binance-tradingview-webhook-bot

[English Docs](README.md) 

币安Tradingview Webhook交易机器人,
通过简单的配置可以实现tradingview发送的信号进行交易。目前支持在币安现货和合约的交易信号。但是现货的需要你处理交易的下单逻辑。可以参考合约的下单方式。

如果你想在tradingview
webhoook里面使用算法交易来降低成本或者滑点，可以考虑使用[howtrader](https://github.com/51bitquant/howtrader),
里面内置了一些算法交易，同时更容易扩展你的交易信号。

# 如何使用

## 1. 购买服务器、域名和安装nginx软件
如果你还没有服务器，可以购买一个服务器和域名，并把你的域名解析到当前服务器ip地址.

**服务器推荐**：[https://www.ucloud.cn/site/active/kuaijie.html?invitation_code=C1x2EA81CD79B8C#dongjing](https://www.ucloud.cn/site/active/kuaijie.html?invitation_code=C1x2EA81CD79B8C#dongjing)

完成上一步之后，你还需要安装nginx软件。window用户可以从这个网站下载[https://nginx.org/en/download.html](https://nginx.org/en/download.html)，对于macOS系统,
你可以在终端输入一下命令安装:

> brew install nginx

其他有用的命令如下:

> brew services start nginx 

> brew services restart nginx

> brew services reload nginx

如果提示你没有brew, 那么你需要安装下homebrew, 具体百度或者谷歌一下。

对于window系统，你可以从以下链接下载nginx:
https://nginx.org/en/download.html, 然后解压到指定目录. 然后启动它:

> start nginx.exe

其他有用的命令如下:

> nginx.exe -s stop

> nginx.exe -s quit

> nginx.exe -s stop

> nginx.exe -s reload (reload)


另外你还需要编辑下nginx.cong文件,该文件只要是配置你的nginx进行端口转发。由于tradingview只能用80端口，所以你需要为你的web服务器进行端口转发。
在http里面添加如下配置信息：

```
server {
        listen 80;
        server_name your.dormain.com;
        charset utf-8;

        location / {
          proxy_pass http://localhost:8888;
        }

    }

```

server_name 可以填写字符串或者你的ip地址都可以的， 比如： server_name
xxx.xxx.xxx.xxx;

修改nginx.conf后需要重启nginx 或者重新加载，你的配置才会生效， 最后运行main.py。

## 创建webhook信号提醒

 创建webhook提醒的时候，勾选Webhook Url 选项,
 然后把你webhook的链接粘贴进去，例如: http://www.your.domain/webhook,
 消息体格式如下

```
{"action": "{{strategy.order.comment}}",
  "symbol": "ETHUSDT",
"exchange": "binance_future",
"price":"{{strategy.order.price}}",
"close": "{{close}}",
"passphrase": "your customized password for safety.",
"strategy_name": "ETHUSDT_5min",
"some other key": "some other value you need"
}

```
需要注意的是，你的strategy_name的值，要跟你在config.py文件中的strategies里面的key要对应起来。
不然它找不到你对应的策略的配置参数。另外在你的策略中，你订单的comment要填写成如下格式:

```

strategy.entry('L', strategy.long, comment="long")
strategy.entry('S', strategy.short, comment="short")
strategy.exit('tp', comment="exit")


```

程序中，采用市价单的方式下单，主要是为了保证及时成交。如果你是跑BTCUSDT,
ETHUSDT等流动性好的品种，那么其滑点是比较小的。如果你想用挂单的方式，可以找到代码的下单方式，修改代码中的orderType和价格即可。

你可以在同一个交易对下面，交易不同的策略，这就通过strategy_name来实现的。strategy_name是策略的名称，他们的持仓是根据策略的名称来识别的。
策略A的持仓和策略B不会关联，他们管理好他们的持仓即可。

最后祝老板发财。

# 联系方式

微信: bitquant51 

discord: 51bitquant#8078

如果使用中遇到任何问题，可以咨询我。