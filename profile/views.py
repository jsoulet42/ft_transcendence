from django.shortcuts import render

# Create your views here.
def profile(request):
	if request.META.get('HTTP_HX_REQUEST'):
		return render(request, 'profile_block.html')
	return render(request, 'profile.html')
