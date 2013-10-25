from setuptools import setup

setup(
    name='arnold',
    version='0.3.0',
    description='Simple migrations for python ORMs',
    long_description='',
    keywords='python, peewee, migrations',
    author='Cameron A. Stitt',
    author_email='cameron@castitt.com',
    url='https://github.com/cam-stitt/arnold',
    license='BSD',
    packages=['arnold'],
    zip_safe=False,
    install_requires=['peewee', 'termcolor'],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
)
