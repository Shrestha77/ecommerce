from django.contrib import admin
from .models import Product, Contact, Customer, Order, OrderItem, ShippingAddress,User


# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'first_name',
                    'last_name', 'email', 'contact', 'is_verified', 'is_active')
    #to add filter by field name
    list_filter = ('is_verified', 'is_active' )
    #to search data by field name
    search_fields = ("user_name__icontains", )
    
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'category',
                    'subcategory', 'price', 'published_date',)
    list_filter = ('category', )
    search_fields = ("product_name__icontains", )
    

class ContactAdmin(admin.ModelAdmin):
    list_display = ('msg_id', 'name',
                    'email', 'phone', 'message',)
    
    list_filter = ('name', )
    
    search_fields = ("email__istartswith", )
    
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'user',
                    'email', 'phone', 'address',)
    
    list_filter = ('address', )
    
    search_fields = ("email__istartswith", )


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'order',
                    'qunatity', 'date_added', )
    
    list_filter = ('date_added', )
    
    search_fields = ("order__startswith", )
    
class OrderAdmin(admin.ModelAdmin):
    list_display = ( 'id', 'customer', 'transaction_id',
                    'complete', 'date_orderd', )
    
    list_filter = ('date_orderd', )
    
    search_fields = ("customer__istartswith", )
    

class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ( 'order', 'customer', 'address',
                    'city', 'district', 'date_added',)
    
    list_filter = ('city',)
    
    search_fields = ("customer__istartswith", )


admin.site.register(User, UserAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(ShippingAddress, ShippingAddressAdmin)


admin.site.site_header = "Online store Admin Dashboard"
admin.site.site_title = "Admin"
admin.site.index_title = "Dashboard"
