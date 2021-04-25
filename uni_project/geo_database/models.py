from django.db import models


# Create your models here.
class Accounts(models.Model):
    account_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, default="random_user")
    entire_name = models.CharField(max_length=100, default="random_person")
    email = models.EmailField()
    password = models.CharField(max_length=15)

    class Meta():
        db_table = "user_accounts"


class Items(models.Model):
    user_id = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    item_id = models.IntegerField(primary_key=True)
    item_name = models.CharField(max_length=200)

    class Meta():
        db_table = "account_items"

