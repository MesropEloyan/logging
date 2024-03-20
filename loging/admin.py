from django.contrib import admin
from .models import Document

# Регистрация модели Document в административной панели
admin.site.register(Document)