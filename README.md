##About

An OpenRefine reconciliation service for [GeoNames](http://www.geonames.org/).

The service queries the [GeoNames API](http://www.geonames.org/export/web-services.html)
and provides normalized scores across queries for reconciling in Refine.

I'm just a small-town (but refusing to be small-time) metadataist in a big code world, so please don't assume I did something 'the hard way' because I had a theory or opinion or whatnot. I probably just didn't know an easier way exists. So please share your corrections and thoughts (but please don't be a jerk about it either).

##Provenance

Michael Stephens wrote a [demo reconcilliation service](https://github.com/mikejs/reconcile-demo) and Ted Lawless wrote a [FAST reconciliation service](https://github.com/lawlesst/fast-reconcile) that this code basically repeats but for a different API.

Please give any thanks for this work to Ted Lawless, and any complaints to Christina.

##Special Notes

This came out of frustration that the Library of Congress authorities are: 

- haphazard in containing Latitude and Longitude in the authority records for geographic names/subjects (although a requirement for authorities now, many such authorities do not contain the coordinates currently)
- the way that the Library of Congress authorities formulate place names for primary headings (not as subdivisions) would often return no results in the GeoNames API because of abbreviations, many of which for U.S. states were unique to the Library of Congress authorities (for example, 'Calif.' for headings of cities in California). 

So this service takes Library of Congress authorities headings (or headings formulated to mimic the LoC authorities structure), expand U.S. abbreviations, then reconcile against GeoNames. The returned GeoNames 'name' gives both the GeoNames name for the location as well as the coordinates. There are, no doubts, better ways to handle getting both in an OpenRefine reconciliation service, but this was a quick hack to get both while I continue to explore how OpenRefine Reconciliation Services are structured.

##Instructions

Before getting started, you'll need python on your computer (this was built/tested with python 2.7.8, should work with python 3 too) and be comfortable using OpenRefine/Google Refine. 

This reconciliation service also requires a GeoNames API username. You can find and use the one used in the original code for testing, but you'll run against maximum number counts quickly, so it is strongly recommended you get your own (free, quick & easy to obtain) GeoNames account.

To do so, go to this webpage and register: http://www.geonames.org/login

- Once you have your GeoNames username, go ahead and clone/download/get a copy of this code repository on your computer.
- Open up reconcile.py and add your username to the variable declaration on line 35 (e.g. geonames_username = 'my_user_name'). Save the file on your computer.
- In the Command Line Interface of your choice (Terminal on my Mac), cd to the directory where you downloaded this code and type in: python reconcile.py --debug (you don't need to use debug but this is helpful for knowing what this service is up to while you are working with it).
- You should see a screen telling you that the service is 'Running on http://0.0.0.0:5000/'.
- Leaving that terminal window open, go start up OpenRefine (however you normally go about it). Open a project in OpenRefine.
- On the column you would like to reconcile with GeoNames, click on the arrow at the top, choose 'Reconcile' > 'Start Reconciling...'
- Click on the 'Add Standard Service' button in the bottom left corner. 
- Now enter the URL that the local 

##Plans for Improvement

I'm hoping to build in next a way for searching within reconciliation cells next. 

I'd like to expand the extremely rudimentary but gets the job done LoC geographic names abbreviations parser/expander text to handle other LoC Authorities abbreviations oddities. I'm afraid to say, since even the states abbreviations vary in their construction, these will need to be added on a case by case basis.

I'd also like to build in a way to use other columns as additional search properties.

Finally, finding a better way to handling the API username updates as well as parsing name plus coordinates (instead of the hack I've put into this for the time being) would be great.

