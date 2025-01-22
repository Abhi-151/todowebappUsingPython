# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AdminLoginAnalytics(models.Model):
    auto_id = models.AutoField(primary_key=True)
    admin = models.ForeignKey('TblAdmin', models.DO_NOTHING)
    login_time = models.DateTimeField(blank=True, null=True)
    ip_address = models.CharField(max_length=45, blank=True, null=True)
    login_status = models.IntegerField(blank=True, null=True)
    failed_attempts = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    login_token = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'admin_login_analytics'


class Tasks(models.Model):
    autoid = models.AutoField(db_column='autoId', primary_key=True)  # Field name made lowercase.
    task_name = models.CharField(max_length=255)
    is_completed = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tasks'


class TblAdmin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(unique=True, max_length=100)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_admin'
