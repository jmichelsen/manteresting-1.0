from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ImageSpec
from imagekit.processors import resize, Adjust


class Category(models.Model):
    title = models.CharField(max_length=100)

    def __unicode__(self):
        return self.title


class Workbench(models.Model):
    user = models.ForeignKey(User, related_name='workbenches')
    title = models.CharField(max_length=100)
    category = models.ForeignKey(Category, related_name='workbenches')

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('workbench', [], dict(pk=self.id))


class Nail(models.Model):
    workbench = models.ForeignKey(Workbench, related_name='nails')
    original = models.ImageField(upload_to='nails')
    normal = ImageSpec(
        [
            resize.Fit(600, 600)
        ],
        image_field='original',
        format='JPEG',
        quality=80,
    )
    small = ImageSpec(
        [
            resize.Fit(200, 400)
        ],
        image_field='original',
        format='JPEG',
        quality=80,
    )
    thumb = ImageSpec(
        [
            Adjust(contrast=1.2, sharpness=1.1),
            resize.Crop(60, 60)
        ],
        image_field='original',
        format='JPEG',
        quality=90,
    )
    description = models.TextField(max_length=500)
    cloned_from = models.ForeignKey('Nail', blank=True, null=True, related_name='clones')


    @models.permalink
    def get_absolute_url(self):
        return ('nail', [], dict(pk=self.id))

