# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields
import shuup.utils.analog
import django.db.models.deletion
from django.conf import settings
import enumfields.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shuup', '0016_shop_contact_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='MailchimpContact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='updated')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('sent_to_mailchimp', models.DateTimeField(null=True, verbose_name='sent to mailchimp')),
                ('latest_push_failed', models.NullBooleanField(verbose_name='latest push failed')),
                ('mailchimp_id', models.CharField(max_length=160, null=True, verbose_name='mailchimp id')),
                ('contact', models.ForeignKey(verbose_name='contact', to='shuup.Contact')),
                ('shop', models.ForeignKey(related_name='+', verbose_name='shop', to='shuup.Shop')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MailchimpContactGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='updated')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('sent_to_mailchimp', models.DateTimeField(null=True, verbose_name='sent to mailchimp')),
                ('latest_push_failed', models.NullBooleanField(verbose_name='latest push failed')),
                ('mailchimp_id', models.CharField(max_length=160, null=True, verbose_name='mailchimp id')),
                ('group', models.ForeignKey(verbose_name='contact group', to='shuup.ContactGroup')),
                ('shop', models.ForeignKey(related_name='+', verbose_name='shop', to='shuup.Shop')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MailchimpContactLogEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='created on')),
                ('message', models.CharField(max_length=256, verbose_name='message')),
                ('identifier', models.CharField(max_length=64, verbose_name='identifier', blank=True)),
                ('kind', enumfields.fields.EnumIntegerField(default=0, enum=shuup.utils.analog.LogEntryKind, verbose_name='log entry kind')),
                ('extra', jsonfield.fields.JSONField(null=True, verbose_name='extra data', blank=True)),
                ('target', models.ForeignKey(related_name='log_entries', verbose_name='target', to='shuup_mailchimp.MailchimpContact')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='user', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
