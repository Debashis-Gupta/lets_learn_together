from django.db import models

# Create your models here.


class Contact(models.Model):
    firstname = models.CharField(max_length=40,null=True)
    lastname = models.CharField(max_length=40,null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    phone = models.IntegerField(null=True)
    email = models.EmailField(blank=True,null=True)

    def __str__(self):
        name = self.firstname +" "+ self.lastname
        return name