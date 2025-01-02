from setuptools import setup, find_packages

setup(
    name="property_rewriter",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "Django>=5.0.0",
        "psycopg2-binary>=2.9.9",
        "requests>=2.31.0",
    ],
    python_requires=">=3.10",
)