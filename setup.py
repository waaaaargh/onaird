import setuptools
from setuptools import version

setuptools.setup(
    name="onaird",
    version="0.1.0",
    author="Johannes 'waaaaargh' Fürmann",
    author_email="fuermannj+pypi@gmail.com",
    description="OnAir host service",
    package_dir={"":"src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",

    install_requires=[
        'fire',
        'requests'
    ],

    # Define Entry Points
    entry_points={
        'console_scripts': [
            'onaird = onaird.cli:main'
        ]
    }
)