# Test exercise for Badi by Carmelo Acosta 


# Run all tests

From the root directory (where is located manage.py file) run

    python manage.py test

# Run a single test

From the root directory (where is located manage.py file) run

    python manage.py test badi.tests.<test_file_name>.<test_class_name>.<test_name>

Example:

    python manage.py test badi.tests.tests_sunlight_hours.SunlightHoursTestCase.test__get_apartment_dawn__ok
