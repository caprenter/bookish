from django.test import TestCase
import bookish.models as m
import uuid


class UUIDModelSubClass(m.UUIDModel):
    pass


class UUIDTestCase(TestCase):
    def setUp(self):
        UUIDModelSubClass.objects.create()

    def test_uuid(self):
        uuid_model_object = UUIDModelSubClass.objects.all()[0]
        # Check that the uuid field is being used as the pk
        self.assertEqual(uuid_model_object.pk, uuid_model_object.uuid)
        # Check that the uuid field is a valid uuid by attempting to create a
        # UUID object with it.
        uuid.UUID(uuid_model_object.uuid)
