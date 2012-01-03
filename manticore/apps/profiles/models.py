import requests
import simplejson

from django.db import models
from django.core.files.base import File
from django.utils.translation import ugettext_lazy as _
from StringIO import StringIO

from idios.models import ProfileBase
from imagekit.models import ImageSpec
from imagekit.processors import resize, Adjust


class Profile(ProfileBase):
    name = models.CharField(_("name"), max_length=50, null=True, blank=True)
    about = models.TextField(_("about"), null=True, blank=True)
    location = models.CharField(_("location"), max_length=40, null=True, blank=True)
    website = models.URLField(_("website"), null=True, blank=True, verify_exists=False)
    avatar = models.ImageField(upload_to='avatars', null=True, blank=True)

    avatar_normal = ImageSpec(
        [
            Adjust(contrast=1.2, sharpness=1.1),
            resize.Crop(50, 50)
        ],
        image_field='avatar',
        format='JPEG',
        quality=80,
    )
    avatar_small = ImageSpec(
        [
            Adjust(contrast=1.2, sharpness=1.1),
            resize.Crop(30, 30)
        ],
        image_field='avatar',
        format='JPEG',
        quality=80,
    )

    def fetch_avatar(self):
        """Fetches avatar from Twitter.
        """
        for auth in self.user.social_auth.all():
            if auth.provider == 'twitter':
                try:
                    profile_url = 'http://api.twitter.com/1/users/lookup.json?user_id={id}&include_entities=true'.format(
                        **auth.extra_data
                    )
                    response = requests.get(profile_url, timeout=3)
                    data = simplejson.loads(response.content)
                    username = data[0]['screen_name']
                    avatar_url = 'http://api.twitter.com/1/users/profile_image?screen_name={username}&size=original'.format(
                        username=username
                    )
                    response = requests.get(avatar_url, timeout=3)
                    fake_file = StringIO(response.content)
                    fake_file.size = len(response.content)
                    self.avatar = File(
                        fake_file,
                        name=username,
                    )
                    self.save()
                    break
                except Exception:
                    raise
