import setuptools


with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='telegraf_pyplug',
    version='0.1.1',
    author='Andrey Okulov',
    author_email='okulov@ya.ru',
    description='Telegraf_pyplug is a software library to simplify and standardize the development '
                'of python input plugins for the Telegraf',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ToolSense/telegraf_pyplug',
    package_data={"telegraf_pyplug": ["py.typed"]},
    packages=setuptools.find_packages(),
    zip_safe=False,
    install_requires=[
        'PyMySQL==0.10.0',
        'pytz==2020.1',
    ],
    extras_require={
        'devel': [
            'mypy>=0.782<1.0',
            'pylint>=2.5.3<3.0',
            'twine==3.2.0',
        ],
    },
    classifiers=[
        'Intended Audience :: System Administrators',
        'Intended Audience :: Developers',
        'Topic :: System :: Monitoring',
        'Environment :: Plugins',
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
    ],
)
