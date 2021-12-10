from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL

    # path for registration

    path(route='', view=views.get_dealerships, name='index'),
    path(route='about', view=views.about, name='About Us'),
    path(route='contact', view=views.contact, name='Contact Us'),
    path(route='login_request', view=views.login_request, name='Login'),
    path(route='logout_request', view=views.logout_request, name='Logout'),
    path(route='registration_page', view=views.registration_page, name='Register'),
    path(route='registration_request', view=views.registration_request, name='Register Req'),

    # path for dealer reviews view

    # path for add a review view

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)