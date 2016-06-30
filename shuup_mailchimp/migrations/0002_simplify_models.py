# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shuup_mailchimp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mailchimpcontactgroup',
            name='group',
        ),
        migrations.RemoveField(
            model_name='mailchimpcontactgroup',
            name='shop',
        ),
        migrations.RemoveField(
            model_name='mailchimpcontact',
            name='contact',
        ),
        migrations.RemoveField(
            model_name='mailchimpcontact',
            name='latest_push_failed',
        ),
        migrations.RemoveField(
            model_name='mailchimpcontact',
            name='mailchimp_id',
        ),
        migrations.AddField(
            model_name='mailchimpcontact',
            name='email',
            field=models.EmailField(default='', max_length=256, verbose_name='email'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='MailchimpContactGroup',
        ),
    ]
