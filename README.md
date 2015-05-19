# Superluminal - Ansible communication for humans.

*Superluminal* is a simple wrapper around Ansible's _PlayBook_ class for purposes of making it easy to run Ansible playbooks and capture the output.

Ansible provides a callback mechanism for capturing the output from the various invocations in a playbook.  Callbacks exist a various stages in the playbook life cycle: playbook setup, module invocation, successful completion, error conditions, etc.  Superluminal gives the user a mechanism for specifying the names of the required Python callback modules, thus making it possible to use Ansible data in a variety of interesting ways.

*Superluminal* is written as a WSGI application using the Python _gunicorn_ and _falcon_ libraries.
Ansible playbooks are invoked in *superluminal* using a simple REST API.

The Ansible library can, of course, be imported directly into in any Python script.  The *superluminal* approach is useful for two purposes:

* As a simple Ansible playbook runner web service that can have an independent existence anywhere in an application ecosystem; and
* As a simple means to avoid having to import Ansible classes directly into code, thus working around potential GPLv3 issues.  Superluminal is open source and licensed under a GPL-compatible license (Apache2) that is nonetheless less restrictive than GPLv3.

# Setup

From the top-level directory, type

```
sudo python setup.py install
```

The superluminal configuration file ```superluminal.conf``` must go in /etc/superluminal.  A sample configuration file is included in the ```/conf``` subdirectory.

The default (_gunicorn_) server can then be run with 

```
sudo python -msuperluminal.server &
```

Since *superluminal* is a web service, it should be run as a non-privileged user.  The sample configuration file assumes a ```superluminal``` user and group, although these are configurable.  Other configurable options include host interface IP and port.

At the moment, *superluminal* is not set up to run under SSL, although this would be an easy enhancement given that it is a WSGI app and runs in a WSGI container.

Ansible must be configured separately.  *Superluminal* only needs to know the path to Ansible playbooks and inventory.

# REST API

At the moment, there is only a single REST endpoint:

```
POST /v1/run?playbook=my_playbook&password=my_password
```

The ```playbook``` parameter is required.  The ```password``` parameter is optional and is passed directly to the Ansible playbook runner.

Output from this POST request is a simple JSON string giving a UUID string, which serves as the ID of the requested playbook run.  The user may do whatever she wants with this, for example, maintain a database of output from each playbook run using the various Ansible callbacks.

# Ansible callbacks

The Ansible playbook runner uses a set of callbacks to inform a calling process of the outcome of the various steps in executing a playbook.  These are not well documented by Ansible, although the official Ansible documentation does refer to them and invites the user to examine the Ansible code to get an idea of how they are used.  In most cases it is pretty clear what data is available.

For example, the ```ansible-playbook``` shell command itself is organized around a set of Ansible callbacks.

The *superluminal* distribution contains a couple of very simple callback plugin examples, using stdout and python logging, respectively, that will give an idea of what is available from Ansible through the callbacks.  Each user's requirements will be somewhat different, however, and mileage may vary.

*TODO: Maybo a little better documentation of the Ansible callbacks?