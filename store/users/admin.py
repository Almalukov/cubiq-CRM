from django.contrib import admin

from users.models import User
from products.admin import BasketAdminInline

admin.site.register(User)
