from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, DetailView, UpdateView, CreateView
from .models import Art
from .forms import UpdateArt, AddArt
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid
from django.urls import reverse

class ArtistView(ListView):
    model = Art
    template_name = 'index.html'
    context_object_name = 'arts'

    def get_queryset(self):
        # Filtrer les œuvres d'art de l'utilisateur connecté
        user_id = self.request.user.id
        return Art.objects.filter(owner=user_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for art in context['arts']:
            # Détecter si le fichier est une image ou une vidéo en fonction de l'extension
            if any(art.file.url.lower().endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".jfif", ".gif"]):
                art.is_image = True
            elif any(art.file.url.lower().endswith(ext) for ext in [".mp4", ".webm", ".avi", ".mov"]):
                art.is_video = True
            else:
                art.is_image = False
                art.is_video = False
        return context

class GalleryView(ListView):
    model = Art
    template_name = "gallery.html"  # Votre template pour afficher la galerie
    context_object_name = 'arts'  # Nom de la variable contextuelle à passer dans le template
    
    def get_queryset(self):
        # Récupérer toutes les œuvres d'art
        return Art.objects.all()

    def get_context_data(self, **kwargs):
        # Ajouter des informations supplémentaires au contexte
        context = super().get_context_data(**kwargs)
        for art in context['arts']:
            # Détecter si le fichier est une image ou une vidéo
            if any(art.file.url.lower().endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".jfif", ".gif"]):
                art.is_image = True
            elif any(art.file.url.lower().endswith(ext) for ext in [".mp4", ".webm", ".avi", ".mov"]):
                art.is_video = True
            else:
                art.is_image = False
                art.is_video = False
        return context

class DetailsArtView(DetailView):
    model = Art
    template_name = "art_details.html"  # Template de détails pour afficher une œuvre
    context_object_name = 'art'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        art = context.get('art')

        # Configuration des paramètres de paiement PayPal
        if art:
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

            # Instanciation du formulaire de paiement PayPal
            paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)
            context['paypal'] = paypal_payment

        # Vérification de l'extension du fichier et ajout des informations is_image et is_video
        if art and art.file:
            if any(art.file.url.lower().endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".jfif", ".gif"]):
                art.is_image = True
                art.is_video = False
            elif any(art.file.url.lower().endswith(ext) for ext in [".mp4", ".webm", ".avi", ".mov"]):
                art.is_video = True
                art.is_image = False
            else:
                art.is_image = False
                art.is_video = False
        else:
            art.is_image = False
            art.is_video = False

        return context

class DeleteArtView(DeleteView):
    model = Art
    template_name = "index.html"  # Template de confirmation de suppression
    success_url = reverse_lazy("list_arts")  # Rediriger après la suppression

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
        # Assigner l'utilisateur connecté comme propriétaire de l'œuvre
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("list_arts")  # Rediriger vers la liste des œuvres après la création
