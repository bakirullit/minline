from setuptools import setup, find_packages

setup(
    name="minline",
    version="0.1.0",
    description="Menu-inline framework for Telegram bots",
    author="bakirullit",
    packages=find_packages(include=["minline", "minline.*"]),
    include_package_data=True,
    install_requires=[
        "aiogram>=3.3",
        "redis>=5.0.0"
    ],
    python_requires=">=3.10",
)
