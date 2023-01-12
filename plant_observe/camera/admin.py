from django.contrib import admin

# Register your models here.
from plant_observe.camera.models import Image

admin.site.register(Image)
