chronam-text
------------

An extraction of raw newspaper page text from [Chronicling
America](http://chroniclingamerica.loc.gov/).  All of this data is
already available through the [Chronam
API](http://chroniclingamerica.loc.gov/about/api/) but it still
requires a little work to grab this subset of data and assemble it
just so.  This package includes scripts for collecting the data and 
a sample of its output for ready access via git/github.


installation
------------

Developed for Python-3.x, with requests installed.  It might be easiest
to create a virtualenv and run:

        % pip install -r requirements.txt


fetching data
-------------

To fetch data, run the ```fetch.py``` command.  Collected data will be
sorted into unique directories for each distinct day, with individual
pages from different newspapers distinguished by their LCCN prefixing 
their file names, followed by the issue edition and sequence number.
This follows the ChronAm site's conventions.

There are a few options:

        % ./fetch.py -y 1916 

This will limit collected page text to the year 1916.

        % ./fetch.py -y 1916 --pageone

This will limit collected page text further to only the first pages
of issues from 1916.

        % ./fetch.py -y 1916 --pageone --limit=300

This will cap the total number of pages of text collected to 300.

Note that only newspaper pages from 1836-1922 are available; if you 
request a year before 1836 or later than 1922 you will see an error
message.


sample data
-----------

A selection of front pages from 1916 is included under the ```dates```
directory.  This set was fetched using the ```--pageone``` and ```-y
1916``` parameters.  Only the text files are in the repo; the ALTO
XML files are excluded due to their combined size (>3Gb).  The
roughly 28,000 files span all of 1916.

The individual text files can be mapped to their newspaper title
bibliographic data using the JSON data in the ```titles``` directory.
Just match the LCCN in the name of the text file to the corresponding
JSON file in ```titles```.

This data was fetched using the ```fetch_titles.py``` script, which
(without options) examines collected data in the ```dates``` directory
to prepare a list of unique LCCNs, then fetches the bibliographic
data for each title/LCCN from ChronAm.

There are 308 title records in ```titles``` corresponding to the
collected front pages from 1916 in ```dates```.
