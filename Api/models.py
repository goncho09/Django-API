from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=255,db_index=True)

    def __str__(self):
        return self.title
    
    class Meta:
        unique_together = ['slug','title']
    
class MenuItem(models.Model):
    title = models.CharField(max_length=255,db_index=True)
    price = models.DecimalField(max_digits=6,decimal_places=2,db_index=True)
    featured = models.BooleanField(db_index=True,default=False)
    category = models.ForeignKey(Category,on_delete=models.PROTECT)

    def __str__(self):
        return self.title
    
    def get(self):
        return {
            'id':self.id,
            'title':self.title,
            'price':self.price,
            'featured':self.featured,
            'category':self.category.title
        }
    
    class Meta:
        unique_together = ['title']
        
        
    
class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    menuItem = models.ForeignKey(MenuItem,on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    unitPrice = models.DecimalField(max_digits=6,decimal_places=2)
    price = models.DecimalField(max_digits=6,decimal_places=2)

    def __str__(self):
        return self.user.username + ' ' + self.menuItem.title

class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    deliveryCrew = models.ForeignKey(User,on_delete=models.SET_NULL,related_name='deliveryCrew',null=True)
    status = models.BooleanField(db_index=True,default=False)
    total = models.DecimalField(max_digits=6,decimal_places=2)
    date = models.DateField(db_index=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    menuItem = models.ForeignKey(MenuItem,on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    unitPrice = models.DecimalField(max_digits=6,decimal_places=2)
    price = models.DecimalField(max_digits=6,decimal_places=2)

    def __str__(self):
        return self.order.user.username + ' ' + self.menuItem.title
    

