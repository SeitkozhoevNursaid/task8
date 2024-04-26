from django.db import models


class Category(models.Model):
    name = models.CharField(("Тип транспортного средства"), max_length=50)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        
        
class Car(models.Model):
    name = models.CharField(("Название машины"), max_length=50)
    description = models.CharField(("Описание машины"), max_length=250)
    price = models.IntegerField(('Цена машины'))
    images = models.ImageField(("Фото машины"), upload_to='images/', null=True, blank=True)
    category = models.ForeignKey(Category, verbose_name=('Категория'), on_delete=models.CASCADE,)

    class Meta:
        verbose_name = 'Машина'
        verbose_name_plural = 'Машины'
        