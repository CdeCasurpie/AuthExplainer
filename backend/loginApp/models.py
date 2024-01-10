from django.db import models
from uuid import uuid4

# USER MODEL
class User(models.Model):
    #id (uuid4), username(text), password(text), email(mail or text)

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=256)
    email = models.EmailField(max_length=254)

    def __str__(self):
        return "{} - {}".format(self.username, self.email)