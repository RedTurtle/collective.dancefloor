Introduction
============

collective.dancefloor is a plugin for `Singing&Dancing <http://pypi.python.org/pypi/collective.dancing>`_
that allows to create different newsletters (not channels) in a site.
This is useful when in a Plone site there are some different editorial staffs and every staff should manage only his newsletter.

Installation
============
To install collective.dancefloor, you just add the product to the eggs in your buildout configuration

::

    [instance]
    eggs +=
        collective.dancefloor

Usage
=====
Installing this product, all folderish contents in the site could be a local newsletter.
This is made by a new field in "*Settings*" schemata that allows to enable/disable newsletter manage in that folder.

.. image:: http://dl.dropbox.com/u/8687422/local_newsletter_field.png
   :alt: The 'local newsletter' new field

Enabling a local newsletter, a new "*Newsletter*" tab appears and it allows users with "*Manage Local Newsletters*" permission to manage this newsletter like a normal newsletter for Singing&Dancing.

.. image:: http://dl.dropbox.com/u/8687422/local_newsletter_config.png
   :alt: The 'local newsletter' configuration

As you can see, it has typical S&D configuration panel, and here you can do all the things that you usually do in portal_newsletters.

Local newsletter managers
-------------------------

The most difference between Singing&Dancing and dancefloor is that in S&D the users with newsletter roles can access to portal_newsletters and can possibly manage all newsletters and channels.
With dancefloor, you can allow different groups or users to manage some specified local newsletters and deny others.
This is done simply with a new local role "*LocalNewsletterManager*"

.. image:: http://dl.dropbox.com/u/8687422/local_newsletter_sharing.png
   :alt: LocalNewsletterManager role

Warning
=======
Singing&Dancing uses a persistent queue object to manage queues for newsletters.
This queue is created the first time you send a newsletter, and is registered for portal_newsletters and is shared with all channels.
This means that if you wants to use collective.dancefloor after having already used S&D on your portal, you will have a shared queue, and the channel A (of local newsletter A) see also the queue of channel B (of local newsletter B).

This is easily fixable erasing the global queue, and allows local channels to create their own queue.
There is a view that do this "*clear_default_queue*", that should be called in portal_newsletters tool: *your_site_url/portal_newsletters/clear_default_queue*


Requirements
============

collective.dancefloor has been tested on Plone 3.3, 4.0 and 4.1. Is possible that also older Plone 3.x version can be used safely.

TODO and know issue
===================

* Provide a full test coverage

Credits
=======

Developed with the support of:

* `Regione Emilia Romagna`__

Regione Emilia Romagna supports the `PloneGov initiative`__.

__ http://www.regione.emilia-romagna.it/
__ http://www.plonegov.it/

Authors
=======

This product was originally created by Ramon Bartl, Stefan Eletzhofer.

Now is maintained by RedTurtle Technology team.

.. image:: http://www.redturtle.net/redturtle_banner.png
   :alt: RedTurtle Technology Site
   :target: http://www.redturtle.net/
