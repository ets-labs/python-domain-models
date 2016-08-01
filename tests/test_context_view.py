"""ContextViews tests."""

import datetime

import unittest2 as unittest

from domain_models import models
from domain_models import fields
from domain_models import views


class Photo(models.DomainModel):
    """Photo DomainModel to be attached to profile."""
    id = fields.Int()
    title = fields.String()
    path = fields.String()
    public = fields.Bool(default=False)


class Profile(models.DomainModel):
    """Profile DomainModel to be tested."""
    id = fields.Int()
    name = fields.String()
    birth_date = fields.Date()
    business_address = fields.String()
    home_address = fields.String()
    main_photo = fields.Model(Photo)
    photos = fields.Collection(Photo)


class PublicProfile(views.ContextView):
    """Profile data in public context."""
    __model_cls__ = Profile

    def _get_oid(self):
        """Calculate open id.

        :rtype: int
        """
        return self.__model__.id << 8

    def _get_photos(self):
        photos = []
        for photo in self.__model__.photos:
            photo_data = PublicPhoto(photo).get_data()
            if photo_data:
                photos.append(photo_data)
        return photos

    def get_data(self):
        main_photo = PublicPhoto(self.__model__.main_photo)
        return {
            'oid': self._get_oid(),
            'name': self.__model__.name,
            'business_address': self.__model__.business_address,
            'main_photo': main_photo.get_data(),
            'photos': self._get_photos()
        }


class PrivateProfile(views.ContextView):
    """Profile data in private context."""
    __model_cls__ = Profile

    def _get_photos(self):
        photos = []
        for photo in self.__model__.photos:
            photo_data = PrivatePhoto(photo).get_data()
            if photo_data:
                photos.append(photo_data)
        return photos

    def get_data(self):
        main_photo = PrivatePhoto(self.__model__.main_photo)
        return {
            'id': self.__model__.id,
            'name': self.__model__.name,
            'birth_date': self.__model__.birth_date,
            'business_address': self.__model__.business_address,
            'home_address': self.__model__.home_address,
            'main_photo': main_photo.get_data(),
            'photos': self._get_photos()
        }


class PublicPhoto(views.ContextView):
    """Photo data in public context."""
    __model_cls__ = Photo

    def _get_oid(self):
        return self.__model__.id << 8

    def get_data(self):
        if not self.__model__.public:
            return {}
        return {
            'oid': self._get_oid(),
            'title': self.__model__.title,
            'path': self.__model__.path
        }


class PrivatePhoto(views.ContextView):
    __model_cls__ = Photo

    def get_data(self):
        return {
            'id': self.__model__.id,
            'title': self.__model__.title,
            'path': self.__model__.path
        }


class ModelUndefinedContext(views.ContextView):
    """Model undefined"""

    def get_data(self):
        pass


class WrongModelContext(views.ContextView):
    """Wrong model defined."""
    __model_cls__ = type

    def get_data(self):
        pass


class GetterUndefinedContext(views.ContextView):
    """Getter undefined."""
    __model_cls__ = Profile


class TestContextView(unittest.TestCase):
    main_photo = Photo(id=1, title='main photo', path='path/to/the/main/photo',
                       public=True)
    photo2 = Photo(id=2, title='photo 2', path='path/to/the/photo2',
                   public=False)
    photo3 = Photo(id=3, title='photo 3', path='path/to/the/photo3',
                   public=True)
    profile = Profile(id=1,
                      name='John',
                      birth_date=datetime.date(1950, 4, 18),
                      business_address='John works here',
                      home_address='John lives here',
                      main_photo=main_photo,
                      photos=[main_photo, photo2, photo3])

    def test_wrong_model_passed(self):
        with self.assertRaises(TypeError):
            PublicProfile("invalid argument")

    def test_model_undefined(self):
        with self.assertRaises(TypeError):
            ModelUndefinedContext("it doesn't matter")

    def test_wrong_model_defined(self):
        with self.assertRaises(TypeError):
            WrongModelContext("it doesn't matter")

    def test_getter_undefined(self):
        contextual_view = GetterUndefinedContext(self.profile)
        with self.assertRaises(NotImplementedError):
            contextual_view.get_data()

    def test_context_view(self):
        public_context = PublicProfile(self.profile)
        private_context = PrivateProfile(self.profile)

        self.assertDictEqual(public_context.get_data(), {
            'oid': 256,
            'name': 'John',
            'business_address': 'John works here',
            'main_photo': {
                'oid': 256,
                'title': 'main photo',
                'path': 'path/to/the/main/photo'
            },
            'photos': [{
                'oid': 256,
                'title': 'main photo',
                'path': 'path/to/the/main/photo'
            }, {
                'oid': 768,
                'title': 'photo 3',
                'path': 'path/to/the/photo3'
            }]
        })

        self.assertDictEqual(private_context.get_data(), {
            'id': 1,
            'name': 'John',
            'birth_date': datetime.date(1950, 4, 18),
            'business_address': 'John works here',
            'home_address': 'John lives here',
            'main_photo': {
                'id': 1,
                'title': 'main photo',
                'path': 'path/to/the/main/photo'
            },
            'photos': [{
                'id': 1,
                'title': 'main photo',
                'path': 'path/to/the/main/photo'
            }, {
                'id': 2,
                'title': 'photo 2',
                'path': 'path/to/the/photo2'
            }, {
                'id': 3,
                'title': 'photo 3',
                'path': 'path/to/the/photo3'
            }]
        })
