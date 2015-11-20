

# Introduction #

This document provides walks you through how to install and use pyvol.

# Installing #

You don't really need to install pyvol. You can just download the latest source distribution from http://code.google.com/p/pyvol/downloads/list, unzip, and work directly with that. This makes it easier to package up your code and submit to a GenericContest.

If you really want to install pyvol, just do "python setup.py install" after you unzip. If you do install pyvol, make sure to either do further edits on the installed files or be careful about setting your paths appropriately.

## Set PYTHONPATH properly ##

If you do not install pyvol but instead want to edit it or develop your own estimators, you will need to tell python where pyvol lives. The simplest way to do this is to edit the PYTHONPATH environment variable on your system to point to the directory where pyvol lives.

If you are unfamiliar with environment variables, an alternative is to do the following
```
>>> import sys; sys.path.append('<path_to>/pyvol')
```
to include the proper pyvol directories when you try the python examples below.

# Using #

Once you have downloaded pyvol, you can test the existing best estimator by typing "python setup.py test" in the main pyvol directory. This will test all the source code and at the end, show the performance of the current "best estimator"

If you want to add your own estimators, you can create a file called `MyVolEst.py` and either put it outside the pyvol source tree or put it into pyvol/experimental if you are planning on submitting your estimator in a GenericContest.

Once you have created your own estimator, you can test it by starting the python interpreter and doing something like the following: (note you may need to [set your path](http://code.google.com/p/pyvol/wiki/Tutorial#Set_PYTHONPATH_properly) properly first).
```
>>> import random, datetime
>>> from pyvol.experimental import ExampleEstimators # or import your stuff
>>> from pyvol.sims import Evaluator  # used to evaluate performance
>>> estimtator = ExampleEstimators.ExponentialCovEstimator(
... .99) # try simple exp smoothing or replaec with our own estimator
>>> results = Evaluator.EvalEstimator(estimtator, seed=64) # do simulation
>>> print results[0]
yearly    : ret = 0.026, vol = 0.195, sqCorrs = 1.000, 0.123, -0.084
quarterly : ret = 0.025, vol = 0.222, sqCorrs = 1.000, 0.103, 0.138
monthly   : ret = 0.026, vol = 0.223, sqCorrs = 1.000, 0.054, 0.158
weekly    : ret = 0.026, vol = 0.242, sqCorrs = 1.000, 0.175, 0.249
daily     : ret = 0.026, vol = 0.250, sqCorrs = 1.000, 0.422, 0.276
targErr= 0.02478, spreadErr= 144.79175, naiveError= 7.86425, minPossible=2.05384
```

If you want to do more detailed work, you can walk through the
steps of generating the simulation yourself as shown below (don't forget to make sure you [set your path](http://code.google.com/p/pyvol/wiki/Tutorial#Set_PYTHONPATH_properly)):

```
>>> import random; random.seed(64) # make things repeatable    
>>> from pyvol.sims import DataSimulator, SimAPI
>>> from pyvol.est import CovEst
>>> simulator = DataSimulator.PriceSimulator(
... startDate=datetime.date(2000, 1, 3), endDate=datetime.date(2009, 1, 5))
>>> returnColName = simulator.levelParams.retNames[-1]
>>> estimator = ExampleEstimators.FullHistoryCovEstimator()
>>> estimator.SetReturnColName(returnColName)
>>> estimatorTx = CovEst.EstimateVols(estimator, 'estimatedVol')
>>> query = simulator.MakeSimulatedData([estimatorTx])
>>> stats = SimAPI.MakeStats(query, simulator.levelParams)
>>> print stats
yearly    : ret = 0.129, vol = 0.286, sqCorrs = 1.000, -0.316, -0.022
quarterly : ret = 0.132, vol = 0.235, sqCorrs = 1.000, -0.123, 0.091
monthly   : ret = 0.142, vol = 0.216, sqCorrs = 1.000, -0.048, -0.023
weekly    : ret = 0.141, vol = 0.262, sqCorrs = 1.000, 0.136, 0.308
daily     : ret = 0.144, vol = 0.272, sqCorrs = 1.000, 0.439, 0.355
```

If you have windows and the windows python tools installed
you can do the following to display the data in Excel:
```
>>> from pyvol.tseries import ExcelTools; ExcelTools.TimeSeqToExcel(results[1])
```

If not, you can just write the output to a file to investigate
or look directly at `results[1].data`:
```
>>> import tempfile, os
>>> filename = tempfile.mktemp(suffix='_pyvol_sim.csv')
>>> results[1].WriteToSimpleCSVFile(filename)
>>> os.remove(filename) # remove the file when you are don with it.
```