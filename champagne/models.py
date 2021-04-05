from django.conf import settings
from django.db import models
from django.utils import timezone

# Create your models here.

User = settings.AUTH_USER_MODEL


class ChampagneBlogPostManagerQuerySet(models.QuerySet):
    def published(self):
        now = timezone.now()
        return self.filter(publish_date__lte=now)


class ChampagneBlogPostManager(models.Manager):
    def get_query_set(self):
        return ChampagneBlogPostManagerQuerySet(self.model, using=self._db)
    

class ChampagneBlogPost(models.Model):  # champagneblogpost_set -> qs
    user = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    content = models.TextField(null=True, blank=True)
    publish_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # objects = ChampagneBlogPostManager()
    
    class Meta:
        ordering = ['-publish_date', '-updated', '-timestamp']
    
    def get_absolute_url(self):
        return f"/blog/{self.slug}"

    def get_edit_url(self):
        return f"/blog/{self.slug}/edit"

    def get_delete_url(self):
        return f"/blog/{self.slug}/delete"
