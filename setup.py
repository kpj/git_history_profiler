from setuptools import setup, find_packages


setup(
    name='git_history_profiler',
    version='0.0.1',

    description='Performance and and stability profiling over the git commit history.',

    setup_requires=['setuptools-markdown'],
    long_description_markdown_filename='README.md',

    url='https://github.com/kpj/git_history_profiler',

    author='kpj',
    author_email='kpjkpjkpjkpjkpjkpj@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only'
    ],

    keywords='git profiling',
    packages=find_packages(exclude=['tests']),

    install_requires=[
        'sh', 'pyyaml', 'click', 'tqdm',
        'pandas', 'seaborn', 'matplotlib'
    ],

    entry_points={
        'console_scripts': [
            'git_history_profiler=git_history_profiler:main',
        ],
    }
)
