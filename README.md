# WhatsApp-Protector

Para más información verificar el post: http://plaintext.do/Whatsapp-Protector/
[for English README](/README-English)

# ¿Qué es WhatsApp Protector?

Es un proyecto que tiene la intención de ayudar a los usuarios a identificar cuando un enlace enviado por WhatsApp es sospechoso. Permitiendo evitar que estos sean víctimas de [Ingeniería Social](https://es.wikipedia.org/wiki/Ingenier%C3%ADa_social_(seguridad_inform%C3%A1tica)).

# ¿Qué hace WhatsApp-Protector?

Verifica los mensajes nuevos de WhatsApp vía https://web.whatsapp.com en búsqueda de URL's, consulta la URL en https://www.fortiguard.com/webfiler y muestra a que categoría pertenece la URL con una advertencia en caso de que la URL sea parte de una categoría sospechosa. 

**Nota** Agradecimientos a [Fortinet](www.fortinet.com) por mantener este servicio público, sin embargo, es importante señalar que, aunque utilizo la web de Fortinet, este desarrollo no está ligado a la compañía en ninguna forma, si ellos cambian la consulta web, el programa tendría que ser modificado.

# ¿Cómo funciona? 

Está diseñado para utilizarse en python3, debido a que WhatsApp no cuenta con un API oficial, este programa funciona haciendo uso de la librería (https://github.com/mukulhase/WebWhatsapp-Wrapper) un proyecto de [Mukul Hase](https://github.com/mukulhase), esta nos permite hacer uso de WhatsApp Web.

# Instalación

Es necesario instalar webwhatsapi los detalles de instalación pueden verlo [aquí](https://github.com/mukulhase/WebWhatsapp-Wrapper) de forma sencilla sería:

``` 
sudo apt install python3
sudo apt install python3-pip
pip3 install webwhatsapi
pip3 install click

# Instalación de geckodriver
wget https://github.com/mozilla/geckodriver/releases/download/v0.20.1/geckodriver-v0.20.1-linux64.tar.gz
tar -xvzf geckodriver-v0.20.1-linux64.tar.gz
chmod +x geckodriver
sudo mv ./geckodriver /usr/local/bin/.
 ```
 
# Uso

```
Usage: whatsapp-protector.py [OPTIONS]

Options:
  -c, --chat-id TEXT     Chat_Id para Revisar Mensajes Nuevos
  -b, --buscar TEXT      Buscar el chat_id basado en el nombre
  -d, --directorio TEXT  Directorio para grabar la sesion
  -t, --tiempo TEXT      Segundos que durará la ejecución. Si no se establece
                         el programa correrá indefinidamente.
  -h, --help             Ayuda

```

**Chat_Id** - Necesitamos el Chat_Id para poder elegir la conversación que queremos monitorear por enlaces, solo configuré uno, pero pueden modificar el código para agregar más.
 
**Buscar** - Si no saben el Chat_Id, pueden utilizar la opción -b o --buscar para indicar el nombre de la conversación (puede ser una persona o grupo).

**Tiempo** - Nos permite definir cuantos segundos durará la ejecución del programa. 
 
**Directorio** - Se utiliza para grabar la sesión, de tal forma que no tengan que estar escaneando el QR siempre. El único inconveniente es que cada vez que inicia, abre un nuevo navegador. Antes de utilizar la opción son necesarios algunos pasos. Basados en la guía de [codemanat](https://github.com/codemanat/WebWhatsAPI/blob/master/README.md)

## Configuración de sesión permanente: 

Abrir la consola de python3 y poner lo siguiente:
 
```
import time
from webwhatsapi import WhatsAPIDriver
from webwhatsapi.objects.message import Message
driver = WhatsAPIDriver(client='Firefox',loadstyles=True)
```

Escanear el código QR y cerrar la consola utilizando CTRL + C.
 
Crear un perfil de Firefox, en la consola (bash) poner lo siguiente:
 
`firefox -p`
 
* Crear Perfil
* Seleccionar un nombre
* Elegir el directorio (Crear un directorio donde se vayan a guardar los registros de Firefox)
* Entrar a https://web.whatsapp.com y escanear el código QR
* Entrar nuevamente a https://web.whatsapp.com y validar si la sesión persiste.
* Finalizar.

# Búsqueda de Chat_id

Para buscar el chat_id utilizamos:

`python3 whatsapp-protector.py -d /home/plaintext/dev/plaintext-profile -b vitilla`

![whatsapp-protector-busqueda](https://raw.githubusercontent.com/juliourena/juliourena.github.io/master/assets/images/ws-busqueda.png)

Y ya tenemos el chat_id de dos conversaciones que tienen el nombre **vitilla**

# Protección de Chat

Para ejecutar la protección solo sería, recuerden que la -t es opcional 😊

`python3 whatsapp-protector.py -d /home/plaintext/dev/plaintext-profile -c 18000070508-1500082004@g.us -t 120`

![whatsapp-protector-busqueda](https://raw.githubusercontent.com/juliourena/juliourena.github.io/master/assets/images/ws-protector.png)

Y así se vería en el Whatsapp 😊

![whatsapp-protector-action](https://raw.githubusercontent.com/juliourena/juliourena.github.io/master/assets/images/whatsapp-action.png)

## Otras menciones:
- Agradecer a los chicos de la Iglesia de Dios Central, por crear el escenario de la idea.
- [rcompton](https://github.com/rcompton), utilicé su [Regex para URLs](https://github.com/rcompton/ryancompton.net/blob/master/assets/praw_drugs/urlmarker.py)
- [cmaddy](https://github.com/chrismaddalena) sus proyectos y codigo me dieron algunas ideas.

Espero que les sea útil, cualquier duda o sugerencia no duden en escribir.

**El servir a Cristo, no es una tarea, sino una relación. Amigos de Dios. Jn 15:15**
 
Dios les bendiga!