from django.db import models


class Department(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Employee(models.Model):
    fullname = models.CharField(max_length=100)
    hobby = models.CharField(max_length=30,blank=True)
    mobile = models.CharField(max_length=15,blank=True)
    department = models.ForeignKey(Department,on_delete=models.CASCADE)

    def __str__(self):
        return self.fullname