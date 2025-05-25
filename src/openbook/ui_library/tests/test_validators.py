# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.core.exceptions import ValidationError
from django.test            import TestCase
from ..                     import validators

class TestValidators(TestCase):
    """
    Test cases for validator functions.
    """
    
    def test_validate_library_name(self):
        """
        Library names should follow similar rules as on npmjs.org.
        """
        validators.validate_library_name("test")
        validators.validate_library_name("@test/test")
        
        with self.assertRaises(ValidationError):
            validators.validate_library_name("a")
        with self.assertRaises(ValidationError):
            validators.validate_library_name("a#b")
        with self.assertRaises(ValidationError):
            validators.validate_library_name("@a")
        with self.assertRaises(ValidationError):
            validators.validate_library_name("@a$b")
        with self.assertRaises(ValidationError):
            validators.validate_library_name("@a/b")
        with self.assertRaises(ValidationError):
            validators.validate_library_name("@a/b!c")
        with self.assertRaises(ValidationError):
            validators.validate_library_name("@a/b.c-xyz")
        
    def test_validate_version_number(self):
        """
        Version numbers use semver format.
        """
        validators.validate_version_number("1.2.3")
        validators.validate_version_number("1.2.3-beta")
        validators.validate_version_number("1.2.3+build")
        validators.validate_version_number("1.2.3-beta+build")
        
        with self.assertRaises(ValidationError):
            validators.validate_version_number("a")
