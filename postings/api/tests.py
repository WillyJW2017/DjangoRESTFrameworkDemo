from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from postings.models import BlogPost
from rest_framework.reverse import reverse as api_reverse
from rest_framework_jwt.settings import api_settings

payload_handler = api_settings.JWT_PAYLOAD_HANDLER
encode_handler = api_settings.JWT_ENCODE_HANDLER

User = get_user_model()

class BlogPostAPITestCase(APITestCase):
    def setUp(self):
        user_obj = User(username='testuser', email='test@test.com')
        user_obj.set_password('somepassword')
        user_obj.save()
        blog_post = BlogPost.objects.create(
            user=user_obj,
            title='New Title 20180525',
            content='This is the test content 05251010'
        )

    def test_single_user(self):
        user_count = User.objects.count()
        self.assertEqual(user_count, 1)

    def test_single_post(self):
        post_count = BlogPost.objects.count()
        self.assertEqual(post_count, 1)

    def test_get_list(self):
        data = {}
        url = api_reverse("api-postings:post-listcreate")
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)

    # def test_post_item(self):
    #     data = {"title":"Some random title", "content":"Some random content"}
    #     url = api_reverse("api-postings:post-listcreate")
    #     response = self.client.post(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_item(self):
        data = {}
        blog_post = BlogPost.objects.first()
        url = blog_post.get_api_url()
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        print(response.data)
        print('-------------------->>>>>>>>>>>>>>>>>>>>>')

    def test_update_item(self):
        blog_post = BlogPost.objects.first()
        data = {"title":"Some random title", "content":"Some random content"}
        url = blog_post.get_api_url()
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_item_with_user(self):
        blog_post = BlogPost.objects.first()
        print(blog_post.content)
        data = {"title":"Some random title", "content":"Some random content"}
        url = blog_post.get_api_url()
        user_obj = User.objects.first()
        payload = payload_handler(user_obj)
        token_rsp = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_rsp)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)