from __future__ import print_function
import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from dotenv import load_dotenv

load_dotenv(override=True)

# Obtener la ruta absoluta al directorio del script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Obtener la ruta al directorio raíz del proyecto (padre de scripts/)
project_root = os.path.abspath(os.path.join(script_dir, os.pardir))

# Construir la ruta al archivo .env en el directorio raíz
dotenv_path = os.path.join(project_root, '.env')

# Cargar las variables de entorno desde el archivo .env en el directorio raíz
load_dotenv(dotenv_path)

# Ahora puedes acceder a las variables de entorno
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')

# Verificar si las variables se cargaron correctamente
if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
    print("Error: No se pudieron cargar las variables de entorno necesarias.")
    exit()

# Ámbitos requeridos
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def main():
    creds = None
    # Ruta al archivo credentials.json
    credentials_path = os.path.join(script_dir, 'credentials.json')

    # Verificar si credentials.json existe
    if not os.path.exists(credentials_path):
        print(f"Error: No se encontró credentials.json en {credentials_path}")
        exit()

    # Ruta al archivo token.pickle
    token_pickle = os.path.join(script_dir, 'token.pickle')

    # El archivo token.pickle almacena los tokens de acceso y actualización
    if os.path.exists(token_pickle):
        with open(token_pickle, 'rb') as token:
            creds = pickle.load(token)
    # Si no hay credenciales válidas, inicia el flujo de autorización
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
            # Guarda las credenciales temporalmente en token.pickle
            with open(token_pickle, 'wb') as token:
                pickle.dump(creds, token)
    # Extraer el refresh_token
    refresh_token = creds.refresh_token
    print("Tu refresh_token es:", refresh_token)
    # Guardar el refresh_token en el archivo .env
    with open(dotenv_path, 'a') as env_file:
        env_file.write(f'\nGOOGLE_REFRESH_TOKEN={refresh_token}\n')
    print("El refresh_token se ha añadido al archivo .env.")

    # Eliminar el archivo token.pickle
    if os.path.exists(token_pickle):
        os.remove(token_pickle)
        print("El archivo token.pickle ha sido eliminado.")

if __name__ == '__main__':
    main()
