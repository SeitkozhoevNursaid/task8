from django.db import models


class Category(models.Model):
    name = models.CharField(("Тип транспортного средства"), max_length=50)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Car(models.Model):
    name = models.CharField(("Название машины"), max_length=250)
    description = models.CharField(("Описание машины"), max_length=800)
    price = models.CharField(('Цена машины'), max_length=250)
    category = models.ForeignKey(Category, verbose_name=('Категория'), on_delete=models.CASCADE, null=True, blank=True, related_name='car')

    class Meta:
        verbose_name = 'Машина'
        verbose_name_plural = 'Машины'

    def __str__(self):
        return self.name


class CarImg(models.Model):
    images = models.FileField(("Фото машины"), upload_to='images/', null=True, blank=True)
    name = models.ForeignKey(Car, verbose_name=('Название машины'), on_delete=models.CASCADE, related_name='image')

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'

    def __str__(self):
        return str(self.name)
