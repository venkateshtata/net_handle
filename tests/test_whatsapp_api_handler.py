import unittest
from unittest.mock import patch
from backend.whatsapp_api_handler import send_whatsapp_message


class TestSendWhatsAppTemplateMessage(unittest.TestCase):

    @patch('your_module_name.requests.post')  # Replace with the actual path to requests in your module
    def test_send_whatsapp_message_success(self, mock_post):
        # Mock a successful API response
        mock_response = {
            "messages": [
                {"id": "wamid.HBgLNDEyMzQ1Njc4OTAxFQIAERgSN0FENDI2Rjk1OTQyNDYyQjAw"}
            ]
        }
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = mock_response

        # Define the parameters
        to_number = "447723456789" # replace with the recipient phone number
        template_name = "nethandle"
        language_code = "en"
        components = [
            {
                "type": "body",
                "parameters": [
                    {"type": "text", "text": "Under implementation"},
                    {"type": "text", "text": "Please wait!!"}
                ]
            }
        ]
        access_token = "test_access_token"

        # Call the function
        response = send_whatsapp_message(to_number, template_name, language_code, components, access_token)

        # Assert that the response matches the mock response
        self.assertEqual(response, mock_response)
        mock_post.assert_called_once()  # Ensure the API was called once

