# Servicio Usuarios ver. 0.6.3 
## [Link a Repositorio](https://github.com/iZeelow/ArquiSW_TareaU4)

Requerimientos para correr el codigo:
- ```docker``` y ```docker compose```
- crear la siguiente red con el comando: ```docker network create microsvcs```

Una vez realizado esto ejecutar ```docker compose build``` y ```docker compose up``` en cada una de las carpetas:
- "api_gateway"
- "message_broker"
- "service_users"
- "chat" (Es posible que una vez inicializado el contenedor el bot se demore un poco en iniciar, recargar la página en ese caso.)

Finalmente, los servicios quedarán ejecutados en los siguientes puertos:
- ```localhost:5000``` para el servicio de ```Users```
- ```localhost:5001``` para el servicio de ```api_gateway```
- ```localhost:5002``` para el servicio de ```Interfaz```

El chat actualmente cuenta con tres comandos:
- ```!comandos``` para listar los comandos disponibles
- ```!jugadores``` para ver la lista de jugadores actuales
- ```!comenzar Nombre username contraseña``` para crear tu usuario en el juego

Para testear es necesario tener los contenedores corriendo excepto de interfaz.
tambien es necesario tener instalado ```pytest``` y ```requests```y proceder a escribir ```pytest```
Se realizó un un testeo para crear un usuario y otro para updatear sus datos, de por medio
también se testeo borrar un usuario para no dejar la base de datos con información extra.//
link a video probando la interfaz: https://drive.google.com/file/d/1wea-sk16EhVU4la07PrfBIHiRis2jG40/view?usp=drive_link//
link a video de la interfaz en el cluster: https://drive.google.com/file/d/1ikkOBhaWrio4MM6_W7J844RQ-gceSRqz/view?usp=sharing
