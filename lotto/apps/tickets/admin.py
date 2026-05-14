from django.contrib import admin
from .models import Ticket, TicketNumber

class TicketNumberInline(admin.TabularInline):
    model = TicketNumber
    extra = 0

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['user', 'ticket_type', 'draw', 'purchased_at']
    inlines = [TicketNumberInline]
