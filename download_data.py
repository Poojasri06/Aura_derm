import kaggle
import os

# Set Kaggle API credentials (user needs to provide their own)
# os.environ['KAGGLE_USERNAME'] = 'your_kaggle_username'
# os.environ['KAGGLE_KEY'] = 'your_kaggle_api_key'

# Download Celeb-DF dataset
kaggle.api.dataset_download_files('liamchalcroft/celeb-df-v2', path='./data', unzip=True)