import os
import urllib
from pathlib import Path
from typing import List, Any
from tqdm import tqdm

def resolve_relative_path(path: str) -> str:
    return os.path.abspath(os.path.join(os.path.dirname(__file__), path))

def conditional_download(download_directory_path: str, urls: List[str]) -> None:  
    if not os.path.exists(download_directory_path):  
        os.makedirs(download_directory_path)  
    
    for url in urls:  
        # Parse the URL to remove query parameters  
        parsed_url = urllib.parse.urlparse(url)  
        clean_filename = os.path.basename(parsed_url.path)  # Get the last part of the path  
        download_file_path = os.path.join(download_directory_path, clean_filename)  
        
        if not os.path.exists(download_file_path):  
            request = urllib.request.urlopen(url)  
            total = int(request.headers.get('Content-Length', 0))  
            with tqdm(total=total, desc='Downloading', unit='B', unit_scale=True, unit_divisor=1024) as progress:  
                urllib.request.urlretrieve(url, download_file_path, reporthook=lambda count, block_size, total_size: progress.update(block_size))