from django.db import DataError
from django.shortcuts import redirect, render
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
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
        city = request.POST.get('city')
        images = request.FILES.getlist('images')  # Retrieve multiple files
        
 
        if not agree:
            messages.error(request, 'You must agree to the terms and conditions to submit the form.')
            return redirect('inquiry')

      

        # Create an Inquiry instance
        inquiry_instance = Inquiry(
            name=name,
            phone=phone,
            message=message,
            city=city,
            type_property=type_property, 
            agree_field=True,
        )

        try:
            # Save the instance to the database
            inquiry_instance.save()
         
            for image in images:
                ImagesInquiry.objects.create(inquiry=inquiry_instance, image=image)
                
             # Send email notification to the admin
            subject = f'Ново запитване от {name}'
            email_message = f"""
            Беше изпратено запитване.

            Име: {name}
            Телефон: {phone} 
            
            Съобшение:
            {message}
            
            ЗА ПОВЕЧЕ ИНФОРМАЦИЯ ВЛЕЗ В АДМИН.
            """
            
            recipient_list = ['greenhomeinvestltd@gmail.com'] 
            send_mail(
                subject,
                email_message,
                settings.DEFAULT_FROM_EMAIL,  
                recipient_list,
                fail_silently=False,
            )    
            messages.success(request, 'Вашето запитване беше успешно изпратено.')
            return redirect('home') 
        except DataError as e:
            
            if 'value too long for type character varying(10)' in str(e):
                messages.error(request, 'Въведете валиден телефонен номер ')
            else:
                messages.error(request, f'Грешка: {e}')
                # print(f'DataError: {e}')
                return redirect('inquiry')


    context = {
        'property_choices': Inquiry.PROPERTY_CHOICES,  
    }

    return render(request, 'inquiry/inquiry_message.html', context)

