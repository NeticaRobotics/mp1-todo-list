from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.utils.decorators import method_decorator
from django.views.generic.base import View

from django.http import JsonResponse
from .forms import SignUpForm
from .models import Card

from django.contrib.auth.mixins import LoginRequiredMixin
from graphene_django.views import GraphQLView

class PrivateGraphQLView(LoginRequiredMixin, GraphQLView):
    """Adds a login requirement to graphQL API access via main endpoint."""
    pass

class LoginRequiredView(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class Index(LoginRequiredView):
    def get(self, request, *args, **kwargs):
        finishedCards = Card.objects.filter(author=request.user, finished=True)
        cards = Card.objects.filter(author=request.user, finished=False)
        return render(request, 'index.html', {
            'cards': cards,
            'finishedCards': finishedCards
        })        

class DataOverview(LoginRequiredView):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            if 'from' not in request.GET or 'to' not in request.GET:
                return JsonResponse({
                    's': 1,
                    'm': 'Not valid request'
                })
            cards = Card.objects.filter(author=request.user,
                    created__range=[request.GET['from'], request.GET['to']])
        else:
            cards = Card.objects.filter(author=request.user)

        total_cards = cards.count()
        total_cards = 0.00000001 if total_cards == 0 else total_cards
        finished_percent = cards.filter(finished=True).count()
        unfinished_percent = cards.filter(finished=False).count()

        low_percent = cards.filter(importance=1).count()
        normal_percent = cards.filter(importance=2).count()
        urgent_percent = cards.filter(importance=3).count()

        ctx = {
            'total_cards': total_cards if total_cards >= 1 else 0,
            'finished_percent': finished_percent,
            'unfinished_percent': unfinished_percent,
            'low_percent': low_percent,
            'normal_percent': normal_percent,
            'urgent_percent': urgent_percent,
        }

        return JsonResponse({
            's': 0,
            'd': ctx
        }) if request.is_ajax() else \
        render(request, 'core/data_overview.html', ctx)

class Profile(LoginRequiredView):
    def get(self, request, *args, **kwargs):
        return render(request, 'core/profile.html', {})

class SignUpView(View):
    def get(self, request, *args, **kwargs):
        form = SignUpForm()
        return render(request, 'registration/signup.html', {
            'form': form
        })

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.userdata.ocupation = form.cleaned_data.get('ocupation')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('core:index')
        else:
            return render(request, 'registration/signup.html', {
                'form': form
            })

@login_required
def settings(request):
    user = request.user

    try:
        github_login = user.social_auth.get(provider='github')
    except UserSocialAuth.DoesNotExist:
        github_login = None

    try:
        linkedin_login = user.social_auth.get(provider='linkedin')
    except UserSocialAuth.DoesNotExist:
        linkedin_login = None

    can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())

    return render(request, 'core/settings.html', {
        'github_login': github_login,
        'linkedin_login': linkedin_login,
        'can_disconnect': can_disconnect
    })

@login_required
def password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordForm(request.user)
    return render(request, 'core/password.html', {'form': form})
