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
$img = "img/swrc.png"; # image file

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
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>SWRC Fit - Result -</title>
  <meta name="author" content="Katsutoshi Seki">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.7.1/katex.min.css" />
  <link rel="stylesheet" TYPE="text/css" HREF="swrc.css">
  <script src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.7.1/katex.min.js"></script>
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.7.1/contrib/auto-render.min.js"></script>
  <script>\$(document).ready(function(){renderMathInElement(document.body,{delimiters: [{left: "[[", right: "]]", display: true},{left: "\$", right: "\$", display: false}]})});</script>
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

##### Get form data
%formdata = plab::getformdata();

$soil = $formdata{'soil'};
$texture = $formdata{'texture'};
$name = $formdata{'name'};
$swrc = $formdata{'swrc'};
@m[1] = $formdata{'BC'};
@m[2] = $formdata{'VG'};
@m[3] = $formdata{'LN'};
@m[4] = $formdata{'FX'};
@m[5] = $formdata{'DB'};
@m[6] = $formdata{'BL'};
# $thetaR = $formdata{'thetaR'};
$onemodel = $formdata{'onemodel'};
$cqs = $formdata{'cqs'};
$qsin = $formdata{'qsin'};
$cqr = $formdata{'cqr'};
$qrin = $formdata{'qrin'};
$fxc = $formdata{'fxc'};
$psir = $formdata{'psir'};
$psimax = $formdata{'psimax'};
$figsize = $formdata{'figsize'};
$showgrid = $formdata{'showgrid'};
$ax = $formdata{'ax'};
$minx = $formdata{'minx'};
$maxx = $formdata{'maxx'};
$miny = $formdata{'miny'};
$maxy = $formdata{'maxy'};
$fontsize = $formdata{'fontsize'};
$showlabel = $formdata{'showlabel'};
$xlab = $formdata{'xlab'};
$showlegend = $formdata{'showlegend'};

# Escape control characters before output for security

$soil  = replacecontrolchars($soil);
$texture  = replacecontrolchars($texture);
$name  = replacecontrolchars($name);
$xlab  = replacecontrolchars($xlab);

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

# Delete old figure
unlink $img;

# Set calculation options

if (@m[1] eq "on") { $opt="bc=1"; } else { $opt="bc=0"; }
if (@m[2] eq "on") { $opt=$opt . " vg=1"; } else { $opt=$opt . " vg=0"; }
if (@m[3] eq "on") { $opt=$opt . " ln=1"; } else { $opt=$opt . " ln=0"; }
if (@m[4] eq "on") { $opt=$opt . " fx=1"; } else { $opt=$opt . " fx=0"; }
if (@m[5] eq "on") { $opt=$opt . " db=1"; } else { $opt=$opt . " db=0"; }
if (@m[6] eq "on") { $opt=$opt . " bl=1"; } else { $opt=$opt . " bl=0"; }
# if ($thetaR eq "on") { $opt=$opt . " qrin=0 cqr=0"; }
if ($onemodel eq "on") { $opt=$opt . " onemodel=1"; }

$qsin=$qsin + 0; # Convert to numeric to disallow insecure input
if ( $qsin < 0 ) { $qsin = 0; }
if ( $qsin > 100 ) { $qsin = 100; }
if ($cqs eq "fix") { $opt=$opt . " cqs=0 qsin=" . $qsin; }
if ($cqs eq "max") { $opt=$opt . " cqs=0"; }

$qrin=$qrin + 0;
if ( $qrin < 0 ) { $qrin = 0; }
if ( $qrin > 10 ) { $qrin = 10; }
if ($cqr eq "fix") { $opt=$opt . " cqr=0 qrin=" . $qrin; }

$psir=$psir + 0;
if ( $psir < 0 ) { $psir = 0; }
if ( $psir > 100000000 ) { $psir = 100000000; }
$psimax=$psimax + 0;
if ( $psimax < 0 ) { $psimax = 0; }
if ( $psimax > 10000000000 ) { $psmax = 10000000000; }
if ($fxc eq "on") { $opt=$opt . " fxc=1 psir=" . $psir . " psimax=" . $psimax; }

if ($figsize eq "1") { $opt=$opt . " figsize=1"; }
if ($figsize eq "2") { $opt=$opt . " figsize=2"; }
if ($showgrid eq "on") { $opt=$opt . " showgrid=1"; }
if ($ax eq "1") { $opt=$opt . " ax=1"; }
if ($ax eq "2") { $opt=$opt . " ax=2"; }

$minx=$minx + 0;
if ( $minx > 0 ) { $opt = $opt . " minx=" . $minx; }
$maxx=$maxx + 0;
if ( $maxx > 0 ) { $opt = $opt . " maxx=" . $maxx; }
$miny=$miny + 0;
if ( $miny > 0 ) { $opt = $opt . " miny=" . $miny; }
$maxy=$maxy + 0;
if ( $maxy > 0 ) { $opt = $opt . " maxy=" . $maxy; }

$fontsize=$fontsize + 0;
if ( $fontsize < 5 ) { $fontsize = 5; }
if ( $fontsize > 30 ) { $fontsize = 30; }
$opt = $opt . " fonsize=" . $fontsize;

if ( $showlabel eq "on" ) {
    $opt = $opt . " showlabel=1 xlab=\"" . $xlab . "\"";
} else {
    $opt = $opt . " showlabel=0";
}

if ( $showlegend eq "on" ) {
    $opt = $opt . " showlegend=1";
} else {
    $opt = $opt . " showlegend=0";
}

# Show option (debug) #####
print ($opt);

##### Calculation #####

# Here, swrcfit is called. setting.txt is automatically read and simple mode is selected.
# Therefore, the output parameter can be directly stored to $result.
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
  if (@m[1] eq "on") {
    @index[$model] = 1;
    @label[$model] = "<tr><td>Brooks and Corey<td>[[ S_e = \\begin{cases}\\left(\\dfrac{h}{h_b}\\right)^{-\\lambda} & (h>h_b) \\\\ 1 & (h \\le h_b)\\end{cases} ]]";
    @p1n[$model] = "h<sub>b</sub>";
    @p2n[$model] = "&lambda;";
    @p3n[$model] = ""; @p4n[$model] = ""; @p5n[$model] = "";
    @qs[$model] = $result[$k];
    @qr[$model] = $result[$k+1];
    @p1[$model] = $result[$k+2];
    @p2[$model] = $result[$k+3];
    @r2[$model] = $result[$k+4];
    @aic[$model] = $result[$k+5];
    $k = $k+6; $model++;
  }
  if (@m[2] eq "on") {
    @index[$model] = 2;
    @label[$model] = "<tr><td>van Genuchten<td>[[ S_e = \\biggl[\\dfrac{1}{1+(\\alpha h)^n}\\biggr]^m ~~ (m=1-1/n) ]]";
    @p1n[$model] = "&alpha;";
    @p2n[$model] = "n";
    @p3n[$model] = ""; @p4n[$model] = ""; @p5n[$model] = "";
    @qs[$model] = $result[$k];
    @qr[$model] = $result[$k+1];
    @p1[$model] = $result[$k+2];
    @p2[$model] = $result[$k+3];
    @r2[$model] = $result[$k+4];
    @aic[$model] = $result[$k+5];
    $k = $k+6; $model++;
  }
  if (@m[3] eq "on") {
    @index[$model] = 3;
    @label[$model] = "<tr><td>Kosugi<td>[[ S_e = Q \\biggl[\\dfrac{\\ln(h/h_m)}{\\sigma}\\biggr] ]]";
    @p1n[$model] = "h<sub>m</sub>";
    @p2n[$model] = "&sigma;";
    @p3n[$model] = ""; @p4n[$model] = ""; @p5n[$model] = "";
    @qs[$model] = $result[$k];
    @qr[$model] = $result[$k+1];
    @p1[$model] = $result[$k+2];
    @p2[$model] = $result[$k+3];
    @r2[$model] = $result[$k+4];
    @aic[$model] = $result[$k+5];
    $k = $k+6; $model++;
  }
  if (@m[4] eq "on") {
    @index[$model] = 4;
    if ($fxc eq "on") {
       @label[$model] = "<tr><td>Fredlund and Xing<td>[[ S_e = C(h) \\biggl[ \\dfrac{1}{\\ln \\left[e+(h / a)^n \\right]} \\biggr]^m ]]  [[ C(h) = - \\frac{ \\ln (1+ \\frac{h}{" . $psir . "})}{ \\ln (1+ \\frac{" . $psimax . "}{" . $psir . "})} +1 ]]";
    } else {
       @label[$model] = "<tr><td>Fredlund and Xing<td>[[ S_e = \\biggl[ \\dfrac{1}{\\ln \\left[e+(h / a)^n \\right]} \\biggr]^m ]]";
    }
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
    $k = $k+7; $model++;
  }
  if (substr($result[$k],0,3) eq "Not" and @m[5] . @m[6]) {
    @m[5]=""; @m[6]="";
     $bimodalerror="Bimodal model is not shown because the result shows that this soil is not bimdodal."; 
  } elsif (substr($result[$k],0,3) eq "Too" and @m[5] . @m[6]) {
    @m[5]=""; @m[6]="";
    $bimodalerror="You need to have at least 8 data poitns for bimodal analysis."
  } else {
    if (@m[5] eq "on") {
      @index[$model] = 5;
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
      $k = $k+9; $model++;
    }
    if (@m[6] eq "on") {
      @index[$model] = 6;
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
      $k = $k+9; $model++;
    }
  }
  $models=$model-1;
}

# If no result is obtained, something is wrong with input data
if ($models == 0) {
if (substr($result[$k],0,3) eq "Not") {
print << "EOF";
<h2>Not bimodal</h2>
<p>As a result of analysis, this soil is not bimodal. Please use unimodal models.</p>
EOF
} elsif (substr($result[$k],0,3) eq "Too") {
print << "EOF";
<h2>Too few points for bimodal analysis</h2>
<p>At least 8 data points is required for bimodal analysis. Please use unimodal models.</p>
EOF
} elsif (@m[1] . @m[2] . @m[3] . @m[4] . @m[5] . @m[6] eq "") {
print << "EOF";
<h2>No model selected</h2>
<p>Please select at least one model.</p>
EOF
} else {
print << "EOF";
<h2>Invalid input data or options</h2>

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
}
} else {

# Show result

print "<table border=\"1\"><tr><th>Model<th>Equation<th>Parameters<th>R<sup>2</sup><th>AIC</tr>";
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
<li>AIC (<a href="https://en.wikipedia.org/wiki/Akaike_information_criterion">Akaike's Information Criterion</a>) = n ln(RSS/n)+2k, where n is sample size, RSS is residual sum of squares and k is the number of estimated parameters.</li>
<li>Effective saturation, S<sub>e</sub> = (&theta;-&theta;<sub>r</sub>)/(&theta;<sub>s</sub>-&theta;<sub>r</sub>). Therefore &theta; = &theta;<sub>r</sub> + (&theta;<sub>s</sub>-&theta;<sub>r</sub>)S<sub>e</sub>.</li>
EOF
if ($thetaR eq "on") {
  print "<li>Parameter restriction: &theta;<sub>r</sub> = 0.</li>";
}
if ($bimodalerror ne "") {
  print "<li>", $bimodalerror, "</li>";
}
$q="Q(x) is the complementary cumulative normal distribution function, defined by Q(x)=1-&Phi;(x), in which &Phi;(x) is a normalized form of the <a href=\"http://mathworld.wolfram.com/NormalDistributionFunction.html\">cumulative normal distribution function</a>.</li>";
if (@m[3] eq "on") {
  if (@m[6] eq "on") {
    print "<li>For Kosugi and Seki models, ", $q;
  } else {
    print "<li>For Kosugi model, ", $q;
  }
} elsif (@m[6] eq "on") {
  print "<li>For Seki model, ", $q;
}
if (@m[4] eq "on") {
  print "<li>For Fredlund and Xing model, e is <a href=\"https://en.wikipedia.org/wiki/E_(mathematical_constant)\">Napier's constant</a>.</li>";
}
print "</ul>";

# Show Figure

print "<h2>Figure</h2>";

if (-e $img) {
  if ($onemodel eq "on") {
    print "<p>Showing the model with the minumim AIC value.</p>";
  }

  # Random number is added to refresh the browzer cash
  print "<img src=\"$img?", int(rand(1000000)), "\" alt=\"graph\">";
} else {
  print "<p>Error: Figure was not generated.</p>";
}
}

# Show reference
print "<h2>Reference</h2>";

print "<ul>";
if (@m[1] eq "on") {
  print "<li>Brooks, R.H., and A.T. Corey (1964): Hydraulic properties of porous media.
Hydrol. Paper 3. Colorado State Univ., Fort Collins, CO, USA.</li>";
}
if (@m[2] eq "on") {
  print "<li>van Genuchten, M. (1980): A closed-form equation for predicting the hydraulic conductivity of unsaturated soils. <i>Soil Sci. Soc. Am. J.</i>, 44:892-898.</li>";
}
if (@m[3] eq "on") {
  print "<li>Kosugi, K. (1996): Lognormal distribution model for unsaturated soil hydraulic properties. <i>Water Resour. Res. </i>, 32: 2697-2703.</li>";
}
if (@m[4] eq "on") {
  print "<li>Fredlund, D.G. and Xing, A. (1994): Equations for the soil-water characteristic curve. <i>Can. Geotech. J.</i>, 31: 521-532.</li>";
}
if (@m[5] eq "on") {
  print "<li>Durner, W. (1994): Hydraulic conductivity estimation for soils with heterogeneous pore structure. <i>Water Resour. Res.</i>, 30(2): 211-223.</li>";
}
if (@m[6] eq "on") {
  print "<li>Seki, K. (2007): SWRC Fit - A nonlinear fitting program with a water retention curve for soils having unimodal and bimodal pore structure. <i>Hydrol. Earth Syst. Sci. Discuss.</i>, 4: 407-437.</li>";
}
print "</ul>";

### Finish showing the result

# Print input data
print "<h2>Original Data</h2>";
print "<pre>";
$swrc  = replacecontrolchars($swrc);
print $swrc;
print "</pre>";

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
<ul>
<li><a href="http://purl.org/net/swrc/">SWRC Fit</a> $swrcfitversion with
<a href="https://github.com/sekika/swrcfit-cgi">swrcfit-cgi</a> $version,
$oct, and $gnuplot.</li>
<li>Seki, K. (2007) SWRC fit - a nonlinear fitting program with a water retention curve for soils having unimodal and bimodal pore structure. Hydrol. Earth Syst. Sci. Discuss., 4: 407-437. <a href="http://dx.doi.org/10.5194/hessd-4-407-2007">doi:10.5194/hessd-4-407-2007</li>
</ul>
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
