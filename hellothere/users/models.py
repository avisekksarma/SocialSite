from django.db import models

# Create your models here.
class EmailCodeConfirmation(models.Model):
    email = models.EmailField(max_length=50)
    code = models.IntegerField()

    def __str__(self):
        return f'Email-{self.email}, code-{self.code}'

class PasswordReset(models.Model):
    email = models.EmailField(max_length=50)
    code = models.IntegerField()

    def __str__(self):
        return f'Email - {self.email}, code- {self.code}'