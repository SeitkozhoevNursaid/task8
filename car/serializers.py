from rest_framework import serializers
from car.models import Car, Category


class CarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Car
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class CarUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(
        max_length=50,
        write_only=True,
        required=False
    )
    description = serializers.CharField(
        max_length=250,
        write_only=True,
        required=False
    )
    price = serializers.IntegerField(
        write_only=True,
        required=False
    )
    category = serializers.CharField(
        write_only=True,
        required=False
    )
    images = serializers.ImageField(
        required=False,
    )

    def validate(self, data):
        category_name = data['category']
        if data == dict():
            raise serializers.ValidationError(
                ('Вы ничего не заполнили!'),
            )

        if not Category.objects.filter(name=category_name).exists():
            raise serializers.ValidationError(
                ('Такой категории не существует')
            )

        return data

    def update(self, instance, validated_data):
        return instance