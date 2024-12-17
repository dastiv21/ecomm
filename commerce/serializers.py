from rest_framework import serializers
from .models import Category, Product, Order

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        # fields = ['id','name','description','price','stock','image','category', ]


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'products', 'total_price', 'created_at']

    def create(self, validated_data):
        # Extract products data
        products_data = validated_data.pop('products', [])
        # Create the order without products first
        order = Order.objects.create(**validated_data)
        # Add products to the ManyToMany field
        order.products.set(products_data)
        return order