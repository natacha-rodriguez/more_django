from django.test import TestCase
from .models import Post, Comment
from django.utils import timezone
from django.contrib.auth.models import User


# Create your tests here.
class PostTestCase(TestCase):
	def setUp(self):
		user1 = User.objects.create(username='test_user1', password='test_pass')
		user2 = User.objects.create(username='test user 2', password = 'test pass2')
		post = Post.objects.create(author = user1, title = 'This is the first test post', text = 'This is a test text for the first test post.')
		Post.objects.create(author = user2, title = 'Hello people!', text = 'This is my first post as second test user...Yay!.')
		Post.objects.create(author = user1, title = 'This user has a few more things to say', text = 'I still have many more posts to write')

		post.publish()


	def test_posts_are_not_published(self):
		unpublished_posts = Post.objects.filter(published_date__isnull= True)
		self.assertEqual(unpublished_posts.count(), 2)
		
	def test_post_is_published(self):
		published_posts = Post.objects.filter(published_date__lte = timezone.now())
		self.assertEqual(published_posts.count(), 1)


class CommentTestCase(TestCase):
	def setUp(self):
		author1 = User.objects.create(username='test user for comments', password = 'whatever')
		author2 = User.objects.create(username='second test user for comments', password = 'whatever2')
		author3 = User.objects.create(username='third test user for comments', password = 'whatever3')
		post_author = User.objects.create(username ='test user for posts to comment', password='samesame')
		post = Post.objects.create(author=post_author, title = 'This is a post to test comments', text='A lot of people will have an opinion about this post!')
		Comment.objects.create(post=post, author= author1, text= 'this is my first comment!')
		Comment.objects.create(post = post, author = author2, text = ' I disagree with the post!')
		Comment.objects.create(post=post, author = author3, text="I'm just troll and I'm here just trolling")
		post.publish()

	def test_comment_count(self):
		post = Post.objects.get(title='This is a post to test comments')
		self.assertEqual(post.comments.count(), 3)

	def test_approve_comment(self):
		post = Post.objects.get(title='This is a post to test comments')
		self.assertEqual(post.approved_comments().count(), 0)
		author = User.objects.get(username='test user for comments')
		comment = post.comments.get(author=author)
		comment.approve()
		self.assertEqual(post.approved_comments().count(), 1)

	def test_remove_comment(self):
		post = Post.objects.get(title='This is a post to test comments')
		self.assertEqual(post.comments.all().count(), 3)
		author = User.objects.get(username='third test user for comments')
		comment = post.comments.get(author=author)
		comment.delete()
		self.assertEqual(post.comments.all().count(), 2)		


