from django.db import models


class Order(models.Model):
    order_number = models.PositiveIntegerField(primary_key=True)
    date_to_delivery = models.DateField()
    price_in_usd = models.PositiveIntegerField()
    price_in_rub = models.PositiveIntegerField()

    def __str__(self):
        return self.order_number
