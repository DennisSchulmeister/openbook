---
mode: 'agent'
---
Please suggest unit tests for the DRF REST webservice implemented in`…ViewSet`.

* Inherit from `django.test.TestCase`
* Name the class `XYZ_ViewSet_Tests`.
* Write a docstring for the class, e.g.:  "Tests for the `SiteViewSet` REST API."
* Keep method names short and concise, e.g.: "test_role_assigned_on_accept"
* Write a short and concise docstring for each method, e.g.: "Role should be assigned when access request is accepted."
* If needed write a `setUp` method to create any necessary objects or data.
* The `setUp` method needs no docstring.
* The list operation always returns a JSON object like this: {'count': 1, 'next': None, 'previous': None, 'results': [...]}`
* The list operation uses query parameter `_search` for searching.
* The list operation uses query parameter `_sort` for sorting.
* The list operation uses query parameters `_page`, and `_page_size` for pagination.
* REST calls typically require an authenticated user and appropriate model permissions.
* Please also test create, update, partial update, and delete operations.
* Please also test that operations without required permissions fail with a 403 Forbidden response.
* Don't leak object existence. DRF returns 404 instead of 403 Forbidden for non-existing objects.
* For partial updates set the `format="json"` argument in the patch call when the model contains file fields.
* Use `APIClient.login()` instead of `APIClient.force_authentication()`.