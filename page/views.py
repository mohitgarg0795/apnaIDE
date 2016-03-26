from django.shortcuts import render
from django.http import HttpResponse
from hack import *
from models import CodeHistory,Users
from django.utils import timezone
from .forms import UserForm
from django.contrib.auth.hashers import make_password


lang_map={
	"C++" : "CPP",
	"C++ 11" : "CPP11",
	"C#" : "CSHARP"
}

def index(request):
	return HttpResponse("mohit")


def login_user(request):
	#if request.method=="POST":
	#	form=
	return render(request,"page/login.html",{})

def register(request):
	if request.method=='POST' :
		form=UserForm(request.POST)
		if form.is_valid():
			user=form.cleaned_data
			username=user['username']
			email=user['email']
			hash_password=make_password(user['password'])
			
			Users.objects.create(username=username,email=email,password=hash_password)
		else:
			return render(request,"page/register.html",{'form':form})

	form=UserForm(initial={
		'username' : "mohit",
		})
	context={
		"form":form,
	}
	return render(request,"page/register.html",context)

def post(request):
	if request.method=="POST":
		data['source']=request.POST.get('code')
		if data['source']=='':	#to avoid empty source code
			data['source']=' ' 
		data['lang']=request.POST.get('language')
		if data['lang'] in lang_map:
			data['lang']=lang_map[data['lang']]
		data['input']=request.POST.get('input')

		context={
			'code':data['source'],
			'lang_default':data['lang'],
			'input':data['input'],
		}

		r = requests.post(RUN_URL, data=data)
		print r.json()

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
		inst.save()
		
		#to save it directly - using model manager
		#CodeHistory.objects.create(code=data['source'],status=run_status,time_used=time_used,lang=data['lang'],web_link=web_link,output=context['output'])

		return render(request,"page/post.html",context)
		
	return render(request,"page/post.html",{'output':'',
											'code':'',
											'lang_default':'C',
											'input':'',
											'status':'',
											})

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


def history(request):
	queryset=CodeHistory.objects.all().order_by("-id")
	for i in queryset:
		i.timestamp=timezone.now()-i.timestamp 
		i.timestamp,i.time_posvalue=display_time(i.timestamp.total_seconds())
	return render(request,"page/history.html",{'queryset':queryset})