"""Test script that is used to test if the transformers library can be used without errors."""
import torch
from transformers import pipeline

print(f"Cuda available: {torch.cuda.is_available()}")
print(f"Number of available GPUs: {torch.cuda.device_count()}")
print(f"GPU Name: {torch.cuda.get_device_name(0)}")

sentiment_analysis = pipeline("sentiment-analysis")

result = sentiment_analysis("Hugging Face is great!")
print(result)
