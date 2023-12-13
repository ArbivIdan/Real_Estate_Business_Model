from setuptools import setup, find_packages

setup(
    name='mortgage_calculator',
    version='0.1.0',
    packages=find_packages(),  # Automatically discover and include all packages
    install_requires=[
        # List your package dependencies here
        'numpy',
    ],
    entry_points={
        'console_scripts': [
            # Define any command-line scripts here
            'run_main = mortgage_calculator.src.main:main_function',
        ],
    },
    author='Idan Arbiv',
    author_email='idan.arbiv@gmail.com',
    description='A project for calculate mortgage',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/idan_arbiv/mortgage_calculator',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
