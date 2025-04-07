from setuptools import setup, find_packages

setup(
    name="super-fastapi-site",
    version="0.1.0",
    description="A FastAPI application with user authentication and CRUD operations",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "fastapi==0.104.1",
        "uvicorn==0.23.2",
        "sqlalchemy==2.0.23",
        "aiosqlite==0.19.0",
        "python-jose==3.3.0",
        "python-multipart==0.0.6",
        "python-dotenv==1.0.0",
        "pydantic==2.4.2",
    ],
    extras_require={
        "dev": [
            "pytest==7.4.3",
            "pytest-asyncio==0.21.1",
            "httpx==0.25.1",
            "pytest-cov==4.1.0",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
) 