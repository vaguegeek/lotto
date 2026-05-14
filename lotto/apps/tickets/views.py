import random
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Ticket, TicketNumber
from apps.draws.models import Draw

def index(request):
    latest_draw = Draw.objects.filter(is_drawn=True).order_by('-round_number').first()
    upcoming_draw = Draw.objects.filter(is_drawn=False).order_by('round_number').first()
    return render(request, 'tickets/index.html', {
        'latest_draw': latest_draw,
        'upcoming_draw': upcoming_draw,
    })

@login_required
def buy_ticket(request):
    upcoming_draw = Draw.objects.filter(is_drawn=False).order_by('round_number').first()
    if not upcoming_draw:
        messages.error(request, '현재 구매 가능한 회차가 없어요.')
        return redirect('tickets:index')

    if request.method == 'POST':
        ticket_type = request.POST.get('ticket_type')
        ticket = Ticket.objects.create(
            user=request.user,
            ticket_type=ticket_type,
            draw=upcoming_draw,
        )

        if ticket_type == 'auto':
            numbers = random.sample(range(1, 46), 6)
        else:
            numbers = [
                int(request.POST.get(f'num{i}'))
                for i in range(1, 7)
            ]
            if len(set(numbers)) != 6 or not all(1 <= n <= 45 for n in numbers):
                ticket.delete()
                messages.error(request, '번호를 올바르게 입력해주세요. (1~45, 중복 없이 6개)')
                return redirect('tickets:buy')

        for num in numbers:
            TicketNumber.objects.create(ticket=ticket, number=num)

        messages.success(request, f'복권 구매 완료! 번호: {sorted(numbers)}')
        return redirect('tickets:my_tickets')

    return render(request, 'tickets/buy.html', {'upcoming_draw': upcoming_draw})

@login_required
def my_tickets(request):
    tickets = Ticket.objects.filter(user=request.user).order_by('-purchased_at')
    ticket_data = []
    for ticket in tickets:
        numbers = list(ticket.numbers.values_list('number', flat=True))
        result = None
        if ticket.draw and ticket.draw.is_drawn:
            draw_result = ticket.draw.result
            winning = draw_result.get_winning_numbers()
            bonus = draw_result.bonus
            matched = len(set(numbers) & set(winning))
            has_bonus = bonus in numbers

            if matched == 6:
                result = '1등'
            elif matched == 5 and has_bonus:
                result = '2등'
            elif matched == 5:
                result = '3등'
            elif matched == 4:
                result = '4등'
            elif matched == 3:
                result = '5등'
            else:
                result = '낙첨'

        ticket_data.append({
            'ticket': ticket,
            'numbers': numbers,
            'result': result,
        })

    return render(request, 'tickets/my_tickets.html', {'ticket_data': ticket_data})
