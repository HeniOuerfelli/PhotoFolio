from django.shortcuts import render
import os
from django.conf import settings
from .clip_model import recognize_image

def image_recognition(request):
    if request.method == 'POST' and request.FILES['image']:
        # Get the uploaded image
        uploaded_image = request.FILES['image']

        # Save the uploaded image to the media directory
        image_path = os.path.join(settings.MEDIA_ROOT_CLIP, uploaded_image.name)
        with open(image_path, 'wb') as f:
            for chunk in uploaded_image.chunks():
                f.write(chunk)

        # Define the image directory to search for similar images
        image_dir = os.path.join(settings.MEDIA_ROOT_CLIP, 'images')  # Store images to be searched here

        # Perform image recognition and get the most similar image
        similar_image, similarity_scores = recognize_image(image_path, image_dir)
        print(os.path.join(settings.MEDIA_ROOT_CLIP, similar_image))
        print(similarity_scores)
        # Display the similar image and its score
        return render(request, 'image_search_recognition/image_recognition_result.html', {
            'similar_image':   similar_image,# os.path.join(settings.MEDIA_ROOT_CLIP, similar_image) ,#similar_image,
            'similarity_scores': similarity_scores[0][1],
            'uploaded_image': uploaded_image.name,
            'similarity_scores1': similarity_scores,# os.path.join(settings.MEDIA_ROOT_CLIP, uploaded_image.name)#uploaded_image.name
        })

    return render(request, 'image_search_recognition/image_recognition_form.html')