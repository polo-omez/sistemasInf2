# Uses rabbitMQ as the server

import os
import sys

import django
import pika

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "visaSite.settings")
django.setup()

from visaAppRPCBackend.models import Pago, Tarjeta


def main():

    if len(sys.argv) != 3:
        print("Debe indicar el host y el puerto")
        exit()

    hostname = sys.argv[1]
    port = sys.argv[2]

    credentials = pika.PlainCredentials("alumnomq", "alumnomq")
    parameters = pika.ConnectionParameters(
        host=hostname, port=port, credentials=credentials
    )
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.queue_declare(queue="pago_cancelacion")

    def callback(ch, method, properties, body):
        id_pago = body.decode()
        print(f"Mensaje recibido solicitando cancelación del pago ID: {id_pago}")

        try:
            pago = Pago.objects.get(id=id_pago)
            pago.codigoRespuesta = "111"
            pago.save()
            print(
                f"Éxito: Pago {id_pago} cancelado satisfactoriamente (codigoRespuesta='111')."
            )
        except Exception as e:
            print(f"Error procesando el pago {id_pago}: {e}")

    channel.basic_consume(
        queue="pago_cancelacion", on_message_callback=callback, auto_ack=True
    )

    print(
        'Servidor MQ iniciado. Esperando mensajes en "pago_cancelacion". Para salir presione CTRL+C'
    )
    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nMQ Server stopped.")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
