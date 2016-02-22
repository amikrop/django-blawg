from os.path import join, dirname
from setuptools import setup

import blawg


with open(join(dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

setup(
    name='django-blawg',
    version=blawg.__version__,
    author='Aristotelis Mikropoulos',
    author_email='amikrop@gmail.com',
    description='Simple blogging application',
    long_description=README,
    license='BSD',
    url='https://github.com/amikrop/django-blawg',
    download_url='https://github.com/amikrop/django-blawg',
    packages=['blawg'],
    install_requires=[
        'Django>=1.9',
        'django-mptt>=0.8',
        'django-autoslug>=1.9',
    ],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: News/Diary',
    ],
)
