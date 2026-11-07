#!/usr/bin/env python3
"""
Setup script for MathType Clone
"""

from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='mathtype-clone',
    version='1.0.0',
    description='A LaTeX equation editor for Linux - MathType Clone',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='asdullah1880-hub',
    author_email='',
    url='https://github.com/asdullah1880-hub/Mathtype-clone',
    packages=find_packages(),
    py_modules=['mathtype_clone'],
    install_requires=[
        'PyQt5>=5.15.0',
        'matplotlib>=3.0.0',
        'latex2mathml>=3.0.0',
        'numpy>=1.20.0',
    ],
    entry_points={
        'gui_scripts': [
            'mathtype-clone=mathtype_clone:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Education',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Text Editors',
    ],
    python_requires='>=3.8',
    keywords='mathtype equation editor latex mathematics',
    project_urls={
        'Bug Reports': 'https://github.com/asdullah1880-hub/Mathtype-clone/issues',
        'Source': 'https://github.com/asdullah1880-hub/Mathtype-clone',
    },
)
