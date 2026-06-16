#!/usr/bin/env python3
"""
Setup script for Hammerspace API Python SDK
"""

from setuptools import setup, find_packages
import os

# Read the README file for long description
def read_file(filename):
    """Read a file and return its contents."""
    with open(os.path.join(os.path.dirname(__file__), filename), encoding='utf-8') as f:
        return f.read()

# Get the version from __init__.py
def get_version():
    """Extract version from __init__.py."""
    version_file = os.path.join(os.path.dirname(__file__), 'hammerspace', '__init__.py')
    version_dict = {}
    with open(version_file, encoding='utf-8') as f:
        exec(f.read(), version_dict)
    return version_dict.get('__version__', '0.1.0')

setup(
    name='hammerspace-api-client',
    version=get_version(),
    author='Hammerspace',
    author_email='support@hammerspace.com',
    description='Python API client for the Hammerspace data management platform',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    url='https://github.com/hammerspace/hammerspace-api-python-sdk',
    project_urls={
        'Bug Reports': 'https://github.com/hammerspace/hammerspace-api-python-sdk/issues',
        'Source': 'https://github.com/hammerspace/hammerspace-api-python-sdk',
        'Documentation': 'https://hammerspace-api-python-sdk.readthedocs.io',
    },
    packages=find_packages(exclude=['tests', 'tests.*', 'SampleScripts', 'SampleScripts.*']),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Filesystems',
        'Topic :: System :: Systems Administration',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
    install_requires=[
        'requests>=2.20.0',
        'python-dotenv>=1.0.0',
        'urllib3>=1.26.0',
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0',
            'pytest-asyncio>=0.21.0',
            'black>=23.0.0',
            'isort>=5.12.0',
            'flake8>=6.0.0',
            'mypy>=1.0.0',
            'pre-commit>=3.0.0',
            'bandit>=1.7.0',
            'safety>=2.0.0',
        ],
        'docs': [
            'sphinx>=7.0.0',
            'sphinx-rtd-theme>=1.2.0',
            'sphinx-autodoc-typehints>=1.23.0',
        ],
    },
    keywords='hammerspace api storage data-management cloud-storage',
    entry_points={
        'console_scripts': [
            # Future CLI tool
            # 'hammerspace-cli=hammerspace.cli:main',
        ],
    },
    include_package_data=True,
    zip_safe=False,
)