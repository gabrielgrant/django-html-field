from setuptools import setup

setup(
    name='django-html-field',
    version='0.1.3',
    packages=[
        'html_field',
        'html_field.db',
        'html_field.db.models',
        'html_field.forms',
        'html_field.tests',
    ],
    include_package_data=True,
    author='Gabriel Grant',
    author_email='g@briel.ca',
    license='LGPL',
    long_description=open('README').read(),
    url='http://github.org/gabrielgrant/django-html-field/',
)

