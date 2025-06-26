#!/usr/bin/env python3
"""
Model Image Uploader

This script helps you upload images for your AI models to the database via the API endpoint.
"""

import requests
import json
import os
from pathlib import Path
import uuid
from PIL import Image
import io
import base64

# Configuration
API_BASE_URL = "http://localhost:3000"  # Update with your actual URL
UPLOAD_ENDPOINT = f"{API_BASE_URL}/api/models/images"
UPDATE_ENDPOINT = f"{API_BASE_URL}/api/models/update-thumbnail"


def upload_model_image(image_path, model_id, model_name):
    """
    Upload an image for a specific model
    
    Args:
        image_path (str): Path to the image file
        model_id (str): UUID of the model
        model_name (str): Name of the model
    
    Returns:
        dict: Response from the API
    """
    try:
        # Check if file exists
        if not os.path.exists(image_path):
            return {"error": f"File not found: {image_path}"}
        
        # Prepare the file for upload
        with open(image_path, 'rb') as image_file:
            files = {
                'image': (os.path.basename(image_path), image_file, 'image/jpeg')
            }
            data = {
                'modelId': model_id,
                'modelName': model_name
            }
            
            # Make the upload request
            response = requests.post(UPLOAD_ENDPOINT, files=files, data=data)
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Successfully uploaded image for model: {model_name}")
                print(f"📸 Thumbnail URL: {result['data']['thumbnailUrl']}")
                return result
            else:
                error_result = response.json() if response.content else {"error": "Unknown error"}
                print(f"❌ Upload failed: {error_result.get('error', 'Unknown error')}")
                return error_result
                
    except Exception as e:
        error_msg = f"Exception during upload: {str(e)}"
        print(f"❌ {error_msg}")
        return {"error": error_msg}


def update_model_thumbnail_in_db(model_id, thumbnail_url):
    """
    Update the model's thumbnail URL in the database
    
    Args:
        model_id (str): UUID of the model
        thumbnail_url (str): URL of the uploaded thumbnail
    
    Returns:
        dict: Response from the API
    """
    try:
        payload = {
            "modelId": model_id,
            "thumbnailUrl": thumbnail_url
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        response = requests.post(UPDATE_ENDPOINT, json=payload, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Successfully updated thumbnail in database")
            return result
        else:
            error_result = response.json() if response.content else {"error": "Unknown error"}
            print(f"❌ Database update failed: {error_result.get('error', 'Unknown error')}")
            return error_result
            
    except Exception as e:
        error_msg = f"Exception during database update: {str(e)}"
        print(f"❌ {error_msg}")
        return {"error": error_msg}


def process_model_image(image_path, model_id, model_name):
    """
    Complete process: Upload image and update database
    
    Args:
        image_path (str): Path to the image file
        model_id (str): UUID of the model
        model_name (str): Name of the model
    
    Returns:
        dict: Combined result
    """
    print(f"🚀 Processing image for model: {model_name}")
    print(f"📁 Image path: {image_path}")
    print(f"🆔 Model ID: {model_id}")
    print("-" * 50)
    
    # Step 1: Upload the image
    upload_result = upload_model_image(image_path, model_id, model_name)
    
    if "error" in upload_result:
        return upload_result
    
    # Step 2: Update the database
    thumbnail_url = upload_result['data']['thumbnailUrl']
    db_result = update_model_thumbnail_in_db(model_id, thumbnail_url)
    
    return {
        "upload": upload_result,
        "database_update": db_result
    }


def generate_model_uuids(count=5):
    """
    Generate sample UUIDs for testing
    
    Args:
        count (int): Number of UUIDs to generate
    
    Returns:
        list: List of UUID strings
    """
    uuids = [str(uuid.uuid4()) for _ in range(count)]
    print(f"Generated {count} sample UUIDs:")
    for i, uuid_str in enumerate(uuids, 1):
        print(f"{i}. {uuid_str}")
    return uuids


def upload_single_model_example():
    """Example: Single model image upload"""
    print("\n" + "="*60)
    print("SINGLE MODEL UPLOAD EXAMPLE")
    print("="*60)
    
    model_data = {
        "image_path": "./sample_images/gpt_model_thumbnail.jpg",  # Update with your image path
        "model_id": "123e4567-e89b-12d3-a456-426614174000",       # Update with your model UUID
        "model_name": "GPT-4 Text Generator"                       # Update with your model name
    }
    
    # Process the image
    result = process_model_image(
        model_data["image_path"],
        model_data["model_id"],
        model_data["model_name"]
    )
    
    print("\n📋 Final Result:")
    print(json.dumps(result, indent=2))
    return result


def upload_batch_models_example():
    """Example: Batch upload multiple model images"""
    print("\n" + "="*60)
    print("BATCH MODEL UPLOAD EXAMPLE")
    print("="*60)
    
    models_batch = [
        {
            "image_path": "./sample_images/text_gen_model.jpg",
            "model_id": "123e4567-e89b-12d3-a456-426614174001",
            "model_name": "Advanced Text Generator"
        },
        {
            "image_path": "./sample_images/image_gen_model.jpg",
            "model_id": "123e4567-e89b-12d3-a456-426614174002",
            "model_name": "AI Image Creator"
        },
        {
            "image_path": "./sample_images/code_gen_model.jpg",
            "model_id": "123e4567-e89b-12d3-a456-426614174003",
            "model_name": "Code Assistant Pro"
        }
    ]
    
    # Process all models
    batch_results = []
    for i, model in enumerate(models_batch, 1):
        print(f"\n🔄 Processing model {i}/{len(models_batch)}")
        result = process_model_image(
            model["image_path"],
            model["model_id"],
            model["model_name"]
        )
        batch_results.append(result)
        print("✅ Completed\n")
    
    print(f"🎉 Batch processing completed! Processed {len(batch_results)} models.")
    return batch_results


def main():
    """Main function to demonstrate usage"""
    print("Model Image Uploader")
    print("=" * 50)
    
    # Generate some sample UUIDs for reference
    print("\n📝 Generating sample UUIDs for reference:")
    sample_uuids = generate_model_uuids(3)
    
    # Uncomment the examples you want to run:
    
    # Example 1: Single model upload
    # upload_single_model_example()
    
    # Example 2: Batch model upload
    # upload_batch_models_example()
    
    print("\n📌 Instructions:")
    print("1. Update the API_BASE_URL with your actual server URL")
    print("2. Uncomment and modify the example functions above")
    print("3. Update image paths and model information")
    print("4. Run the script to upload your model images")


if __name__ == "__main__":
    main()