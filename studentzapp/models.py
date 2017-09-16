from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.db.models.signals import post_save
from django.db import models
from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from django.contrib.auth import get_user_model


from django.db.models.signals import post_save
from django.db import models
from rest_framework.authtoken.models import Token
from django.dispatch import receiver




class AccountManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have a valid email address.')

        account = self.model()

   
        account.save()

        return account





class Account(AbstractBaseUser):
    email = models.EmailField(blank=True)
    displayname = models.CharField(max_length=40, blank=True)
    accesstoken = models.CharField(max_length=750)
    fbid = models.CharField(max_length=140, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AccountManager()

    USERNAME_FIELD = 'fbid'
    
    def __unicode__(self):
        return self.email





class BlogPost(models.Model):
    """This class represents the blogpost model."""
    title = models.CharField(max_length=255, blank=False,default="")
    content = models.TextField(blank=False,default="")
    owner = models.ForeignKey(get_user_model(),related_name='blogposts',on_delete=models.CASCADE)
    likescount = models.IntegerField(default=0)
    likes = models.ManyToManyField('Like',blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    objects=models.Manager

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.name)


class Like(models.Model):
    """This class represents the blogpost model."""
    postid = models.IntegerField()
    post = models.ForeignKey(BlogPost,null=True)
    user = models.ForeignKey(get_user_model(),default=1)
    ownername = models.ForeignKey(get_user_model(),related_name='owname',on_delete=models.CASCADE, default=1)
    ownerfbid = models.ForeignKey(get_user_model(),related_name='likess',on_delete=models.CASCADE)
    isliked = models.BooleanField(default=False)

@receiver(post_save, sender=get_user_model())
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        token=Token.objects.create(user=instance)
        print ("token="+token.key)