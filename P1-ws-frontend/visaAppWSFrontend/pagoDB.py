import requests
from django.conf import settings

API_URL = settings.RESTAPIBASEURL


def verificar_tarjeta(tarjeta_data):
    """
    Check if the tarjeta is registered calling the REST API.
    :param tarjeta_data: dictionary with the tarjeta data
    :return True if valid, False otherwise
    """
    if not tarjeta_data:
        return False

    url = f"{API_URL}tarjeta/"
    try:
        response = requests.post(url, json=tarjeta_data)
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"Error conectando con la API (verificar_tarjeta): {e}")
        return False


def registrar_pago(pago_dict):
    """
    Register a payment calling the REST API.
    :param pago_dict: dictionary with the pago data
    :return new pago info (dict) if succesful, None otherwise
    """
    url = f"{API_URL}pago/"
    try:
        response = requests.post(url, json=pago_dict)
        if response.status_code == 200:
            return response.json()
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error conectando con la API (registrar_pago): {e}")
        return None


def eliminar_pago(idPago):
    """
    Delete a pago calling the REST API.
    :param idPago: id of the pago to be deleted
    :return True if succesful, False otherwise
    """
    url = f"{API_URL}pago/{idPago}"
    try:
        response = requests.delete(url)
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"Error conectando con la API (eliminar_pago): {e}")
        return False


def get_pagos_from_db(idComercio):
    """
    Gets pagos correspondint to some idComercio calling the REST API.
    :param idComercio: id of the comercio
    :return list of pagos found or None
    """
    url = f"{API_URL}comercio/{idComercio}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error conectando con la API (get_pagos_from_db): {e}")
        return None
