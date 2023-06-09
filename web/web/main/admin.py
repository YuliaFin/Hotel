from django.contrib import admin
from .models import Post, Request, Request_Staffer, Room, Room_request, Staffer,Status, Type_room, User, occupancy_of_rooms, Room_price

admin.site.register(Post)
admin.site.register(Request)
admin.site.register(Request_Staffer)
admin.site.register(Room)
admin.site.register(Room_request)
admin.site.register(Staffer)
admin.site.register(Status)
admin.site.register(Type_room)
admin.site.register(User)
admin.site.register(occupancy_of_rooms)
admin.site.register(Room_price)
