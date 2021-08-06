from rest_framework import serializers
from .models import Products

class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['name', 'type', 'kcal', 'carb', 'prot', 'fat']




# class ProductsSerializer(serializers.Serializer):
#     name = serializers.CharField(max_length=50)
#     type = serializers.CharField(max_length=50)
#     kcal = serializers.FloatField()
#     carb = serializers.FloatField()
#     prot = serializers.FloatField()
#     fat = serializers.FloatField()
#
#     def create(self, validated_data):
#         return Products.objects.create(validated_data)
#
#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.type = validated_data.get('type', instance.type)
#         instance.kcal = validated_data.get('kcal', instance.kcal)
#         instance.carb = validated_data.get('carb', instance.carb)
#         instance.prot = validated_data.get('carb', instance.prot)
#         instance.fat = validated_data.get('carb', instance.fat)
#         instance.save()
#         return instance