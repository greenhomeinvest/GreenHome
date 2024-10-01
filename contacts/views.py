from django.shortcuts import redirect, render
from django.contrib import messages
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from contacts.models import Contact
from listings.models import Listing
from django.template.loader import render_to_string
# Create your views here.
def contact(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']
        #Check if the user made inqueue already
        if request.user.is_authenticated:
            user_id = request.user.id 
            has_contacted = Contact.objects.all().filter(listing_id=listing_id,user_id=user_id)
            if has_contacted:
                messages.error(request,'Направено е запитване за този имот')
                return redirect('/listings/'+ listing_id)
            
            
        contact = Contact(listing_id=listing_id,name=name,email=email,phone=phone, message=message, user_id=user_id)
        contact.save()
        
         # Fetch the Listing object
        listing_obj = Listing.objects.get(id=listing_id)
        # Fetch the Realtor object
        realtor = listing_obj.realtor
    
        
         # Prepare the email content
        email_subject = 'Ново запитване за имот'
        email_context = {
            'realtor_name': realtor.name,
            'listing_title': listing,
            'listing_id': listing_id,
            # 'listing_address': listing_obj.address,
            'name': name,
            'email': email,
            'phone': phone,
            'message': message,
        }
        
        # Render the HTML template with context
        email_body = render_to_string('email/contact_email.html', email_context)
        
         # Send the email
        # email = EmailMessage(
        #     email_subject,
        #     email_body,
        #     'web.dev.by.vi@gmail.com',  # Your email address
        #     [realtor_email, 'web.dev.by.vi@gmail.com']
        # )greenhomeinvestltd@gmail.com
        email = EmailMessage(
        email_subject,
        email_body,
        'greenhomeinvestltd@gmail.com',  # Your email address
        [realtor_email, 'greenhomeinvestltd@gmail.com']
        )
        email.content_subtype = 'html'  # Ensure the email is sent as HTML
        email.send()
        
        messages.success(request,'Вашето запитване беше изпратено успешно.Брокер ще се свържи с вас скоро')
        return redirect('/listings/'+ listing_id)
        