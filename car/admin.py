from django.contrib import admin

from car.models import Category, Car, CarImg


class CarImageInline(admin.TabularInline):
    model = CarImg
    extra = 1


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    inlines = [CarImageInline]


admin.site.register(CarImg)
admin.site.register(Category)
