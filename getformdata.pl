# This code was obtained from PERL-LABO at
# http://www.perl-labo.org/formdata/jpname/

package plab;

sub getformdata
{
	local $rawdata;
	local %formdata;
	local @inputs;
	local($input, $name, $val);

	if ($ENV{'REQUEST_METHOD'} eq "POST") {
		read(STDIN, $rawdata, $ENV{'CONTENT_LENGTH'});
	}
	elsif ($ENV{'REQUEST_METHOD'} eq "GET") {
		$rawdata = $ENV{'QUERY_STRING'};
	}

	@inputs = split('&', $rawdata);

	foreach $input (@inputs) {
		($name, $val) = split('=', $input);
		$val =~ tr/+/ /;
		$val =~ s/%([A-Fa-f0-9][A-Fa-f0-9])/pack("C", hex($1))/eg;
		$formdata{$name} = $val;
	}

	return %formdata;
}

1;
