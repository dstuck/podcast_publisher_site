from __future__ import unicode_literals

from django.db import models


class Sermon(models.Model):
    date = models.DateField()
    scripture = models.CharField(max_length=120, default='')
    sermon_title = models.CharField(max_length=120, default='')
    preacher = models.CharField(max_length=120, default='')
    comment = models.TextField(default='')
    description = models.TextField(default='')
    tmp_filename = models.TextField(default='')
    pb_ep_id = models.TextField(default='')
    file_exists = models.NullBooleanField(default=None)
    updated_at = models.DateField(auto_now=True)
    has_ftp_file = models.NullBooleanField(default=None)
    is_published_wordpress = models.BooleanField(default=False)

    def __repr__(self):
        return str(self.description)

    def __unicode__(self):
        file_symbol = ' '
        if self.has_ftp_file is not None:
            file_symbol = 'o' if self.has_ftp_file else 'x'
        return "{} | {:14s} | {:19s} | {:25s}".format(
            file_symbol, self.date.strftime('%b %d, %Y'),
            self.preacher, self.sermon_title
        )

    def pretty_title(self):
        return '{} - {}'.format(
            self.sermon_title, self.date.strftime('%B %d, %Y')
        )

    @classmethod
    def create(cls, **kwargs):
        preacher = kwargs.pop('filename')
        kwargs['preacher'] = preacher
        clean_date = kwargs['date'].strftime('%B %d, %Y')
        verb = 'preaches'
        if '&' in preacher:
            verb = 'preach'
        if 'none' or '.mp3' in preacher:
            description =  'First Congregational Church sermon on {}.'.format(
                clean_date
            )
        description = '{} {} at First Congregational Church on {}.'.format(
            preacher.encode('utf8'), verb, clean_date
        )
        kwargs['description'] = description
        return cls(**kwargs)
