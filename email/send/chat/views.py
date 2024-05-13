from django.shortcuts import redirect, render
from django.core.mail import send_mail
from .forms import ContactForm
from django.template.loader import render_to_string

# Create your views here.
def index(request):
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)

        if form.is_valid():
            name=(form.cleaned_data['name'])
            email=(form.cleaned_data['email'])
            content=(form.cleaned_data['content'])
            pdf = form.cleaned_data['pdf']

            html =  render_to_string('emails/contactform.html',{
                'name':name,
                'email':email,
                'content':content,
            })

           


            print('the form was valid')
            send_mail('the contact form subject','this is the  message','poonamsaliya02@gmail.com',['poonamsaliya02@gmail.com'],html_message=html)



            return redirect ('index')
        else:
            form=ContactForm()




    form= ContactForm()
    return render(request, 'index.html',{'form':form})
