#!/usr/bin/env perl
#
# swrc.cgi - SWRC Fit web interface
#
# Web: http://seki.webmasters.gr.jp/swrc/
# Purl: http://purl.org/net/swrc/
# Source: https://github.com/sekika/swrcfit-cgi
# Author: Katsutoshi Seki
   $version="3.0";
#
# This program requires SWRC Fit: http://swrcfit.sourceforge.net/
# SWRC Fit requires GNU Octave and some packages
# See user's manual of SWRC Fit for detail.
#
# You can set up SWRC Fit web interface anywhere if the access is restricted to
# certain group of people by access control, and proper credit is clearly indicated.
# To set up this program on servers where anyone can access, please get permission
# from the author. See document for detail.
# https://github.com/sekika/swrcfit-cgi/blob/master/README.md

# Include 2 perl codes obtained from PERL-LABO
# http://www.perl-labo.org/
require 'getformdata.pl';
require 'lock.pl';

# Load setting
require 'setting.pl';
$lockdir    = "data/lock"; # lock directory
$fswrc = "data/swrc.txt"; # data file

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
  <meta http-equiv="Content-Type" content="text/html;CHARSET=UTF-8">
  <title>SWRC Fit - Result -</title>
  <meta name="author" content="Katsutoshi Seki">
  <LINK REL="stylesheet" TYPE="text/css" HREF="swrc.css">
</head>
<body>
EOF

# Check referrer

$referrer=$ENV{'HTTP_REFERER'};

$file = $referrer;
$referrer =~ s/index.*\.html//g;
$file =~ s/http.*jp\///g;

if ($referrer eq $validreferrer) {
print "<h1>SWRC Fit - Result -</h1>\n";

# Get form data

%formdata = plab::getformdata();

$soil = $formdata{'soil'};
$texture = $formdata{'texture'};
$name = $formdata{'name'};
$swrc = $formdata{'swrc'};
$AIC = $formdata{'AIC'};
$BC = $formdata{'BC'};
$VG = $formdata{'VG'};
$LN = $formdata{'LN'};
$FX = $formdata{'FX'};
$DB  = $formdata{'DB'};
$BL = $formdata{'BL'};
$thetaR = $formdata{'thetaR'};

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

# Write data file
open FILE, "> $fswrc";
print FILE $swrc;
close FILE;

if ($AIC eq "on") {
    $BC="on"; $VG="on"; $LN="on"; $FX="on"; $DB="on"; $BL="on";
}

##### Start of calculation #####

&calc;

# If no result is obtained, something is wrong with input data
if ($models == 0) {
print << "EOF";
<h2>Invalid input data</h2>

<p>The input data, i.e., the soil water retention curve, should be numbers with two columns.
The first column is the suction head and the second column is the volumetric water content,
where space is used as a delimiter. For example;</p>

<pre>
0 0.2628
20 0.237
30 0.223
40 0.211
50 0.2035
70 0.1855
100 0.169
200 0.151
430 0.1399
640 0.131
1050 0.1159
</pre>

<p>Lines beginning with "#" are regarded as comment and neglected.
Any unit can be used as the input data, and the calculated data depends on the unit used as the input data.</p>

<p>Optionally, the input data can have the third column. When it has the third column,
it is interpreted as a weight for each parameter.</p>

<p>For example,</p>

<pre>
0 0.2628 1
20 0.237 1
40 0.211 1
70 0.1855 1
100 0.169 1
1050 0.1159 3
</pre>

<p>This data has weight of 1 for the suction of 0, 20, 40, 70, 100 and 3 for the suction of 1050.</p>

EOF
} else {

# Show result

print "<table border=\"1\"><tr><td>Model<td>Equation<td>Parameters<td>R<sup>2</sup><td>AIC</tr>";
$model = 0;
while ($model < $models ){
  $model++;
  print @label[$model];
  print "<td>&theta;<sub>s</sub> = ", @qs[$model];
  print "<br>&theta;<sub>r</sub> = ", @qr[$model];
  print "<br>", @p1n[$model], " = ",, @p1[$model];
  print "<br>", @p2n[$model], " = ",, @p2[$model];
  if (@p3n[$model] ne "") { print "<br>", @p3n[$model], " = ",, @p3[$model];}
  if (@p4n[$model] ne "") { print "<br>", @p4n[$model], " = ",, @p4[$model];}
  if (@p4n[$model] ne "") { print "<br>", @p5n[$model], " = ",, @p5[$model];}
  print "<td>", @r2[$model];
  print "<td>", @aic[$model], "</tr>";
}
print <<"EOF";
</tr>
</table>
<ul>
<li><img src="img/Se.png" width=76 height=42 alt=Se>, i.e., <img src="img/Se2.png" alt=theta></li>
EOF
if ($LN eq "on") {
  print "<li>For Kosugi model, Q(x) is the complementary cumulative normal distribution function,
defined by Q(x)=1-&Phi;(x), in which &Phi;(x) is a normalized form of the
<a href=\"http://mathworld.wolfram.com/NormalDistributionFunction.html\">cumulative normal distribution function</a></li>"
}
if ($FX eq "on") {
  print "<li>For Fredlund and Xing model, e is <a href=\"https://en.wikipedia.org/wiki/E_(mathematical_constant)\">Napier's constant</a>. For modifying the correction function C(h), please use offline version of SWRC Fit.</li>"
}
print "</ul>";

# Select best model

print "<h2>Figure</h2>";

if ($AIC eq "on") {
  print "<p>Figure is shown for selected 2 models with lowest AIC.</p>";
  @aicsort = sort {$a <=> $b} @aic;
  if (@aic[1] <= @aicsort[1]) { $BC="on"; } else { $BC=""; }
  if (@aic[2] <= @aicsort[1]) { $VG="on"; } else { $VG=""; }
  if (@aic[3] <= @aicsort[1]) { $LN="on"; } else { $LN=""; }
  if (@aic[4] <= @aicsort[1]) { $FX="on"; } else { $FX=""; }
  if (@aic[5] <= @aicsort[1]) { $DB="on"; } else { $DB=""; }
  if (@aic[6] <= @aicsort[1]) { $BL="on"; } else { $BL=""; }
  &calc;
}

# Random number is added to refresh the browzer cash
print "<img src=\"img/swrc.png?", int(rand(1000000)), "\" alt=\"graph\">";

}

# Print input data
print "<h2>Original Data</h2>";
print "<pre>";
$swrc  = replacecontrolchars($swrc);
print $swrc;
print "</pre>";

# Show reference
print "<h2>Reference</h2>";

if ($AIC eq "on") {
    $BC="on"; $VG="on"; $LN="on"; $FX="on"; $DB="on"; $BL="on";
}

print "<ul>";
if ($BC eq "on") {
  print "<li>Brooks, R.H., and A.T. Corey (1964): Hydraulic properties of porous media.
Hydrol. Paper 3. Colorado State Univ., Fort Collins, CO, USA.</li>";
}
if ($VG eq "on") {
  print "<li>van Genuchten, M. (1980): A closed-form equation for predicting the hydraulic conductivity of unsaturated soils. <i>Soil Sci. Soc. Am. J.</i>, 44:892-898.</li>";
}
if ($LN eq "on") {
  print "<li>Kosugi, K. (1996): Lognormal distribution model for unsaturated soil hydraulic properties. <i>Water Resour. Res. </i>, 32: 2697-2703.</li>";
}
if ($FX eq "on") {
  print "<li>Fredlund, D.G. and Xing, A. (1994): Equations for the soil-water characteristic curve. <i>Can. Geotech. J.</i>, 31: 521-532.</li>";
}
if ($DB eq "on") {
  print "<li>Durner, W. (1994): Hydraulic conductivity estimation for soils with heterogeneous pore structure. <i>Water Resour. Res.</i>, 30(2): 211-223.</li>";
}
if ($BL eq "on") {
  print "<li>Seki, K. (2007): SWRC Fit - A nonlinear fitting program with a water retention curve for soils having unimodal and bimodal pore structure. <i>Hydrol. Earth Syst. Sci. Discuss.</i>, 4: 407-437.</li>";
}
print "</ul>";

# Invalid referrer
} else {
print << "EOF";
<h1>Error</h1>
<p>Referrer is invalid. Please check your browser's setting and make sure that your browser is
sending correct referrer.</p>
EOF
}

# Delete data file
unlink $fswrc;

# Unlock
plab::unlock($lockdir);

# Print footer

$swrcfitversion = `($swrcfit -v) 2> /dev/null | sed -e 's/swrcfit //'`;
$oct = `(octave -v | grep version) 2> /dev/null | sed -e 's/, version//'`;
$gnuplot = `(gnuplot -V) 2> /dev/null | sed -e 's/ patchlevel /./'`;

print << "EOF";
<hr>
<p><a href="http://purl.org/net/swrc/">SWRC Fit</a> $swrcfitversion with $oct, $gnuplot and <a href="https://github.com/sekika/swrcfit-cgi">swrcfit-cgi</a> $version.</p>
</body>
</html>
EOF

######################################### Finish

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

##### Calculation routine #####

sub calc {

# Set calculation options

if ($BC eq "on") {
    $opt="bc=1";
} else {
    $opt="bc=0";
}
if ($VG eq "on") {
    $opt=$opt . " vg=1";
} else {
    $opt=$opt . " vg=0";
}
if ($LN eq "on") {
    $opt=$opt . " ln=1";
} else {
    $opt=$opt . " ln=0";
}
if ($FX eq "on") {
    $opt=$opt . " fx=1";
} else {
    $opt=$opt . " fx=0";
}
if ($DB eq "on") {
    $opt=$opt . " db=1";
} else {
    $opt=$opt . " db=0";
}
if ($BL eq "on") {
    $opt=$opt . " bl=1";
} else {
    $opt=$opt . " bl=0";
}
if ($thetaR eq "on") {
    $opt=$opt . " qrin=0 cqr=0";
}

# Here, swrcfit is called. setting.txt is automatically read and simple mode is selected.
# Therefore, the output parameter can directoly be stored to $result.
# Difference in the calculation option is specified by setting files.
# Error message from octave is discarded to /dev/null.
# Sometimes learsqr.m output message of "CONVERGENCE NOT ACHIEVED!".
# To supress this message, the output is piped to `grep -v "CON"`.

@result = `($swrcfit $fswrc $opt) 2> /dev/null | grep -v "CON"`;

# If no result is obtained, something is wrong with input data
if ($result[0] eq "" or $result[0] == "0") {
  $models=0;
} else {
  $k=0; $model=1;
  if ($BC eq "on") {
    @label[$model] = "<tr><td>Brooks and Corey<td><img src=\"img/BC.png\" width=146 height=75 alt=BC>";
    @p1n[$model] = "h<sub>b</sub>";
    @p2n[$model] = "&lambda;";
    @p3n[$model] = ""; @p4n[$model] = ""; @p5n[$model] = "";
    @qs[$model] = $result[$k];
    @qr[$model] = $result[$k+1];
    @p1[$model] = $result[$k+2];
    @p2[$model] = $result[$k+3];
    @r2[$model] = $result[$k+4];
    @aic[$model] = $result[$k+5];
    $k = $k+6; $model = $model + 1;
  }
  if ($VG eq "on") {
    @label[$model] = "<tr><td>van Genuchten<td><img src=\"img/VG.png\" width=108 height=48 alt=VG> (m=1-1/n)";
    @p1n[$model] = "&alpha;";
    @p2n[$model] = "n";
    @p3n[$model] = ""; @p4n[$model] = ""; @p5n[$model] = "";
    @qs[$model] = $result[$k];
    @qr[$model] = $result[$k+1];
    @p1[$model] = $result[$k+2];
    @p2[$model] = $result[$k+3];
    @r2[$model] = $result[$k+4];
    @aic[$model] = $result[$k+5];
    $k = $k+6; $model = $model + 1;
  }
  if ($LN eq "on") {
    @label[$model] = "<tr><td>Kosugi<td><img src=\"img/LN.png\" width=110 height=42 alt=LN>";
    @p1n[$model] = "h<sub>m</sub>";
    @p2n[$model] = "&sigma;";
    @p3n[$model] = ""; @p4n[$model] = ""; @p5n[$model] = "";
    @qs[$model] = $result[$k];
    @qr[$model] = $result[$k+1];
    @p1[$model] = $result[$k+2];
    @p2[$model] = $result[$k+3];
    @r2[$model] = $result[$k+4];
    @aic[$model] = $result[$k+5];
    $k = $k+6; $model = $model + 1;
  }
  if ($FX eq "on") {
    @label[$model] =  "<tr><td>Fredlund and Xing<td><img src=\"img/FX.png\" width=190 height=53 alt=FX> (C(h)=1)";
    @p1n[$model] = "a";
    @p2n[$model] = "m";
    @p3n[$model] = "n";
    @p4n[$model] = ""; @p5n[$model] = "";
    @qs[$model] = $result[$k];
    @qr[$model] = $result[$k+1];
    @p1[$model] = $result[$k+2];
    @p2[$model] = $result[$k+3];
    @p3[$model] = $result[$k+4];
    @r2[$model] = $result[$k+5];
    @aic[$model] = $result[$k+6];
    $k = $k+7; $model = $model + 1;
  }
  if (substr($result[$k],0,3) eq "Not") {
    $DB=""; $BL="";  
  } elsif (substr($result[$k],0,3) eq "Too") {
    $DB=""; $BL="";  
  } else {
    if ($DB eq "on") {
      @label[$model] = "<tr><td>Durner<td><img src=\"img/DB.png\" width=292 height=52 alt=DB><br>";
      @p1n[$model] = "w<sub>1</sub>";
      @p2n[$model] = "&alpha;<sub>1</sub>";
      @p3n[$model] = "n<sub>1</sub>";
      @p4n[$model] = "&alpha;<sub>2</sub>";
      @p5n[$model] = "n<sub>2</sub>";
      @qs[$model] = $result[$k];
      @qr[$model] = $result[$k+1];
      @p1[$model] = $result[$k+2];
      @p2[$model] = $result[$k+3];
      @p3[$model] = $result[$k+4];
      @p4[$model] = $result[$k+5];
      @p5[$model] = $result[$k+6];
      @r2[$model] = $result[$k+7];
      @aic[$model] = $result[$k+8];
      $k = $k+9; $model = $model + 1;
    }
    if ($BL eq "on") {
      @label[$model] = "<tr><td>Seki<td><img src=\"img/BL.png\" width=282 height=49 alt=BL>";
      @p1n[$model] = "w<sub>1</sub>";
      @p2n[$model] = "h<sub>m1</sub>";
      @p3n[$model] = "&sigma;<sub>1</sub>";
      @p4n[$model] = "h<sub>m2</sub>";
      @p5n[$model] = "&sigma;<sub>2</sub>";
      @qs[$model] = $result[$k];
      @qr[$model] = $result[$k+1];
      @p1[$model] = $result[$k+2];
      @p2[$model] = $result[$k+3];
      @p3[$model] = $result[$k+4];
      @p4[$model] = $result[$k+5];
      @p5[$model] = $result[$k+6];
      @r2[$model] = $result[$k+7];
      @aic[$model] = $result[$k+8];
      $k = $k+9; $model = $model + 1;
    }
  }
  $models=$model-1;
}
}
