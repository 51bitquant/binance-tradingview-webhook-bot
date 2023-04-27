# binance-tradingview-webhook-bot

[中文文档](README-Chinese.md)

A tradingview webhook trading bot for Binance Exchange. you can just
simply set up your own signal alert from tradingview, and the bot will
help you place order to Binance Spot or Binance Future.

if you want to use algo trader in your strategy, we recommend you to use
[howtrader](https://github.com/51bitquant/howtrader), it implements a
few algo trader in tv strategy.


# how-to use
Follow the following step you can create your own Binance tradingview
webhook bot.

## 1. buy a server、 domain and install the nginx software.
If you don't have a server, you need to buy a server and a domain. Then
resolve your domain to your server ip.

**window server
recommendation**：[https://www.ucloud.cn/site/active/kuaijie.html?invitation_code=C1x2EA81CD79B8C#dongjing](https://www.ucloud.cn/site/active/kuaijie.html?invitation_code=C1x2EA81CD79B8C#dongjing)


After setup your own server, you also need to install the nginx
software. For window, you can download from
[https://nginx.org/en/download.html](https://nginx.org/en/download.html) , For MacOs system, you can just
type this command into your terminal:

> brew install nginx

Other useful command are:


> brew services start nginx 

> brew services restart nginx

> brew services reload nginx

if you don't have the brew installed, just google how to install the
homebrew.

For window server, you just download the nginx software from:
https://nginx.org/en/download.html, then unzip and cd to the current
directory. Here are the useful command.

> start nginx.exe

> nginx.exe -s stop

> nginx.exe -s quit

> nginx.exe -s stop

> nginx.exe -s reload (reload)


Then edit the nginx.conf file, and add a server for the Flask Server,
then save the nginx.conf

```

http {

    server {
            listen 80;
            server_name your.domain.com;
            charset utf-8;
    
            location / {
              proxy_pass http://localhost:8888;
            }
    
        }
        
        
     }
     
     # other configurations.

```


After editing the eginx.conf, you need to restart nginx.conf or reload
the eginx. Finally,  run the main.py, like python main.py. You may need
to create a python virtual environment.

## create an alert from tradingview.
 
You may need to register an account from https://www.tradingview.com and
develop your own strategy and create an alert.

## config your webhook details.
 
when creating an alert, select the box Webhook Url, and past your
webhook url like: http://www.your.domain/webhook, for the message body,
you can config like this:

```
{"action": "{{strategy.order.comment}}",
  "symbol": "ETHUSDT",
"exchange": "binance_future",
"price":"{{strategy.order.price}}",
"close": "{{close}}",
"passphrase": "your custom password for safety.",
"strategy_name": "ETHUSDT_15min",
"some other key": "some other value you need"
}

```
In this tradingbot, in order to make the order filled immediately, we
use the market order type. If you trade BTCUSDT, ETHUSDT pairs, the
slippage is very small. If you want to use the limit order type, please
checkout the code and just change the order type to limit and change the
order's price. Last but not least, you also need to set the commemt at
the your order, like:

```

strategy.entry('L', strategy.long, comment="long")
strategy.entry('S', strategy.short, comment="short")
strategy.exit('tp', comment="exit")


```

## how to run the code
1. download the codes and unzip it
2. create a python interpreter, we recommend using anaconda and create a
   python 3.9 version interpreter, execute the following command.
   > create -n mytrader python==3.9
   
   then activate your python interpreter.
   
   > conda activate mytrader
 
  
3. cd to your code and install the requirements
    
   >  pip install -r requirements.txt
   
   the requirements.txt is in the code directories. or you can install
   the dependencies one by one:
   
   > pip install requests
   
   > pip install flask
   
4. config your strategy
   
   edit the config.py file, config your apikey, passphrase and
   strategies parameters.
   
5. run the codes.

    if you run on your local computer, you can just run the main.py in
    pycharm editor(remember to config your project interpreter before
    running it). or you can execute it in your terminal: 
    
   > python main.py
   
    if you run on your server, you can use the start.sh script. or input
    the following command in your terminal:
    
    > nohup python -u main.py > log.txt 2>&1 &
   

moreover, if you want to place the order in limit or maker order, just
change place_order function's parameter:

maker order
``` python 
status, order = binance_future_client.place_order(
                symbol=symbol,
                order_side=OrderSide.BUY,
                order_type=OrderType.MAKER,
                quantity=Decimal(vol1),
                price=Decimal(price),
                client_order_id=order_id
            )

```

limit order
``` python 
status, order = binance_future_client.place_order(
                symbol=symbol,
                order_side=OrderSide.BUY,
                order_type=OrderType.LIMIT,
                quantity=Decimal(vol1),
                price=Decimal(price),
                client_order_id=order_id
            )

```


Ok, happy using the Binance Tradingview Webhook bot and have a good
luck.


# Contact

discord:51bitquant#8078

If you have any question, please feel free to contact me.