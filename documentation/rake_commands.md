# Rake commands

The following rake tasks are defined by Quintel Intelligence:


## ETSource repository

The following rake tasks kan be performed to import the Input Data from the ETDataset repository into the ETSource repository

`rake import`
import all Input Data from the ETDataset repository

`rake import DATASET=nl`
import all Input Data for the specified country from the ETDataset repository


## Atlas repository

All rake tasks performed on the atlas repository work with files from ETSource (not ETDataset).  When using the `atlas` repository, you may find these commands interesting:

`bundle exec rake debug`
will calculate a 'graph' in refinery and trace any caculation and validation errors. The energy flow is visualized in pictures, which can be found in the debug folders on .../atlas/tmp/...

`rake debug` 
short version of `bundle exec rake debug`

`rake debug DATASET=nl`
this will perform the debug task only on the country specified. (nl for Netherlans, de for Germany, etc.)

`rake debug DATASET=nl FAST=true`
this will only calculate and validate the graph, without producing the pictures (which takes a long time). Very useful for checking if your CSV files on `etsource` are functional. 

`rake import`
this will copy all CSV files (in the `etdataset`/ouput folders) to their respective location on `etsource`. 

`rake import DATASET=nl`
this will perform a `rake import` for only one country. 