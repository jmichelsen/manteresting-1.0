import datetime

from django.db import models, transaction, IntegrityError
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from imagekit.models import ImageSpec
from imagekit.processors import resize, Adjust
from follow import utils
from follow.signals import followed, unfollowed


class Category(models.Model):
    title = models.CharField(max_length=100)

    def __unicode__(self):
        return self.title


class Workbench(models.Model):
    user = models.ForeignKey(User, related_name='workbenches')
    title = models.CharField(max_length=100)
    category = models.ForeignKey(Category, related_name='workbenches')
    timestamp = models.DateTimeField(blank=True)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        # this method used to store UTC time in the database,
        # because Django's auto_now=True saves local time and
        # this behavior is wrong.

        if self.timestamp is None:
            self.timestamp = datetime.datetime.utcnow()
        return super(Workbench, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('workbench', [], dict(pk=self.id))


class Nail(models.Model):
    user = models.ForeignKey(User, related_name='nails')
    workbench = models.ForeignKey(Workbench, related_name='nails')
    original = models.ImageField(upload_to='nails')
    normal = ImageSpec(
        [
            resize.Fit(600, 1200)
        ],
        image_field='original',
        format='JPEG',
        quality=80,
    )
    small = ImageSpec(
        [
            resize.Fit(250, 500)
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
    cloned_from = models.ForeignKey('Nail', blank=True, null=True, related_name='clones', on_delete=models.SET_NULL)
    source_url = models.URLField(blank=True, null=True)
    source_title = models.CharField(max_length=128, blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, db_index=True)

    def save(self, *args, **kwargs):
        if self.timestamp is None:
            self.timestamp = datetime.datetime.utcnow()
        return super(Nail, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('nail', [], dict(pk=self.id))


class FriendFeed(models.Model):
    """A feed of nails by followed users and followed workbenches.

    Used to aggregate all new nails from whom you follow. This will be relatively
    easy to update this feed asynchronously on signals and to scale it up
    if neccessary.
    """

    user = models.ForeignKey(User, related_name='friendfeed')
    nail = models.ForeignKey(Nail, related_name='friendfeed', unique=True)
    timestamp = models.DateTimeField(db_index=True)

    def save(self, *args, **kwargs):
        if self.timestamp is None:
            self.timestamp = datetime.datetime.utcnow()
        return super(FriendFeed, self).save(*args, **kwargs)

    @staticmethod
    @transaction.commit_on_success
    def rebuild_for(user):
        FriendFeed.objects.filter(user=user).delete()
        for item in user.following.all():
            query = item.target.nails.all().order_by('-timestamp')
            FriendFeed.populate_user_feed(user, query)

    @staticmethod
    @transaction.commit_on_success
    def populate_user_feed(user, query):
        """Add's nails from query to user's friendfeed.
        """
        for nail in query:
            try:
                FriendFeed.objects.create(
                    user=user, nail=nail, timestamp=nail.timestamp
                )
            except IntegrityError:
                # just ignore dupes
                pass

utils.register(User)
utils.register(Workbench)


@receiver(post_save, sender=Nail)
def nail_saved(sender, instance=None, created=None, **kwargs):
    if not created:
        # remove nail from old friendfeeds
        instance.friendfeed.all().delete()

    query = [instance]

    # for each follower of the workbench, add this nail to a friendfeed
    for follow in instance.workbench.get_follows():
        FriendFeed.populate_user_feed(follow.user, query)

    # for each author's follower, add this nail to his friendfeed
    for follow in instance.user.get_follows():
        FriendFeed.populate_user_feed(follow.user, query)


@receiver(followed, sender=Workbench)
@receiver(followed, sender=User)
def workbench_or_user_followed(user, target, instance, **kwargs):
    """Add all nails from that workbench to user's friendfeed.
    """
    FriendFeed.populate_user_feed(user, target.nails.all())


@receiver(unfollowed, sender=Workbench)
@receiver(unfollowed, sender=User)
def workbench_or_user_unfollowed(user, target, instance, **kwargs):
    """Add all nails from that workbench to user's friendfeed.
    """
    FriendFeed.objects.filter(user=user, nail__in=target.nails.all()).delete()

