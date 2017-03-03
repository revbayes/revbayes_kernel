"""Setup script for revbayes_kernel package.
"""
import glob

DISTNAME = 'revbayes_kernel'
DESCRIPTION = 'A Jupyter kernel for RevBayes.'
LONG_DESCRIPTION = open('README.md', 'rb').read().decode('utf-8')
MAINTAINER = 'Simon Frost'
MAINTAINER_EMAIL = 'sdwfrost@gmail.com'
URL = 'http://github.com/sdwfrost/revbayes_kernel'
LICENSE = 'MIT'
REQUIRES = ["metakernel (>=0.19.0)", "jupyter_client (>=4.3.0)", "ipykernel"]
INSTALL_REQUIRES = ["metakernel >=0.19.0", "jupyter_client >=4.3.0", "ipykernel"]
PACKAGES = [DISTNAME]
PACKAGE_DATA = {DISTNAME: ['*.m'] + glob.glob('%s/**/*.m' % DISTNAME) }
CLASSIFIERS = """\
Intended Audience :: Science/Research
License :: OSI Approved :: BSD License
Operating System :: OS Independent
Programming Language :: Python
Programming Language :: Python :: 2.7
Programming Language :: Python :: 3.3
Programming Language :: Python :: 3.4
Topic :: Scientific/Engineering
Topic :: Software Development
Topic :: System :: Shells
"""
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('revbayes_kernel/__init__.py', 'rb') as fid:
    for line in fid:
        line = line.decode('utf-8')
        if line.startswith('__version__'):
            version = line.strip().split()[-1][1:-1]
            break


setup(
    name=DISTNAME,
    version=version,
    maintainer=MAINTAINER,
    maintainer_email=MAINTAINER_EMAIL,
    packages=PACKAGES,
    package_data=PACKAGE_DATA,
    include_package_data=True,
    url=URL,
    download_url=URL,
    license=LICENSE,
    platforms=["Any"],
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    classifiers=list(filter(None, CLASSIFIERS.split('\n'))),
    requires=REQUIRES,
    install_requires=INSTALL_REQUIRES
 )

