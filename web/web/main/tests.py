import unittest
from unittest import mock
from django.test import RequestFactory
from django.contrib.auth.models import User
from .views import staf

class StafTestCase(unittest.TestCase):
    def setUp(self):
        self.factory = RequestFactory()# создается экземпляр RequestFactory, который будет использоваться для создания запросов

    def test_staf(self): # Этот метод является тестовым методом, который проверяет поведение функции staf() в определенных условиях
        # Создание поддельного пользователя
        user = mock.Mock(spec=User) # создает поддельный объект, который имеет те же атрибуты и методы, что и класс User
        user.staffer.post_id = 1  # Предположим, что должность с ID=1 не требует проверки должности сотрудника

        # Создание запроса с указанием метода POST и данных формы
        request = self.factory.post('/staf/', {'param1': 'value1', 'param2': 'value2'})
        #Здесь используется экземпляр RequestFactory для создания запроса с заданными параметрами
        request.user = user # Затем атрибут user запроса устанавливается равным созданному поддельному пользователю

        # Вызов функции staf() с эмулированными объектами

        '''
        mock.patch() позволяет временно заменить указанный объект или атрибут во время выполнения блока кода. 
        В данном случае, мы заменяем вызовы Status.objects.all(), Request.objects.order_by() и Room.objects.all() 
        эмулированными объектами, чтобы предотвратить взаимодействие с базой данных при выполнении теста
        '''
        with mock.patch('main.views.Status.objects.all'):
            with mock.patch('main.views.Request.objects.order_by'):
                with mock.patch('main.views.Room.objects.all'):
                    response = staf(request)

        # Проверка ожидаемого результата
        self.assertEqual(response.status_code, 200)


class StafTestCase(unittest.TestCase):
    def setUp(self):
        self.factory = RequestFactory()# создается экземпляр RequestFactory, который будет использоваться для создания запросов

    def test_staf(self): # Этот метод является тестовым методом, который проверяет поведение функции staf() в определенных условиях
        # Создание поддельного пользователя
        user = mock.Mock(spec=User) # создает поддельный объект, который имеет те же атрибуты и методы, что и класс User
        user.staffer.post_id = 1  # Предположим, что должность с ID=1 не требует проверки должности сотрудника

        # Создание запроса с указанием метода POST и данных формы
        request = self.factory.post('/staf/', {'param1': 'value1', 'param2': 'value2'})
        #Здесь используется экземпляр RequestFactory для создания запроса с заданными параметрами
        request.user = user # Затем атрибут user запроса устанавливается равным созданному поддельному пользователю

        # Вызов функции staf() с эмулированными объектами

        '''
        mock.patch() позволяет временно заменить указанный объект или атрибут во время выполнения блока кода. 
        В данном случае, мы заменяем вызовы Status.objects.all(), Request.objects.order_by() и Room.objects.all() 
        эмулированными объектами, чтобы предотвратить взаимодействие с базой данных при выполнении теста
        '''
        with mock.patch('main.views.Status.objects.all'):
            with mock.patch('main.views.Request.objects.order_by'):
                with mock.patch('main.views.Room.objects.all'):
                    response = staf(request)

        # Проверка ожидаемого результата
        self.assertEqual(response.status_code, 200)
