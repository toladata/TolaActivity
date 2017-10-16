__author__ = 'glind'
# Fix: email is not unique.
# from django.contrib.auth.models import User
# User._meta.local_fields[1].__dict__['max_length'] = 75
# User._meta.get_field('email')._unique = True
