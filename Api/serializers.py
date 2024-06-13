from . models import Category,MenuItem,Cart,Order,OrderItem
from rest_framework import serializers
from django.contrib.auth.models import User,Group

class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name']
        

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class MenuItemSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(write_only=True)
    category = CategorySerializer(read_only=True)
    class Meta:
        model = MenuItem
        fields = ['id','title','price','featured','category_id','category']

class CartSerializer(serializers.ModelSerializer):
    menuItem = MenuItemSerializer(read_only=True)
    menuItem_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = Cart
        fields = ['id','quantity','unitPrice','price','menuItem','menuItem_id']

class OrderSerializer(serializers.ModelSerializer):
    deliveryCrew = UserSerializer(read_only=True)
    deliveryCrew_id = serializers.IntegerField(write_only=True)
    total = serializers.DecimalField(read_only=True,max_digits=6,decimal_places=2)
    user = UserSerializer(read_only=True)
    class Meta:
        model = Order
        fields = ['id','deliveryCrew_id','status','total','date','deliveryCrew','user']       

class OrderItemSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)
    order_id = serializers.IntegerField(write_only=True)
    menuItem = MenuItemSerializer(read_only=True)
    menuItem_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = OrderItem
        fields = ['id','order','menuItem','menuItem_id','quantity','unitPrice','price','order_id']
        
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

