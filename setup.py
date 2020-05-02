"""
extract_emails
"""
from setuptools import setup, find_packages

from extract_emails import __version__ as version

INSTALL_REQUIRES = []

EXTRAS_DEV_TESTFILES_COMMON = [
    "contextlib2; python_version<'3.0'",
    "mock",
    "six",
]

EXTRAS_DEV_LINT = [
    "flake8>=3.6.0,<3.7.0",
    "isort>=4.3.4,<4.4.0",
]

EXTRAS_DEV_TEST = [
    "coverage",
    "pytest>=3.10",
]

EXTRAS_DEV_DOCS = [
    "readme_renderer",
    "sphinx",
    "sphinx_rtd_theme>=0.4.0",
]

with open('README.rst') as readme:
    r = str(readme.read())

setup(
    name='extract_emails',
    version=version,
    packages=find_packages(exclude=['*test*']),
    url='https://github.com/dmitriiweb/extract-emails',
    license='MIT',
    author='Dmitrii K',
    author_email='dmitriik@tutanota.com',
    description='Extract email addresses from given URL.',
    long_description=r,
    install_requires=INSTALL_REQUIRES,
    extras_require={
        "dev": (EXTRAS_DEV_TESTFILES_COMMON +
                EXTRAS_DEV_LINT +
                EXTRAS_DEV_TEST +
                EXTRAS_DEV_DOCS),
        "dev-lint": (EXTRAS_DEV_TESTFILES_COMMON +
                     EXTRAS_DEV_LINT),
        "dev-test": (EXTRAS_DEV_TESTFILES_COMMON +
                     EXTRAS_DEV_TEST),
        "dev-docs": EXTRAS_DEV_DOCS,
        "timezone": ["pytz"],
    },
    keywords='extract emails email',
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
    ),
)
