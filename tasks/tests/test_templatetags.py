from django.test import TestCase, RequestFactory
from tasks.templatetags.query_transform import query_transform

class TemplateTagsTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_query_transform_add_param(self):
        # Testing adding a new parameter to empty GET
        request = self.factory.get("/")
        result = query_transform(request, page=2)
        self.assertEqual(result, "page=2")

    def test_query_transform_update_param(self):
        # Testing updating an existing parameter
        request = self.factory.get("/?page=1&sort=name")
        result = query_transform(request, page=2)
        # Parameters might be in any order in urlencoded string
        self.assertIn("page=2", result)
        self.assertIn("sort=name", result)

    def test_query_transform_remove_param(self):
        # Testing removing a parameter by setting it to None
        request = self.factory.get("/?page=1&sort=name")
        result = query_transform(request, page=None)
        self.assertEqual(result, "sort=name")

    def test_query_transform_multiple_params(self):
        # Testing adding and updating multiple parameters at once
        request = self.factory.get("/?page=1")
        result = query_transform(request, page=5, sort="id", filter="active")
        self.assertIn("page=5", result)
        self.assertIn("sort=id", result)
        self.assertIn("filter=active", result)

    def test_query_transform_preserve_existing(self):
        # Testing that other parameters are not affected
        request = self.factory.get("/?search=work&status=done")
        result = query_transform(request, page=2)
        self.assertIn("search=work", result)
        self.assertIn("status=done", result)
        self.assertIn("page=2", result)