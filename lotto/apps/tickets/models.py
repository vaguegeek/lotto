from django.db import models
from django.contrib.auth.models import User

class Ticket(models.Model):
    MANUAL = 'manual'
    AUTO = 'auto'
    TYPE_CHOICES = [(MANUAL, '수동'), (AUTO, '자동')]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticket_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    purchased_at = models.DateTimeField(auto_now_add=True)
    draw = models.ForeignKey(
        'draws.Draw', on_delete=models.SET_NULL,
        null=True, blank=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.purchased_at}"

class TicketNumber(models.Model):
    ticket = models.ForeignKey(
        Ticket, on_delete=models.CASCADE,
        related_name='numbers'
    )
    number = models.IntegerField()

    class Meta:
        ordering = ['number']
