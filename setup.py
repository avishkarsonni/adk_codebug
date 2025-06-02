from setuptools import setup, find_packages

setup(
    name="bug_finder",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "google-adk>=1.0.0",
        "google-generativeai>=0.3.2",
        "python-dotenv>=1.0.0",
        "astroid>=3.0.1",  # For Python code analysis
        "pylint>=3.0.2"    # For bug detection
    ],
    python_requires=">=3.8",
    author="Your Name",
    description="A Google ADK-based system for finding and fixing bugs in Python code",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
) 