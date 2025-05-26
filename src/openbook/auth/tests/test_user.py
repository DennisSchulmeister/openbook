# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.contrib.auth       import get_user_model
from django.core.exceptions    import ValidationError
from django.test               import TestCase

from ..middleware.current_user import reset_current_user
from ..                        import models

class User_Model_Tests(TestCase):
    """
    Tests for the `User` and `UserProfile` models.
    """
    def test_user_creation_without_email(self):
        """
        The e-mail address should be obligatory when a new user is created.
        """
        # Directly saving without validation works
        User = get_user_model()
        User.objects.create_user("test1", password="test1234")

        # Model validation should raise an exception
        with self.assertRaises(ValidationError):
            user = User(username="test2", password="test1234")
            user.full_clean()
            user.save()

    def test_user_profile_created(self):
        """
        Each user should have a user profile, automatically created when a new
        user is created.
        """
        # User profile gets automatically created
        User = get_user_model()
        user = User.objects.create_user("test", password="test1234", email="test@example.com")

        self.assertEqual(
            models.UserProfile.objects.filter(user=user).count(), 1,
            "User profile was not created when a new user is created."
        )

        # User profile remains untouched after re-saving the user
        user_profile = user.profile
        user_profile.description = "Should not get lost!"

        user.save()

        self.assertIs(
            user_profile, user.profile,
            "User profile was overwritten when the user was saved again."
        )

        self.assertEqual(
            user_profile.description, user.profile.description,
            "User profile description got lost after saving user."
        )

class User_ViewSet_Test(TestCase):
    """
    Tests for the `UserViewSet` REST API.
    """
    def setUp(self):
        reset_current_user()