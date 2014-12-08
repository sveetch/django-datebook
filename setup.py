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
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[
        'autobreadcrumbs >= 1.0',
        'django-braces>=1.2.0,<1.4',
        'crispy-forms-foundation>=0.3.5',
        'arrow',
    ],
    include_package_data=True,
    zip_safe=False
)