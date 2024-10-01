from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Feedback
from listings.models import Listing
from realtors.models import Realtor

def feedback(request):
    if request.method == 'POST':
        name = request.POST.get('name') or None  # Use None if name is empty
        message = request.POST.get('message')
        listing_id = request.POST.get('listing')
        realtor_id = request.POST.get('realtor')
        # user_id = request.user.id if request.user.is_authenticated else None

        try:
            listing = Listing.objects.get(id=listing_id)
            realtor = Realtor.objects.get(id=realtor_id)
        except Listing.DoesNotExist:
            messages.error(request, 'Selected listing does not exist.')
            return redirect('feedback')
        except Realtor.DoesNotExist:
            messages.error(request, 'Selected realtor does not exist.')
            return redirect('feedback')

        feedback_instance = Feedback(
            listing=listing,
            realtor=realtor,
            name=name,  # Allow None
            message=message,
            # user_id=user_id
        )
        try:
            feedback_instance.save()
            messages.success(request, 'Your feedback was successfully submitted.')
            return redirect('home')
        except Exception as e:
            messages.error(request, f'Error saving feedback: {e}')
            print(request, f'{e}')
            return redirect('feedback')

    listings = Listing.objects.all()
    realtors = Realtor.objects.all()

    context = {
        'listings': listings,
        'realtors': realtors,
    }

    return render(request, 'feedback/feedback_form.html', context)
