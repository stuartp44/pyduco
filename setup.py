from setuptools import setup, find_packages

setup(
    name="pyduco",
    version="0.3.0",
    packages=find_packages(),
    install_requires=[
        "zeroconf",
        "requests",
        "pytest"
    ],
    author="Stuart Pearson",
    author_email="noreply@hnuk.net",
    description="A library to discover and interact with Duco air systems.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/stuartp44/ducopython",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)