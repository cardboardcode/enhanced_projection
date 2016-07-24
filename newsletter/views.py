from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render

# Create your views here.
from .forms import ContactForm, SignUpForm

def home(request):
     title = 'Sign Up Now!'
     # if request.user.is_authenticated():
     #    title = "Welcome %s" %(request.user)
    
    #if request.method =="POST":
      #print request.POST
    
     form = SignUpForm(request.POST or None)

     context = {
         "title": title,
          "form": form
       }
    

     if form.is_valid():
      #form.save()
        instance = form.save(commit=False)
      
        full_name = form.cleaned_data.get("full_name")
        if not full_name:
          full_name = "New full name"
        instance.full_name = full_name
      
        #if not instance.full_name:
        #  instance.full_name = "Cardboard"
        instance.save()
        print instance.email
        print instance.timestamp
        context = {
          "title": "Thank You for Signing Up With Projection"
        }
     if request.user.is_authenticated and request.user.is_staff:
        context = {
          "queryset": "Authentication confirmed. Welcome back, sir."
        }
     return render(request, "home.html",context)

     

def contact(request):
      title = 'Got A Problem?'
      title_align_center = True
      form = ContactForm(request.POST or None)
      if form.is_valid():
        #for key,value in form.cleaned_data.iteritems():
           #print key, value
          form_email = form.cleaned_data.get("email")
          form_message = form.cleaned_data.get("message")
          form_full_name = form.cleaned_data.get("full_name")
          subject = 'Site contact form'
          from_email = settings.EMAIL_HOST_USER
          to_email = [from_email,'youotheremail@email.com']
          contact_message = "%s: %s via %s"%(
                     form_full_name, 
                     form_message,
                     form_email)
          some_html_message = """
          <h1>hello</h1>
          """
          send_mail (subject, 
                     contact_message, 
                     from_email,  
                     to_email,  
                     html_message = some_html_message,
                     fail_silently=True)
      context = {
        "form": form,
        "title": title,
        "title_align_center": title_align_center
      }
      return render (request, "forms.html",context)
