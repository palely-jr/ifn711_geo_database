from django.db import models
from django.contrib.auth.models import User


#items sections

class ItemsManager(models.Manager):
    def create_item(self, item_file, item_name, user_id):
        item = self.create(item_file=item_file, item_name=item_name, user_id=user_id)
        return item

class Items(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=False)
    item_id = models.AutoField(primary_key=True)
    item_name = models.CharField(max_length=200)
    item_file = models.FileField()

    class Meta():
        db_table = "account_items"

    objects = ItemsManager()

#end items section