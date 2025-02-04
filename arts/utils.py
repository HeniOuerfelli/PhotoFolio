from diffusers import StableDiffusionPipeline
import torch
import os

# Initialize the Stable Diffusion pipeline
pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
pipe.to("cuda" if torch.cuda.is_available() else "cpu")

def generate_image(prompt):
    # """Generate an image based on the given prompt."""
    # image = pipe(prompt, num_inference_steps=50).images[0]
    # output_path = f"/ArtGallery/PhotoFolio-main-GestionArtiste/static/images{prompt.replace(' ', '_')}.png"
    # image.save(output_path)
    # return f"/ArtGallery/PhotoFolio-main-GestionArtiste/static/images/{prompt.replace(' ', '_')}.png"

    static_folder = os.path.join("static", "images")
    os.makedirs(static_folder, exist_ok=True)  # Create the folder if it doesn't exist

    filename = f"{prompt.replace(' ', '_')}.png"
    output_path = os.path.join(static_folder, filename)

    # Generate the image
    image = pipe(prompt, num_inference_steps=50).images[0]
    image.save(output_path)

    # Return the relative URL for Django templates
    return f"/static/images/{filename}"