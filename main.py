import json
import os
from dotenv import load_dotenv
import boto3
import botocore
import pandas as pd

load_dotenv()

# Obtener las credenciales y la región desde las variables de entorno
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
aws_region = os.getenv('AWS_REGION', 'us-east-1')  # Asegúrate de tener la región especificada

if not aws_access_key_id or not aws_secret_access_key or not aws_region:
    raise ValueError("Las credenciales de AWS y la región deben estar configuradas en el archivo .env")

# Crear un cliente de boto3 utilizando las credenciales y la región
bedrock_runtime = boto3.client(
    'bedrock-runtime',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=aws_region
)

def generate_report(prompt):
    body = json.dumps({
        "prompt": prompt,
        "max_gen_len": 1024,  # Incrementar el límite de generación
        "top_p": 0.9,         # Ajustar el top_p para mayor diversidad
        "temperature": 0.7    # Ajustar la temperatura para mayor creatividad
    })

    modelId = "meta.llama3-70b-instruct-v1:0"
    accept = "application/json"
    contentType = "application/json"

    try:
        response = bedrock_runtime.invoke_model(
            body=body, modelId=modelId, accept=accept, contentType=contentType
        )
        response_body = json.loads(response.get("body").read())
        print("Response Body:", response_body)  # Añadir mensaje de depuración
        return response_body["generation"]
    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == 'AccessDeniedException':
            print(f"\x1b[41m{error.response['Error']['Message']}\
                \nTo troubleshoot this issue please refer to the following resources.\
                \nhttps://docs.aws.amazon.com/IAM/latest/UserGuide/troubleshoot_access-denied.html\
                \nhttps://docs.aws.amazon.com/bedrock/latest/userguide/security-iam.html\x1b[0m\n")
        else:
            raise error
    except Exception as e:
        print(f"Unexpected error: {e}")

def main():
    # Leer el archivo CSV
    file_path = './emergencies.csv'  # Reemplaza con la ruta de tu archivo CSV
    data = pd.read_csv(file_path)
    print("Datos cargados correctamente")  # Añadir mensaje de depuración
    
    # Seleccionar la primera fila del dataset
    row = data.iloc[0]
    print("Primera fila seleccionada")  # Añadir mensaje de depuración
    
    # Generar el prompt basado en la fila seleccionada
    prompt = (
        f"Reporte de Emergencias Médicas\n"
        f"Alerta de \"Emergencia Médica\"\n\n"
        f"Detalles del Incidente:\n"
        f"Número del incidente: {row['id']}\n"
        f"Fecha y hora del incidente: {row['date']}\n"
        f"Dirección del incidente: {row['address']}\n"
        f"Latitud: {row['lat']}\n"
        f"Longitud: {row['lng']}\n"
        #f"Fuente: {row['source'] if 'source' in row else 'No disponible'}\n"
        #f"Color de alerta asignado al incidente: #1565C0\n\n"
        f"Por favor, proporciona recomendaciones detalladas y específicas para esta emergencia médica, considerando el tipo de incidente, la ubicación y otras circunstancias relevantes.\n\n"
        f"Recomendaciones:\n"
    )
    print("Prompt generado:\n", prompt)  # Añadir mensaje de depuración
    
    # Generar el reporte usando la API de Bedrock
    generated_text = generate_report(prompt)
    
    # Verificar si el texto generado está vacío
    if not generated_text:
        print("El texto generado está vacío.")
    else:
        # Limpiar el texto generado de cualquier contenido innecesario
        end_phrases = ["¿Necesitas más ayuda o tienes alguna pregunta adicional sobre esta emergencia médica?"]
        generated_text_cleaned = generated_text
        for phrase in end_phrases:
            if phrase in generated_text_cleaned:
                generated_text_cleaned = generated_text_cleaned.split(phrase)[0].strip()
        
        # Texto puntual para el archivo .txt
        report_text = (
            f"Alerta de Emergencia Médica\n"
            f"Ubicación: {row['address']}, Fecha y hora: {row['date']}\n"
            f"Si quieres saber más.\n"
            f"http://127.0.0.1:5500/reporte_generado.html"
        )
        
        # Guardar el reporte puntual en un archivo de texto
        with open('reporte_generado.txt', 'w', encoding='utf-8') as file:
            file.write(report_text)
        print("Reporte puntual generado y guardado como 'reporte_generado.txt'")
        
        # Combinar el reporte fijo con las recomendaciones generadas para el HTML
        report = (
            f"Reporte de Emergencias Médicas\n"
            f"Alerta de \"Emergencia Médica\"\n\n"
            f"Detalles del Incidente:\n"
            f"Número del incidente: {row['id']}\n"
            f"Fecha y hora del incidente: {row['date']}\n"
            f"Dirección del incidente: {row['address']}\n"
            f"Latitud: {row['lat']}\n"
            f"Longitud: {row['lng']}\n"
            f"Recomendaciones:\n"
            f"{generated_text_cleaned}\n"
        )
        
        google_maps_api_key = "AIzaSyDl4YDAOuhZT4IjMaa-aHpnDsoA8qkbNZY"
        map_url = f"https://maps.googleapis.com/maps/api/staticmap?center={row['lat']},{row['lng']}&zoom=15&size=600x400&markers=color:red%7C{row['lat']},{row['lng']}&key={google_maps_api_key}"
        report_html = (
            f"<!DOCTYPE html>\n"
            f"<html lang='es'>\n"
            f"<head>\n"
            f"    <meta charset='UTF-8'>\n"
            f"    <meta name='viewport' content='width=device-width, initial-scale=1.0'>\n"
            f"    <title>Reporte de Emergencias Médicas</title>\n"
            f"    <style>\n"
            f"        body {{ font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f7f7f7; }}\n"
            f"        .container {{ max-width: 800px; margin: 0 auto; padding: 20px; background: white; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); text-align: center; }}\n"
            f"        .header {{ background-color: #e30613; padding: 10px 20px; color: white; border-radius: 8px 8px 0 0; }}\n"
            f"        .content {{ margin: 20px 0; }}\n"
            f"        .map {{ margin: 20px 0; }}\n"
            f"        .images {{ margin: 20px 0; }}\n"
            f"        .footer {{ background-color: #e30613; padding: 10px 20px; text-align: center; color: white; border-radius: 0 0 8px 8px; }}\n"
            f"        img {{ max-width: 100%; height: auto; }}\n"
            f"    </style>\n"
            f"</head>\n"
            f"<body>\n"
            f"    <div class='container'>\n"
            f"        <div class='header'>\n"
            f"            <h1>Reporte de Emergencias Médicas</h1>\n"
            f"            <h2>Alerta de \"Emergencia Médica\"</h2>\n"
            f"        </div>\n"
            f"        <div class='content'>\n"
            f"            <h3>Detalles del Incidente:</h3>\n"
            f"            <p><strong>Número del incidente:</strong> {row['id']}</p>\n"
            f"            <p><strong>Fecha y hora del incidente:</strong> {row['date']}</p>\n"
            f"            <p><strong>Dirección del incidente:</strong> {row['address']}</p>\n"
            f"            <p><strong>Latitud:</strong> {row['lat']}</p>\n"
            f"            <p><strong>Longitud:</strong> {row['lng']}</p>\n"
            f"        </div>\n"
            f"        <div class='map'>\n"
            f"            <h3>Ubicación del Incidente:</h3>\n"
            f"            <img src='{map_url}' alt='Mapa de la ubicación'>\n"
            f"        </div>\n"
            f"        <div class='content'>\n"
            f"            <h3>Recomendaciones:</h3>\n"
            f"            <p>{generated_text_cleaned.replace('\n', '<br>')}</p>\n"
            f"        </div>\n"
            f"        <div class='footer'>\n"
            f"            <p>Este reporte ha sido generado automáticamente.</p>\n"
            f"        </div>\n"
            f"    </div>\n"
            f"</body>\n"
            f"</html>"
        )
        
        # Guardar el reporte en un archivo HTML
        with open('reporte_generado.html', 'w', encoding='utf-8') as file:
            file.write(report_html)
        print("Reporte generado y guardado como 'reporte_generado.html'")

if __name__ == "__main__":
    main()
