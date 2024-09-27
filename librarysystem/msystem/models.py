from django.db import models
from django.utils import timezone
from datetime import timedelta
# Create your models here.
from django.contrib.auth.models import User

class Libraryman(models.Model):

    user=models.OneToOneField(User,on_delete=models.CASCADE)

class Student(models.Model):

    user=models.OneToOneField(User,on_delete=models.CASCADE)

    total_fine = models.DecimalField(max_digits=5,decimal_places=2, default=0.00)

class Book(models.Model):

    title = models.CharField(max_length=50)
    auhter = models.CharField(max_length=50)
    publication_year = models.PositiveIntegerField()
    available_copies = models.PositiveIntegerField()


    def __str__(self):
        return self.title


class Issuedbook(models.Model):

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    issued_book = models.ForeignKey(Book , on_delete=models.CASCADE)
    issued_date = models.DateTimeField(default=timezone.now)
    return_date = models.DateTimeField(null= True, blank= True)
   
    @property
    def overdue(self):


        if self.return_date is None:
            overdue_days =  (timezone.now() - self.issued_date).days -7
            if overdue_days > 0:
                return overdue_days
            
        return 0
    
    def calculated_fine(self):


        overdue_day = self.overdue
        return overdue_day * 10  if overdue_day > 0 else 0

