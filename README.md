##About

An OpenRefine reconciliation service for [GeoNames](http://www.geonames.org/).

**Tested with, working on python 2.7.10, 3.4.3**

The service queries the [GeoNames API](http://www.geonames.org/export/web-services.html)
and provides normalized scores across queries for reconciling in Refine.

I'm just a small-town metadataist in a big code world, so please don't assume I did something 'the hard way' because I had a theory or opinion or whatnot. I probably just don't know that an easier way exists. So please share your corrections and thoughts (but please don't be a jerk about it either).

If you'd like to hear my thoughts about why do this instead of creating a column by pulling in URLs, or what I do with this data once I export my data to metadata records, or if we should even have to keep coordinates in bibliographic metadata records, see some thoughts here: http://christinaharlow.com/thoughts-on-geospatial-metadata and http://christinaharlow.com/walkthrough-of-geonames-recon-service

##Provenance

Michael Stephens wrote a [demo reconcilliation service](https://github.com/mikejs/reconcile-demo) and Ted Lawless wrote a [FAST reconciliation service](https://github.com/lawlesst/fast-reconcile) that this code basically repeats but for a different API.

Please give any thanks for this work to Ted Lawless, and any complaints to Christina. Also give thanks to Trevor Muñoz for some cleanups to make this code easier to work with.

##Special Notes

This came out of frustration that the Library of Congress authorities are:

- haphazard in containing Latitude and Longitude in the authority records for geographic names/subjects (although a requirement for authorities now, many such authorities do not contain the coordinates currently)
- the way that the Library of Congress authorities formulate place names for primary headings (not as subdivisions) would often return no results in the GeoNames API because of abbreviations, many of which for U.S. states were unique to the Library of Congress authorities (for example, 'Calif.' for headings of cities in California).

So this service takes Library of Congress authorities headings (or headings formulated to mimic the LoC authorities structure), expand U.S. abbreviations, then reconcile against GeoNames. The returned GeoNames 'name' gives both the GeoNames name for the location as well as the coordinates. There are, no doubts, better ways to handle getting both in an OpenRefine reconciliation service, but this was a quick hack to get both while I continue to explore how OpenRefine Reconciliation Services are structured.

##Instructions

Before getting started, you'll need python on your computer (this was built with python 2.7.8, updated to work with python3.4, most recently tested and worked with python 2.7.10 and 3.4.3) and be comfortable using OpenRefine/Google Refine.

This reconciliation service also requires a GeoNames API username. You can find and use the one used in the original code for testing, but you'll run against maximum number counts quickly, so it is strongly recommended you get your own (free, quick & easy to obtain) GeoNames account.

To do so, go to this webpage and register: http://www.geonames.org/login
After your account is activated, enable it for free web services: http://www.geonames.org/manageaccount

- Once you have your GeoNames username, create an environment variable on your computer with your Geonames username as so:
	- Open the Command Line Interface of your choice (Terminal on is default on a Mac)
	- Type in $ export GEONAMES_USERNAME="username" (replacing username with your username)
	- You may need to restart your terminal window, but probably not.
- Go ahead and clone/download/get a copy of this code repository on your computer.
- In the Command Line Interface, change to the directory where you downloaded this code (cd directory/with/code/ )
- Type in: python reconcile.py --debug (you don't need to use debug but this is helpful for knowing what this service is up to while you are working with it).
- You should see a screen telling you that the service is 'Running on http://0.0.0.0:5000/'.
- Leaving that terminal window open and the service running, go start up OpenRefine (however you normally go about it). Open a project in OpenRefine.
- On the column you would like to reconcile with GeoNames, click on the arrow at the top, choose 'Reconcile' > 'Start Reconciling...'
- Click on the 'Add Standard Service' button in the bottom left corner.
- Now enter the URL that the local service is running on - if you've changed nothing in the code except your GeoNames API username, it should be 'http://0.0.0.0:5000/reconcile'. Click Add Service.
	- If nothing happens upon entering 'http://0.0.0.0:5000/reconcile', try 'http://localhost:5000/reconcile' or 'http://127.0.0.1:5000/reconcile' instead.
- You should now be greeted by a list of possible reconciliation types for the GeoNames Reconciliation Service. They should be fairly straight-forward to understand, and use /geonames/all if you need the broadest search capabilities possible.
- Click 'Start Reconciling' in the bottom right corner.
- Once finished, you should see the closest options that the GeoNames API found for each cell. You can click on the options and be taken to the GeoNames site for that entry. Once you find the appropriate reconciliation choice, click the single arrow box beside it to use that choice just for the one cell, or the double arrows box to use that choice for all other cells containing that text.
- Once you've got your reconciliation choices done or rejected, you then need to store the GeoNames name, id, and coordinates (or any subset of those that you want to keep in the data) in your OpenRefine project. This is important:

**Although it appears that you have retrieved your reconciled data into your OpenRefine project, OpenRefine is actually storing the original data still. You need to explicit save the reconciled data in order to make sure it appears/exists when you export your data. Annoying as mosquito in your bedroom, I know, but please learn from my own mistakes, sweat and confusion.**

- So, depending on whether or not you wish to keep the original data, you can replace the column with the reconciled data or add a column that contains the reconciled data. I'll do the latter here. On the reconciled data column, click the arrow at the top, then Choose 'Edit Columns' > 'Add a new column based on this column'
- In the GREL box that appears, put the following depending on what you want to pull:
	- Name and Coordinates: `cell.recon.match.name` (will pull the GeoNames Name plus coordinates, separated by a | - you can split that column later to have just name then coordinates)
	- URI: `cell.recon.match.id` (will pull the GeoNames URI/link)
	- Coordinates Only: `replace(substring(cell.recon.match.name, indexOf(cell.recon.match.name, ' | ')), ' | ', '')`
	- Name, Coordinates, and URI each separated by | (for easier column splitting later): `cell.recon.match.name + " | " + cell.recon.match.id`

I'll maybe make a screencast of this work later if I get time or there is interested.

Holla if you have questions - email is charlow2(at)utk(dot)edu and Twitter handle is @cm_harlow


##Plans for Improvement

I'm hoping to build in next a way for searching within reconciliation cells next.

I'd like to expand the extremely rudimentary but gets the job done LoC geographic names abbreviations parser/expander text to handle other LoC Authorities abbreviations oddities. I'm afraid to say, since even the states abbreviations vary in their construction, these will need to be added on a case by case basis.

I'd also like to build in a way to use other columns as additional search properties.

Finally, finding a better way to handling the API username updates as well as parsing name plus coordinates (instead of the hack I've put into this for the time being) would be great.

