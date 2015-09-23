import re
import uuid
from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField
from django.core.validators import RegexValidator

from .. import common


class OCDIDField(models.CharField):

    def __init__(self, *args, **kwargs):
        self.ocd_type = kwargs.pop('ocd_type')
        if self.ocd_type != 'jurisdiction':
            kwargs['default'] = lambda: 'ocd-{}/{}'.format(self.ocd_type, uuid.uuid4())
            # len('ocd-') + len(ocd_type) + len('/') + len(uuid)
            #       = 4 + len(ocd_type) + 1 + 36
            #       = len(ocd_type) + 41
            kwargs['max_length'] = 41 + len(self.ocd_type)
            regex = '^ocd-' + self.ocd_type + '/[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12}$'
        else:
            kwargs['max_length'] = 300
            regex = common.JURISDICTION_ID_REGEX

        kwargs['primary_key'] = True
        # get pattern property if it exists, otherwise just return the object (hopefully a string)
        msg = 'ID must match ' + getattr(regex, 'pattern', regex)
        kwargs['validators'] = [RegexValidator(regex=regex, message=msg, flags=re.U)]
        super(OCDIDField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(OCDIDField, self).deconstruct()
        if self.ocd_type != 'jurisdiction':
            kwargs.pop('default')
        kwargs.pop('max_length')
        kwargs.pop('primary_key')
        kwargs['ocd_type'] = self.ocd_type
        return (name, path, args, kwargs)


class OCDBase(models.Model):
    """ common base fields across all top-level models """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    extras = JSONField(default=dict, blank=True)
    locked_fields = ArrayField(base_field=models.TextField(), blank=True, default=list)

    class Meta:
        abstract = True


class RelatedBase(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class LinkBase(RelatedBase):
    note = models.CharField(max_length=300, blank=True)
    url = models.URLField(max_length=2000)

    def transfer_links(persistent, obsolete, link_name="links"):
        for l in getattr(obsolete, link_name).all():
            matches = getattr(persistent, link_name).filter(url=l.url)
            for m in matches:
                m.delete()
            getattr(persistent, link_name).add(l)

    class Meta:
        abstract = True


class MimetypeLinkBase(RelatedBase):
    media_type = models.CharField(max_length=100)
    url = models.URLField(max_length=2000)
    text = models.TextField(default='')

    class Meta:
        abstract = True


class IdentifierBase(RelatedBase):
    identifier = models.CharField(max_length=300)
    scheme = models.CharField(max_length=300)

    def transfer_identifiers(persistent, obsolete):
        #pass 2 objects with related identifiers, this will combine them
        for i in obsolete.identifiers.all():
            persistent_matches = persistent.identifiers.filter(identifier=i.identifier,
                                                               scheme=i.scheme)

            if len(persistent_matches) == 0:
                persistent.identifiers.add(i)
            else:
                i.delete()



    class Meta:
        abstract = True


class RelatedEntityBase(RelatedBase):
    name = models.CharField(max_length=2000)
    entity_type = models.CharField(max_length=20, blank=True)

    # optionally tied to an organization or person if it was linkable
    organization = models.ForeignKey('Organization', null=True)
    person = models.ForeignKey('Person', null=True)

    @property
    def entity_name(self):
        if self.entity_type == 'organization' and self.organization_id:
            return self.organization.name
        elif self.entity_type == 'person' and self.person_id:
            return self.person.name
        else:
            return self.name

    @property
    def entity_id(self):
        if self.entity_type == 'organization':
            return self.organization_id
        if self.entity_type == 'person':
            return self.person_id
        return None

    class Meta:
        abstract = True
