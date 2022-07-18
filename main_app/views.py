from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from .models import Item
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your views here.
def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def profile(request):
  item_listed = Item.objects.all().filter(posted=True)
  item_unlisted = Item.objects.all().filter(posted=False)
  return render(request, 'profile.html', {'item_listed':  item_listed,
    'item_unlisted': item_unlisted})

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

def items_index(request):
  items = Item.objects.all()
  return render(request, 'items/index.html', { 'items': items })

class ItemCreate(LoginRequiredMixin, CreateView):
  model = Item
  fields = ['name', 'quantity', 'description', 'min_bid']
  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class ItemDelete(DeleteView):
  model = Item
  success_url = '/profile/' 

class ItemUpdate(UpdateView):
  model = Item
  fields = ['name', 'description']

def items_detail(request, item_id):
  item = Item.objects.get(id=item_id)
  return render(request, 'items/detail.html', {
    'item': item, 
     })

def add_post(request, item_id):
  item = Item.objects.get(id=item_id)
  print(request, item)
  item.posted = True
  item.save()
  return redirect('profile', item_id=item_id)