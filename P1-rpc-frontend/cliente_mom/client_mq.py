import sys

import pika


def cancelar_pago(hostname, port, id_pago):

    try:
        port = int(port)
        credentials = pika.PlainCredentials("alumnomq", "alumnomq")
        parameters = pika.ConnectionParameters(
            host=hostname, port=port, credentials=credentials
        )
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()

    except Exception as e:
        print(f"Error al conectar al host remoto: {e}")
        exit()

    channel.queue_declare(queue="pago_cancelacion")

    channel.basic_publish(
        exchange="", routing_key="pago_cancelacion", body=str(id_pago)
    )
    print(f"Solicitud enviada para cancelar pago ID: {id_pago}")

    connection.close()


def main():

    if len(sys.argv) != 4:
        print(
            "Debe indicar el host, el numero de puerto, y el ID del pago a cancelar como un argumento."
        )
        exit()

    cancelar_pago(sys.argv[1], sys.argv[2], sys.argv[3])


if __name__ == "__main__":
    main()
