from distutils.core import setup

setup(
    name='distcache',
    version='0.1.1.1',
    author='Wasim Akram Khan',
    keywords='open-source, cache, distributed-cache, in-memory, database',
    description='Distcache is a python open-source distributed in-memory cache and database.',
    packages=['distcache', 'usage', 'benchmark', 'tests', 'docs'],
    license='MIT License ',
    long_description=open('docs/pypi_readme.md').read(),
    project_urls={
        "Source Code": "https://github.com/wasimusu/distcache",
    },
)
