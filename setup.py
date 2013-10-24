from setuptools import setup, find_packages

setup(
    name='shift',
    version='0.1.0',
    description='Simple migrations for python ORMs',
    long_description='',
    keywords='python, peewee, migrations',
    author='Cameron A. Stitt',
    author_email='cameron@castitt.com',
    url='https://github.com/cam-stitt/shift',
    license='BSD',
    packages=find_packages(),
    zip_safe=False,
    install_requires=['peewee', 'termcolor'],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
)
