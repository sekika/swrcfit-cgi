swrcfit-cgi - SWRC Fit web interface
===========
This is a source code of web interface of [SWRC Fit](http://swrcfit.sourceforge.net/).

* Web: http://seki.webmasters.gr.jp/swrc/
* Purl: http://purl.org/net/swrc/
* Source: https://github.com/sekika/swrcfit-cgi
* Author: [Katsutoshi Seki](http://researchmap.jp/sekik/)
* Version: 2.0

This document can be read here. https://github.com/sekika/swrcfit-cgi/blob/master/README.md

## How to use the web interface

It is documented in [user's manual of SWRC Fit](https://github.com/sekika/swrcfit/blob/master/README.md#web-interface-of-the-swrc-fit).

## Setting up alternative site

### Getting permission

You can set up SWRC Fit web interface anywhere if the access is restricted to a
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

I assume that you have a shell access to your web server. Without the shell access, installation
of this program is very difficult, if not possible.

- Install Perl if it is not yet installed on your system.
- Install the latest version of [SWRC Fit](http://swrcfit.sourceforge.net/) as described in the user's manual.
This program requires version 2.0 or higher.

If you do not have root access to your server, install SWRC Fit and necessary programs
(perl, gnuplot, GNU Octave, struct and optim packages of octave forge) in your home directory;
compile the programs from source by changing the path setting.

The latest source code of the web interface can be obtained from GitHub by

```
git clone git://github.com/sekika/swrcfit-cgi
```

Please note that you are using appropriate version of swrcfig-cgi corresponding to the version
of swrcfit that you are using. Older releases can be obtained from [Releases](https://github.com/sekika/swrcfit-cgi/releases).

|Version of swrcfit-cgi| Version of swrcfit|
|--------|-----------|
|2.0     |2.0, 2.1   |

All the necessary files are included. Change the permissions of data and img directory by
```
chmod 777 data img
```
Edit `setting.pl` (required) and `setting.txt` (optional).

If you are using apache 2, make sure that [mod_cgi](http://httpd.apache.org/docs/current/en/mod/mod_cgi.html)
is enabled and you may also have to set up `.htaccess` file of something like

```
Options +ExecCGI
AddHandler cgi-script cgi
```

Please make sure that this is allowed on your system (check AllowOverride in the directory).
Read [Apache Tutorial: Dynamic Content with CGI](http://httpd.apache.org/docs/current/en/howto/cgi.html)
if you have trouble setting up cgi.
