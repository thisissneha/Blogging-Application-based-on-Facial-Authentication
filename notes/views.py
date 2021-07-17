from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from notes.templatetags import extras
from django.contrib.auth.decorators import login_required
from .forms import *
from notes.models import *
from home.models import Profile
import json
from django.views.decorators.csrf import csrf_exempt
from PayTm import Checksum

MERCHANT_KEY = '*****'

# Create your views here.
@login_required
def index(request):
	current_user = request.user
	tasks = Task.objects.filter(author=current_user)
	profiles = Profile.objects.filter(user=current_user)
	form = TaskForm()
	if request.method =='POST':
		form = TaskForm(request.POST)

		if form.is_valid():
			print('valid')
			temp = form.save(commit=False)
			temp.author = request.user # add the logged in user, as the author

			if temp.VisibilityMode == 'Pri':
				temp.save()
				random_number = User.objects.make_random_password(length=3, allowed_chars='123456789')
				param_dict = {

					'MID': 'Worl*******',
					'ORDER_ID': random_number,
					'TXN_AMOUNT': '30',
					'CUST_ID': request.user.email,
					'INDUSTRY_TYPE_ID': 'Retail',
					'WEBSITE': 'WEBSTAGING',
					'CHANNEL_ID': 'WEB',
					'CALLBACK_URL': 'http://127.0.0.1:8000/notes/handlerequest/',

				}
				param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
				return render(request, 'tasks/paytm.html', {'param_dict': param_dict})
			else:
				pass
			temp.save()


		else:
			print(form.errors)
		return redirect('../notes/dashboard')

	context = {'tasks':tasks, 'form':form, 'profiles': profiles}
	return render(request, 'tasks/list.html', context)


@login_required
def notes(request, pk):
	current_user = request.user
	profiles = Profile.objects.filter(user=current_user)
	tasks = Task.objects.filter(id=pk).first()
	context = {'tasks':tasks, 'profiles': profiles}
	return render(request, 'tasks/notes.html', context)


@login_required
def dashboard(request):
	current_user = request.user
	profiles = Profile.objects.filter(user=current_user)
	tasks = Task.objects.filter(author=current_user)
	num_post = Task.objects.filter(author=current_user).count()
	num_post_pub = Task.objects.filter(author=current_user, VisibilityMode='Pub').count()
	num_post_pri = Task.objects.filter(author=current_user, VisibilityMode='Pri').count()
	context = {'profiles': profiles, 'num_post': num_post, 'num_post_pub': num_post_pub, 'num_post_pri': num_post_pri, 'tasks':tasks}
	return render(request, 'tasks/dashboard.html', context)


@login_required
def public(request):
	form = TaskForm()
	current_user = request.user
	tasks = Task.objects.filter(author=current_user)
	profiles = Profile.objects.filter(user=current_user)
	context = {'profiles': profiles, 'tasks':tasks, 'form':form}
	return render(request, 'tasks/public.html', context)

@login_required
def edit(request):
	current_user = request.user
	tasks = Task.objects.filter(author=current_user)
	profiles = Profile.objects.filter(user=current_user)
	context = {'profiles': profiles, 'tasks':tasks}
	return render(request, 'tasks/edit.html', context)


@login_required
def private(request):
	current_user = request.user
	tasks = Task.objects.filter(author=current_user)
	profiles = Profile.objects.filter(user=current_user)
	context = {'profiles': profiles, 'tasks': tasks}
	return render(request, 'tasks/private.html', context)



@csrf_exempt
def handlerequest(request):
    checksum=""
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
        else:
            print('order was not successful because' + response_dict['RESPMSG'])

    return render(request, 'tasks/paymentstatus.html', {'response': response_dict})




@login_required
def updateTask(request, pk):
	current_user = request.user
	profiles = Profile.objects.filter(user=current_user)
	task = Task.objects.get(id=pk)
	form = TaskForm(instance=task)

	if request.method == 'POST':
		form = TaskForm(request.POST, instance=task)
		if form.is_valid():
			form.save()
			return redirect('../../dashboard')

	context = {'form':form, 'task':task, 'profiles': profiles}

	return render(request, 'tasks/update_task.html', context)

@login_required
def deleteTask(request, pk):
	current_user = request.user
	profiles = Profile.objects.filter(user=current_user)
	item = Task.objects.get(id=pk)
	task = Task.objects.get(id=pk)

	if request.method == 'POST':
		item.delete()
		return redirect('../../dashboard')

	context = {'item':item,'task':task, 'profiles': profiles}
	return render(request, 'tasks/delete.html', context)

def basic(request):
	current_user = request.user
	profiles = Profile.objects.filter(user=current_user)
	context = {'profiles': profiles}
	return render(request, 'basic.html', context)


