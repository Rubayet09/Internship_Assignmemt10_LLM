# setup.py
from setuptools import setup, find_packages

setup(
    name="projectscrape",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "psycopg2-binary>=2.9.10",
        "pytest>=8.3.4",
        "pytest-cov>=6.0.0",
        "scrapy>=2.12.0",
        "sqlalchemy>=2.0.36",
    ],
    python_requires=">=3.10",
)