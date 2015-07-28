# coding=utf-8

from django.db import models, transaction, IntegrityError
from django.db.models.signals import post_delete
from django.dispatch import receiver

class Order(models.Model):
  pass

class Item(models.Model):
  order = models.ForeignKey(Order, related_name="items")

class LogEntry(models.Model):
  order = models.ForeignKey(Order, related_name="log_entries")

@receiver(post_delete, sender=Item)
@transaction.atomic
def on_item_post_delete(instance, **kwargs):
  print("Item deleted: #%d" % instance.pk)

  # At this point, there's no way for checking if "instance.order" is valid or
  # not. Constraint violations will be deferred until the end of the
  # transaction.

  order = Order.objects.get(pk=instance.order_id)

  try:
    with transaction.atomic(savepoint=True):
      LogEntry(order=instance.order).save()
  except IntegrityError:
    pass

  # Possible "quick" solutions:
  # 1) Set order.pk to None before firing post_delete.
  # 2) Make accessing instance.order raise an exception -- this does actually
  #    happen when using the SQLite3 adapter.
