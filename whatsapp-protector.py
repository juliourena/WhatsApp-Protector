#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Desarrollador:	Julio Ureña "PlainText"
Blog:		http://plaintext.do
Proyecto:	WhatsApp Protector
Versión:	0.1
Descripción:	Es un proyecto que tiene la intención de ayudar a los usuarios 
		a identificar cuando un enlace enviado por WhatsApp es sospechoso.
		Permitiendo evitar que estos sean víctimas de [Ingeniería Social].
				
		De igual forma, mostrar cómo se puede utilizar WhatsAPIDriver, para
		aquellos desarrolladores que quieran probar otras cosas utilizando 
		esta herramienta como base o guía.
"""

import time, re, requests, click, traceback

from webwhatsapi import WhatsAPIDriver
from webwhatsapi.objects.message import Message

# Regex para obtener la URL del texto
# Fuente: https://github.com/rcompton/ryancompton.net/blob/master/assets/praw_drugs/urlmarker.py
regex = r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))"""

# Nombre de Categorias para crear la advertencia, para otras categorias visitar fortiguard.com 
warning = ['Unrated', 'Not Rated','Phishing', 'Malicious Websites','Child Abuse','Discrimination','Drug Abuse','Explicit Violence','Extremist Groups','Hacking', 'Illegal or Unethical', 'Plagiarism','Proxy Avoidance','Nudity and Risque','Pornography', 'Newly Observed Domain', 'Newly Registered Domain']

def Conexion(directorio):
	global driver
	print("[+] Conectando...")
	try:
		driver = WhatsAPIDriver(client='firefox',loadstyles=True,profile=directorio)
		print("[+] Esperando validación de QR")
		driver.wait_for_login()
		print("[+] Robot Conectado!")
		return True
	except:
		print("[-] No se pudo conectar, intente otra vez.")
		return False

def Protector(chat_id, timeout=0):
	try:
		#driver.send_message_to_id(chat_id, '[+] Protección de Chat Iniciada. \n'+ time.ctime())
		while True:
			if timeout > 0 and (time.time() > timeout):
				break
			# Buscará cada 3 segundos por mensajes nuevos.
			time.sleep(3)
			#print('[*] Checking for more messages, status', driver.get_status())
			for contact in driver.get_unread():
				for message in contact.messages:
					# Validar para que personas o grupos quieres aplicar la regla.
					if chat_id in message.chat_id:
						# Imprimir en la consola (Aquí podrías incluso guardar esta información en una base de datos.
						print('')
						print('[+] Recibido: ', time.ctime())
						print('[+] Chat: ', contact.chat.name)
						print('[+] Enviado por: ', message.sender.name)
						if message.type == 'chat':
							print('[+] Mensaje: ', message.content)

							# Buscar dentro del mensaje de texto las URLs
							urls = re.findall(regex,message.content)
							if len(urls) >= 1:
								for url in urls:
									print("[+] Consultando la categoría de la URL en FortiGuard")
									# Consultar FortiGuard para saber la categoria a la que pertenece la pagina.
									r = requests.get('https://fortiguard.com/webfilter?q=' + url)
									
									# Extraer la categoría de Fortguard
									category = re.findall("Category: (.*) />",r.text)[0].replace("\"","")
									print("[+] La Categoría es: " + category + "\n\r")
									
									# Definir el mensaje a responder segun la categoría.
									if category in warning:
										driver.send_message_to_id(message.chat_id, 'El enlace ('+ url +') está categorizado como: *' + category +'*. \n\nNo es recomendable visitar este enlace. ')
									#else:
										#driver.send_message_to_id(message.chat_id, 'El enlace ('+ url +') está categorizado como: *' + category +'*. \n\nNo se evidencia peligro en la categoría. ')							
						else:
							print('[-] No link in Message type: ', message.type)
						
						
									
		#driver.send_message_to_id(chat_id, '[-] Protección de Chat Finalizada. \n'+ time.ctime())
	except Exception as e:
		print("[-] Type error: " + str(e))
		print(traceback.format_exc())
		driver.send_message_to_id(chat_id, '[-] Protección de Chat Finalizada. \n'+ time.ctime())
		
def Busqueda(nombre):
	global driver
	try:
		encontrados = []
		chats_ids = driver.get_all_chat_ids()
		time.sleep(3)
		for chat_id in chats_ids:
			contact_name = driver.get_contact_from_id(chat_id)
			if nombre.lower() in contact_name.formatted_name.lower():
				print("[+] El Chat_Id de "+ contact_name.formatted_name + " Es: " + chat_id)
				encontrados.append(chat_id)			

		if len(encontrados) == 0:
			print("[-] No se pudo encontrar ningun contacto que contenga: " + nombre)
	except Exception as e:
		print("[-] Type error: " + str(e))
		print(traceback.format_exc())
		
# En caso que no se especifiquen los parametros, mostrar el help.
def print_help(self, param, value):
	if value is False:
		return
	click.echo(self.get_help())
	self.exit()

@click.command()
@click.option('-c', '--chat-id', 'chat_id', help='Chat_Id para Revisar Mensajes Nuevos', required=False)
@click.option('-b', '--buscar', 'buscar_nombre', help='Buscar el chat_id basado en el nombre', required=False)
@click.option('-d', '--directorio', 'directorio',default='/tmp', help='Directorio para grabar la sesion', required=False)
@click.option('-t', '--tiempo', 'tiempo', type=int, default=0,help='Segundos que durará la ejecución. Si no se establece el programa correrá indefinidamente.', required=False)
@click.option('-h', '--help', 'help', help='Ayuda', is_flag=True, callback=print_help, expose_value=False, is_eager=False)
@click.pass_context

# Inicio del programa 
def main(self, chat_id, buscar_nombre, directorio, tiempo):
	if not chat_id and not buscar_nombre:
		print_help(self, None,  value=True)
		print("[-] Para la guia de uso, utilice la opcion --help")
		exit(0)
		
	if (chat_id) and (buscar_nombre):
		print("\n[-] No es posible utilizar ambas opciones (-c / -b) al mismo tiempo. Para más información consulte la ayuda.\n")
		print_help(self, None,  value=True)
		exit(0)
		
	if Conexion(directorio):
		if (chat_id):			
			timeout = time.time() + tiempo
			print("[+] Iniciando Protección [" + time.ctime() + "]")
			if tiempo > 0:
				Protector(chat_id, timeout)
			else:
				Protector(chat_id)
		else:
			print("[+] Iniciando Busqueda [" + time.ctime() + "]")
			Busqueda(buscar_nombre)
	else:
		exit(0)

if __name__ == '__main__':
	main()
