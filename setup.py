from setuptools import setup, find_packages

setup(
    name="falconeda",  # Name of your package
    version="0.1.0",   # Package version
    author="Riley Heiman",
    author_email="your_email@example.com",
    description="A Streamlit-based app for fast and interactive exploratory data analysis",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/falconeda",  # Replace with your GitHub repo
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "streamlit>=1.0",
        "pandas>=1.3",
        "numpy>=1.21",
        "altair>=4.2"
    ],
    entry_points={
        "console_scripts": [
            "falconeda=falconeda.main:run",  # Command-line entry point
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
