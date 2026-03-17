from setuptools import setup, find_packages

setup(
    name="schema-vault",
    version="1.0.0",
    description="Database schema management and migration CLI",
    author="Tristan Wentzel",
    packages=find_packages(),
    install_requires=[
        "psycopg2-binary>=2.9",
        "PyMySQL>=1.1",
        "tomli>=2.0; python_version < '3.11'",
        "click>=8.1",
    ],
    entry_points={
        "console_scripts": [
            "sv=schema_vault.cli:main",
        ],
    },
    python_requires=">=3.9",
    license="MIT",
)
