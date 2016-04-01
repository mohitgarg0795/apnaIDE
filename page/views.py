from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from hack import *
from models import CodeHistory as CodeHistory
from django.utils import timezone
from .forms import UserForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required


lang_map={
	"C++" : "CPP",
	"C++ 11" : "CPP11",
	"C#" : "CSHARP"
}

reverse_lang_map={
	"CPP" : "C++",
	"CPP11" : "C++ 11",
	"CSHARP" : "C#" 
}

def display_time(time_taken):		#to convert time in seconds its highest unit possible
	days=int(time_taken)/86400
	if(days):
		return days,"days"
	hr=int(time_taken)/3600
	if(hr):
		return hr,"hours"
	minutes=int(time_taken)/60
	if(minutes):
		return minutes,"minutes"
	return int(time_taken)%60,"seconds"


def login_user(request):
	context={
		'username' : '',
		'password' : '',
	}

	if request.method=="POST":
		username=request.POST.get("username")
		password=request.POST.get("password")
		user=authenticate(username=username, password=password)
		#print user
		if user:
			if request.user.is_authenticated():
				print request.user
				print "You are already logged in"

			else:
				print "not logged in"
				login(request,user)
				return HttpResponseRedirect("post")
		else:
			context['username']=username
			context['password']=password
			context['error']="Invalid username or password : Please try again "

			print render(request,"page/login.html",context)

	return render(request,"page/login.html",context)


#@login_required(redirect_field_name="login")
@login_required(login_url="/login")
def logout_user(request):
	logout(request)
	return HttpResponseRedirect("post")


def register(request):
	if request.method=='POST' :
		form=UserForm(request.POST)
		if form.is_valid():

			user=form.save(commit=False)
			user=User.objects.create_user(username=user.username, email=user.email, password=user.password)
			user.save()

			return render(request,"page/register.html",{ 'registered' : True})
			"""user=form.cleaned_data
			username=user['username']
			email=user['email']
			hash_password=make_password(user['password'])
			
			User.objects.create(username=username,email=email,password=hash_password)"""
		else:
			return render(request,"page/register.html",{'form':form})

	if request.user.is_authenticated():
		return HttpResponseRedirect('post')

	form=UserForm()
	context={
		"form":form,
	}
	return render(request,"page/register.html",context)

def post(request):
	user=request.user
	print user

	if request.method=="POST":
		data['source']=request.POST.get('code')
		if data['source']=='':	#to avoid empty source code
			data['source']=' ' 
		data['lang']=request.POST.get('language')
		data['input']=request.POST.get('input')

		context={
			'code':data['source'],
			'lang_default':data['lang'],
			'input':data['input'],
		}

		if data['lang'] in lang_map:
			data['lang']=lang_map[data['lang']]

		r = requests.post(RUN_URL, data=data)
		#print r.json()

		run_status=r.json()['run_status']['status']
		web_link=r.json()['web_link']				

		if run_status=="AC":	
			context['output']=r.json()['run_status']['output']
			context['status']='Successful'
			time_used=r.json()['run_status']['time_used']

		if run_status=="CE":
			context['output']=r.json()['compile_status']
			context['status']='Compilation Error'
			time_used=0.0

		if run_status=="RE":
			context['output']=r.json()['run_status']['stderr']
			context['status']='Runtime Error'
			time_used=r.json()['run_status']['time_used']

		if run_status=="TLE":
			context['output']=r.json()['run_status']['output']
			context['status']='Time Limit Exceeded'
			time_used=r.json()['run_status']['time_used']

		#to save record to database, instantiate the model class 		
		inst=CodeHistory(code=data['source'],status=run_status,time_used=time_used,lang=data['lang'],web_link=web_link,output=context['output'])
		if user.is_authenticated():		#to store valid username corresponding to each submission, not for anonymoususer
			inst.username=user
		inst.save()
		
		#to save it directly - using model manager
		#CodeHistory.objects.create(code=data['source'],status=run_status,time_used=time_used,lang=data['lang'],web_link=web_link,output=context['output'])
		context['user']=user

		request.session['lang']=reverse_lang_map.get(data['lang'],data['lang'])		# make last used language to be default lang for next time

		return render(request,"page/post.html",context)

	if 'lang' in request.session:
		x=request.session['lang']
	else:
		x='C'

	return render(request,"page/post.html",{'code':'',
											'lang_default': x,
											'input':'',
											'status':'',
											'user':user,
											})


def history(request):
	queryset=CodeHistory.objects.all().order_by("-id")
	for i in queryset:
		i.timestamp=timezone.now()-i.timestamp 
		i.timestamp,i.time_posvalue=display_time(i.timestamp.total_seconds())
	return render(request,"page/history.html",{'queryset':queryset,
												'user' : request.user })

@login_required(login_url="/login")
def mycodes(request):
	user=request.user
	
	#if not user.is_authenticated():		//used login_required() decorator instead
	#	return HttpResponseRedirect("login")

	queryset=CodeHistory.objects.all().filter(username=user).order_by("-id")
	for i in queryset:
		i.timestamp=timezone.now()-i.timestamp 
		i.timestamp,i.time_posvalue=display_time(i.timestamp.total_seconds())

	return render(request,"page/mycodes.html",{'queryset':queryset})


@login_required(login_url="/login")
def change_password(request):
	user=request.user

	#if not user.is_authenticated():
	#	return HttpResponseRedirect("login")

	if request.method=="POST":
		oldpass=request.POST['oldpass']
		newpass=request.POST['newpass']
		repass=request.POST['repass']
		
		user=authenticate(username=user,password=oldpass)
		if user and newpass==repass:
			user.set_password(repass)
			user.save()
			logout(request)
			return HttpResponseRedirect("login")
		else:
			return render(request,"page/changepassword.html",{ 'error' : "Passwords don't match, please try again"})

	return render(request,"page/changepassword.html",{})
