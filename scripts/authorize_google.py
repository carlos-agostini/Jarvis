from __future__ import print_function
import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Ámbitos requeridos
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def main():
    creds = None
    # El archivo token.pickle almacena los tokens de acceso y actualización
    token_pickle = 'token.pickle'
    if os.path.exists(token_pickle):
        with open(token_pickle, 'rb') as token:
            creds = pickle.load(token)
    # Si no hay credenciales válidas, inicia el flujo de autorización
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
            # Guarda las credenciales temporalmente en token.pickle
            with open(token_pickle, 'wb') as token:
                pickle.dump(creds, token)
    # Extraer el refresh_token
    refresh_token = creds.refresh_token
    print("Tu refresh_token es:", refresh_token)
    # Guardar el refresh_token en el archivo .env
    with open('.env', 'a') as env_file:
        env_file.write(f'\nGOOGLE_REFRESH_TOKEN={refresh_token}\n')
    print("El refresh_token se ha añadido al archivo .env.")

    # Eliminar el archivo token.pickle
    if os.path.exists(token_pickle):
        os.remove(token_pickle)
        print("El archivo token.pickle ha sido eliminado.")

if __name__ == '__main__':
    main()
