# Chatbot de Gestión de Vacaciones

## Descripción

Proyecto académico desarrollado para la materia Organización Empresarial.

El sistema automatiza el proceso de solicitud de vacaciones mediante un chatbot de Telegram, utilizando BPMN 2.0 para modelar el flujo de negocio.

## Tecnologías

- Python 3
- Telegram Bot API
- CSV como base de datos
- BPMN 2.0
- GitHub

## Estructura

empleados.csv
solicitudes.csv
bot.py
README.md

## Instalación
1. Clonar el repositorio:
git clone URL_DEL_REPOSITORIO
2. Ingresar a la carpeta del proyecto:
cd nombre-del-proyecto
3. Instalar dependencias:
pip install python-telegram-bot

## Configuración

Editar el archivo bot.py y reemplazar el valor de la variable TOKEN por el token generado mediante BotFather en Telegram.

Ejemplo:

TOKEN = "AQUI_SU_TOKEN"

## Funcionalidades

- Validación de empleados
- Consulta de saldo disponible
- Registro de solicitudes
- Manejo de errores
- Máquina de estados

## Ejecución

1. Instalar Python.
2. Instalar la librería python-telegram-bot.
3. Configurar el token del bot.
4. Ejecutar:

python bot.py

Si la ejecución es correcta se mostrará el mensaje:

Bot iniciado...

## USO
1. Ingresar al bot desde Telegram.
2. Ejecutar el comando:
/start
3. Ingresar el número de legajo.
4. Ingresar la cantidad de días solicitados.

El sistema validará la disponibilidad y registrará la solicitud.

## Persistencia de datos
empleados.csv
Contiene la información de los empleados:

- Legajo
- Nombre
- Días disponibles

solicitudes.csv
Contiene el historial de solicitudes registradas por el chatbot.
## Autor
Melana Colavita Maria Luciana
Trabajo Práctico Integrador
Organización Empresarial
