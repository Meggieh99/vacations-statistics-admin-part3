from django.db import models

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        managed = False
        db_table = "vacations_role"

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True, null=False, blank=False)
    password = models.CharField(max_length=128)
    role = models.ForeignKey(Role, on_delete=models.PROTECT)
    is_staff = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = "vacations_user"

class Country(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False, blank=False)

    class Meta:
        managed = False
        db_table = "vacations_country"

class Vacation(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image_filename = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "vacations_vacation"

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vacation = models.ForeignKey(Vacation, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = "vacations_like"
        unique_together = ('user', 'vacation')
