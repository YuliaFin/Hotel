from django.db import models
from django.contrib.auth.models import User as DefaultUser

class Post(models.Model):
    name_post=models.CharField(max_length=32)
    def __str__(self):
        return self.name_post

class Status(models.Model):
    status=models.CharField(max_length=32)
    def __str__(self):
        return self.status

class Type_room(models.Model):
    type=models.CharField(max_length=16)

    def __str__(self):
        return self.type

class User(models.Model):
    user=models.OneToOneField(DefaultUser, on_delete=models.CASCADE)
    login=models.CharField(max_length=32,default='')
    password_user=models.CharField(max_length=256,default='')
    name=models.CharField(max_length=16,default='')
    surname=models.CharField(max_length=32,default='')
    patronymic=models.CharField(max_length=20,default='')
    email=models.CharField(max_length=256,default='')
    phone_number=models.CharField(max_length=17,default='')
    def __str__(self):
        return self.login

class Staffer(models.Model):
    user = models.OneToOneField(DefaultUser, on_delete=models.CASCADE)
    login = models.CharField(max_length=32)
    password_user = models.CharField(max_length=32)
    name = models.CharField(max_length=16)
    surname = models.CharField(max_length=32)
    patronymic = models.CharField(max_length=20)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    def __str__(self):
        return self.login

class Request(models.Model):
    main_place=models.IntegerField()
    additional_place=models.IntegerField()
    date_of_arrival=models.DateField()
    date_of_departure=models.DateField()
    status=models.ForeignKey('Status', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)


class Request_Staffer(models.Model):
    request=models.ForeignKey('Request', on_delete=models.CASCADE)
    staffer=models.ForeignKey('Staffer', on_delete=models.CASCADE)

class Room(models.Model):
    description=models.TextField(blank=True)
    name_room=models.CharField(max_length=64)
    type_room = models.ForeignKey('Type_room', on_delete=models.CASCADE)
    def __str__(self):
        return f'Комната: {self.name_room} | Тип: {self.type_room.type}'

    def is_available(self, date_of_arrival, date_of_departure):
        # Проверяем, есть ли бронирования для номера в указанный период
        bookings = occupancy_of_rooms.objects.filter(
            room=self,
            date_of_arrival__lte=date_of_departure,
            date_of_departure__gte=date_of_arrival,
        )
        return not bookings.exists()

class occupancy_of_rooms(models.Model):
    date_of_arrival = models.DateField()
    date_of_departure = models.DateField()
    room = models.ForeignKey('Room', on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.room} | Даты занятости номера: {self.date_of_arrival} - {self.date_of_departure}'

class Room_request(models.Model):
    request = models.ForeignKey('Request', on_delete=models.CASCADE)
    room = models.ForeignKey('Room', on_delete=models.CASCADE)
    def save(self, *args, **kwargs):
        super(Room_request, self).save(*args, **kwargs)

class Room_price(models.Model):
    room = models.ForeignKey('Room', on_delete=models.CASCADE, related_name='prices')
    additional_place = models.BooleanField()
    price = models.DecimalField(max_digits=8,decimal_places=2)
