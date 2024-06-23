# from connection import sns_client

# phone_numbers = ["+51955329623", "+51934003487", "+51942758083"]  # Lista de números de teléfono

# message = "Te ganaste una camioneta, deposita en la siguiente cuenta 100 dolares"

# for phone_number in phone_numbers:
#     response = sns_client.publish(
#         PhoneNumber=phone_number,
#         Message=message
#     )
#     print(f"Mensaje enviado a {phone_number}: {response}")
import boto3
import botocore
from connection import sns_client

# Lista de números de teléfono a los que enviar el mensaje
phone_numbers = ["+51955329623"]  # Reemplaza con tus números de teléfono

# Leer el contenido del archivo de reporte
with open('reporte_generado.txt', 'r', encoding='utf-8') as file:
    message = file.read()

# Enviar el mensaje a cada número de teléfono
for phone_number in phone_numbers:
    try:
        response = sns_client.publish(
            PhoneNumber=phone_number,
            Message=message
        )
        print(f"Mensaje enviado a {phone_number}: {response}")
    except botocore.exceptions.ClientError as error:
        print(f"Error sending message to {phone_number}: {error}")
