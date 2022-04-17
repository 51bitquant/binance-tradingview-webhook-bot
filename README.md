# binance-tradingview-webhook-bot

[中文文档](README-Chinese.md)

A tradingview webhook trading bot for Binance Exchange. you can just
simply set up your own signal alert from tradingview, and the bot will
help you place order to Binance Spot or Binance Future.


# how-to use
Follow the following step you can create your own Binance tradingview
webhook bot.

## 1. buy an server、 domain and install nginx software.
If you don't have a server, you need to buy a server and a domain. Then
resolve your domain to your server ip.

After setup your own server, you also need to install the nginx
software. For MacOs system, you can just type this command into your
terminal:

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
            server_name your.dormain.com;
            charset utf-8;
    
            location / {
              proxy_pass http://localhost:8888;
            }
    
        }
        
        
     }
     
     # other configurations.

```


Then run the main.py, like python main.py. You may need to create a
python virtual environment.

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
"passphrase": "your custom password for safety."
"some other key": "some other value you need"
}

```


Remember, you also need to set the commemt at the your order, like:

```

strategy.entry('L', strategy.long, comment="long")
strategy.entry('S', strategy.short, comment="short")
strategy.exit('tp', comment="exit")


```

Ok, happy using the Binance Tradingview Webhook bot.


# Contact

twitter: @51bitquant.eth
discord:51bitquant#8078

If you have any question, please feel free to contact me.