from django.contrib import admin
from .models import Draw, DrawResult

@admin.register(Draw)
class DrawAdmin(admin.ModelAdmin):
    list_display = ['round_number', 'draw_date', 'is_drawn']

@admin.register(DrawResult)
class DrawResultAdmin(admin.ModelAdmin):
    list_display = ['draw', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6', 'bonus']
