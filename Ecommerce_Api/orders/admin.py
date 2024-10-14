from django.contrib import admin
from .models import Order  

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('user__username', 'user__email')
    ordering = ('-created_at',)

admin.site.register(Order, OrderAdmin)
