from setuptools import setup, find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='nautical_api',
    version="0.0.1",
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    python_requires='>=3.6, <4',
    install_requires=[
        'nautical',
        'elasticsearch'
    ],
    url='https://github.com/barbacbd/nautical_api',
    download_url='https://github.com/barbacbd/nautical_api/archive/v_001.tar.gz',
    description='Scripts for the backend and database connection for the nautical API',
    author='Brent Barbachem',
    author_email='barbacbd@dukes.jmu.edu',
    package_data={'': ['*.json', '*.mysql']},
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'NauticalDatabaseProvider=nautical_api.__main__:main'
        ]
    },
)
