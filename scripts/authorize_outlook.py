import os
from dotenv import load_dotenv
from O365 import Account, FileSystemTokenBackend

# Obtener la ruta absoluta al directorio del script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Obtener la ruta al directorio raíz del proyecto (padre de scripts/)
project_root = os.path.abspath(os.path.join(script_dir, os.pardir))

# Construir la ruta al archivo .env en el directorio raíz
dotenv_path = os.path.join(project_root, '.env')

# **Agregar impresión para verificar la ruta al .env**
print(f"Ruta al archivo .env: {dotenv_path}")

# Cargar las variables de entorno desde el archivo .env en el directorio raíz
load_dotenv(dotenv_path)

# Ahora puedes acceder a las variables de entorno
client_id = os.getenv('MICROSOFT_CLIENT_ID')
client_secret = os.getenv('MICROSOFT_CLIENT_SECRET')
tenant_id = os.getenv('MICROSOFT_TENANT_ID')

# **Agregar impresiones para verificar los valores cargados (sin exponer información sensible)**
print(f"MICROSOFT_CLIENT_ID cargado: {'Sí' if client_id else 'No'}")
print(f"MICROSOFT_CLIENT_SECRET cargado: {'Sí' if client_secret else 'No'}")
print(f"MICROSOFT_TENANT_ID cargado: {'Sí' if tenant_id else 'No'}")

# Verificar si las variables se cargaron correctamente
if not client_id or not client_secret or not tenant_id:
    print("Error: No se pudieron cargar una o más variables del archivo .env.")
    exit()


# Resto del código para la autenticación
# Ruta donde se almacenará el token
token_backend = FileSystemTokenBackend(token_path='tokens', token_filename='o365_token.txt')

# Crear la cuenta con las credenciales y el backend de tokens
account = Account((client_id, client_secret), token_backend=token_backend, tenant_id=tenant_id)

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
