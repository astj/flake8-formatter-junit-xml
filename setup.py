from __future__ import with_statement
import setuptools

requires = [
    "flake8 > 3.0.0",
    "junit-xml >= 1.8"
]

readme = open('README.rst').read()

setuptools.setup(
    name="flake8_formatter_junit_xml",
    license="MIT",
    version="0.0.5",
    description="JUnit XML Formatter for flake8",
    long_description=readme,
    author="Asato Wakisaka",
    author_email="asato.wakisaka@gmail.com",
    url="https://github.com/astj/flake8-formatter-junit-xml",
    packages=setuptools.find_packages(exclude=['examples']),
    install_requires=requires,
    entry_points={
        'flake8.report': [
            'junit-xml = flake8_formatter_junit_xml:JUnitXmlFormatter',
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
