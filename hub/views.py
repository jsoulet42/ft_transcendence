from django.shortcuts import render
from backend.models import CustomUser
from django.contrib.auth.models import Group

# Create your views here.
def hub(request):
	try:
		group = Group.objects.get(name='Dev')
		devs = group.user_set.all()
	except Group.DoesNotExist:
		devs = []

	#if request.META.get('HTTP_HX_REQUEST') and request.META.get('reload', None):
	#	return render(request, 'hub_block.html', {'devs', devs})
	return render(request, 'hub.html', {'devs': devs})
