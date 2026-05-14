import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from .models import Draw, DrawResult

def draw_list(request):
    draws = Draw.objects.order_by('-round_number')
    return render(request, 'draws/list.html', {'draws': draws})

def draw_detail(request, round_number):
    draw = get_object_or_404(Draw, round_number=round_number)
    result = getattr(draw, 'result', None)
    return render(request, 'draws/detail.html', {
        'draw': draw,
        'result': result,
    })

@staff_member_required
def do_draw(request, round_number):
    draw = get_object_or_404(Draw, round_number=round_number)
    if draw.is_drawn:
        return redirect('draws:detail', round_number=round_number)

    if request.method == 'POST':
        numbers = random.sample(range(1, 46), 7)
        winning = sorted(numbers[:6])
        bonus = numbers[6]

        DrawResult.objects.create(
            draw=draw,
            num1=winning[0], num2=winning[1], num3=winning[2],
            num4=winning[3], num5=winning[4], num6=winning[5],
            bonus=bonus,
        )
        draw.is_drawn = True
        draw.save()
        return redirect('draws:detail', round_number=round_number)

    return render(request, 'draws/do_draw.html', {'draw': draw})
