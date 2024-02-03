from setuptools import setup, find_packages

setup(
    name='disco-cli',
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'requests',
        'sseclient-py'
    ],
    entry_points={
        'console_scripts': [
            'disco = discocli.cli:main',
        ],
    },
)
