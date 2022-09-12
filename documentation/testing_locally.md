# Testing a dataset on your local machine

Once you have finished your dataset, it is important to test if the ETM is able to cope with your dataset. Testing your dataset for the ETM involves two steps:

1. You should test if the defined [graph structure](https://github.com/quintel/documentation#the-energy-calculation) and the corresponding energy flows (for the base year) can be calculated. This process is performed by [Atlas](https://github.com/quintel/atlas). See [Testing with Atlas](#testing_with_atlas) for more information.

2. When Atlas is able to initialize the graph, you can test and investigate your dataset by running the model using [ETEngine](https://github.com/quintel/etengine) and [ETModel](https://github.com/quintel/etmodel). See [Testing with ETEngine and ETModel](#testing-with-etengine-and-etmodel) for more information.


## Getting started with testing

1. Import all relevant files in the `data/country/year/output` folders of ETDataset in ETSource. This can be done by running `bundle exec rake import`, or `bundle exec rake import DATASET=nl` in ETSource. Replace `nl` with the country you want to import.


## Testing with Atlas

1. Gain access to the [Atlas](https://github.com/quintel/atlas) repository.
- Get up to speed with running Atlas.
- Test if all converter demands can be calculated. Go to the Atlas repository, and run `bundle exec rake debug DATASET=nl`. Replace `nl` with the country you want to test. (You may want to add `FAST=true` to that command line, to skip the generation of graphs. Advanced users: alternatively, you can also run `bundle exec rspec` on ETSource, which also tests whether the rspec-tests in
the [Mechanical Turk repository](https://github.com/quintel/mechanical_turk) succeed.)

<!-- How to "Get up to speed with running Atlas?" -->


## Testing with ETEngine and ETModel

1. Gain access to the [ETEngine](https://github.com/quintel/etengine) and [ETModel](https://github.com/quintel/etmodel) repositories.
- Get up to speed with running ETEngine and ETModel.
- Run ETEngine and ETModel locally and compare with the [beta](http://beta.pro.et-model.com) or [production](http://pro.et-model.com) servers of the ETM.

<!-- How to "Get up to speed with running ETEngine and ETModel?" -->
