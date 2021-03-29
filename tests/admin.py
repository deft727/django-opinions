from django.contrib import admin
from .models import *


admin.site.register(Tests)
admin.site.register(Profile)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Answer)