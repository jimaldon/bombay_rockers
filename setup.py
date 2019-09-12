import setuptools
from setuptools import find_packages


packages = find_packages()


SETUP = dict(
    name='bombay-party',
    packages=packages,
    entry_points={
        'console_scripts': [
            'server = app.app:main',
        ],
    },
)


if __name__ == '__main__':
    setuptools.setup(**SETUP)
