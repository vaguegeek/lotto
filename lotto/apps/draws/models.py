from django.db import models

class Draw(models.Model):
    round_number = models.IntegerField(unique=True)
    draw_date = models.DateField()
    is_drawn = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.round_number}회차"

class DrawResult(models.Model):
    draw = models.OneToOneField(
        Draw, on_delete=models.CASCADE,
        related_name='result'
    )
    num1 = models.IntegerField()
    num2 = models.IntegerField()
    num3 = models.IntegerField()
    num4 = models.IntegerField()
    num5 = models.IntegerField()
    num6 = models.IntegerField()
    bonus = models.IntegerField()

    def get_winning_numbers(self):
        return [self.num1, self.num2, self.num3,
                self.num4, self.num5, self.num6]

    def __str__(self):
        return f"{self.draw.round_number}회차 결과"
