from rest_framework import serializers
from car.models import Car, Category, CarImg


class CarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Car
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class CarUpdateSerializer(serializers.Serializer):  # TODO: recode
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

    def validate(self, data):
        if data == dict():  # TODO: ????
            raise serializers.ValidationError(
                ('Вы ничего не заполнили!'),
            )

        return data

    def update(self, instance, validated_data):  # TODO ???
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        category_name = validated_data.get('category', instance.category)
        if category_name:
            category, categor = Category.objects.get_or_create(name=category_name)
            instance.category = category
        else:
            instance.category
        instance.save()
        return instance


class CarImgSerializer(serializers.ModelSerializer):  # TODO: Incorrect

    class Meta:
        model = CarImg
        fields = '__all__'


class CarCreateSerializer(serializers.ModelSerializer):
    img = serializers.FileField(required=False)
    
    class Meta:
        model = Car
        fields = '__all__'

    def create(self, validated_data):
        img = validated_data.pop('img')
        car = Car.objects.create(**validated_data)
        files = [img]
        images = []
        for file in files:
            images.append(CarImg(name=car, images=file))
        CarImg.objects.bulk_create(images)
        return car
