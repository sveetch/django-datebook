from setuptools import setup, find_packages

setup(
    name='django-datebook',
    version=__import__('datebook').__version__,
    description=__import__('datebook').__doc__,
    long_description=open('README.rst').read(),
    author='David Thenon',
    author_email='sveetch@gmail.com',
    url='http://pypi.python.org/pypi/django-datebook',
    license='MIT',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        "Development Status :: 5 - Production/Stable",
        'Environment :: Web Environment',
        'Framework :: Django',
        "Framework :: Django :: 1.6",
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[
        'Django>=1.6,<1.7',
        'django-assets>=0.8,<0.12',
        'autobreadcrumbs>=1.0,<2.0.0',
        'django-braces>=1.2.0,<1.4',
        'django-crispy-forms==1.5.2',
        'crispy-forms-foundation==0.5.3',
        'arrow==0.7.0',
        'yuicompressor==2.4.8',
    ],
    include_package_data=True,
    zip_safe=False
)