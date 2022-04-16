from setuptools import setup, find_packages
from os import path
from json import loads


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open("about.json") as about:
    jd = loads(about.read())
    
    
setup(
    name=jd["project"],
    version=jd["version"],
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    python_requires='>=3.6, <4',
    install_requires=[
        'nautical',
        'flask',
        'flask_restful',
        'singleton_decorator',
        'waitress'
    ],
    url=jd["url"],
    download_url='{}/archive/v_{}.tar.gz'.format(jd["url"], jd["version"].replace(".", "")),
    description='A simple rest application that exposes information gathered from the nautical library.',
    author=jd["author"],
    author_email=jd["email"],
    package_data={},
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'nautical_rest=nautical_api.app:main'
        ]
    },
)
