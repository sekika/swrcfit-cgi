#!/usr/bin/perl --
#
# swrc.cgi - SWRC Fit web interface
# http://seki.webmasters.gr.jp/swrc/
# Author: Katsutoshi Seki
#
# This program requires SWRC Fit: http://swrcfit.sourceforge.net/
# SWRC Fit requires GNU Octave and some packages
# See user's manual of SWRC Fit for detail.
#
# You can set up SWRC Fit web interface anywhere if the access is restricted to
# certain group of people by access control, and proper credit is clearly indicated.
# To set up this program on servers where anyone can access, please get permission
# from the author. Detail will be written in the document.

# Include 2 perl codes obtained from PERL-LABO
# http://www.perl-labo.org/
require 'getformdata.pl';
require 'lock.pl';

# Initial setting
$swrcfit = "/usr/local/bin/swrcfit"; # swrcfit program
$lockdir    = "data/lock"; # lock directory
$fswrc = "data/swrc.txt"; # data file
$bimodal = "bimodal.txt"; # setting for bimodal model
$qr0 = "qr0.txt"; # setting for theta_r = 0

# This should be modified when using at different server
$validreferrer = "http://seki.webmasters.gr.jp/swrc/";

# Lock

if (! plab::lock($lockdir)) {
        plab::printlockerror();
        exit;
}

# Print header

print << "EOF";
Content-type: text/html

<!DOCTYPE html>
<html lang="en">
<head>
  <meta http-equiv="Content-Type" content=\"text/html;CHARSET=UTF-8">
  <title>SWRC Fit - Result -</title>
  <meta name="author" content=\"Katsutoshi Seki">
  <LINK REL="stylesheet" TYPE="text/css" HREF="swrc.css">
</head>
<body>
EOF

# Check referrer

$referrer=$ENV{'HTTP_REFERER'};

$file = $referrer;
$referrer =~ s/unsoda.*html//g;
$referrer =~ s/index\.html//g;
$file =~ s/http.*jp\///g;

if ($referrer eq $validreferrer) {
print "<h1>SWRC Fit - Result -</h1>\n";

# Get form data

%formdata = plab::getformdata();

$soil = $formdata{'soil'};
$texture = $formdata{'texture'};
$name = $formdata{'name'};
$swrc = $formdata{'swrc'};
$thetaR = $formdata{'thetaR'};
$DB = $formdata{'DB'};

# Escape control characters before output for security

$soil  = replacecontrolchars($soil);
$texture  = replacecontrolchars($texture);
$name  = replacecontrolchars($name);

# Output sample information

print "<ul>";
print "<li>Soil sample: $soil</li>";
print "<li>Texture: $texture</li>";
print "<li>Name: $name</li>";
print "</ul>";

##### Start of unimodal model #####

print "<h2>Unimodal models</h2>";

# Write data file
open FILE, "> $fswrc";
print FILE $swrc;
close FILE;

### Calculation ###

# Here, swrcfit is called. setting.txt is automatically read and simple mode is selected.
# Therefore, the output parameter can directoly be stored to $result.
# Difference in the calculation option is specified by setting files.
# Error message from octave is discarded to /dev/null.
# Sometimes learsqr.m output message of "CONVERGENCE NOT ACHIEVED!".
# To supress this message, the output is piped to `grep -v "CON"`.

if ($thetaR eq "on") {
  @result = `($swrcfit $fswrc $qr0) 2> /dev/null | grep -v "CON"`;
}
else {
  @result = `($swrcfit $fswrc) 2> /dev/null | grep -v "CON"`;
}

print "<table border=\"1\"><tr><td>Model<td>Equation<td>Parameters<td>R<sup>2</sup></tr>";
print "<tr><td>Brooks and Corey<td><img src=\"img/BC.png\" width=146 height=75 alt=BC>";
print "<td>&theta;<sub>s</sub> = ", $result[0];
print "<br>&theta;<sub>r</sub> = ", $result[1];
print "<br>h<sub>b</sub> = ",, $result[2];
print "<br>&lambda; = ", $result[3];
print "<td>", $result[4], "</tr>";
print "<tr><td>van Genuchten<td><img src=\"img/VG.png\" width=108 height=48 alt=VG> (m=1-1/n)";
print "<td>&theta;<sub>s</sub> = ", $result[5];
print "<br>&theta;<sub>r</sub> = ", $result[6];
print "<br>&alpha; = ", $result[7];
print "<br>n = ", $result[8];
print "<td>", $result[9], "</tr>";
print "<tr><td>Kosugi<td><img src=\"img/LN.png\" width=110 height=42 alt=LN>";
print "<td>&theta;<sub>s</sub> = ", $result[10];
print "<br>&theta;<sub>r</sub> = ", $result[11];
print "<br>h<sub>m</sub> = ", $result[12];
print "<br>&sigma; = ", $result[13];
print "<td>", $result[14];

print <<"EOF";
</tr>
</table>
where <img src="img/Se.png" width=76 height=42 alt=Se>, i.e., <img src="img/Se2.png" alt=theta>
and Q(x) is the complementary cumulative normal distribution function,
defined by Q(x)=1-&Phi;(x), in which &Phi;(x) is a normalized form of the
<a href="http://mathworld.wolfram.com/NormalDistributionFunction.html">cumulative normal distribution function</a>
<br><br>
EOF

# Random number is added to refresh the browzer cash
print "<img src=\"img/swrc.png?", int(rand(1000000)), "\">";

# Show reference

print <<"EOF";
<ul>
<li>Brooks, R.H., and A.T. Corey (1964): Hydraulic properties of porous media.
Hydrol. Paper 3. Colorado State Univ., Fort Collins, CO, USA.</li>
<li>van Genuchten, M. (1980): A closed-form equation for predicting the hydraulic conductivity of unsaturated soils.
<i>Soil Sci. Soc. Am. J.</i> 44:892-898.</li>
<li>Kosugi, K. (1996): Lognormal distribution model for unsaturated soil hydraulic properties.
<i>Water Resour. Res.</i> 32: 2697-2703.</li>
</ul>
EOF

##### Bimodal models #####

if ($DB eq "on") {
  print "<h2>Bimodal models</h2>";
if ($thetaR eq "on") {
  @result = `($swrcfit $fswrc $bimodal $qr0) 2> /dev/null | grep -v "CON"`;
}
else {
  @result = `($swrcfit $fswrc $bimodal) 2> /dev/null | grep -v "CON"`;
}

if (substr($result[0],0,3) eq "Not") {
  print "<p>Not bimodal.</p>";
} elsif (substr($result[0],0,3) eq "Too") {
  print "<p>Too few points for bimodal analysis.</p>";
} else {

print "<table border=\"1\"><tr><td>Model<td>Equation<td>Parameters<td>R<sup>2</sup></tr>";
print "<tr><td>Durner<td><img src=\"img/DB.png\" width=292 height=52 alt=DB><br>";
print "(m<sub>i</sub>=1-1/n<sub>i</sub>)";
print "<td>&theta;<sub>s</sub> = ", $result[0];
print "<br>&theta;<sub>r</sub> = ", $result[1];
print "<br>w<sub>1</sub> = ", $result[2];
print "<br>&alpha;<sub>1</sub> = ", $result[3];
print "<br>n<sub>1</sub> = ", $result[4];
print "<br>&alpha;<sub>2</sub> = ", $result[5];
print "<br>n<sub>2</sub> = ", $result[6];
print "<td>", $result[7];
print "</tr>";
print "<tr><td>Seki<td><img src=\"img/BL.png\" width=282 height=49 alt=BL>";
print "<td>&theta;<sub>s</sub> = ", $result[8];
print "<br>&theta;<sub>r</sub> = ", $result[9];
print "<br>w<sub>1</sub> = ", $result[10];
print "<br>h<sub>m1</sub> = ", $result[11];
print "<br>&sigma;<sub>1</sub> = ", $result[12];
print "<br>h<sub>m2</sub> = ", $result[13];
print "<br>&sigma;<sub>2</sub> = ", $result[14];
print "<td>", $result[15];
print "</tr>";
print "</table>";
print "<img src=\"img/bimodal.png?", int(rand(1000000)), "\">";

print << "EOF";
<ul>
<li>Durner, W. (1994): Hydraulic conductivity estimation for soils with heterogeneous pore structure.
<i>Water Resour. Res.</i>, 30(2): 211-223.</li>
<li>Seki, K. (2007): SWRC Fit - A nonlinear fitting program with a water retention curve for soils
having unimodal and bimodal pore structure. <i>Hydrol. Earth Syst. Sci. Discuss.</i>, 4: 407-437.</li>
</ul>
EOF
}
}

# Print input data
print "<h2>Original Data</h2>";
print "<pre>";
$swrc  = replacecontrolchars($swrc);
print $swrc;
print "</pre>";
}

# Invalid referrer
else {
print << "EOF";
<h1>Error</h1>
<p>Referrer is invalid. Please check your browser's setting and make sure that your browser is
sending correct referrer.</p>
EOF
}

# Unlock
plab::unlock($lockdir);

# Print footer

print << "EOF";
<hr>
<p><a href="http://purl.org/net/swrc/">SWRC Fit</a></p>
</body>
</html>
EOF

# Function to replace control charactrers

sub replacecontrolchars
{
        local $s = $_[0];
        $s =~ s/\r\n/\n/g;
        while (chomp($s)) {
                ;
        }
        $s =~ s/&/&amp;/g;
        $s =~ s/</&lt;/g;
        $s =~ s/>/&gt;/g;
        $s =~ s/"/&quot;/g;
        $s =~ s/'/&apos;/g;
        $s =~ s/\n/<br>/g;
        return $s;
}