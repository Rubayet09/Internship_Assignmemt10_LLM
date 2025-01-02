# import json
# import requests
# from django.conf import settings

# class GeminiService:
#     def __init__(self):
#         self.api_key = settings.GEMINI_API_KEY
#         self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

#     def generate_content(self, prompt):
#         """Generate content using Gemini API"""
#         url = f"{self.base_url}?key={self.api_key}"
        
#         payload = {
#             "contents": [{
#                 "parts": [{
#                     "text": prompt
#                 }]
#             }]
#         }

#         try:
#             response = requests.post(url, json=payload)
#             response.raise_for_status()
            
#             result = response.json()
#             if 'candidates' in result and len(result['candidates']) > 0:
#                 return result['candidates'][0]['content']['parts'][0]['text']
#             return None
#         except Exception as e:
#             print(f"Error calling Gemini API: {e}")
#             return None

#     def generate_property_summary(self, property_data):
#         """Generate a summary for a property"""
#         prompt = f"""
#         Please generate a comprehensive summary for this property:
#         Title: {property_data.title}
#         Location: {property_data.location}
#         Room Type: {property_data.room_type}
#         Price: {property_data.price}
#         Rating: {property_data.rating}
        
#         Generate a detailed summary highlighting the key features and location benefits.
#         """
#         return self.generate_content(prompt)

#     def generate_property_review(self, property_data):
#         """Generate a review and rating for a property"""
#         prompt = f"""
#         Based on this property information:
#         Title: {property_data.title}
#         Location: {property_data.location}
#         Room Type: {property_data.room_type}
#         Price: {property_data.price}
        
#         Please generate:
#         1. A detailed review of the property (considering location, amenities, and value for money)
#         2. A rating out of 5 stars
        
#         Format the response as JSON with 'review' and 'rating' fields.
#         """
        
#         response = self.generate_content(prompt)
#         try:
#             parsed = json.loads(response)
#             return parsed.get('rating'), parsed.get('review')
#         except:
#             return None, None


import json
import requests
from django.conf import settings

class GeminiService:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

    def generate_content(self, prompt):
        """Generate content using Gemini API"""
        url = f"{self.base_url}?key={self.api_key}"
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }]
        }

        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            
            result = response.json()
            if 'candidates' in result and len(result['candidates']) > 0:
                return result['candidates'][0]['content']['parts'][0]['text']
            return None
        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            return None

    def generate_property_summary(self, property_data):
        """Generate a summary for a property"""
        prompt = f"""
        Please generate a comprehensive summary for this property:
        Title: {property_data.title}
        Location: {property_data.location}
        Room Type: {property_data.room_type}
        Price: {property_data.price}
        Rating: {property_data.rating}
        
        Generate a detailed summary highlighting the key features and location benefits.
        """
        return self.generate_content(prompt)

    def generate_property_review(self, property_data):
        """Generate a review and rating for a property"""
        prompt = f"""
        Based on this property information:
        Title: {property_data.title}
        Location: {property_data.location}
        Room Type: {property_data.room_type}
        Price: {property_data.price}
        
        Generate a detailed review and rating in the following JSON format:
        {{
            "rating": 4.5,
            "review": "Your detailed review here"
        }}
        
        The rating should be a number between 1 and 5.
        """
        
        response = self.generate_content(prompt)
        if not response:
            print(f"No response received for property: {property_data.title}")
            return None, None

        try:
            # Try to find JSON-like content within the response
            response = response.strip()
            start_idx = response.find('{')
            end_idx = response.rfind('}')
            
            if start_idx >= 0 and end_idx >= 0:
                json_str = response[start_idx:end_idx + 1]
                parsed = json.loads(json_str)
                
                rating = float(parsed.get('rating', 0))
                review = parsed.get('review', '')
                
                # Validate rating is within expected range
                if 1 <= rating <= 5 and review:
                    return rating, review
                else:
                    print(f"Invalid rating or empty review for property: {property_data.title}")
                    return None, None
            else:
                print(f"No JSON content found in response for property: {property_data.title}")
                return None, None
                
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Error parsing response for property {property_data.title}: {e}")
            print(f"Raw response: {response}")
            return None, None