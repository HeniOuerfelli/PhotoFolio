from django.urls import path
from .views import *

urlpatterns = [
    path('list/', ArtistView.as_view(), name='list_arts'), 
    path('delete/<int:pk>', DeleteArtView.as_view(), name='delete_art'),  
    path('detail/<int:pk>', DetailsArtView.as_view(), name='details_arts'),   
    path('update/<int:pk>', UpdateArtView.as_view(), name='update_art'),
    path('create/', CreateArtView.as_view(), name='create_art'),
    path('gallery/', GalleryView.as_view(), name='gallery'),
]
