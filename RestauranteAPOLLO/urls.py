from django.urls import path
from .views import ReservaCreateView, ReservaListView, ReservaCancelView, ReservaDeleteView
from . import views
from .views import PostListView, PostDetailView

urlpatterns = [
    path('reservas/nova/', ReservaCreateView.as_view(), name='nova_reserva'),
    path('reservas/', ReservaListView.as_view(), name='minhas_reservas'),
    path('reservas/<int:pk>/cancelar/', ReservaCancelView.as_view(), name='cancelar_reserva'),
    path('reservas/<int:pk>/deletar/', ReservaDeleteView.as_view(), name='deletar_reserva'),
    
    # Caminho da página inicial
    path('', views.home, name='home'),
    path('blog/', PostListView.as_view(), name='blog'),
    path('sobre-nos/', views.Sobre_nos, name='sobre_nos'),
    path('blog/<int:pk>/', PostDetailView.as_view(), name='post_detalhe'),
]