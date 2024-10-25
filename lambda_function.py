import boto3
import json
import requests
from datetime import datetime
import os
import logging

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Constants
HF_API_TOKEN = "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"  # Replace with your actual Hugging Face API token
HF_API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-3.2-1B"
HEADERS = {
    "Authorization": f"Bearer {HF_API_TOKEN}",
    "Content-Type": "application/json"
}

def blog_generate_using_huggingface(blogtopic: str) -> str:
    """Generate blog content using Hugging Face API with google/flan-t5-large"""
    try:
        # Prepare the prompt
        prompt = f"Write a article about {blogtopic}"
        
        # Prepare the payload
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_length": 500,
                "temperature": 0.7,
                "top_p": 0.8,
                "num_return_sequences": 3
            }
        }
        
        logger.info(f"Making request to Hugging Face API for topic: {blogtopic}")
        response = requests.post(HF_API_URL, headers=HEADERS, json=payload)
        
        if response.status_code != 200:
            logger.error(f"HuggingFace API error: {response.status_code} - {response.text}")
            raise Exception(f"API request failed with status code: {response.status_code}")
            
        # Extract the generated text
        result = response.json()
        if isinstance(result, list) and len(result) > 0:
            generated_text = result[0].get('generated_text', '')
            # Clean up the text
            blog_content = generated_text.replace(prompt, '').strip()
            return blog_content
        else:
            raise Exception("Unexpected API response format")
            
    except Exception as e:
        logger.error(f"Error generating blog: {str(e)}")
        raise

def save_blog_details_s3(s3_key: str, s3_bucket: str, generate_blog: str):
    """Save the generated blog to S3 in .txt format"""
    s3 = boto3.client('s3')
    
    try:
        # Create plain text format for the blog content
        text_content = f"Generated Blog Post:\n\n{generate_blog}\n\nGenerated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        logger.info(f"Attempting to save blog to S3: {s3_bucket}/{s3_key}")
        
        # Upload to S3 as a .txt file
        s3.put_object(
            Bucket=s3_bucket,
            Key=s3_key,
            Body=text_content.encode('utf-8'),
            ContentType='text/plain'
        )
        logger.info(f"Successfully saved blog to s3://{s3_bucket}/{s3_key}")
        
    except Exception as e:
        logger.error(f"Error saving to S3: {str(e)}")
        raise

def lambda_handler(event, context):
    try:
        # Parse the input event
        if not isinstance(event.get('body', ''), str):
            logger.error("Invalid input format received")
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Invalid input format'})
            }
            
        event_body = json.loads(event['body'])
        blogtopic = event_body.get('blog_topic')
        
        if not blogtopic:
            logger.error("No blog topic provided")
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'blog_topic is required'})
            }
        
        # Get S3 bucket name from environment variables
        s3_bucket = os.environ.get('S3_BUCKET_NAME')
        if not s3_bucket:
            logger.error("S3_BUCKET_NAME environment variable not set")
            return {
                'statusCode': 500,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'S3 bucket not configured'})
            }
        
        # Generate the blog content using flan-t5-large model
        generate_blog = blog_generate_using_huggingface(blogtopic=blogtopic)
        
        if not generate_blog:
            logger.error("Failed to generate blog content")
            return {
                'statusCode': 500,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Failed to generate blog content'})
            }
            
        # Create a URL-friendly filename
        safe_topic = ''.join(c if c.isalnum() else '-' for c in blogtopic)[:50]
        current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
        s3_key = f"blog-output/{safe_topic}_{current_time}.txt"
        
        # Save to S3 as .txt
        save_blog_details_s3(s3_key, s3_bucket, generate_blog)
        
        # Generate the public URL for the blog
        s3_url = f"https://{s3_bucket}.s3.amazonaws.com/{s3_key}"
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'message': 'Blog generation completed successfully',
                'blog_content': generate_blog,
                'blog_url': s3_url
            })
        }
            
    except Exception as e:
        logger.error(f"Unexpected error in lambda_handler: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }
