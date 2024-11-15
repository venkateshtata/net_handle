import requests

def send_whatsapp_message(to_number, template_name, language_code, components, access_token):
    """
    Sends a WhatsApp message using a specified template via the Facebook Graph API.
    
    Args:
        to_number (str): The recipient's phone number in international format (e.g., "447774839645").
        template_name (str): The name of the WhatsApp template to use (e.g., "nethandle").
        language_code (str): The language code for the template (e.g., "en_US" or "en").
        components (list): List of components (e.g., body text parameters) to customize the template.
        access_token (str): The authorization token for the WhatsApp Business API.

    Returns:
        dict: The API response as a dictionary.
    """
    url = "https://graph.facebook.com/v21.0/502264102963657/messages"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "template",
        "template": {
            "name": template_name,
            "language": {
                "code": language_code
            },
            "components": components
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return {"error": str(e)}