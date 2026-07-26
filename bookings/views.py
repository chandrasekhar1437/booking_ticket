from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.db import IntegrityError
from .models import Movie, Booking, Show, Seat

# 1. Movie List / Home Page
def movie_list(request):
    movies = Movie.objects.all()
    context = {'movies': movies}
    return render(request, 'bookings/movie_list.html', context)

# 2. Movie Detail Page
def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    shows = Show.objects.filter(movie=movie) if 'Show' in globals() else []
    
    context = {
        'movie': movie,
        'shows': shows,
    }
    return render(request, 'bookings/movie_detail.html', context)

# 3. User Sign Up View
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

# 4. User Bookings Dashboard
@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    context = {'bookings': bookings}
    return render(request, 'bookings/my_bookings.html', context)

# 5. Book Seat (Tracks booked seats & sends Gmail confirmation)
@login_required
def book_seat(request, show_id):
    show = get_object_or_404(Show, id=show_id)
    seats = Seat.objects.all()
    
    # ఇప్పటికే బుక్ అయిన సీట్ల IDలను ఫిల్టర్ చేయడం
    booked_seat_ids = Booking.objects.filter(show=show).values_list('seat_id', flat=True)

    if request.method == 'POST':
        selected_seat_id = request.POST.get('seat')

        if not selected_seat_id:
            messages.error(request, "Please select a seat.")
            return redirect('book_seat', show_id=show_id)

        seat = get_object_or_404(Seat, id=selected_seat_id)

        try:
            booking = Booking.objects.create(
                user=request.user,
                seat=seat,
                show=show,
            )
        except IntegrityError:
            messages.error(request, "This seat is already booked. Please choose another one.")
            return redirect('book_seat', show_id=show_id)

        # --- SEND CONFIRMATION TICKET TO USER GMAIL ---
        user_email = request.user.email
        if user_email:
            subject = "🎟️ Booking Confirmed - BookMySeat"
            message = (
                f"Hi {request.user.username},\n\n"
                f"Your ticket booking for {show} (Seat: {seat}) has been successfully confirmed!\n"
                f"Booking ID: #{booking.id}\n\n"
                f"Thank you for booking with BookMySeat."
            )
            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [user_email],
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Email failed to send: {e}")

        messages.success(request, "Ticket booked successfully! Confirmation email sent.")
        return redirect('my_bookings')

    context = {
        'show': show,
        'seats': seats,
        'booked_seat_ids': booked_seat_ids,
    }
    return render(request, 'bookings/book_seat.html', context)

# 6. Cancel Ticket View
@login_required
def cancel_ticket(request, booking_id):
    if request.method == 'POST':
        try:
            booking = Booking.objects.get(id=booking_id, user=request.user)
            booking.delete()
            messages.success(request, "Ticket cancelled successfully.")
        except Booking.DoesNotExist:
            messages.error(request, "Booking not found or you do not have permission to cancel it.")
            
    return redirect('my_bookings')