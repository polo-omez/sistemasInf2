from django.contrib import admin

from .models import Pago, Tarjeta

admin.site.register(Tarjeta)
admin.site.register(Pago)
# Register your models here.
