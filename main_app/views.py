from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from .models import Item, Bid, Photo
from .forms import BidForm
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Max
import uuid
import boto3
import os

# Create your views here.
def add_photo(request, item_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            # build the full url string
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            # we can assign to cat_id or cat (if you have a cat object)
            Photo.objects.create(url=url, item_id=item_id)
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
    return redirect('detail', item_id=item_id)




def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

@login_required
def profile(request):
  item_listed = Item.objects.all().filter(posted=True).filter(user=request.user)
  item_unlisted = Item.objects.all().filter(posted=False).filter(user=request.user)
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

def popular_index(request):
  # Need to tweak this to filter out popular items
  popular_items = Item.objects.order_by('-date')
  return render(request, 'items/popular_index.html', { 'popular_items': popular_items })

class ItemCreate(LoginRequiredMixin, CreateView):
  model = Item
  fields = ['name', 'quantity', 'description', 'min_bid']
  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class ItemDelete(LoginRequiredMixin, DeleteView):
  model = Item
  success_url = '/profile/' 

class ItemUpdate(LoginRequiredMixin, UpdateView):
  model = Item
  fields = ['name', 'description', 'quantity']

def items_detail(request, item_id):
  item = Item.objects.get(id=item_id)
  bid_form = BidForm()
  current_bid = item.bid_set.all().aggregate(Max('current_bid'))['current_bid__max']
  return render(request, 'items/detail.html',  {
    'item': item,
    'bid_form': bid_form,
    'current_bid': current_bid
     })

@login_required
def add_post(request, item_id):
  item = Item.objects.get(id=item_id)
  print(request, item)
  item.posted = True
  item.save()
  return redirect('profile')

@login_required
def add_bid(request, item_id):
  form = BidForm(request.POST)
  if form.is_valid():
    new_bid = form.save(commit=False)
    new_bid.item_id = item_id
    new_bid.user_id = request.user.id
    new_bid.save()
    # item_bid = Item.objects.get(id=item_id)
    # item_bid.min_bid = new_bid.current_bid
    # item_bid.save()
  return redirect('detail', item_id=item_id)

