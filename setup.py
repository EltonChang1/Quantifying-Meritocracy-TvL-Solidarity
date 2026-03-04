from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="quantifying-meritocracy",
    version="1.0.0",
    author="Elton Chang",
    description="Extending Talent vs. Luck Model to Incorporate Solidarity",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Intended Audience :: Science/Research",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.21.0",
        "matplotlib>=3.4.0",
        "scipy>=1.7.0",
        "pandas>=1.3.0",
        "pytest>=6.2.0",
        "jupyter>=1.0.0",
        "ipython>=7.0.0",
        "scikit-learn>=0.24.0",
        "seaborn>=0.11.0",
        "networkx>=2.6.0",
        "tqdm>=4.62.0",
        "pyyaml>=5.4.0",
    ],
)
