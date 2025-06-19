from django.shortcuts import render, get_object_or_404, redirect
from .models import Event, Registration
from .forms import RegistrationForm
from django.utils import timezone
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

def upcoming_events(request):
    query = request.GET.get('q')
    events = Event.objects.filter(date__gte=timezone.now())
    if query:
        events = events.filter(title__icontains=query)
    return render(request, 'events/upcoming_events.html', {'events': events})

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            if Registration.objects.filter(event=event, email=email).exists():
                messages.error(request, "This email has already registered for this event.")
            else:
                registration = form.save(commit=False)
                registration.event = event
                registration.save()

                # Send confirmation email
                send_mail(
                    subject='Event Registration Confirmation',
                    message=f'Thank you {name} for registering for {event.title}.',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    fail_silently=True,
                )

                messages.success(request, 'You have successfully registered!')
                return redirect('confirmation')
    else:
        form = RegistrationForm()

    return render(request, 'events/event_detail.html', {'event': event, 'form': form})


def confirmation(request):
    return render(request, 'events/confirmation.html')

def past_events(request):
    events = Event.objects.filter(date__lt=timezone.now()).order_by('-date')
    return render(request, 'events/past_events.html', {'events': events})
