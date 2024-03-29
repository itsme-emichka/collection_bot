from tortoise.models import Model
from tortoise import fields
from tortoise.validators import MaxValueValidator, MinValueValidator


NULL: int = 0
MAX_RATING_NUMBER: int = 10


class User(Model):
    id = fields.IntField(pk=True,)
    username = fields.CharField(max_length=512,)
    first_name = fields.CharField(max_length=512, null=True,)
    last_name = fields.CharField(max_length=512, null=True,)


class Type(Model):
    id = fields.SmallIntField(pk=True,)
    name = fields.CharField(max_length=256, unique=True, null=True,)
    slug = fields.CharField(max_length=256,)


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
    image_url = fields.CharField(max_length=1024, null=True)

    def __str__(self) -> str:
        return self.name


class UserTitle(Model):
    user = fields.ForeignKeyField(
        'models.User',
        related_name='user_title',
        on_delete=fields.OnDelete.CASCADE
    )
    title = fields.ForeignKeyField(
        'models.Title',
        related_name='user_title',
        on_delete=fields.OnDelete.CASCADE,
    )
