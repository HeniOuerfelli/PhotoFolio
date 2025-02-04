from django.urls import path
from .views import *
from . import views
urlpatterns = [
    path('list/', ArtistView.as_view(), name='list_arts'), 
    path('delete/<int:pk>', DeleteArtView.as_view(), name='delete_art'),  
    path('detail/<int:pk>', DetailsArtView.as_view(), name='details_arts'),   
    path('update/<int:pk>', UpdateArtView.as_view(), name='update_art'),
    path('create/', CreateArtView.as_view(), name='create_art'),
    path('gallery/', GalleryView.as_view(), name='gallery'),
    path('toggle_is_public/<int:art_id>/', ToggleIsPublic.as_view(), name='toggle_is_public'),
    path('like/<int:art_id>/', LikeArtView.as_view(), name='like_art'),
    path('add-comment/<int:art_id>/', AddCommentView.as_view(), name='add_comment'),
    path('delete_comment/<int:art_id>/<int:comment_id>/', DeleteComment.as_view(), name='confirm_delete_comment'),
    path('comments/<int:art_id>/', CommentView.as_view(), name='list_comments'),
    path('export-comments/<int:art_id>/', ExportCommentsCSVView.as_view(), name='export_comments_csv'),
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/add/<int:art_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:art_id>/', views.remove_from_cart, name='remove_from_cart'),
    path("generate/", views.generate_artwork, name="generate_artwork"),

]
