
from setuptools import find_packages, setup


version = open('Ctl/VERSION').read().strip()
requirements = open('Ctl/requirements.txt').read().split("\n")
test_requirements = open('Ctl/requirements-test.txt').read().split("\n")


setup(
    name='django-inet',
    version=version,
    author='20C',
    author_email='code@20c.com',
    description='django internet utilities',
    long_description='',
    license='LICENSE.txt',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django :: 1.8',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages = find_packages(),
    include_package_data=True,
    url='https://github.com/20c/django-inet',
    download_url='https://github.com/20c/django-inet/%s' % version,

    install_requires=requirements,
    test_requires=test_requirements,

    zip_safe=True
)
