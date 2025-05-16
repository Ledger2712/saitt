from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def ind1_view(request):
    return render(request, 'ind1.html', {
        'first_name': request.user.first_name
    })
