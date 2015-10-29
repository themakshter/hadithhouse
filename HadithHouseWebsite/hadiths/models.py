from django.db import models


class Person(models.Model):
  """A model describing a person."""
  title = models.CharField(max_length=16)
  display_name = models.CharField(max_length=48)
  full_name = models.CharField(max_length=128)
  ref = models.CharField(max_length=32, null=True, blank=True, unique=True)
  brief_desc = models.CharField(max_length=256)
  # We don't use DateField because it doesn't allow us to keep null
  # some parts of the date if they are unknown.
  birth_year = models.SmallIntegerField(null=True, blank=True)
  birth_month = models.SmallIntegerField(null=True, blank=True)
  birth_day = models.SmallIntegerField(null=True, blank=True)
  death_year = models.SmallIntegerField(null=True, blank=True)
  death_month = models.SmallIntegerField(null=True, blank=True)
  death_day = models.SmallIntegerField(null=True, blank=True)
  added_on = models.DateTimeField(auto_now=False, auto_now_add=True)
  updated_on = models.DateTimeField(auto_now=True, auto_now_add=True)

  def __unicode__(self):
    return self.display_name or self.full_name


class HadithTag(models.Model):
  """A model describing a tag for hadiths."""
  name = models.CharField(max_length=32, unique=True)
  added_on = models.DateTimeField(auto_now=False, auto_now_add=True)
  updated_on = models.DateTimeField(auto_now=True, auto_now_add=True)

  def __unicode__(self):
    return self.name


class Hadith(models.Model):
  """A model describing a hadith."""
  text = models.TextField()
  person = models.ForeignKey(Person)
  tags = models.ManyToManyField(HadithTag)
  added_on = models.DateTimeField(auto_now=False, auto_now_add=True)
  updated_on = models.DateTimeField(auto_now=True, auto_now_add=True)

  def __unicode__(self):
    return self.text[:100] + '...' if len(self.text) > 100 else self.text


class Chain(models.Model):
  hadith = models.ForeignKey(Hadith)


class ChainLink(models.Model):
  chain = models.ForeignKey(Chain)
  person = models.ForeignKey(Person)
  order = models.SmallIntegerField(null=False, blank=False)


# TODO: Move this to a better place.
PERMISSION_CAN_ADD_HADITH = 1 << 0
PERMISSION_CAN_EDIT_HADITH = 1 << 1
PERMISSION_CAN_DELETE_HADITH = 1 << 2
PERMISSION_CAN_ADD_PERSON = 1 << 3
PERMISSION_CAN_EDIT_PERSON = 1 << 4
PERMISSION_CAN_DELETE_PERSON = 1 << 5
PERMISSION_CAN_ADD_TAG = 1 << 6
PERMISSION_CAN_EDIT_TAG = 1 << 7
PERMISSION_CAN_DELETE_TAG = 1 << 8
PERMISSION_CAN_APPROVE_UNAPPROVED_DATA = 1 << 9
PERMISSION_CAN_UNAPPROVE_APPROVED_DATA = 1 << 10


class User(models.Model):
  fb_id = models.BigIntegerField(unique=True, db_index=True)
  permissions = models.BigIntegerField()

  def set_permission(self, permission):
    self.permissions |= permission

  def clear_permission(self, permission):
    self.permissions &= ~permission

  def can_add_hadith(self):
    return (self.permissions & PERMISSION_CAN_ADD_HADITH) != 0

  def can_edit_hadith(self):
    return (self.permissions & PERMISSION_CAN_EDIT_HADITH) != 0

  def can_delete_hadith(self):
    return (self.permissions & PERMISSION_CAN_DELETE_HADITH) != 0

  def can_add_person(self):
    return (self.permissions & PERMISSION_CAN_ADD_PERSON) != 0

  def can_edit_person(self):
    return (self.permissions & PERMISSION_CAN_EDIT_PERSON) != 0

  def can_delete_person(self):
    return (self.permissions & PERMISSION_CAN_DELETE_PERSON) != 0

  def can_add_tag(self):
    return (self.permissions & PERMISSION_CAN_ADD_TAG) != 0

  def can_edit_tag(self):
    return (self.permissions & PERMISSION_CAN_EDIT_TAG) != 0

  def can_delete_tag(self):
    return (self.permissions & PERMISSION_CAN_DELETE_TAG) != 0

  def can_approve_unapproved_data(self):
    return (self.permissions & PERMISSION_CAN_APPROVE_UNAPPROVED_DATA) != 0

  def can_unapprove_approved_data(self):
    return (self.permissions & PERMISSION_CAN_UNAPPROVE_APPROVED_DATA) != 0

