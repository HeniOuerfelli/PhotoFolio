from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, DetailView, UpdateView, CreateView
from .models import *
from .forms import UpdateArt, AddArt
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from django.views import View
from django.http import HttpResponse
from .forms import CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
import csv
from .forms import PromptForm
from .utils import generate_image

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, DetailView, UpdateView, CreateView
from .models import *
from .forms import UpdateArt, AddArt
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views import View
from django.http import HttpResponse, HttpResponseNotAllowed
from .forms import CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
import csv

import os
from django.conf import settings
from image_search_recognition.clip_model import recognize_image



def image_recognition(request):
    if request.method == 'POST' and request.FILES.get('image'):
        # Get the uploaded image
        uploaded_image = request.FILES['image']

        # Save the uploaded image to the media directory
        image_path = os.path.join(settings.MEDIA_ROOT_CLIP, uploaded_image.name)
        with open(image_path, 'wb') as f:
            for chunk in uploaded_image.chunks():
                f.write(chunk)

        # Define the image directory to search for similar images
        image_dir = os.path.join(settings.MEDIA_ROOT_CLIP, 'images')  # Store images to be searched here
        image_dir = "arts/img"
        # Perform image recognition and get the most similar image
        similar_image, similarity_scores = recognize_image(image_path, image_dir)
        print(os.path.join(settings.MEDIA_ROOT_CLIP, similar_image))

        print(similarity_scores)
        # Display the similar image and its score
        return render(request, 'image_search_recognition/image_recognition_result.html', {
            'similar_image': similar_image,
            'similarity_scores': similarity_scores[0][1],
            'uploaded_image': uploaded_image.name,
            'similarity_scores1': similarity_scores,
        })

    return render(request, 'image_search_recognition/image_recognition_form.html')
class ExportCommentsCSVView(View):
    def get(self, request, art_id):
        try:
            # Récupérer l'œuvre d'art correspondante
            art = get_object_or_404(Art, id=art_id)

            # Récupérer les commentaires associés à cette œuvre d'art
            comments = art.comments.all()

            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="{art.title}_comments.csv"'
            writer = csv.writer(response)
            writer.writerow(['Art Title', 'comment', 'Username', 'Created At'])
            for comment in comments:
                writer.writerow([art.title, comment.text, comment.user.username, comment.created_at])

            return response

        except Exception as e:
            # Log the error for debugging
            print(f"Error: {e}")
            return HttpResponse("An error occurred while generating the CSV.", status=500)
class AddCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "comment.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        art_id = self.kwargs.get('art_id')
        context['art'] = get_object_or_404(Art, id=art_id)
        return context
    def form_valid(self, form):
        art_id = self.kwargs.get('art_id')
        art = get_object_or_404(Art, id=art_id)
        form.instance.user = self.request.user
        form.instance.art = art
        return super().form_valid(form)
    def get_success_url(self):
        art_id = self.kwargs.get('art_id')
        return reverse_lazy('add_comment', kwargs={'art_id': art_id})

class DeleteComment(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'comment_delete.html'

    # Ici, `success_url` sera calculé dynamiquement après la suppression
    def get_success_url(self):
        art_id = self.kwargs.get('art_id')  # Récupération de l'ID de l'article
        return reverse_lazy('add_comment', kwargs={'art_id': art_id})  # Redirection vers la vue addcomment avec l'ID de l'article

    def get_object(self, queryset=None):
        comment_id = self.kwargs.get('comment_id')
        return Comment.objects.get(pk=comment_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        art_id = self.kwargs.get('art_id')
        context['art'] = get_object_or_404(Art, id=art_id)
        return context
class CommentView(ListView):
    model = Comment
    template_name = "list_comments.html"
    context_object_name = "comments"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        art_id = self.kwargs.get('art_id')
        context['art'] = get_object_or_404(Art, id=art_id)
        return context

    def get_queryset(self):
        art_id = self.kwargs.get('art_id')
        art = get_object_or_404(Art, id=art_id)
        # Trier par 'created_at' en ordre décroissant
        return art.comments.all().order_by('-created_at')


class ArtistView(ListView):
    model = Art
    template_name = 'index.html'
    context_object_name = 'arts'
    paginate_by = 8

    def post(self, request, *args, **kwargs):
        # Handle POST requests for both search and image upload
        return self.get(request, *args, **kwargs)

    def get_queryset(self):
        user_id = self.request.user.id
        search_query = self.request.POST.get('search', '')
        is_public = self.request.POST.get('is_public', None)
        sort_likes = self.request.POST.get('sort_likes', False)

        uploaded_image = self.request.FILES.get('image', None)

        queryset = Art.objects.filter(owner=user_id)

        # Handle image recognition if an image is uploaded
        if uploaded_image:

            print("image uploaded")
            image_path = os.path.join(settings.MEDIA_ROOT_CLIP, uploaded_image.name)
            with open(image_path, 'wb') as f:
                for chunk in uploaded_image.chunks():
                    f.write(chunk)

            image_dir = os.path.join(settings.MEDIA_ROOT_CLIP, 'images')
            image_dir = "arts/img"
            _, similarity_scores = recognize_image(image_path, image_dir)
            img_names = ["arts/img/" + score[0] for score in similarity_scores]
            print(img_names)
            # print(queryset)
            qset = []
            for img in img_names:
                for q in queryset:
                    if img == q.file:
                        qset.append(q)
                        continue
            queryset = qset
            """for q in queryset:
                print(q.file)"""
            # queryset = queryset.filter(file__in=img_names)
        else:
            # Handle title search
            if search_query:
                queryset = queryset.filter(title__icontains=search_query)

            # Handle filtering by public/private status
            if is_public in ['true', 'false']:
                queryset = queryset.filter(is_public=(is_public == 'true'))

            # Sort based on likes if needed
            queryset = queryset.annotate(like_count=Count('arts_likes'))
            queryset = queryset.order_by('-like_count' if sort_likes else '-created_at')

        return queryset
class GalleryView(ListView):
    model = Art
    template_name = 'gallery.html'
    context_object_name = 'arts'
    paginate_by = 8  # Display 8 items per page

    def get_queryset(self):
        category_filter = self.request.GET.get('category', '')
        favorites_filter = self.request.GET.get('favorites', '')
        queryset = Art.objects.filter(is_public=True)

        if category_filter:
            queryset = queryset.filter(category=category_filter)

        if favorites_filter and self.request.user.is_authenticated:
            liked_art_ids = Like.objects.filter(user=self.request.user).values_list('art_id', flat=True)
            queryset = queryset.filter(id__in=liked_art_ids)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Art.objects.values_list('category', flat=True).distinct()

        if self.request.user.is_authenticated:
            user_likes = Like.objects.filter(user=self.request.user).values_list('art_id', flat=True)
            context['user_likes'] = set(user_likes)

        return context
class DetailsArtView(DetailView):
    model = Art
    template_name = "art_details.html"  # Template de détails pour afficher une œuvre
    context_object_name = 'art'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        art = context.get('art')

        if art:
            art.is_image = art.is_image()  # Use model method
            art.is_video = art.is_video()  # Use model method

        # PayPal configuration
        host = self.request.get_host()
        paypal_checkout = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': art.price,
            'item_name': art.title,
            'invoice': uuid.uuid4(),
            'currency_code': 'USD',
            'notify_url': f"http://{host}{reverse('paypal-ipn')}",
            'return_url': f"http://{host}{reverse('payment-success', kwargs={'art_id': art.id})}",
            'cancel_url': f"http://{host}{reverse('payment-failed', kwargs={'art_id': art.id})}",
        }

        paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)
        context['paypal'] = paypal_payment

        return context


class DeleteArtView(DeleteView):
    model = Art
    template_name = "art_delete.html"  # Template de confirmation de suppression
    context_object_name = 'art'
    def get_success_url(self):
        return reverse_lazy("list_arts")  # Redirection après suppression

class UpdateArtView(UpdateView):
    model = Art
    template_name = "art_update.html"  # Template de mise à jour de l'œuvre
    form_class = UpdateArt
    context_object_name = 'art'

    def get_success_url(self):
        return reverse_lazy("list_arts")  # Rediriger vers la liste des œuvres après la mise à jour

class CreateArtView(CreateView):
    model = Art
    template_name = "art_create.html"  # Template de création de l'œuvre
    form_class = AddArt
    context_object_name = 'art'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("list_arts")  # Rediriger vers la liste des œuvres après la création
class UpdateIsPublicView(View):
    def post(self, request, art_id):
        # Récupérer l'art par son ID
        art = get_object_or_404(Art, id=art_id)
        
        # Inverser la valeur de is_public
        art.is_public = not art.is_public
        art.save()

        # Redirection vers la galerie ou autre page après la mise à jour
        return redirect('gallery')
class ToggleIsPublic(View):
    def get(self, request, art_id):
        # Récupérer l'objet art
        art = get_object_or_404(Art, id=art_id)
        
        # Afficher une page de confirmation
        context = {
            'art': art,
            'confirmation_message': f"Voulez-vous {'publier' if not art.is_public else 'mettre en privé'} cet art ?",
        }
        return render(request, 'confirm.html', context)

    def post(self, request, art_id):
        # Récupérer l'objet art
        art = get_object_or_404(Art, id=art_id)
        
        # Basculer l'état de is_public
        art.is_public = not art.is_public
        art.save()
        
        # Rediriger vers la liste des arts
        return redirect('list_arts')

class LikeArtView(View):
    def post(self, request, art_id):
        art = get_object_or_404(Art, id=art_id)
        user = request.user

        # Vérifie si le like existe
        like, created = Like.objects.get_or_create(user=user, art=art)


        if not created:
            # Si le like existe déjà, le supprime
            like.delete()
        else:
            # Si le like est nouveau, il est déjà enregistré avec `get_or_create`
            pass

        # Redirige vers la galerie
        return redirect('gallery')

    
def cart_view(request):
    # Retrieve the cart from session
    cart = request.session.get('cart', {})
    items = []
    total = 0
    item_names = []

    for art_id, quantity in cart.items():
        art = get_object_or_404(Art, id=art_id)
        items.append({
            'art': art,
            'quantity': quantity,
            'subtotal': art.price * quantity
        })
        total += art.price * quantity
        item_names.append(f"{art.title} (x{quantity})")

    # PayPal configuration for the total payment
    host = request.get_host()
    paypal_checkout = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': total,
        'item_name': ", ".join(item_names[:5]) + ("..." if len(item_names) > 5 else ""),
        'invoice': uuid.uuid4(),
        'currency_code': 'USD',
        'notify_url': f"http://{host}{reverse('paypal-ipn')}",
        'return_url': f"http://{host}{reverse('payment-success', kwargs={'art_id': cart.art.id})}",
        'cancel_url': f"http://{host}{reverse('payment-failed', kwargs={'art_id': cart.art.id})}"
    }

    paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)
    context = {
        'items': items,
        'total': total,
        'paypal': paypal_payment
    }

    return render(request, 'cart.html', context)

def cart_view(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0

    for art_id, quantity in cart.items():
        art = get_object_or_404(Art, id=art_id)
        items.append({
            'art': art,
            'quantity': quantity,
            'subtotal': art.price * quantity
        })
        total += art.price * quantity

    return render(request, 'cart.html', {'items': items, 'total': total})

def add_to_cart(request, art_id):
    cart = request.session.get('cart', {})
    cart[art_id] = cart.get(art_id, 0) + 1
    request.session['cart'] = cart
    return redirect('cart_view')

def remove_from_cart(request, art_id):
    cart = request.session.get('cart', {})
    if str(art_id) in cart:  # Vérifiez si l'article est dans le panier
        del cart[str(art_id)]
        request.session['cart'] = cart
    return redirect('cart_view')
    
def generate_artwork(request):
    image_url = None
    if request.method == "POST":
        form = PromptForm(request.POST)
        if form.is_valid():
            prompt = form.cleaned_data['prompt']
            image_url = generate_image(prompt)
    else:
        form = PromptForm()
    return render(request, "generate_image.html", {"form": form, "image_url": image_url})

