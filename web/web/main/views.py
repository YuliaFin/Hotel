from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import RequestForm
from .models import Room, Request, Status, Room_request, occupancy_of_rooms, User, Request_Staffer
from django.contrib import messages
from django.shortcuts import render, redirect
from django.shortcuts import render
from .forms import RoomAvailabilityForm
from datetime import datetime
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from django.shortcuts import get_object_or_404

def index(request):
    return render(request, 'main/index.html')

def how_book(request):
    return render(request, 'main/How_book.html')

def rooms(request):
    rooms = Room.objects.all()
    arrival_date = request.GET.get('arrival_date')
    departure_date = request.GET.get('departure_date')

    if arrival_date and departure_date:
        # Пользователь указал даты заезда и выезда
        occupied_rooms = occupancy_of_rooms.objects.filter(
            date_of_arrival__lte=datetime.strptime(departure_date, '%Y-%m-%d'),
            date_of_departure__gte=datetime.strptime(arrival_date, '%Y-%m-%d')
        )
        rooms = rooms.exclude(id__in=occupied_rooms.values_list('room_id', flat=True))

    return render(request, 'main/rooms.html', {'rooms': rooms})

def about(request):
    return render(request, 'main/about.html')

def profile(request):
    return render(request, 'main/profile.html')

def contacts(request):
    return render(request, 'main/contacts.html')

def check_room_availability(request):
    return render(request, 'main/check_room_availability.html')

@login_required
def booking(request, room_id=None):
    errors = []
    user_login = request.user.user.id
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            date_of_arrival = form.cleaned_data['date_of_arrival']
            date_of_departure = form.cleaned_data['date_of_departure']

            if date_of_arrival >= date_of_departure:
                errors.append('Дата заезда должна быть раньше даты выезда')
            else:
                booking_req = form.save(commit=False)
                booking_req.user_id = user_login
                booking_req.status_id = 1
                booking_req.save()
                room_id = request.POST.get('room')
                room = get_object_or_404(Room, id=room_id)
                form.initial['room'] = room
                room = form.cleaned_data['room']
                r = Room_request(request=booking_req, room=room)
                r.save()
                messages.success(request, 'Заявка успешно отправлена')
                return redirect('index')
        else:
            errors.append('Ошибка в заполнении формы')
    else:
        if room_id:
            room = get_object_or_404(Room, id=room_id)
            initial_data = {'room': room}
            form = RequestForm(initial=initial_data)
        else:
            form = RequestForm()

    context = {'form': form, 'errors': errors}
    return render(request, 'main/booking.html', context)

def staf(request):
    statuses = Status.objects.all()
    req = Request.objects.order_by('status__id')
    rooms = Room.objects.all()

    if request.method == 'POST':
        for el in req:
            status = request.POST.get(str(el.id))

            # Проверяем должность сотрудника
            if request.user.staffer.post_id != 2:
                if status:
                    el.status_id = status
                    el.save()
                    # Создаем запись в модели Request_Staffer
                    Request_Staffer.objects.create(request=el, staffer=request.user.staffer)

        # Обновляем список заявок после сохранения изменений в базу данных
        req = Request.objects.all()

    context = {
        'statuses': statuses,
        'req': req,
        'rooms': rooms
    }

    return render(request, 'main/staf.html', context)


def occupancy_edit(request):
    rooms = Room.objects.all()
    if request.method == 'POST':
        date_of_arrival = request.POST.get('date_of_arrival')
        date_of_departure = request.POST.get('date_of_departure')
        room_id = request.POST.get('room_id')

        # получаем список объектов occupancy_of_rooms для данной комнаты
        occupancies = occupancy_of_rooms.objects.filter(room_id=room_id)

        #если объекта нет, создаем новый
        room = Room.objects.get(id=room_id)
        occupancy = occupancy_of_rooms(room_id=room_id, date_of_arrival=date_of_arrival, date_of_departure=date_of_departure)
        occupancy.save()

        occupancy.date_of_arrival = date_of_arrival
        occupancy.date_of_departure = date_of_departure
        occupancy.save()

    return render(request, 'main/occupancy_of_rooms.html', {'rooms': rooms})


def profile(request):
    user = request.user.user
    user_requests = Request.objects.filter(user=user)
    room_requests = Room_request.objects.filter(request__in=user_requests)
    requests_data = []
    for room_request in room_requests:
        request_data = {
            'date_of_arrival': room_request.request.date_of_arrival,
            'date_of_departure': room_request.request.date_of_departure,
            'main_place': room_request.request.main_place,
            'additional_place': room_request.request.additional_place,
            'status': room_request.request.status,
            'room_number': room_request.room
        }
        requests_data.append(request_data)
    return render(request, 'main/profile.html', {'requests_data': requests_data})

def check_room_availability(request, date_of_arrival=None, date_of_departure=None):
    if request.method == 'POST':
        form = RoomAvailabilityForm(request.POST)
        if form.is_valid():
            room_number = form.cleaned_data['room_number']
            date_of_arrival = form.cleaned_data['date_of_arrival']
            date_of_departure = form.cleaned_data['date_of_departure']
        else:
            room_number = request.POST.get('room_number')
            date_of_arrival = request.POST.get('date_of_arrival')
            date_of_departure = request.POST.get('date_of_departure')
    else:
        form = RoomAvailabilityForm()
        if date_of_arrival and date_of_departure:
            # Устанавливаем значения дат в форме, если они переданы в GET-запросе
            form.fields['date_of_arrival'].initial = datetime.strptime(date_of_arrival, '%Y-%m-%d').date()
            form.fields['date_of_departure'].initial = datetime.strptime(date_of_departure, '%Y-%m-%d').date()
        room_number = request.GET.get('room_number')
        date_of_arrival = request.GET.get('date_of_arrival')
        date_of_departure = request.GET.get('date_of_departure')
    message = None
    if room_number and date_of_arrival and date_of_departure:
        # Проверка занятости комнаты
        try:
            room = Room.objects.get(id=room_number)
        except Room.DoesNotExist:
            message = 'Комната с номером {} не найдена'.format(room_number)
        else:
            occupancy = occupancy_of_rooms.objects.filter(
                room=room,
                date_of_arrival__lte=date_of_departure,
                date_of_departure__gte=date_of_arrival,
            ).first()
            if occupancy:
                message = 'Комната занята в указанные даты'
            else:
                message = 'Комната свободна в указанные даты'
    context = {
        'form': form,
        'message': message,
    }
    return render(request, 'main/check_room_availability.html', context)


def generate_report(response):
    # Получаем данные из базы данных
    rooms = Room.objects.all()
    # Создаем PDF-документ
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="example.pdf"'
    pdfmetrics.registerFont(TTFont('Roboto', 'C:/Users/yulia/Downloads/Roboto-Italic.ttf'))
    # Создаем canvas объект и настраиваем его
    p = canvas.Canvas(response, pagesize=landscape(letter))
    p.setTitle("Отчет по занятости номеров")

    # Устанавливаем шрифт и кодировку
    p.setFont("Roboto", 16)
    # Добавляем заголовок отчета
    p.drawCentredString(400, 720, "Отчет по занятости номеров")

    # Добавляем информацию о заказах
    y = 500
    for room in rooms:
        p.setFont("Roboto", 14)
        p.drawString(100, y, f"Номер комнаты {room.id}")
        occupancies = occupancy_of_rooms.objects.filter(room=room)
        y -= 30
        p.setFont("Roboto", 12)
        p.drawString(100, y, f"Дата заезда")
        p.drawString(200, y, f"Дата выезда")
        p.line(100, y - 3, 700, y - 3)
        y -= 20
        for occup in occupancies:
            if y < 100:
                p.showPage()
                y = 650
                p.setFont("Roboto", 16)
                p.drawCentredString(400, 720, "Отчет по занятости номеров")
                p.setFont("Roboto", 12)
                p.drawString(100, y, f"Номер комнаты {room.id}")
                y -= 30
                p.drawString(100, y, f"Дата заезда")
                p.drawString(200, y, f"Дата выезда")
                p.line(100, y - 3, 700, y - 3)
                y -= 20
            p.setFont("Roboto", 10)
            p.drawString(100, y, f"{occup.date_of_arrival}")
            p.drawString(200, y, f"{occup.date_of_departure}")
            y -= 20
        y -= 30
    # Сохраняем PDF-документ и возвращаем его
    p.showPage()
    p.save()
    return response


def generate_report_1(request):
    # Получаем данные из базы данных и сортируем по возрастанию номера заявки
    requests = Request.objects.order_by('id').all()

    # Остальной код отчета остается без изменений
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="example.pdf"'
    pdfmetrics.registerFont(TTFont('Roboto', 'C:/Users/yulia/Downloads/Roboto-Italic.ttf'))

    # Создаем canvas объект и настраиваем его
    p = canvas.Canvas(response, pagesize=landscape(letter))
    p.setTitle("Отчет о заявках на бронирование")

    # Устанавливаем шрифт и кодировку
    p.setFont("Roboto", 16)
    # Добавляем заголовок отчета
    p.drawCentredString(400, 720, "Отчет о заявках на бронирование")

    # Добавляем информацию о заявках и о том, кто их оформил
    y = 500
    for req in requests:
        if y < 100:
            # Создаем новую страницу, если оставшееся пространство закончилось
            p.showPage()
            # Сбрасываем координаты y и добавляем заголовок на новой странице
            y = 720
            p.setFont("Roboto", 16)
            p.drawCentredString(400, 720, "Отчет о заявках на бронирование")
        p.setFont("Roboto", 14)
        user = User.objects.get(id=req.user.id)
        p.drawString(100, y, f"Заявка {req.id}")
        y -= 20
        p.drawString(100, y, f"Клиент: {user.surname} {user.name} {user.patronymic}")
        y -= 30
        p.setFont("Roboto", 12)
        room_request = Room_request.objects.filter(request=req)
        rooms = []
        for r in room_request:
            room_name = r.room.name_room
            rooms.append(f"{room_name} (№ {r.room.id})")
        p.drawString(100, y, f"Комната: {', '.join(rooms)}")
        p.drawString(100, y - 20, f"Основное место: {req.main_place}")
        p.drawString(300, y - 20, f"Дополнительное место: {req.additional_place}")
        y -= 40
        p.drawString(100, y, f"Дата заезда: {req.date_of_arrival}")
        p.drawString(300, y, f"Дата выезда: {req.date_of_departure}")
        y -= 10
        p.line(100, y - 3, 500, y - 3)
        y -= 40

    # Сохраняем PDF-документ и возвращаем его
    p.showPage()
    p.save()
    return response





