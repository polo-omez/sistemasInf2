import os
import time

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "visaSite.settings")
django.setup()

from visaAppRPCFrontend.models import Tarjeta

try:
    lista_numeros = list(Tarjeta.objects.values_list("numero", flat=True)[:1000])

    if not lista_numeros:
        print("Error: No hay datos en la tabla tarjeta.")
        start_time = time.time()
        for num in lista_numeros:
            Tarjeta.objects.get(pk=num)

        end_time = time.time()

        print(
            f"Tiempo invertido en buscar las 1000 entradas una a una (ORM): {end_time - start_time:.6f} segundos"
        )

except Exception as e:
    print(f"Error: {e}")
