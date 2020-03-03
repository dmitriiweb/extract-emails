from setuptools import setup

with open('README.rst') as readme:
    r = str(readme.read())

setup(
    name='extract_emails',
    version='3.0.5',
    packages=['extract_emails'],
    url='https://github.com/dmitriiweb/extract-emails',
    license='MIT',
    author='Dmitrii K',
    author_email='winston.smith.spb@gmail.com',
    description='Extract email addresses from given URL.',
    long_description=r,
    install_requires=[
        'requests>=2.18.4',
        'lxml>=4.1.1',
    ],
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
    ),
)
