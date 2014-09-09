swrcfit-cgi - SWRC Fit web interface
===========
This is a source code of web interface of [SWRC Fit](http://swrcfit.sourceforge.net/).

* Web: http://seki.webmasters.gr.jp/swrc/
* Purl: http://purl.org/net/swrc/
* Source: https://github.com/sekika/swrcfit-cgi
* Author: [Katsutoshi Seki](http://researchmap.jp/sekik/)

## How to use the web insterface

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
you can set up the alternative server. Please post the address in the thread.

Alternative servers should have proper credit and link to the main site of SWRC Fit web interface.

### Technical note on setting up alternative site

This program requires [SWRC Fit](http://swrcfit.sourceforge.net/).
Currently it is running with developing code available from GitHub repository. Obtain the code with

```
git clone git://github.com/sekika/swrcfit
``` 

SWRC Fit requires GNU Octave and some packages from octave forge, as described in user's manual of SWRC Fit.
If you do not have root access to your server, you might have to install these programs in your
home directory.

The source code of the web interface can be obtained from GitHub by

```
git clone git://github.com/sekika/swrcfit-cgi
``` 

All the necessary files are included, except ./data directory (permission 777) and
unsoda----.html files. Read the source code of `swrc.cgi` and `setting.txt` and edit some
settings to meet your server's environment.

