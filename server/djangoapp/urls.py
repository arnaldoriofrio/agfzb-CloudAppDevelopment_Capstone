from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    path(route='', view=views.get_dealerships, name='Index'),
    path(route='about', view=views.about, name='About Us'),
    path(route='contact', view=views.contact, name='Contact Us'),
    path(route='login_request', view=views.login_request, name='Login'),
    path(route='logout_request', view=views.logout_request, name='Logout'),
    path(route='registration_page', view=views.registration_page, name='Register'),
    path(route='registration_request', view=views.registration_request, name='Register Req'),
    path(route='dealer/<int:dealer_id>/', view=views.get_dealer_details, name='Dealer Details'),
    path(route='dealer/<int:dealer_id>/add_review_page', view=views.add_review_page, name='Add Review GET'),
    path(route='dealer/<int:dealer_id>/add_review_request', view=views.add_review_request, name='Add Review POST')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)