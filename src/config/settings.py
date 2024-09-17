# settings.py

import os
from dotenv import load_dotenv

# Obtener la ruta absoluta al directorio de settings.py
settings_dir = os.path.dirname(os.path.abspath(__file__))

# Obtener la ruta al directorio raíz del proyecto (padre de src/config/)
project_root = os.path.abspath(os.path.join(settings_dir, os.pardir, os.pardir))

# Construir la ruta al archivo .env en el directorio raíz
dotenv_path = os.path.join(project_root, '.env')

# Cargar las variables de entorno desde el archivo .env en el directorio raíz
load_dotenv(dotenv_path)

# Ahora puedes acceder a las variables de entorno
# OpenAI
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Google API
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
GOOGLE_REFRESH_TOKEN = os.getenv('GOOGLE_REFRESH_TOKEN')

# Microsoft API
MICROSOFT_CLIENT_ID = os.getenv('MICROSOFT_CLIENT_ID')
MICROSOFT_CLIENT_SECRET = os.getenv('MICROSOFT_CLIENT_SECRET')
MICROSOFT_TENANT_ID = os.getenv('MICROSOFT_TENANT_ID')
MICROSOFT_REFRESH_TOKEN = os.getenv('MICROSOFT_REFRESH_TOKEN')

# Twilio WhatsApp API
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_WHATSAPP_NUMBER = os.getenv('TWILIO_WHATSAPP_NUMBER')
