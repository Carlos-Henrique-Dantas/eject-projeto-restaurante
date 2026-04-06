from django.urls import path
from .views import ReservaCreateView, ReservaListView, ReservaCancelView, ReservaDeleteView

urlpatterns = [
    path('reservas/nova/', ReservaCreateView.as_view(), name='nova_reserva'),
    path('reservas/', ReservaListView.as_view(), name='minhas_reservas'),
    path('reservas/<int:pk>/cancelar/', ReservaCancelView.as_view(), name='cancelar_reserva'),
    path('reservas/<int:pk>/deletar/', ReservaDeleteView.as_view(), name='deletar_reserva'),
]