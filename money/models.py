from django.db import models
# Create your models here.
class Money(models.Model):
    use_date = models.DateField()
    detail = models.CharField(max_length=200)
    cost = models.IntegerField(default=0)
    category = models.CharField(max_length=10)   
    location= models.CharField(max_length=10)
    def __str__(self):
        return self.detail + ' ￥' + str(self.cost)