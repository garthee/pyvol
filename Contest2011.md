# Introduction #

This article describes the 2011 volatility challenge. Selected candidates have been asked to demonstrate their skills by attempting to build better volatility estimators. All candidates should download the python [source code](http://pyvol.googlecode.com/files/pyvol-1.0.zip) and follow the instructions below to build and submit their estimators by **12 Noon on Monday, February 7th, 2011**. Late submissions may or may not be reviewed depending on how busy the contest organizers are.

# Details #

Your goal is to produce an interesting volatility estimator and describe why it is effective. The pyvol package provides some simple volatility estimators which you can use as examples to start from. See the [Tutorial](Tutorial.md) article for details on how to use pyvol. If you are not familiar with programming in python, you may find the python tutorial at
http://docs.python.org/tutorial/ useful for getting started.

See the article on PerformanceMeasurement for a brief discussion of some ways to decide if a volatility estimator is good. As discussed there, achieving a good vol targetting error should be fairly easy so we will mostly be interested in submissions which minimize the vol spread error while also having a reasonably small vol targeting error (e.g., say less than .01).

To develop (or modify) an existing estimator, follow the instructions for the article on GenericContest. Basically, we will evaluate submissions by the vol spread error achieved when we run
```
python setup.py test -m pyvol.testing._test_EvalBest
```
on a submission. Note that we will use **different random seeds** than the ones provided in the software you download, so you should strive to develop a technique which makes sense and does well in general as opposed to one which does well for a specific random seed. We may also try solutions on samples of real asset returns.

# Submission #

Your submission should be a zip file produced by "python setup.py dist" as discussed in [GenericContest#Submitting\_Your\_Estimators](GenericContest#Submitting_Your_Estimators.md). The zip file should include your estimator in the `experimental` directory and should have `pyvol.experimental.BestEstimator.MakeEstimator` set to produce a version of your estimator. Email the zip file to **pyvoler+contest@gmail.com**.