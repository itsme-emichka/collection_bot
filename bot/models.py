from tortoise.models import Model
from tortoise import fields
from tortoise.validators import MaxValueValidator, MinValueValidator

from bot.validators import SlugValidator


NULL: int = 0
MAX_RATING_NUMBER: int = 10


class User(Model):
    id = fields.IntField(pk=True,)


class Type(Model):
    id = fields.SmallIntField(pk=True,)
    name = fields.CharField(max_length=256, unique=True,)
    slug = fields.CharField(max_length=256, validators=[SlugValidator],)


class Title(Model):
    id = fields.IntField(pk=True,)
    kinopoisk_id = fields.IntField(unique=True,)
    name = fields.CharField(max_length=256,)
    type = fields.ForeignKeyField(
        'models.Type',
        related_name='title',
        on_delete=fields.OnDelete.CASCADE,
    )
    description = fields.TextField(null=True,)
    rating = fields.DecimalField(
        max_digits=2,
        decimal_places=1,
        validators=[
            MinValueValidator(NULL),
            MaxValueValidator(MAX_RATING_NUMBER),
        ],
    )
    director = fields.CharField(max_length=256, null=True,)
    release_year = fields.SmallIntField(validators=[MinValueValidator(NULL)],)
    genre = fields.CharField(max_length=256, null=True,)
