from django.contrib import admin
from .models import Genre, Filmwork, GenreFilmwork, PersonFilmwork, Person

class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork

class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork

@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline, PersonFilmworkInline)
    list_display = ('title', 'type', 'rating', 'creation_date', 'created',)
    list_filter = ('type', 'creation_date', 'created',)
    search_fields = ('title', 'description', 'id', 'rating', 'creation_date',)

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'created',)
    list_filter = ('created',)
    search_fields = ('name', 'created',)

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'created',)
    list_filter = ('created',)
    search_fields = ('full_name', 'created')
    
