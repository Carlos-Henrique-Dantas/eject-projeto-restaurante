from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from .models import Reserva
from .forms import ReservaForm
from django.views.generic import ListView, DetailView
from .models import Post


# Create - fazer nova reserva
class ReservaCreateView(CreateView):
    model = Reserva
    form_class = ReservaForm
    template_name = 'reserva_form.html'
    success_url = reverse_lazy('minhas_reservas')

    def form_valid(self, form):
        # Atribui automaticamente status "pendente" (já é o padrão)
        return super().form_valid(form)

# Read - listar reservas (apenas as do cliente, se tiver login; por enquanto lista todas)
class ReservaListView(ListView):
    model = Reserva
    template_name = 'lista_reservas.html'
    context_object_name = 'reservas'
    ordering = ['-data', '-horario']

# Update - cancelar ou editar reserva (fazer uma view para cancelar)
class ReservaCancelView(UpdateView):
    model = Reserva
    fields = []  # não vamos editar campos, só mudar status
    template_name = 'reserva_confirm_cancel.html'
    success_url = reverse_lazy('minhas_reservas')

    def form_valid(self, form):
        reserva = form.save(commit=False)
        reserva.status = 'cancelada'
        reserva.save()
        return super().form_valid(form)

# Delete - remover reserva 
class ReservaDeleteView(DeleteView):
    model = Reserva
    template_name = 'reserva_confirm_delete.html'
    success_url = reverse_lazy('minhas_reservas')

def home(request):
    return render(request, 'index.html')


class PostListView(ListView):
    model = Post
    template_name = 'blog.html'
    context_object_name = 'posts'
    queryset = Post.objects.filter(ativo=True)

class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detalhe.html'
    context_object_name = 'post'