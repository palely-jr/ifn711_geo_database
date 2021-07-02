from django.db import models
from django.contrib.auth.models import User







class CompanyManager(models.Manager):
    def create_Company(self, company_name, company_email):
        company = self.create(company_name=company_name, company_email=company_email)
        return company
    def check_company(self, company_name):
        if company_name==company_name:
            return True
        else:
            return False

    def get_id(self, company_name):
        if company_name == company_name:
            return id
        else:
            return False


class Company(models.Model):
    id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=200)
    company_email = models.CharField(max_length=200)
    class Meta():
        db_table = "company_details"

    objects = CompanyManager()
    

class FileStorageManager(models.Manager):
    def create_initial_storage(self, total_file_size, used_file_size, company_id,company_name):
        remaining_size = total_file_size - used_file_size
        storage = self.create(total_file_size=total_file_size,
                              used_file_size=0,
                              remaining_file_size=remaining_size,
                              company=company_id,company_name=company_name)
        return storage

class fileStorage(models.Model):
    id = models.AutoField(primary_key=True)
    total_file_size = models.CharField(max_length=200)
    used_file_size = models.CharField(max_length=200)
    remaining_file_size = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200,default="")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, unique=False)

    class Meta():
        db_table = "file_storage"

    objects = FileStorageManager()



class ItemsManager(models.Manager):
    def create_item(self, item_file, item_name, item_long, item_lat, company_id):
        item = self.create(item_file=item_file, item_name=item_name, item_long=item_long, item_lat=item_lat, company=company_id)
        return item

class Items(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, unique=False)
    item_id = models.AutoField(primary_key=True)
    item_name = models.CharField(max_length=200)
    item_file = models.FileField()
    item_long = models.FloatField()
    item_lat = models.FloatField()

    class Meta:
        db_table = "account_items"

    objects = ItemsManager()

class SharedItemsManager(models.Manager):
    def create_shared_items(self, current_company, shared_company, item):
        shared_item = self.create(company_current=current_company, company_shared=shared_company, item=item)
        return shared_item

class SharedItems(models.Model):
    item = models.ForeignKey(Items, on_delete=models.CASCADE, unique=False)
    company_current = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="company_current",
        unique=False,
        db_column="company_current"
    )
    company_shared = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        unique=False,
        related_name="company_shared",
        db_column="company_shared"
    )

    class Meta:
        db_table = "shared_files"

    objects = SharedItemsManager()


class CompanyUserManager(models.Manager):
    def get_company_id(self, company_id, user_id):
        if company_id == company_id and user_id == user_id:
            return company_id
        else:
            return False

    def create_relationship(self, company_id, user_id):
        relationship = self.create(company=company_id, user_id=user_id)
        return relationship



#this creates the relationship
class UserCompanyRelationship(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, unique=False)

    class Meta:
        db_table = "Company_User_Relationship"

    objects = CompanyUserManager()



class SharedItemsManager(models.Manager):
    def create_shared_item(self, item, company_current, company_shared):
        shared_item = self.create(item=item, company_current=company_current, company_shared=company_shared)
        return shared_item


#end items section