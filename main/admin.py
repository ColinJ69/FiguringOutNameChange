from django.contrib import admin
from main.models import points_model, donate_model, newsletter, user_donate_model
from django.contrib.auth.admin import UserAdmin

# Register your models here.
admin.site.register(points_model)
admin.site.register(donate_model)
admin.site.register(newsletter)
admin.site.register(user_donate_model)