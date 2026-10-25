from setuptools import setup

setup(
    name="vantage-cli",
    version="1.0.0",
    description="Instant network data retrieval and geolocation CLI.",
    author="Your Name",
    py_modules=["main", "api", "cli"],
    install_requires=[
        "requests>=2.25.1",
    ],
    entry_points={
        "console_scripts": [
            "vantage=main:main",
        ],
    },
)