from setuptools import setup, find_packages

setup(
    name="bug_finder",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "google-adk",
        "google-generativeai",
    ],
) 