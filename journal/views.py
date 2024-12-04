from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import auth, User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.core.mail import send_mail
from django.conf import settings
from . forms import RegistrationForm, LoginForm, ThoughtForm, CredentialsForm, ProfilePicForm
from . models import Thought, Profile

def home(request):
  return render(request, 'journal/index.html')

def register(request):
  if request.method != 'POST':
    form = RegistrationForm()
  else:
    form = RegistrationForm(data=request.POST)
    if form.is_valid():
      current_user = form.save(commit=False)
      form.save()
      send_mail(
        'Welcome to ThoughtsJournal',
        'Congrats on registering with us',
        settings.DEFAULT_FROM_EMAIL,
        [current_user.email]
      )
      current_profile = Profile.objects.create(user=current_user)
      messages.success(request, 'user created')
      return redirect('login')
  context = {'form': form}  
  return render(request, 'journal/register.html', context)

def login(request):
  if request.method != 'POST':
    form = LoginForm()
  else:
    form = LoginForm(request, data=request.POST)
    if form.is_valid():
      username = request.POST.get('username')
      password = request.POST.get('password')
      user = authenticate(
        request=request,
        username=username,
        password=password
      )
      if user is not None:
        auth.login(request, user)
        return redirect('dashboard')
  context = {'form': form}      
  return render(request, 'journal/login.html', context)

def logout(request):
  auth.logout(request)
  return redirect('')

@login_required(login_url='login')
def dashboard(request):
  profile = Profile.objects.get(user=request.user)
  context = {'profile': profile}
  return render(request, 'journal/dashboard.html', context)

@login_required(login_url='login')
def create_thought(request):
  if request.method != 'POST':
    form = ThoughtForm()
  else:
    form = ThoughtForm(data=request.POST)
    if form.is_valid():
      thought = form.save(commit=False)
      thought.user = request.user
      thought.save()
      return redirect('view-thoughts')
  context = {'form': form}    
  return render(request, 'journal/create-thought.html', context)

@login_required(login_url='login')
def view_thoughts(request):
  logged_in_user = request.user.id
  thoughts = Thought.objects.all().filter(user=logged_in_user)
  context = {'thoughts': thoughts}
  return render(request, 'journal/view-thoughts.html', context)

@login_required(login_url='login')
def update_thought(request, thought_id):
  thought = Thought.objects.get(id=thought_id)
  if thought.user != request.user:
    raise Http404
  if request.method != 'POST':
    form = ThoughtForm(instance=thought)
  else:
    form = ThoughtForm(data=request.POST, instance=thought)
    if form.is_valid():
      form.save()
      return redirect('view-thoughts')
  context = {'form': form}    
  return render(request, 'journal/update-thought.html', context)

@login_required(login_url='login')
def delete_thought(request, thought_id):
  if request.method == 'POST':
    try:
      Thought.objects.filter(id=thought_id, user=request.user).delete()
      return redirect('view-thoughts')
    except:
      raise Http404
  return render(request, 'journal/delete-thought.html')

@login_required(login_url='login')
def profile_management(request):
  profile = Profile.objects.get(user=request.user)
  if request.method != 'POST':
    form = CredentialsForm(instance=request.user)
    pic = ProfilePicForm(instance=profile)
  else:
    form = CredentialsForm(data=request.POST, instance=request.user)
    pic = ProfilePicForm(
      request.POST,
      request.FILES,
      instance=profile
    )
    if form.is_valid() and pic.is_valid():
      form.save()
      pic.save()
      return redirect('dashboard')
  context = {'form': form, 'pic': pic}    
  return render(request, 'journal/profile-mgt.html', context)

@login_required(login_url='login')
def delete_account(request):
  if request.method == 'POST':
    User.objects.filter(username=request.user).delete()
    messages.warning(request, 'account deleted')
    return redirect('register')
  return render(request, 'journal/delete-account.html')