import unittest
from unittest.mock import patch, MagicMock, Mock
from PIL import Image
from io import BytesIO
import main

class TestMain(unittest.TestCase):
    @patch('main.input', return_value='test')
    def test_prompt_user_for_theme(self, input):
        self.assertEqual(main.prompt_user_for_theme(), 'test')

    def test_fetch_images_from_unsplash(self):
        mock_img = Image.new('RGB', (64, 64))
        byte_arr = BytesIO()
        mock_img.save(byte_arr, format='PNG')
        byte_img = byte_arr.getvalue()

        mock_response = Mock()
        mock_response.content = byte_img
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'results': [{'urls': {'small': 'http://example.com'}}]  # Only one image URL
        }
        
        with patch('main.requests.get', return_value=mock_response) as mock_get:
            images = main.fetch_images_from_unsplash('test', {'match_aspect_ratio': False})
            self.assertEqual(len(images), 1)

    def test_convert_to_grayscale_and_contrast(self):
        img = Image.new('RGB', (64, 64))
        converted_img = main.convert_to_grayscale_and_contrast(img)
        self.assertEqual(converted_img.mode, 'L')

    @patch('main.os.path.exists', return_value=False)
    @patch('main.os.makedirs')
    @patch('PIL.Image.new')
    def test_save_icons_to_directory(self, mock_new, mock_makedirs, mock_exists):
        mock_img = MagicMock()
        mock_new.return_value = mock_img

        main.save_icons_to_directory([mock_img], 'test', 'Base')

        mock_makedirs.assert_called_once()
        mock_img.save.assert_called_once()

if __name__ == '__main__':
    try:
        unittest.main(verbosity=2,exit=False)
    except Exception as e:
        print(e)