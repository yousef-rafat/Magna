from setuptools import setup, find_packages

setup(
    name="magna",
    version="1.0.0",
    author="Yousef Gamaleldin",
    author_email="yrafat38@gmail.com",
    description="AI-powered embedding similarity search for documents",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yousef-rafat/Magna",
    packages=find_packages(),
    install_requires=open("requirements.txt").readlines(),
    entry_points={
        "console_scripts": [
            "magna = magna.main:main",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
