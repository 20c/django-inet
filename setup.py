from setuptools import setup

version = open('facsimile/VERSION').read().strip()
requirements = open('facsimile/requirements.txt').read().split("\n")

setup(
    name='django-inet',
    version=version,
    author='20C',
    author_email='code@20c.com',
    description='django internet utilities',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=[
      'django_inet',
    ],
    url = 'https://github.com/20c/django-inet',
    download_url = 'https://github.com/20c/django-inet/%s' % version,
    include_package_data=True,
    install_requires=requirements,
    zip_safe=True
)
