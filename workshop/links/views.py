"""
    Django views for link application
"""

def refresh_list(request):
    return render(
        request,
        'view1.html',
        context={
            'screens': SCREENS_TO_REFRESH
        })
