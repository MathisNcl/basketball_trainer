import factory
from factory import fuzzy
from faker import Faker

from bball_trainer import models, settings
from bball_trainer.models.database import SessionScoped

faker = Faker(locale="fr-FR")


class BaseFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        sqlalchemy_session = SessionScoped
        sqlalchemy_session_persistence = "commit"


class UserFactory(BaseFactory):
    class Meta:
        model = models.User
        sqlalchemy_get_or_create = "pseudo"

    pseudo = factory.Faker("user_name", locale=settings.LANGUAGE_CODE)
    password_hash = factory.Faker("swift", locale=settings.LANGUAGE_CODE)

    last_name = factory.Faker("last_name", locale=settings.LANGUAGE_CODE)
    first_name = factory.Faker("first_name", locale=settings.LANGUAGE_CODE)
    age = fuzzy.FuzzyChoice([None, fuzzy.FuzzyInteger(13, 99)])

    @factory.post_generation
    def game(self, created, extracted, **kwargs):
        from tests.utils.factories import GameRecordFactory  # noqa

        if created and extracted:
            GameRecordFactory(user=self.pseudo, **kwargs)


class GameRecordFactory(BaseFactory):
    class Meta:
        model = models.GameRecord

    score = fuzzy.FuzzyInteger(0, 30)
