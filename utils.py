import random
import re
from typing import List, Dict
import time
from functools import wraps

def rate_limit(seconds: int):
    """Rate limiting decorator"""
    last_run = {}
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            if func.__name__ in last_run and now - last_run[func.__name__] < seconds:
                raise Exception("Please wait before making another request")
            last_run[func.__name__] = now
            return func(*args, **kwargs)
        return wrapper
    return decorator

def generate_unique_gradient() -> str:
    """Generate a unique gradient with safe color combinations"""
    def generate_safe_color():
        return f"#{random.randint(30, 200):02x}{random.randint(30, 200):02x}{random.randint(30, 200):02x}"
    
    return f"linear-gradient(135deg, {generate_safe_color()}, {generate_safe_color()})"

def sanitize_html(text: str) -> str:
    """Sanitize HTML content"""
    # Remove potentially dangerous tags and attributes
    dangerous_tags = ['script', 'style', 'iframe', 'object', 'embed']
    for tag in dangerous_tags:
        text = re.sub(f'<{tag}.*?</{tag}>', '', text, flags=re.DOTALL)
    return text
