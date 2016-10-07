CKAN Repo Extension
===================

**Status:** Unstable

**CKAN Version:** >= 2.0.0

A CKAN extension that displays the version of CKAN being used, the commit, and
the date of last update. This extension is **unstable** and is written for use
in master.ckan.org and beta.ckan.org instances.

Installation
------------

1. Install the extension as usual, e.g. (from an activated virtualenv):

    ::

    $ pip install -e
    git+https://github.com/ckan/ckanext-repo.git#egg=ckanext-repo

2. Edit your configuration ini file to activate the plugin with:

   ::

      ckan.plugins = repo_info

   (If there are other plugins activated, add this to the list.  Each
   plugin should be separated with a space).

3. Restart your CKAN instance.


You should see the repo information in the footer. You may have to run `git
fetch origin` to create the file that's used to fetch the information from.
