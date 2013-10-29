=======
hipchav
=======

A minimal Python HipChat client with command-line interface.

Setup
=====

Install ``hipchav`` from source, or using ``pip``::

    pip install hipchav

Then you'll need to configure it with your HipChat API key::

    export HIPCHAT_V1_TOKEN=thisismyhextokentheygaveme

or for the v2 API::

    export HIPCHAT_V2_TOKEN=thisismyhextokentheygaveme

Usage
=====

HipChav currenly only supports two functions, listing rooms and sending messages.

Listing rooms
-------------

::

    $ hipchav.py rooms
    Developers
    Whole company
    Bots only

Sending messages
----------------

Messages are quite straight-forward to send::

    $ hipchav.py message 'Whole company' 'Freshly baked cookies in the kitchen'


You can also change their color and send notifications to people in the room::

    $ hipchav.py message --color=red --notify 'Developers' 'Um, the build is broken'

With the v1 API, you can also choose who the message appears from::

    $ hipchav.py message --from=Glados 'Whole company' 'Dispensing deadly neurotoxin'

Check its usage information for full options::

    $ hipchav.py --help


Changelog
=========

v0.1.1
------

- Also support v1 API, autodetect based on environment variables present
- For v1 API, support the from field with the ``--from`` option.
- You'll need to update ``HIPCHAT_AUTH_TOKEN`` to either ``HIPCHAT_V1_TOKEN`` or ``HIPCHAT_V2_TOKEN``

v0.1.0
------

- Initial release, supports listing rooms and messaging with color and notifications
