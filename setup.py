from setuptools import setup, find_packages

setup(
    name='quickvu',
    version='0.1.0',
    description='A no-code solution to data analysis needs',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'seaborn',
        'matplotlib',
        'scikit-learn',
        'streamlit'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
