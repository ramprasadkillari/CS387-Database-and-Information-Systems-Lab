from django.test import TestCase

# Create your tests here.
from forum.models import User,Topic, Comment

class MyTestCases(TestCase):
	def setUp(self):
		User.objects.create(name='santa')
		User.objects.create(name='banta')
		Topic.objects.create(title='politics',created_by=User.objects.get(name='santa'))
		Topic.objects.create(title='eggs',created_by=User.objects.get(name='banta'))
		Comment.objects.create(topic=Topic.objects.get(title='politics'),created_by=User.objects.get(name='santa'),subject="Elections 2019",message="Won by Rp party")
		Comment.objects.create(topic=Topic.objects.get(title='politics'),created_by=User.objects.get(name='banta'),subject="Elections 2020",message="Won by PRK party")
		Comment.objects.create(topic=Topic.objects.get(title='eggs'),created_by=User.objects.get(name='santa'),subject="Nutrition Value",message="Contains Calcium, Good for bone strength")
		Comment.objects.create(topic=Topic.objects.get(title='eggs'),created_by=User.objects.get(name='banta'),subject="Vegetarian",message="Egg is Vegetarian item")

	def test_topic_search(self):
		
		Polt = Topic.objects.filter(title="politics")
		for topic in Polt:
			self.assertEqual(topic.title, 'politics')

	def test_comments_per_topic(self):
		
		Egg = Comment.objects.filter(topic=Topic.objects.get(title='eggs'))
		for comment in Egg:
			self.assertEqual(comment.topic.title, 'eggs')

	def test_comments_by_selected_users(self):
		
		Nta = Comment.objects.filter(created_by__name__contains='nta')
		self.assertEqual(len(Nta),4)
	  
