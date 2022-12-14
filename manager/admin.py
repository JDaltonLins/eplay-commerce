import inspect
import sys
from django.contrib import admin

# Register your models here.

# Pega todos os modelos do .models e registra no admin, dinamicamente

clsmembers = inspect.getmembers(sys.modules['manager.models'], inspect.isclass)
# Pega todo tipo de modelo que extende a classe Model e retorna somente os que não são abstratos, somente os validos

for name, cls in clsmembers:
    if cls.__module__ == 'manager.models' and issubclass(cls, models
        print('Registering model: ' + name)
        admin.site.register(cls)
