from django.shortcuts import redirect, render
from django.contrib import messages
from inquiry_message.models import ImagesInquiry, Inquiry

# Inquiry view to handle form submission
# def inquiry(request):
#     if request.method == 'POST':
#         # Get form data from POST request
#         name = request.POST.get('name')
#         phone = request.POST.get('phone')
#         message = request.POST.get('message')
#         type_property = request.POST.get('type_property')
#         agree = request.POST.get('agree')

#         # Check if the user has agreed to the terms
#         if not agree:
#             messages.error(request, 'You must agree to the terms and conditions to submit the form.')
#             return redirect('inquiry')
        
        
#         # Create an Inquiry instance
#         inquiry_instance = Inquiry(
#             name=name,
#             phone=phone,
#             message=message,
#             type_property=type_property,
#         )
        
#         try:
#             # Save the instance to the database
#             inquiry_instance.save()
#             messages.success(request, 'Your inquiry was successfully submitted.')
#             return redirect('home')  # Redirect to 'home' after successful submission
#         except Exception as e:
#             messages.error(request, f'Error saving inquiry: {e}')
#             print(f'Error: {e}')
#             return redirect('inquiry')  # Redirect back to the inquiry page on error

#     return render(request, 'inquiry/inquiry_message.html')  # Render the form page if not a POST request
def inquiry(request):
    if request.method == 'POST':
        # Get form data from POST request
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        type_property = request.POST.get('type_property')
        agree = request.POST.get('agree')
        images = request.FILES.getlist('images') 
        # Check if the user has agreed to the terms
        if not agree:
            messages.error(request, 'You must agree to the terms and conditions to submit the form.')
            return redirect('inquiry')

        # Create an Inquiry instance
        inquiry_instance = Inquiry(
            name=name,
            phone=phone,
            message=message,
            type_property=type_property,  # Save the selected type_property
        )

        try:
            # Save the instance to the database
            inquiry_instance.save()
             # Save the uploaded images
            for image in images:
                ImagesInquiry.objects.create(inquiry=inquiry_instance, image=image)
            messages.success(request, 'Your inquiry was successfully submitted.')
            return redirect('home')  # Redirect to 'home' after successful submission
        except Exception as e:
            messages.error(request, f'Error saving inquiry: {e}')
            print(f'Error: {e}')
            return redirect('inquiry')  # Redirect back to the inquiry page on error

    # Pass the property choices to the form
    context = {
        'property_choices': Inquiry.PROPERTY_CHOICES,  # Fetch choices directly from the model
    }

    return render(request, 'inquiry/inquiry_message.html', context)

