swrcfit-cgi - SWRC Fit web interface
===========
This is a source code of web interface of [SWRC Fit](http://swrcfit.sourceforge.net/).

* Web: http://seki.webmasters.gr.jp/swrc/
* Purl: http://purl.org/net/swrc/
* Source: https://github.com/sekika/swrcfit-cgi
* Author: [Katsutoshi Seki](http://researchmap.jp/sekik/)

This document can be read here. https://github.com/sekika/swrcfit-cgi/blob/master/README.md

## How to use the web interface

It is documented in [user's manual of SWRC Fit](https://github.com/sekika/swrcfit/blob/master/README.md#web-interface-of-the-swrc-fit).

## Setting up alternative site

### Getting permission

You can set up SWRC Fit web interface anywhere if the access is restricted to
certain group of people by access control, and proper credit is clearly indicated.

To set up alternative site on servers where anyone can access, please get permission
from the author. You can just send me request as a question from [here](https://github.com/sekika/swrcfit-cgi/issues?q=is%3Aissue+label%3Aquestion).
After you get permission and you setup a server, post URL of the site in the thread.
I will make a list of alternative servers of SWRC Fit [here](http://swrcfit.sourceforge.net/).
This way, when the main site is not available for some reason, people can use the alternative site.
If you do not get permission within 2 weeks after you send the request as written above,
you can set up the alternative server. Please post URL of the site in the thread.

Alternative servers should have proper credit and link to the main site of SWRC Fit web interface.

### Technical note on setting up alternative site

This program requires [SWRC Fit](http://swrcfit.sourceforge.net/) version 2.0 or higher.
Please get the latest release from https://github.com/sekika/swrcfit/releases and install it.

SWRC Fit requires GNU Octave and some packages from octave forge, as described in user's manual of SWRC Fit.
If you do not have root access to your server, you might have to install these programs in your
home directory.

The source code of the web interface can be obtained from GitHub by

```
git clone git://github.com/sekika/swrcfit-cgi
``` 

All the necessary files are included. Change the permissions of data and img directory by
```
chmod 777 data img
```
Edit the first line of swrc.cgi
```
#!/usr/bin/perl --
```
to path of swrcfit installation. Edit `setting.pl` (required) and `setting.txt` (optinal).

If you are using apache 2, make sure that [mod_cgi](http://httpd.apache.org/docs/current/en/mod/mod_cgi.html) is enabled and you may also have to set up `.htaccess` file of something like

```
Options +ExecCGI
AddHandler cgi-script cgi
```

Read [Apache Tutorial: Dynamic Content with CGI](http://httpd.apache.org/docs/current/en/howto/cgi.html) if you have trouble setting up cgi.
