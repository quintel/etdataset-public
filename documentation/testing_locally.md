# Testing a dataset on your local machine

<!-- Introduction about testing -->

<!-- Gain access to Atlas, ETEngine and ETModel -->

<!-- More about running ETsource, Atlas, ETengine and ETmodel -->

1. Import all relevant files in the `data/country/year/output` folders of ETDataset in ETSource. This can be done by running `rake import`, or `rake import DATASET=nl` in ETSource. Replace `nl` with the country you want to import.

2. Test if all converter demands can be calculated. Go to the Atlas repository, and run `rake debug DATASET=nl`. Replace `nl` with the country you want to test. (You may want to add `FAST=true` to that command line, to skip the generation of graphs. Advanced users: alternatively, you can also run `bundle exec rspec` on ETSource, which also tests whether the rspec-tests in
the [Mechanical Turk repository](https://github.com/quintel/mechanical_turk) succeed.)

3. Run ETEngine and ETModel locally and compare with the [beta](http://beta.pro.et-model.com) or [production](http://pro.et-model.com) servers of the ETM.
