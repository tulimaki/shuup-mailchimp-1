# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def remove_duplicates(apps, schema_editor):
    if not schema_editor.connection.alias == 'default':
        return

    already_in_table = set()
    MailchimpContact = apps.get_model('shuup_mailchimp', 'MailchimpContact')
    for contact in MailchimpContact.objects.all():
        email = contact.email
        if email in already_in_table:
            contact.delete()
        else:
            already_in_table.add(email)


class Migration(migrations.Migration):

    dependencies = [
        ('shuup', '0019_contact_merchant_notes'),
        ('shuup_mailchimp', '0002_simplify_models'),
    ]

    operations = [
        migrations.RunPython(remove_duplicates, reverse_code=migrations.RunPython.noop),
        migrations.AlterField(
            model_name='mailchimpcontact',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='email'),

        ),
        migrations.AddField(
            model_name='mailchimpcontact',
            name='contact',
            field=models.ForeignKey(related_name='+', verbose_name='contact', blank=True, to='shuup.Contact', null=True),
        ),

    ]
