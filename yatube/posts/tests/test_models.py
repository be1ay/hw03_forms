from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
        )

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        post = PostModelTest.post
        group = PostModelTest.group
        self.assertEqual(post.__str__(), 'Тестовый пост')
        self.assertEqual(group.__str__(), 'Тестовая группа')
        verbosePost = post._meta.get_field('text').verbose_name
        self.assertEqual(verbosePost, 'Текст поста')
        verboseGroup = post._meta.get_field('group').verbose_name
        self.assertEqual(verboseGroup, 'Группа')
