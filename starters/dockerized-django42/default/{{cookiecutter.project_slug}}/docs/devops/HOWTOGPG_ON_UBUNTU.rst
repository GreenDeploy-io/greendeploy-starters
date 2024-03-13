===========================================
Creating GPG Keys on an Ubuntu 22.04 Server
============================================

:Author: Kimsia
:Date: 2023-10-25 Wednesday
:Version: 0.0.1

.. contents:: Table of Contents
   :depth: 2


Purpose
=======

This guide aims to help you create a GPG key on an Ubuntu 22.04 server for decrypting Blackbox files and accessing secrets stored in a Git repository.

Steps
=====

Step 1: Install GnuPG
----------------------

If GnuPG is not installed, you can install it by running:

.. code-block:: bash

   sudo apt update
   sudo apt install gnupg

Step 2: Generate the GPG Key
------------------------------

To generate the GPG key, execute the following command:

.. code-block:: bash

   gpg --batch --generate-key <<EOF
   %no-protection
   Key-Type: RSA
   Key-Length: 4096
   Name-Real: <server-user@server-machine-name>
   Name-Email: <server-user@server-machine-name-ipaddr>
   Expire-Date: 0
   EOF

Step 3: Export the Public Key
-----------------------------

Export the newly created public key to a file:

.. code-block:: bash
   mkdir ~/.gpgkeys
   gpg --armor --export <server-user@server-machine-name-ipaddr> > public-key.gpg

To view the exported public key to copy paste, you can run:

.. code-block:: bash

   cat ~/.gpgkeys/public-key.gpg



Step 4: Import Public Key into Laptop
--------------------------------------

If using gpg keychain in macOS, once you copied the gpg using Cmd+C, it will auto detect and try to import.


Rationale
=========

Step 1: Install GnuPG
----------------------