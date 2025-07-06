from setuptools import find_packages, setup

setup(
    name="ranked_choice",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "Django>=4.2.0,<5.0.0",
        "djangorestframework>=3.14.0,<4.0.0",
        "psycopg2-binary>=2.9.6,<3.0.0",
        "gunicorn>=20.1.0,<21.0.0",
        "django-cors-headers>=4.0.0,<5.0.0",
        "python-dotenv>=1.0.0,<2.0.0",
        "pytest>=7.0.0,<8.0.0",
        "pytest-django>=4.5.2,<5.0.0",
    ],
)
