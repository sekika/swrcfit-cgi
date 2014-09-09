# This code was obtained from PERL-LABO at
# http://www.perl-labo.org/location/4/
# Japanese message was modified to English messsage

package plab;

# Parameter (Directory)
sub lock
{
	local $ok;
	local $lockdir;

	$lockdir = $_[0];
	$ok      = 0;

	for (1 .. 3) {
		if (mkdir($lockdir, 0755)) {
			$ok = 1;
			last;
		}
		else {
			sleep(1);
		}
	}

	if ($ok == 0){
		if ((-M $lockdir)*60*60*24 >= 30) {
			rmdir($lockdir);
			if (mkdir($lockdir, 0755)) {
				$ok = 1;
			}
		}
	}

	return $ok;
}

# Parameter (Directory)
sub unlock
{
	rmdir($_[0]);
}

sub printlockerror
{
	print "Content-type: text/html\n";
	print "\n";
	print "Fail to lock the file.<br>\n";
	print "Please try again later.<br>\n";
}

1;
