from django.contrib import admin
from django.urls import URLPattern, path
from django.conf import settings
from django.conf.urls.static import static



from .import views

urlpatterns = [
    path("", views.index, name="Shop Home"),
    path("about/", views.about, name="About Us"),
    path("contact/", views.contact, name="Contact Us"),
    path("tracker/", views.tracker, name="Tracking Status"),
    path("search/", views.search, name="Search"),
    path("product/<int:myid>", views.product, name="Product"),
    path("checkout", views.checkout, name="Check Out")
]