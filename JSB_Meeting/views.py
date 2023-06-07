from django.shortcuts import render, redirect
from django.http import HttpResponse
from Book_Meeting.forms import BookingForm
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse
from Book_Meeting.models import BookedRoom
from django.db.models import Q
import datetime
from django.core.mail import send_mail
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders


def started_view(request):
    return render(request, 'index.html')

def home_view(request):
    return render(request, 'home.html')

def booking_view(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            
            room = form.cleaned_data['Room']
            date = form.cleaned_data['Date']
            time_from = form.cleaned_data['Time_From']
            time_slot = request.POST.get('Time')
            print(time_slot)# Get the selected time slot value from the user input
            delta = None
            if time_slot == '1':
                delta = datetime.timedelta(minutes=30)
            elif time_slot == '2':
                delta = datetime.timedelta(hours=1)
            elif time_slot == '3':
                delta = datetime.timedelta(hours=2)
            else:
                #handle invalid input
                pass
            
            if delta is not None:
                time_end = (datetime.datetime.combine(datetime.date.today(), time_from) + delta).time()
                
            # Send email to the booked_by
            # recipient_list = [form.cleaned_data['Booked_By']]
            # subject = 'Room Booking Confirmation'
            # message = f'Your booking for room {room} on {date} from {time_from} to {time_end} has been confirmed.'
            # sender = 'kushalpandey732@gmail.com'
            # send_mail(subject, message, sender, recipient_list)
            
            recipients = [form.cleaned_data['Booked_By']]
            msg = MIMEMultipart()
            msg['To'] = ', '.join(recipients)
            msg['From'] = 'itcasetracker@nbventuresme.com'
            # msg['CC'] = 'rachel.rodelas@jsbgroupme.com'
            msg['Subject'] = 'Room Booking Confirmation'
            body = f'Your booking for room has been confirmed. Please find the details below:\nRoom: "{room}"\nDate: "{date}"\nTime: "{time_from}" - "{time_end}"'
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP('smtp.office365.com', 587)  ### put your relevant SMTP here
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login('ramdhani@nbventuresme.com', 'Kushal@732')  ### if applicable
            server.send_message(msg)
            server.quit()
            
            
            # Check if the selected room and time slot is available
            if not BookedRoom.objects.filter(Q(Room=room) & Q(Date=date) & ((Q(Time_From__lte=time_from) & Q(Time_End__gt=time_from)) | (Q(Time_From__lt=time_end) & Q(Time_End__gte=time_end)))).exists():
                # Create a new entry in the BookedRoom table
                booked_room = BookedRoom(
                    Room=room,
                    Booked_By=form.cleaned_data['Booked_By'],
                    Date=date,
                    Time_From=time_from,
                    Time_End=time_end,
                    Time=form.cleaned_data['Time']
                )
                booked_room.save()
                
                # Redirect to the home page
                return redirect(reverse('home_view'))
            else:
                # The selected room and time slot is already booked, so show an error message
                return HttpResponse('This room is already booked for the selected time slot')
    else:
        form = BookingForm()
    return render(request, 'book.html', {'form':form})


def transaction_view(request):
    query = BookedRoom.objects.all().order_by('id')
    return render(request, 'view-booking.html', {'query':query})

# def booking_view(request):

#     if request.method == 'POST':
#         form = BookingForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect(reverse('home_view'))
#         else:
#             return HttpResponse('INVALID REQUEST...')
#     else:
#         form = BookingForm()
#     return render(request, 'book.html', {'form':form})