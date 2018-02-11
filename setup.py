from setuptools import setup

with open('README.rst') as readme:
    r = str(readme.read())

setup(
    name='extract_emails',
    version='2.0.0',
    packages=['extract_emails'],
    url='https://github.com/dmitriiweb/extract-emails',
    license='MIT',
    author='Dmitrii K',
    author_email='winston.smith.spb@gmail.com',
    description='Extract email addresses from given URL.',
    long_description=r,
    install_requires=[
        'requests==2.18.4',
        'lxml==4.1.1',
        'fake-useragent==0.1.10'
    ],
)
