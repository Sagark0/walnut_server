from django.db import models

class Transaction(models.Model):
    transaction_id = models.CharField()
    amount = models.IntegerField()
    category = models.CharField()
    details = models.CharField(default="No Details")
    date = models.DateField()
    time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.transaction_id
