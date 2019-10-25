from django.db import models


from django.db import models


def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2: 
            # letters only as well
            errors['first_name'] = "First name must be at least 2 characters."
        if hasNumbers(postData['first_name']):
            errors['first_name_letters_only'] = "LETTERS ONLY!"
        if len(postData['last_name']) < 2:
            # letters only as well
            errors['last_name'] = "Last name must be at least 2 characters."
        if hasNumbers(postData['last_name']):
            errors['last_name_letters_only'] = "LETTERS ONLY!"
        if postData['email'] == "":
            errors['email'] = "Email is required"
        if User.objects.filter(email=postData['email']):
            errors['email_exists'] = "Email already exists."
        if len(postData['password']) < 8 or postData['password'] == "" or postData['password'] != postData['password_confirmation']:
            errors['password'] = "Password is required.  Please make sure it is at least 8 characters and matches with your password confirmation."
        return errors
    

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=69)
    email = models.EmailField()
    password = models.CharField(max_length=50)
    team_name = models.CharField(max_length=69)
    W = models.IntegerField()
    L = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class Player(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gsis_id = models.CharField(max_length=200)
    position = models.CharField(max_length=3)
    total_points = models.DecimalField(max_digits=5, decimal_places=2)
    user = models.ForeignKey(User, related_name="players")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TWeek(models.Model):
    total_score = models.DecimalField(max_digits=5, decimal_places=2)
    W = models.BooleanField()
    QB_score = models.DecimalField(max_digits=5, decimal_places=2)
    RB1_score = models.DecimalField(max_digits=5, decimal_places=2)
    RB2_score = models.DecimalField(max_digits=5, decimal_places=2)
    WR1_score = models.DecimalField(max_digits=5, decimal_places=2)
    WR2_score = models.DecimalField(max_digits=5, decimal_places=2)
    WR3_score = models.DecimalField(max_digits=5, decimal_places=2)
    TE_score = models.DecimalField(max_digits=5, decimal_places=2)
    record = models.CharField(max_length=30)
    user = models.ForeignKey(User, related_name="weeks")
    week = models.IntegerField()

class PWeek(models.Model):
    points = models.DecimalField(max_digits=5, decimal_places=2)
    passing_yards = models.IntegerField()
    rushing_yards = models.IntegerField()
    receiving_yards = models.IntegerField()
    passing_tds = models.IntegerField()
    rushing_tds = models.IntegerField()
    receiving_tds = models.IntegerField()
    receptions = models.IntegerField()
    player = models.ForeignKey(Player, related_name="weeks")
    week = models.IntegerField()



# Create your models here.
