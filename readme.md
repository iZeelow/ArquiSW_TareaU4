# Servicio Usuarios ver. 0.3.0

Requerimientos para correr el codigo:
- ```docker``` y ```docker compose```
- crear la siguiente red con el comando: ```docker network create tarea_u4```

Una vez realizado esto ejecutar docker compose up en cada una de las carpetas:
- "api_gateway"
- "message_broker"
- "service_users"

Finalmente, los servicios quedarán ejecutados en los siguientes puertos:
- ```localhost:5000``` para el servicio de ```Users```
- ```localhost:5001``` para el servicio de ```api-gateway```