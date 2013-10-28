=======
hipchav
=======

A minimal Python HipChat client with command-line interface.

Setup
=====

Install ``hipchav`` from source, or using ``pip``::

    pip install hipchav

Then you'll need to configure it with your HipChat v2 API key::

    export HIPCHAT_AUTH_TOKEN=thisismyhextokentheygaveme

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

Check its usage information for full options::

    $ hipchav.py --help


Changelog
=========

v0.1.0
------

- Initial release, supports listing rooms and messaging with color and notifications
