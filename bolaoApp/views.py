from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
from django import forms
from django.contrib.auth import logout
from .models import Game
from .models import Account
from .forms import BetForm
from .forms import registration_form
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from datetime import datetime

def load_index(request):
    return render(request, 'bolaoApp/index.html', {})

# Carrega jogos que ainda estão recebendo apostas.

def load_games(request):
    # O Filtro de datas permite que os jogos sejam ocultos assim que forem expirados.

    games = Game.objects.filter(winner='Aposta Ainda Não Finalizada', last_day__gte=datetime.now()).order_by('last_day')
    return render(request, 'bolaoApp/partidas.html', {'games': games})

    # Mostra todos os usuários ordenados pelos ganhos no site. Administradores não aparecem.
def load_ranking(request):
    accounts = Account.objects.exclude(is_superuser=True).order_by('-money_won')
    return render(request, 'bolaoApp/ranking.html', {'accounts': accounts})

@login_required
def load_bet_form(request):
    BetForm.base_fields['game_name'] = forms.ModelChoiceField(queryset=Game.objects.filter(winner='Aposta Ainda Não Finalizada', last_day__gte=datetime.now()).order_by('last_day'), empty_label=None)

    if request.method == "POST":
        form = BetForm(request.POST, request=request)

        if form.is_valid():
            user = request.user
            bet = form.save(commit=False)
            bet.bettor = request.user
            bet.save()

            user.credits -= 5
            user.save()
            return render(request, 'bolaoApp/aposta_feita.html', {})
    else:
        form = BetForm(request=request)
    return render(request, 'bolaoApp/apostar.html', {'form': form})

def login_page(request):
    if request.user.is_authenticated:
        return redirect('bolaoApp/index.html')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            form = AuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})

    else:
        form = AuthenticationForm()
        return render(request, 'registration/login.html', {'form': form})

def sign_up(request):
    if request.method == 'POST':
        form = registration_form(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
    else:
        form = registration_form()
    return render(request, 'registration/registrar.html', {'form': form})

def logout_page(request):
    logout(request)

    return redirect('/')
