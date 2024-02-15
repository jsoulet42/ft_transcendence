from django.shortcuts import render
from backend.models import CustomUser

# Create your views here.
def hub(request):
	devs = CustomUser.objects.filter(is_dev = True)
	if request.META.get('HTTP_HX_REQUEST'):
		return render(request, 'hub_block.html', {'devs': devs})
	return render(request, 'hub.html', {'devs': devs})
