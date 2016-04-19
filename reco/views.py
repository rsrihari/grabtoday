from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from reco.models import UserProfile, Activities, Rating
from django.contrib.auth import authenticate
from data.user import text as userdata
from data.rates import text as ratedata
from data.acts import text as actdata
from reco.recommed import getRecommendations

def welcome(request):
	if request.user.is_authenticated():
		redirect('/home/')
	else:
		return render(request, 'welcome.html' )
	
def ratepage(request):
	recid_=request.GET['recid']
	userid_=request.GET['userid']
	rated_=Rating.objects.filter(user=userid_, activity=recid_)
	if len(rated_)!=0:
		return render(request,'rateerror.html')
	return render(request, 'rate.html',{'recid':recid_,'userid':userid_})

def display(request):
	try:
		rate_=request.POST['rating']
		user_=UserProfile.objects.get(id=request.POST['userid'])
		act_=Activities.objects.get(id=request.POST['recid'])
		rate_=Rating(user=user_, activity=act_, rating=rate_)
		rate_.save()
	except:
		if 'signupbutton' in request.POST:
			try:
				username_=request.POST['username']
				email_=request.POST['email']
				password_=request.POST['password']
				userprof_=User.objects.create_user(username_, email_, password_)
				userprof_.save()
				user_=UserProfile(user=userprof_, age=33, sex='Male')
				user_.save()
			except:
				return redirect('/welcome/')
		else:
			try:
				username_=request.POST['username']
				password_=request.POST['password']
				userprof_=authenticate(username=username_, password=password_)
				user_=UserProfile.objects.get(id=userprof_.id)
			except:
				return redirect('/welcome/')
		if user_ is None:
			return render(request, 'welcome.html')
		print user_.id
	ratematrix={}
	for rateuser in UserProfile.objects.all():
		ratematrix[rateuser.id]={}
	for rate in Rating.objects.all():
		ratematrix[rate.user.id][rate.activity.id]=rate.rating
	recos=getRecommendations(ratematrix, int(user_.id))
	final_recos=[]
	for item in recos:
		final_recos.append(item[1])
	for num in range(len(Activities.objects.all())-1, 0,-1):
		if(Activities.objects.all()[num].id not in final_recos):
			final_recos.append(Activities.objects.all()[num].id)
		if(len(final_recos)>20):
			break
	thingstodo=[]
	for num in final_recos:
		curract=Activities.objects.get(id=num)
		typetologo={'MV':'film',
			'FD':'spoon',
			'OT':'group',
			'TR':'university'
				}
		thingstodo.append([num,typetologo[curract.actype], curract.name, curract.detail])
		if(len(thingstodo)>=20):
			break

	return render(request, 'home.html', {'name':user_.user.username,'userid':user_.id, 'recos':thingstodo })

def update(request):
	users_=userdata.split('\n')
	print users_
	for user in users_:
		try:
			user_details=user.split(',')
			print user_details
			user_=User.objects.create_user(user_details[0], user_details[1],user_details[2])
			user_.save()
			userprof_=UserProfile(user=user_, age=33, sex='Male')
			userprof_.save()
		except:
			pass
	acts_=actdata.split('\n')
	print acts_
	for act in acts_:
		print act
		try:
			act_details=act.split(',')
			print act_details
			act_=Activities(actype=act_details[0], name=act_details[1], detail=act_details[2])
			act_.save()
		except:
			pass
	rates_=ratedata.split('\n')
	print rates_
	for rate in rates_:
		print rate
		try:
			rate_details=rate.split(',')
			print rate_details
			rateuser=UserProfile.objects.get(user=int(rate_details[0]))
			rateact=Activities.objects.get(id=int(rate_details[1]))
			rateval=int(rate_details[2])
			rate_=Rating(user=rateuser, activity=rateact, rating=rateval)
			rate_.save()
		except:
			pass
	return render(request, 'welcome.html')


