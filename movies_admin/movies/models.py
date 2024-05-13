import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class TimeStampedMixin(models.Model):
    created = models.DateTimeField('Дата создания объекта', auto_now_add=True)
    modified = models.DateTimeField('Дата последнего изменения', auto_now=True)
    class Meta:
        abstract = True
        
class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    class Meta:
        abstract = True

        
class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField('Название', max_length=255)
    def __str__(self):
        return self.name

    class Meta:
        db_table = "genre"
        
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Filmwork(UUIDMixin, TimeStampedMixin):
    title = models.CharField('Название', max_length=255)
    description = models.TextField('Описание')
    creation_date = models.DateField('Дата создания')
    rating = models.FloatField('Рейтинг фильма', blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    TYPE_CHOICES = [('movie', 'Movie'),
                    ('tv_show', 'TV Show')]
    type = models.CharField('Тип', max_length=20, choices=TYPE_CHOICES)

    genres = models.ManyToManyField(Genre, through='GenreFilmwork')
    def __str__(self):
        return self.title

    class Meta:
        db_table = "film_work"
        
        verbose_name = 'Кинопроизведение'
        verbose_name_plural = 'Кинопроизведения'


class GenreFilmwork(UUIDMixin):
    genre = models.ForeignKey('Genre', models.DO_NOTHING, blank=True, null=True)
    film_work = models.ForeignKey('Filmwork', models.DO_NOTHING, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "genre_film_work"
        unique_together = (('genre', 'film_work'),)
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField('ФИ человека', max_length=100)

    def __str__(self):
        return self.full_name
    
    class Meta:
        db_table = "person"
        verbose_name = "Актер"
        verbose_name_plural = "Актеры"
        

class PersonFilmwork(UUIDMixin):
    person = models.ForeignKey('Person', models.DO_NOTHING, blank=True, null=True)
    film_work = models.ForeignKey('Filmwork', models.DO_NOTHING, blank=True, null=True)
    role = models.CharField('Роль', max_length=50)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "person_film_work"
        unique_together = (('person', 'film_work'),)
        verbose_name = "Актер"
        verbose_name_plural = "Актеры"

