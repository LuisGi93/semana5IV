import os

from setuptools import setup, find_packages


setup(
    # Application name:
    name="Recetas_cocina",

    # Version number (initial):
    version="0.1.0",

    # Application author details:
    author="Luis Gil Guijarro",
    author_email="luisgguijarro@correo.ugr.es",

    # Packages

    # Include additional files into the package
    include_package_data=True,

    # Details
    url="https://github.com/LuisGi93/",

    #
    # license="LICENSE.txt",
    description="GPL-3.0",

    # long_description=open("README.txt").read(),

    # Dependent packages (distributions)
    install_requires=[
  "Flask==0.10.1",
  "Flask-SQLAlchemy==2.1",
  "Jinja2==2.7.1",
  "Flask-Login==0.3.2",
   "Flask-Bcrypt==0.7.1",
  "Flask-wtf==0.13.1",
  "Flask-security==1.7.5",
  "Flask-session==0.3.0",
  "flask-migrate==2.0.0",
  "flask-testing==0.6.1",
    ],
    packages=find_packages()
)

