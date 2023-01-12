from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from core.models import TimeStampedModel

class User(AbstractUser):
    """
    Default custom user model for plant_observe.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """

        return reverse("users:detail", kwargs={"username": self.username})

class Flavor(TimeStampedModel):
    title = models.CharField(max_length=200)

# Create your models here.
# 게시글(Post)엔 제목(title), 내용(contents)이 존재합니다
class Post(models.Model):
    title = models.CharField(max_length=50)
    mainphoto = models.ImageField(blank=True, null=True)
    contents = models.TextField()

    # 게시글의 제목(title)이 Post object 대신하기
    def __str__(self):
        return "[{}] {}".format(self.id, self.title)
