from setuptools import setup, find_packages

setup(
    name="pybustcall",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.28.0",
        "pydantic>=1.10.0",
        "asyncio-mqtt>=0.13.0"
    ],
    extras_require={
        "dev": ["pytest>=7.0.0", "black>=22.0.0", "mypy>=0.991"]
    },
    python_requires=">=3.8",
    author="OBINexus Team",
    description="Python binding for OBINexus Bustcall cache management system",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown"
)
