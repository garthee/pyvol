# Introduction #

One of the goals of pyvol is to allow class projects, contests, and other comparisons of different volatility estimation approaches. This page describes how to use pyvol in such a framework.



# For contestants #

If you are entering a pyvol contest, you should do the following:

## Developing Your Estimators ##

To develop your own estimators:

  1. Download pyvol from the [downloads](http://code.google.com/p/pyvol/downloads/list).
    * You generally want the most recent version which ends in .zip (i.e., the source distribution).
  1. Unzip the source distribution and take a look at `pyvol/est/CovEst.py`.
    * This module contains the basic API for vol estimation used by pyvol.
  1. Create a new python file in `pyvol/experimental/MyCovEst.py` for your estimators.
  1. Write your own vol estimator in `pyvol/experimental/MyCovEst.py` by subclassing `pyvol.est.CovEst.CovEstimator` and overriding the Estimate method.
    * You can look in `pyvol.experimental.ExampleEstimators` for an example.
    * You should not change anything outside the experimental directory as discussed in more detail [below](GenericContest#Important_Points.md).
  1. Edit `pyvol.est.BestEstimator.MakeEstimator` to produce an instance of your estimator.
  1. In the main pyvol directory, do
```
python setup.py test
```
> > to test your edits.
    * This will test all the code and at the end, do a test of the estimator in `pyvol.est.BestEstimator.MakeEstimator`.
    * If you set `MakeEstimator` properly, this will show the performance of your estimator.
    * If you just want to test your estimator (which is faster than testing all the code), you can do
```
python setup.py test -m pyvol.testing._test_EvalBest
```
  1. To submit your estimator as an entry in the contest, follow the instructions in the section on [Submitting Your Estimators](GenericContest#Submitting_Your_Estimators.md).

## Submitting Your Estimators ##

Once you have tested your estimators and are ready to submit, do the following:

  1. Open a command prompt and enter the main pyvol directory that contains setup.py.
  1. Edit setup.py as follows:
    1. Set name = `"pyvol-<first_name>-<last_name>"` to distinguish your entry from others.
    1. Set the version if you like.
    1. Set the author and author\_email fields to yourself or your team.
    1. Edit long\_description to provide a description of your approach or point to other files documenting your approach.
  1. Do `"python setup.py sdist"` to create a zipped version of your project (this will appear in the dist subdirectory).
  1. Submit the resulting zip distribution as described by the contest organizer.

## Important Points ##

You should make sure that "python setup.py test" passes all tests before submitting. The contest organizer will either use this command (probably with a secretely chosen seed) or otherwise write a script to create an instance of your estimator via `pyvol.est.BestEstimator.MakeEstimator`, run it through simulations, and measure its performance.

Also, you should generally avoid modifying anything outside `pyvol/experimental`. The contest organizer will probably just extract the code in pyvol/experimental and use his own version of the contest framework. This is simpler for the organizer, makes it less likely that a rogue submission accidentally (or perhaps intetionally) circumvents the contest rules, and reduces the amount of code the contest organizer has to look at. This is worth pointing out again:
  * **Anything outside pyvol/experimental will be ignored by the contest organizer**.



# Configuring pyvol for your own project or contest #

If you want to create your own contest, you can do the following:

  1. Download the source code for pyvol
  1. Edit as desired (e.g., setting default simulation parameters)
  1. Rename to `pyvol-<your-contenst-name>`
  1. Create a source distribution via `python setup.py sdist`
  1. Distribute the source distribution to contestants and use the above ways of running the contest.

Please let us know if you run a contest like that and we will link to it from here.

# Details #

Add your content here.  Format your content with:
  * Text in **bold** or _italic_
  * Headings, paragraphs, and lists
  * Automatic links to other wiki pages