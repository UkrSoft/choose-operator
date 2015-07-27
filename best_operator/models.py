__author__ = 'Kostiantyn Bezverkhyi'


from django.db import models

class Operator(models.Model):
    # Type of fields will be updated after additional learning of types
    operator_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=100)
