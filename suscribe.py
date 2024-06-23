from connection import sns_client
import subprocess
import os


python_interpreter = os.path.join(os.getcwd(), 'env', 'Scripts', 'python.exe')  
try:
    result = subprocess.run([python_interpreter, "main.py"], check=True, capture_output=True, text=True)
    print("main.py output:", result.stdout)
except subprocess.CalledProcessError as e:
    print("Error al ejecutar main.py:", e.stderr)
    exit(1)
# client.subscribe(
#     TopicArn="arn:aws:sns:us-east-2:891376999830:Rimac",
#     Protocol="email",
#     Endpoint="diego.rojas.v@uni.pe",
#     ReturnSubscriptionArn=True
# )
with open('reporte_generado.txt', 'r', encoding='utf-8') as file:
    message = file.read()

response = sns_client.publish(
    TopicArn="arn:aws:sns:us-east-2:891376999830:Rimac",
    Message=message,
    Subject="Mensaje de prueba"
)

print(response)