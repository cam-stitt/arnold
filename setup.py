from setuptools import setup, find_packages

install_requires = ['peewee', 'termcolor']

try:
    import importlib
except ImportError:
    install_requires.append('importlib')

setup(
    name='arnold',
    version='0.3.7',
    description='Simple migrations for python ORMs',
    long_description='',
    keywords='python, peewee, migrations',
    author='Cameron A. Stitt',
    author_email='cameron@castitt.com',
    url='https://github.com/cam-stitt/arnold',
    license='BSD',
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    zip_safe=False,
    install_requires=install_requires,
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
)
