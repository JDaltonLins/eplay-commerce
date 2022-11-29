import inspect
import sys
from django.contrib import admin

# Register your models here.

# Pega todos os modelos do .models e registra no admin, dinamicamente

clsmembers = inspect.getmembers(sys.modules['manager.models'], inspect.isclass)

for name, cls in clsmembers:
    if name != 'BaseModel':
        admin.site.register(cls)
