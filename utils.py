import random

def generate_unique_gradient():
    color1 = f"#{random.randint(0, 255):02x}{random.randint(0, 255):02x}{random.randint(0, 255):02x}"
    color2 = f"#{random.randint(0, 255):02x}{random.randint(0, 255):02x}{random.randint(0, 255):02x}"
    return f"linear-gradient(135deg, {color1}, {color2})"

def extract_topics_and_content(ai_response):
    if not ai_response:
        return []
    
    topics_and_content = []
    sections = ai_response.split("**Topic")[1:]
    
    for section in sections:
        try:
            title = "Topic" + section.split("**")[0].strip()
            content = "**".join(section.split("**")[1:]).strip()
            topics_and_content.append({"topic": title, "content": content})
        except IndexError:
            continue
            
    return topics_and_content
