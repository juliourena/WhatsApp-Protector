# WhatsApp-Protector

For more information check the post: http://plaintext.do/Whatsapp-Protector/

# What is WhatsApp Protector?

It is a project that is intended to help users identify when a link sent over WhatsApp is suspicious. Allowing them to avoid being victims of [Social Engineering](https://en.wikipedia.org/wiki/Social_engineering_(security))

# What does WhatsApp-Protector do?

It checks new WhatsApp messages via https://web.whatsapp.com and searchs for URL's, then it check the URL's category at https://www.fortiguard.com/webfiler and response to the chat (user or group) to which category the URL belongs to, including a warning in case of that the URL is part of a suspicious category.

**Note** Thanks to [Fortinet](www.fortinet.com) for maintaining this public service, however, it is important to note that, although I use the Fortinet website, this development is not linked to the company in any way, if they change the web query, the program would have to be modified.

# How does it work?

It is designed to be used in python3, because WhatsApp does not have an official API, this program works by using the library (https://github.com/mukulhase/WebWhatsapp-Wrapper) a project of [Mukul Hase](https : //github.com/mukulhase), which allows us to use WhatsApp Web.

# Installation

It is necessary to install webwhatsapi the installation details can be found in [here](https://github.com/mukulhase/WebWhatsapp-Wrapper) in a simple way it would be:

```
sudo apt install python3
sudo apt install python3-pip
pip3 install webwhatsapi
pip3 install click

# Installation of geckodriver
wget https://github.com/mozilla/geckodriver/releases/download/v0.20.1/geckodriver-v0.20.1-linux64.tar.gz
tar -xvzf geckodriver-v0.20.1-linux64.tar.gz
chmod + x geckodriver
sudo mv ./geckodriver /usr/local/bin/.
```
 
# Use

```
Usage: whatsapp-protector.py [OPTIONS]

Options:
  -c, --chat-id TEXT Chat_Id to Review New Messages
  -b, --buscar for TEXT Search for the chat_id based on the name
  -d, --directory TEXT Directory to record the session
  -t, - time INTEGER Seconds that the execution will last. If it is not established
                         the program will run indefinitely.
  -h, --help Help

```

**Chat_Id** - We need the Chat_Id to be able to choose the conversation that we want to monitor, I only configured one, but they can modify the code to add more. You can also use `-c '@g.'` for all group chats (as far as I know, all group Id's ends with `@g.` and something like the country which in my case usually are .us
 
**Buscar (Search)** - If you do not know the Chat_Id, you can use the -b or --buscar options to indicate the name of the conversation (it can be a person or group).

**Time** - Allows us to define how many seconds the monitor will be on.
 
**Directory** - It is used to record the session, so you do not have to be scanning the QR always. The only drawback is that every time you start it, it will open a new browser. Some steps are necessary before using the option. Based on the [codemanat] guide (https://github.com/codemanat/WebWhatsAPI/blob/master/README.md)

## Permanent session configuration:

Open the python3 console and put the following:
 
```
import time
from webwhatsapi import WhatsAPIDriver
from webwhatsapi.objects.message import Message
driver = WhatsAPIDriver (client='Firefox', loadstyles=True)
```

Scan the QR code and close the console using CTRL + C
 
Create a Firefox profile, in the console (bash) put the following:
 
`firefox -p`
 
* Create Profile
* Select a name
* Choose the directory (Create a directory where Firefox logs will be saved)
* Enter https://web.whatsapp.com and scan the QR code
* Enter again to https://web.whatsapp.com and validate if the session persists.
* Finalize.

# Search for Chat_id

To find the chat_id we use:

`python3 whatsapp-protector.py -d /home/plaintext/dev/plaintext-profile --search vitilla`

![whatsapp-protector-search](https://raw.githubusercontent.com/juliourena/juliourena.github.io/master/assets/images/ws-busqueda.png)

And we already have the chat_id of two conversations that have the name **vitilla**

# Chat Protection

To execute the protection would only be, remember that the -t is optional 😊

`python3 whatsapp-protector.py -d /home/plaintext/dev/plaintext-profile -c 18000070508-1500082004@g.us -t 120`

![whatsapp-protector-search](https://raw.githubusercontent.com/juliourena/juliourena.github.io/master/assets/images/ws-protector.png)

And so it would look on the Whatsapp 😊

![whatsapp-protector-action](https://raw.githubusercontent.com/juliourena/juliourena.github.io/master/assets/images/whatsapp-action.png)

## Other mentions:
- Thank the children of the Central Church of God, for creating the scenario of the idea.
- [rcompton] (https://github.com/rcompton), I used your [Regex for URLs] (https://github.com/rcompton/ryancompton.net/blob/master/assets/praw_drugs/urlmarker.py)
- [cmaddy](https://github.com/chrismaddalena) your projects and code gave me some ideas.

I hope you find it useful, any questions or suggestions do not hesitate to write.

Serving Christ is not a task, but a relationship. Friends of God Jn 15:15

God bless you!