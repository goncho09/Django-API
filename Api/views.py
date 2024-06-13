from django.shortcuts import render
from rest_framework import generics
from .models import MenuItem as MenuItemModel,Cart as CartModel,Order as OrderModel,OrderItem as OrderItemModel
from .serializers import MenuItemSerializer,UserSerializer,GroupSerializer,CartSerializer,OrderSerializer,OrderItemSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User,Group    
from django.core.paginator import Paginator,EmptyPage

# Create your views here.
class MenuItemsView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MenuItemSerializer

    def get(self,request):
        perPage = request.query_params.get('perPage',default=5)
        page = request.query_params.get('page',default=1)
        queryset = MenuItemModel.objects.all()
        paginator = Paginator(queryset,per_page=perPage)
        try:
            queryset = paginator.page(page)
        except EmptyPage:
            queryset = []
        serializer_class = MenuItemSerializer(queryset,many=True)
        return Response(data = {'count':paginator.count,'page':page,'results':serializer_class.data},status=200)
    
    def post(self,request):
        user = request.user
        if(user.is_staff == False and user.is_superuser == False):
           return Response(data = {'status:':'unauthorized','data':'You are not authorized to view this page.'},status=403)
       
        post = MenuItemSerializer(data=request.data)
        if post.is_valid():
            post.save()
            return Response(data = {'status':'ok','result':'The item was created.'},status=201)
        else:
            return Response(data = {'status':'error','data':post.errors},status=400)     
           
           
class MenuItemView(generics.RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MenuItemSerializer
    def get(self,request,id):
        try:
            menuItem = MenuItemModel.objects.get(id=id)
            serializer_class = MenuItemSerializer(menuItem)
            return Response(data = {'status':'ok','result':serializer_class.data},status=200)
        except Exception as e:
            return Response(data = {'status':'error','data':'This item not exists.'},status=404)
        
    def delete(self,request,id):
        user = request.user
        if(user.is_staff == False and user.is_superuser == False):
           return Response(data = {'status:':'unauthorized','data':'You are not authorized to view this page.'},status=403)
        print(user)
        try:
            menuItem = MenuItemModel.objects.get(id=id)
            menuItem.delete()
            return Response(data = {'status':'ok','result':'The item was deleted.'},status=200)
        except Exception as e:
            return Response(data = {'status':'error','data':'This item does not exist.'},status=404)
        
        
class GroupsView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    def get(self,request):
        user = request.user
        if(user.is_staff == False and user.is_superuser == False):
           return Response(data = {'status:':'unauthorized','data':'You are not authorized to view this page.'},status=403)
        queryset = User.objects.filter(groups__name='Manager')
        serializer_class = UserSerializer(queryset,many=True)
        return Response(data = {'results':serializer_class.data},status=200)
    def post(self,request):
        user = request.user
        if(user.is_staff == False and user.is_superuser == False):
           return Response(data = {'status:':'unauthorized','data':'You are not authorized to view this page.'},status=403)
       
        username = request.data.get('user')
        try:
            user = User.objects.get(username=username)
            group = Group.objects.get(name='Manager')
            groupSerializer = GroupSerializer(group)
            user.groups.add(groupSerializer.data['id'])
            return Response(data = {'status':'ok','result':'The user was added to the group.'},status=201)
        except Exception:
            return Response(data = {'status':'error','data':'This user does not exist.'},status=404)
        
class GroupView(generics.DestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    def delete(self,request,id):
        user = request.user
        if(user.is_staff == False and user.is_superuser == False):
           return Response(data = {'status:':'unauthorized','data':'You are not authorized to view this page.'},status=403)
       
        try:
            user = User.objects.get(id=id)
            group = Group.objects.get(name='Manager')
            groupSerializer = GroupSerializer(group)
            user.groups.remove(groupSerializer.data['id'])
            return Response(data = {'status':'ok','result':'The user was removed of the group.'},status=201)
        except Exception:
            return Response(data = {'status':'error','data':'This user does not exist.'},status=404)

class DeliverysView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    def get(self,request):
        user = request.user
        if(user.is_staff == False and user.is_superuser == False):
           return Response(data = {'status:':'unauthorized','data':'You are not authorized to view this page.'},status=403)
        queryset = User.objects.filter(groups__name='Delivery Crew')
        serializer_class = UserSerializer(queryset,many=True)
        return Response(data = {'results':serializer_class.data},status=200)
    def post(self,request):
        user = request.user
        if(user.is_staff == False and user.is_superuser == False):
           return Response(data = {'status:':'unauthorized','data':'You are not authorized to view this page.'},status=403)
       
        username = request.data.get('username')
        try:
            user = User.objects.get(username=username)
            group = Group.objects.get(name='Delivery Crew')
            groupSerializer = GroupSerializer(group)
            user.groups.add(groupSerializer.data['id'])
            return Response(data = {'status':'ok','result':'The user was added to the group.'},status=201)
        except Exception:
            return Response(data = {'status':'error','data':'This user or the group does not exist.'},status=404)
        
class DeliveryView(generics.DestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    def delete(self,request,id):
        user = request.user
        if(user.is_staff == False and user.is_superuser == False):
           return Response(data = {'status:':'unauthorized','data':'You are not authorized to view this page.'},status=403)
       
        try:
            user = User.objects.get(id=id)
            group = Group.objects.get(name='Delivery Crew')
            groupSerializer = GroupSerializer(group)
            user.groups.remove(groupSerializer.data['id'])
            return Response(data = {'status':'ok','result':'The user was removed of the group.'},status=201)
        except Exception:
            return Response(data = {'status':'error','data':'This user does not exist.'},status=404)
        
class CartsView(generics.DestroyAPIView,generics.ListCreateAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        results = Group.objects.filter(user=user)
        client = False
        for result in results:
            if result == 'Client':
                client = True
                break
        if(client == False and user.is_superuser == False):
           return Response(data = {'status:':'unauthorized','data':'You are not authorized to view this page.'},status=403)
        queryset = CartModel.objects.all()
        serializer_class = CartSerializer(queryset,many=True)
        return Response(data = {'results':serializer_class.data},status=200)
    
    def post(self,request):
        user = request.user
        results = Group.objects.filter(user=user)
        client = False
        for result in results:
            if result == 'Client':
                client = True
                break
        if(client == False and user.is_superuser == False):
           return Response(data = {'status:':'unauthorized','data':'You are not authorized to view this page.'},status=403)
        
        request.data._mutable = True
        request.data.update({'user_id':user.id})
        post = CartSerializer(data=request.data)
        
        if post.is_valid():
            try:
                userId = post.initial_data['user_id']
                userPost = User.objects.get(id=userId)
                post.save(user=userPost)
                return Response(data = {'status':'ok','result':'The item was added to the cart.'},status=201)
            except Exception as e:
                return Response(data = {'status':'error','data':e.args},status=404)
        else:
            return Response(data = {'status':'error','data':post.errors},status=400)
        
    def delete(self,request):
        user = request.user
        results = Group.objects.filter(user=user)
        client = False
        for result in results:
            if result == 'Client':
                client = True
                break
        if(client == False and user.is_superuser == False):
           return Response(data = {'status:':'unauthorized','data':'You are not authorized to view this page.'},status=403)
        try:
            cart = CartModel.objects.get(user=user)
            cart.delete()
            return Response(data = {'status':'ok','result':'The cart was deleted.'},status=200)
        except Exception as e:
            return Response(data = {'status':'error','data':'This cart does not exist.'},status=404)
        
class OrdersView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        user = request.user
        perPage = request.query_params.get('perPage',default=5)
        page = request.query_params.get('page',default=1)
        queryset = MenuItemModel.objects.all()
    
        if(user.is_staff == True or user.is_superuser == True or user.groups.filter(name='Manager').exists()):
            queryset = OrderModel.objects.all()
            paginator = Paginator(queryset,per_page=perPage)
            try:
                queryset = paginator.page(page)
            except EmptyPage:
                queryset = []
            serializer_class = OrderSerializer(queryset,many=True)
            return Response(data = {'count':paginator.count,'page':page,'results':serializer_class.data},status=200)
        elif user.groups.filter(name='Client').exists():
            queryset = OrderModel.objects.filter(user=user)
            paginator = Paginator(queryset,per_page=perPage)
            try:
                queryset = paginator.page(page)
            except EmptyPage:
                queryset = []
            serializer_class = OrderSerializer(queryset,many=True)
            return Response(data = {'count':paginator.count,'page':page,'results':serializer_class.data},status=200)
        else:
            queryset = OrderModel.objects.filter(deliveryCrew=user)
            paginator = Paginator(queryset,per_page=perPage)
            try:
                queryset = paginator.page(page)
            except EmptyPage:
                queryset = []
            serializer_class = OrderSerializer(queryset,many=True)
            return Response(data = {'count':paginator.count,'page':page,'results':serializer_class.data},status=200)
    
    def post(self,request):
        user = request.user
        results = Group.objects.filter(user=user)
        client = False
        for result in results:
            if result == 'Client':
                client = True
                break
        if(client == False and user.is_superuser == False):
           return Response(data = {'status:':'unauthorized','data':'You are not authorized to view this page.'},status=403)
        
        request.data._mutable = True
        request.data.update({'user_id':user.id})
        post = OrderSerializer(data=request.data)
        if post.is_valid():
            try:
                userId = post.initial_data['user_id']
                userPost = User.objects.get(id=userId)
                cart = CartModel.objects.filter(user=user)
                total = 0
                post.save(user=userPost,total =0)
                for item in cart:
                    total += item.price
                    orderItemPost = {
                    'order_id':post.data['id'],
                    'menuItem_id':item.id,
                    'quantity':item.quantity,
                    'unitPrice':item.unitPrice,
                    'price':item.price
                    }
                    itemsPost = OrderItemSerializer(data=orderItemPost)
                    if itemsPost.is_valid():
                        itemsPost.save()
                    else:
                        return Response(data = {'status':'error','data':itemsPost.errors},status=400)
                cart.delete()
                OrderModel.objects.filter(id=post.data['id']).update(total=total)
                return Response(data = {'status':'ok','result':'The order was created.'},status=201)
            except Exception as e:
                return Response(data = {'status':'error','data':e.args},status=404)
        else:
            return Response(data = {'status':'error','data':post.errors},status=400)  


class OrderView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    def get(self,request,id):
        user = request.user
        queryset = OrderModel.objects.filter(id=id,user=user)
        if queryset.exists() == False:
            return Response(data = {'status':'error','data':'This order does not exist.'},status=404)
        
        if (user.groups.filter(name='Client').exists() == True or user.is_superuser == True):
            orderItems = OrderItemModel.objects.filter(order=id)
            orderSerializer = OrderItemSerializer(orderItems,many=True)
            return Response(data = {'status':'ok','results':orderSerializer.data},status=200)
        
        else:
            return Response(data = {'status:':'unauthorized','data':'You are not authorized to view this page.'},status=403)
            
    def delete(self,request,id):
        user = request.user
        if(user.is_staff == False and user.is_superuser == False and user.groups.filter(name='Manager').exists() == False):
           return Response(data = {'status:':'unauthorized','data':'You are not authorized to view this page.'},status=403)
        try:
            order = OrderModel.objects.get(id=id)
            order.delete()
            return Response(data = {'status':'ok','result':'The order was deleted.'},status=200)
        except Exception as e:
            return Response(data = {'status':'error','data':'This order does not exist.'},status=404)
        
    def patch(self,request,id):
        user = request.user
        try:
            if user.groups.filter(name='Delivery Crew').exists() == True:
                order = OrderModel.objects.get(id=id)
                order.update(status=not order.status)
                return Response(data = {'status':'ok','result':'The status was changed.'},status=200)
            elif user.groups.filter(name='Client').exists() == True:
                order = OrderModel.objects.get(id=id)
                order.update(data = request.data)
                return Response(data = {'status':'ok','result':'The order was changed.'},status=200)
        except Exception as e:
            return Response(data = {'status':'error','data':'This order does not exist.'},status=404)