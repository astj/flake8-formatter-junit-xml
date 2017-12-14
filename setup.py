from __future__ import with_statement
import setuptools

requires = [
    "flake8 > 3.0.0",
]

readme = open('README.rst').read()

setuptools.setup(
    name="flake8_formatting_junit",
    license="MIT",
    version="0.0.1",
    description="TBD",
    long_description=readme,
    author="Asato Wakisaka",
    author_email="asato.wakisaka@github.com",
    url="https://github.com/astj/flake8-formatting-junit",
    py_modules=['flake8_formatting_junit'],
    install_requires=requires,
    entry_points={
        'flake8.report': [
            'junit = flake8_formatting_junit:JUnitFormatter',
        ],
    },
    classifiers=[
        "Framework :: Flake8",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
    ],
)
