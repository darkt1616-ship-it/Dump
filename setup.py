"""
Setup configuration for Breach Research package
"""

from setuptools import setup, find_packages

# Leggi il README per la descrizione lunga
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Leggi i requirements
with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="breach-research",
    version="1.0.0",
    author="[Il Tuo Nome]",
    author_email="[tua.email@universita.it]",
    description="Research tool for credential stuffing and breach analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/[tuo-username]/breach-research",
    packages=find_packages(include=["src", "src.*"]),
    py_modules=["main"],
    package_dir={"": "."},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Topic :: Security",
        "Topic :: Scientific/Engineering",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "isort>=5.12.0",
        ],
        "gpu": [
            "cupy-cuda11x>=12.0.0",
        ],
        "notebook": [
            "jupyter>=1.0.0",
            "ipykernel>=6.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "breach-research=main:cli",
            "breach-generate=src.generator:genera_dataset",
            "breach-analyze=src.analyzer:main",
            "breach-test=src.security_tester:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    project_urls={
        "Bug Reports": "https://github.com/[tuo-username]/breach-research/issues",
        "Source": "https://github.com/[tuo-username]/breach-research",
    },
)

# Post-install script per creare le directory
if __name__ == "__main__":
    # Crea directory necessarie
    from pathlib import Path


    directories = ["data", "logs", "reports"]
    for dir_name in directories:
        Path(dir_name).mkdir(exist_ok=True)
        print(f"📁 Directory creata: {dir_name}")