# MeetBooking
Система бронирования переговорок.

## Issues
1. Переименовать модуль MeetBooking в meet_booking.
2. Необходимо полная докеризация приложения, начало положено, но нехватает контейнера с приложением в compouse файле.
3. Не совсем понял как файл .env преобразуется в переменные окружения. Так же не понял каким образом env в компоуз 
   пробрасывается.
4. Для чего нужен модуль accoutn_user?
5. booking/api_views - обычно api выделяют либо в отдельный модуль, либо делают сабмодуль api и все держат там, 
   что к нему относится. Да и само именование файлов с вью сомнительно.    
6. booking.mixins.SerializerMixin - слишком общее имя, оно не отражает назначение миксина.
7. booking.api_views.cabinet_view_set.CabinetViewSet.get_object - а тут можно было бы использовать метод get_object_or_404
8. booking/templates/email_message/owner_message.html - а css тут намеренно вшит в шаблон? или просто было лень разносить?
9. booking/tasks.py:47 мне кажется нет смысла предупреждать создателя отдельно. По факту он такой же участник.
10. booking.tests.create_test_event - попытка начать писать тесты это хорошо, но сначала неплохо бы почитать как это 
    правильно делать в Django https://docs.djangoproject.com/en/3.2/intro/tutorial05/