# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# author: rmarabini
"Interface with the dataabse"

from xmlrpc.client import ServerProxy

from django.conf import settings


def verificar_tarjeta(tarjeta_data):
    """
    Invokes the remote procedure to verify if the card is registered.
    :param tarjeta_data: Dictionary containing the card data to be verified.
    :return: Boolean (True if the card is valid, False otherwise).
    """
    with ServerProxy(settings.RPCAPIBASEURL) as proxy:
        return proxy.verificar_tarjeta(tarjeta_data)


def registrar_pago(pago_dict):
    """
    Invokes the remote procedure to register a payment.
    :param pago_dict: Dictionary containing the payment information (including tarjeta_id).
    :return: Dictionary with the new payment information if successful, None in case of error.
    """
    try:
        with ServerProxy(settings.RPCAPIBASEURL) as proxy:
            return proxy.registrar_pago(pago_dict)
    except Exception as e:
        print("Error: Registering payment via RPC: ", e)
        return None


def eliminar_pago(idPago):
    """
    Invokes the remote procedure to delete an existing payment.
    :param idPago: Identifier (integer or string) of the payment to be deleted.
    :return: Boolean (True if successfully deleted, False otherwise).
    """
    with ServerProxy(settings.RPCAPIBASEURL) as proxy:
        return proxy.eliminar_pago(idPago)


def get_pagos_from_db(idComercio):
    """
    Invokes the remote procedure to get the payments for a specific commerce.
    :param idComercio: String containing the commerce identifier.
    :return: List of dictionaries representing the payments found for that commerce.
    """
    with ServerProxy(settings.RPCAPIBASEURL) as proxy:
        return proxy.get_pagos_from_db(idComercio)
