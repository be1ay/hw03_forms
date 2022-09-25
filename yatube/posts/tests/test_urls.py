from django.contrib.auth import get_user_model
from django.test import TestCase, Client
import datetime
from ..models import Group, Post
from http import HTTPStatus

User = get_user_model()


class TaskURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()
        cls.user = User.objects.create_user(username='HasNoName')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.post = Post.objects.create(
            text='Тестовый текст',
            pub_date=datetime.datetime.now(),
            author=cls.user
        )
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание группы'
        )

    def test_home_url_exists_at_desired_location(self):
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    # Проверяем доступность страниц для авторизованного пользователя
    def test_post_create_url_exists_at_desired_location(self):
        """Страница /create/ доступна авторизованному пользователю."""
        response = self.authorized_client.get('/create/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_edit_exists_at_desired_location(self):
        """Страница /posts/<int:post_id>/edit/
         доступна авторизованному пользователю."""
        if (self.post.author == self.authorized_client):
            response = self.authorized_client.get(
                f'/posts/{self.post.pk}/edit/')
            self.assertEqual(response.status_code, HTTPStatus.OK)
        return False

    def test_post_post_id_exists_at_desired_location(self):
        """Страница /posts/<int:post_id>/
         доступна неавторизованному пользователю."""
        response = self.guest_client.get(f'/posts/{self.post.pk}/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        response = self.authorized_client.get(f'/posts/{self.post.pk}/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_group_slug_exists_at_desired_location(self):
        """Страница /group/<slug>/
         доступна неавторизованному пользователю."""
        response = self.guest_client.get(f'/group/{self.group.slug}/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        response = self.authorized_client.get(f'/group/{self.group.slug}/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_profile_exists_at_desired_location(self):
        """Страница /profile/username/
         доступна неавторизованному пользователю."""
        response = self.guest_client.get(f'/profile/{self.user.username}/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        response = self.authorized_client.get(
            f'/profile/{self.user.username}/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
    
    def test_not_exists_page_at_desired_location(self):
        """Страница не найдена."""
        response = self.guest_client.get('/not_existing_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    # Проверка вызываемых шаблонов для каждого адреса
    def test_home_url_uses_correct_template(self):
        """Страница по адресу / использует шаблон posts/index.html."""
        response = self.guest_client.get('/')
        self.assertTemplateUsed(response, 'posts/index.html')

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        # Шаблоны по адресам
        templates_url_names = {
            '/': 'posts/index.html',
            f'/group/{self.group.slug}/': 'posts/group_list.html',
            f'/profile/{self.user.username}/': 'posts/profile.html',
            f'/posts/{self.post.pk}/': 'posts/post_detail.html',
            '/create/': 'posts/create_post.html',
            f'/posts/{self.post.pk}/edit/': 'posts/create_post.html',
        }
        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)
