from django.contrib import admin
from .models import *

# Register your model without any custom configuration
admin.site.register(CustomUser)
admin.site.register(Account)
admin.site.register(FinancialTransaction)
