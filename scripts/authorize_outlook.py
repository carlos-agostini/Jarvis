import os
from dotenv import load_dotenv
from O365 import Account, FileSystemTokenBackend

load_dotenv(override=True)

# Cargar variables de entorno
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, os.pardir))
dotenv_path = os.path.join(project_root, '.env')
load_dotenv(dotenv_path)

# Obtener variables de entorno (sin client_secret)
client_id = os.getenv('MICROSOFT_CLIENT_ID')
tenant_id = os.getenv('MICROSOFT_TENANT_ID')

# Verificar que las variables no estén vacías
if not client_id or not tenant_id:
    print("Error: Las variables de entorno no se cargaron correctamente.")
    exit()

# Crear las credenciales sin client_secret
credentials = (client_id, )

# Ruta donde se almacenará el token
token_backend = FileSystemTokenBackend(token_path='tokens', token_filename='o365_token.txt')

# Crear la cuenta con auth_flow_type='public'
account = Account(credentials, tenant_id=tenant_id, token_backend=token_backend, auth_flow_type='public')

# Definir los scopes necesarios
scopes = [
    'offline_access',
    'https://graph.microsoft.com/Mail.Send',
    'https://graph.microsoft.com/Mail.ReadWrite',
    'https://graph.microsoft.com/Calendars.ReadWrite'
]

# Realizar la autenticación
if not account.is_authenticated:
    # Esto abrirá el navegador para autenticación
    result = account.authenticate(scopes=scopes)
    if result:
        print("Autenticación exitosa.")
    else:
        print("No se pudo autenticar. Verifica tus credenciales.")
        exit()

# Obtener el token
token = account.connection.token_backend.token

# Extraer el refresh_token
refresh_token = token.get('refresh_token')
print("Tu refresh_token es:", refresh_token)

# Guardar el refresh_token en el archivo .env
with open(dotenv_path, 'a') as env_file:
    env_file.write(f'\nMICROSOFT_REFRESH_TOKEN={refresh_token}\n')
print("El refresh_token se ha añadido al archivo .env.")

# Opcional: Eliminar el archivo de token si no deseas almacenarlo
import shutil
shutil.rmtree('tokens')
print("El directorio de tokens ha sido eliminado.")
