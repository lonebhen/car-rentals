from django.urls import path
from .views import CarView, CarDetailView, CarSearchAPIView, BookCarAPIView, UserRentalBookingsAPIView, ApprovedUserRentalBookingsAPIView


urlpatterns = [
    path('cars/',CarView.as_view(), name='cars'),
    path('cars/<int:pk>/', CarDetailView.as_view(), name='car-detail'),
    path('cars/search/', CarSearchAPIView.as_view(), name='car_search'),
    path('book-car/', BookCarAPIView.as_view(), name='rent_a_car' ),
    path('user/rentals', UserRentalBookingsAPIView.as_view(), name='users_rentals'),
    path('user/approved-rentals', ApprovedUserRentalBookingsAPIView.as_view(), name='approved_user_rentals' )
]
