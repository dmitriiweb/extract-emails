from setuptools import setup

setup(
    name='extract_emails',
    version='1.0.1',
    packages=['extract_emails'],
    url='https://github.com/dmitriiweb/extract-emails',
    license='MIT',
    author='Dmitrii K',
    author_email='winston.smith.spb@gmail.com',
    description='Extract email addresses from given URL.',
    install_requires=[
        'requests',
        'beautifulsoup4',
    ],
)
