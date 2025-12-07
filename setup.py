from setuptools import setup, find_packages

setup(
    name="ApopToSiS",
    version="3.0.0",
    packages=find_packages(),
    package_dir={"ApopToSiS": "."},
    license="MIT",
    author="FluxAI Runtime Contributors",
    description="ApopAI v3 — PrimeFlux-powered runtime with ICM, LCM, and three-agent cognition loop",
    python_requires=">=3.11",
)
