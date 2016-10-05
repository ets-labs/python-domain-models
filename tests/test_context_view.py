"""ContextViews tests."""
import datetime

import unittest2 as unittest

from domain_models import models
from domain_models import fields
from domain_models import views


class Photo(models.DomainModel):
    """Photo model to be attached to profile."""
    id = fields.Int()
    title = fields.String()
    path = fields.String()
    public = fields.Bool(default=False)


class Profile(models.DomainModel):
    """Profile model to be tested."""
    id = fields.Int()
    name = fields.String()
    birth_date = fields.Date()
    business_address = fields.String()
    home_address = fields.String()
    main_photo = fields.Model(Photo)
    photos = fields.Collection(Photo)


class ProfilePublicContext(views.ContextView):
    """Profile data in public context."""
    __model_cls__ = Profile
    __include__ = (Profile.name, Profile.business_address)

    @property
    def oid(self):
        """Calculate open id.

        :rtype: int
        """
        return self.__model__.id << 8

    @property
    def photos(self):
        """Return list of public photos' data.

        :rtype: list
        """
        photos = []
        for photo in self.__model__.photos:
            if not photo.public:
                continue
            photo_data = PhotoPublicContext(photo).get_data()
            if photo_data:
                photos.append(photo_data)
        return photos

    @property
    def main_photo(self):
        """Return main photo data within public context.

        :rtype: dict
        """
        return PhotoPublicContext(self.__model__.main_photo).get_data()


class ProfilePrivateContext(views.ContextView):
    """Profile data in private context."""
    __model_cls__ = Profile

    @property
    def photos(self):
        """Return list of private photos' data.

        :rtype: list
        """
        photos = []
        for photo in self.__model__.photos:
            photo_data = PhotoPrivateContext(photo).get_data()
            if photo_data:
                photos.append(photo_data)
        return photos

    @property
    def main_photo(self):
        """Return public data of main photo.

        :rtype: dict
        """
        return PhotoPrivateContext(self.__model__.main_photo).get_data()


class PhotoPublicContext(views.ContextView):
    """Photo data in public context."""
    __model_cls__ = Photo
    __include__ = (Photo.title, Photo.path)

    @property
    def oid(self):
        """Calculate open id.

        :rtype: int
        """
        return self.__model__.id << 8


class PhotoPrivateContext(views.ContextView):
    __model_cls__ = Photo
    __exclude__ = (Photo.public,)


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
            ProfilePublicContext("invalid argument")

    def test_model_undefined(self):
        with self.assertRaises(AttributeError):
            class ModelUndefinedContext(views.ContextView):
                pass

    def test_wrong_model_defined(self):
        with self.assertRaises(TypeError):
            class WrongModelContext(views.ContextView):
                __model_cls__ = type

    def test_include_exclude(self):
        with self.assertRaises(AttributeError):
            class WrongContext(views.ContextView):
                __model_cls__ = Profile
                __include__ = (Profile.birth_date,)
                __exclude__ = (Profile.business_address,)

    def test_context_view(self):
        public_profile = ProfilePublicContext(self.profile)
        private_profile = ProfilePrivateContext(self.profile)

        self.assertEqual(public_profile.oid, 256)
        self.assertEqual(public_profile.name, 'John')
        self.assertEqual(public_profile.business_address, 'John works here')
        self.assertDictEqual(public_profile.main_photo, {
            'oid': 256,
            'title': 'main photo',
            'path': 'path/to/the/main/photo'
        })
        self.assertEqual(public_profile.photos, [{
            'oid': 256,
            'title': 'main photo',
            'path': 'path/to/the/main/photo'
        }, {
            'oid': 768,
            'title': 'photo 3',
            'path': 'path/to/the/photo3'
        }])

        self.assertDictEqual(public_profile.get_data(), {
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

        self.assertEqual(private_profile.id, 1)
        self.assertEqual(private_profile.name, 'John')
        self.assertEqual(private_profile.birth_date,
                         datetime.date(1950, 4, 18))
        self.assertEqual(private_profile.business_address, 'John works here')
        self.assertEqual(private_profile.home_address, 'John lives here')
        self.assertDictEqual(private_profile.main_photo, {
            'id': 1,
            'title': 'main photo',
            'path': 'path/to/the/main/photo'
        })
        self.assertEqual(private_profile.photos, [{
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
        }])

        self.assertDictEqual(private_profile.get_data(), {
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
