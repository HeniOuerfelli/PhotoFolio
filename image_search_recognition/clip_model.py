import torch
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import os

# Load the pretrained CLIP model and processor
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# Move the model to GPU if available
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

# Function to extract features for an image
def extract_image_features(image_path):
    """
    Extracts features from an image using the CLIP model.
    """
    # Open and preprocess the image
    image = Image.open(image_path)

    # Process the image using CLIP's processor
    inputs = processor(images=image, return_tensors="pt", padding=True).to(device)

    # Perform inference (forward pass) and extract the image features
    with torch.no_grad():
        outputs = model.get_image_features(**inputs)

    # Normalize features to unit length (important for cosine similarity)
    image_features = outputs / outputs.norm(p=2, dim=-1, keepdim=True)
    return image_features

# Function to recognize the uploaded image and find the most similar image from the directory
def recognize_image(uploaded_image_path, image_dir, threshold=0.1):
    """
    Recognizes the uploaded image and returns the most similar image(s)
    from a directory of images based on cosine similarity with a threshold.
    """
    # Extract features for the uploaded image
    uploaded_image_features = extract_image_features(uploaded_image_path)

    similarity_scores = []
    filtered_matches = []

    # Ensure image_dir is a proper string
    if isinstance(image_dir, list):  # In case image_dir is mistakenly a list, use the first element
        image_dir = image_dir[0] if image_dir else None

    if not image_dir or not os.path.isdir(image_dir):
        raise ValueError(f"The provided image directory '{image_dir}' is invalid or doesn't exist.")

    # Loop through the images in the specified directory to compare with the uploaded image
    for filename in os.listdir(image_dir):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            img_path = os.path.join(image_dir, filename)

            # Extract features for each image in the directory
            image_features = extract_image_features(img_path)

            # Calculate cosine similarity between the uploaded image and current image
            similarity = torch.cosine_similarity(uploaded_image_features, image_features).item()

            # Apply threshold to filter out irrelevant matches
            if similarity >= threshold:
                filtered_matches.append((filename, similarity))

            # Store all similarity scores (optional)
            similarity_scores.append((filename, similarity))

    # Sort filtered matches by similarity score (highest first)
    filtered_matches.sort(key=lambda x: x[1], reverse=True)
    filtered_matches=filtered_matches[:4]
    # Get the most similar image if any matches exist
    most_similar_image = filtered_matches[0][0] if filtered_matches else None

    # Return the most similar image and filtered similarity scores
    return most_similar_image, filtered_matches