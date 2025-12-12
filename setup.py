from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="primeflux-ai",
    version="3.0.0",
    packages=find_packages(),
    package_dir={"ApopToSiS": "."},
    license="MIT",
    author="ApopTosis AI LLC",
    author_email="info@apoptosisai.com",
    description="PrimeFlux AI — Offline-first AGI runtime with multi-agent coordination",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.11",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "apop=apop:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="ai agi primeflux apoptosis quantacoin offline llm",
    project_urls={
        "Homepage": "https://github.com/pdk5mjmvfd-cpu/primeFluX.ai",
        "Documentation": "https://github.com/pdk5mjmvfd-cpu/primeFluX.ai#readme",
        "Bug Reports": "https://github.com/pdk5mjmvfd-cpu/primeFluX.ai/issues",
    },
)
