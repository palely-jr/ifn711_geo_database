from django.db import models
from django.contrib.auth.models import User



class StorageManager(models.Manager):
    def create_fileStorage(self, total_file_size, used_file_size, remaining_file_size,user_id):
        item = self.create(total_file_size=total_file_size, used_file_size=used_file_size, remaining_file_size=remaining_file_size,user_id=user_id)
        return item

class fileStorage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=False)
    id = models.AutoField(primary_key=True)
    total_file_size = models.CharField(max_length=200)
    used_file_size = models.CharField(max_length=200)
    remaining_file_size = models.CharField(max_length=200)
    class Meta():
        db_table = "file_storage"

    objects = StorageManager()
    

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