from setuptools import setup, find_packages
import os

version = '0.4.0'

setup(name='collective.dancefloor',
      version=version,
      description="S&D extension to allow local newsletters",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Ramon Bartl, Stefan Eletzhofer',
      author_email='ramon.bartl@inquant.de, stefan.eletzhofer@inquant.de',
      url='https://svn.plone.org/svn/collective/collective.dancefloor/trunk',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'collective.dancing',
          'archetypes.schemaextender',
      ],
      entry_points="""
      # -*- entry_points -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
