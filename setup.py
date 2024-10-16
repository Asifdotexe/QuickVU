from setuptools import setup, find_packages

setup(
    name='customer_analysis_tool',
    version='0.1.0',
    description='A reusable tool for customer sales and marketing data analysis',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'seaborn',
        'matplotlib',
        'scikit-learn',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
