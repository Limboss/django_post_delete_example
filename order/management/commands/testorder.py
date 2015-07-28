# coding=utf-8

from order.models import Order, Item, LogEntry

from django.core.management.base import BaseCommand
from django.db import transaction

class Command(BaseCommand):
  @transaction.atomic
  def handle(self, *args, **kwargs):
    print("Wiping tables")
    Order.objects.all().delete()
    Item.objects.all().delete()
    LogEntry.objects.all().delete()

    print("****************************************")
    print("Starting test")
    Order(pk=1).save()
    Item(pk=1, order_id=1).save()
    Item(pk=2, order_id=1).save()
    Item(pk=3, order_id=1).save()

    Item.objects.get(pk=1).delete()

    print("!!!!!!!!!!!!!!!!!!")
    print("Now deleting whole order")
    Order.objects.get(pk=1).delete()
