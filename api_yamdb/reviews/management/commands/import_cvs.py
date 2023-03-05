import csv
import logging
import sys

from django.core.management.base import BaseCommand
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s, %(levelname)s, %(message)s',
    stream=sys.stdout
)

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Import data from CSV files from /static/data/'

    def handle(self, *args, **options):
        path = 'static/data/'
        logger.info('Import Users')
        with open(path + 'users.csv', encoding="utf8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                User.objects.create(
                    id=row['id'], username=row['username'],
                    email=row['email'], role=row['role'],
                    bio=row['bio'], first_name=row['first_name'],
                    last_name=row['last_name']
                )

        logger.info('Import Categories')
        with open(path + 'category.csv', encoding="utf8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Category.objects.create(
                    id=row['id'], name=row['name'], slug=row['slug']
                )

        logger.info('Import Genres')
        with open(path + 'genre.csv', encoding="utf8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Genre.objects.create(
                    id=row['id'], name=row['name'], slug=row['slug']
                )

        logger.info('Import Titles')
        with open(path + 'titles.csv', encoding="utf8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Title.objects.create(
                    id=row['id'], name=row['name'],
                    year=row['year'], category_id=row['category']
                )

        logger.info('Import Reviews')
        with open(path + 'review.csv', encoding="utf8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Review.objects.create(
                    id=row['id'], title_id=row['title_id'],
                    text=row['text'], author_id=row['author'],
                    score=row['score'], pub_date=row['pub_date']
                )

        logger.info('Import Comments')
        with open(path + 'comments.csv', encoding="utf8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Comment.objects.create(
                    id=row['id'], review_id=row['review_id'],
                    text=row['text'], author_id=row['author'],
                    pub_date=row['pub_date']
                )

        logger.info('Import Genre_Title')
        with open(path + 'genre_title.csv', encoding="utf8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                title = Title.objects.get(id=row['title_id'])
                genre = Genre.objects.get(id=row['genre_id'])
                title.genre.add(genre)
        logger.info('Import CVS complete')
