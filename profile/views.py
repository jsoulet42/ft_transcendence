from django.shortcuts import render
from authentication.views import login_required

# Create your views here.
@login_required
def profile(request):
	if request.META.get('HTTP_HX_REQUEST'):
		return render(request, 'profile_block.html')
	return render(request, 'profile.html')
