

# Introduction #

This document describes the initial model for pyvol is a multiple cluster volatility model in `pyvol.sims.MultiClusterSimulator`. The purpose of this model is to try to capture an effect known as volatility clustering. As noted by Mandelbrot (1963), "large changes tend to be followed by large changes, of either sign, and small changes tend to be followed by small changes."

The figures below show the autocorrelations of log S&P500 excess **squared** returns on the time scales of days, weeks, months, years. As the figures show, the last day/week/month does a fairly good job of predicting whether the current day/week/month will have large squared returns. Note: this doesn't mean that you can predict the direction of the returns, just the magnitude (i.e., you may know it's likely to be a big day just not whether it is up or down).

![http://pyvol.googlecode.com/svn/wiki/MultiClusterModel.attach/SmallDailyVolClusters.png](http://pyvol.googlecode.com/svn/wiki/MultiClusterModel.attach/SmallDailyVolClusters.png)

![http://pyvol.googlecode.com/svn/wiki/MultiClusterModel.attach/SmallWeeklyVolClusters.png](http://pyvol.googlecode.com/svn/wiki/MultiClusterModel.attach/SmallWeeklyVolClusters.png)

![http://pyvol.googlecode.com/svn/wiki/MultiClusterModel.attach/SmallMonthlyVolClusters.png](http://pyvol.googlecode.com/svn/wiki/MultiClusterModel.attach/SmallMonthlyVolClusters.png)

![http://pyvol.googlecode.com/svn/wiki/MultiClusterModel.attach/SmallYearlyVolClusters.png](http://pyvol.googlecode.com/svn/wiki/MultiClusterModel.attach/SmallYearlyVolClusters.png)

# The Multi Cluster Model #

Understanding, modeling, and capturing this volatility clustering effect seems important in understanding markets. Previous work initiated by Engle and Bollerslev have modelled volatility clustering with the ARCH, GARCH, and further variations of auto-regressive volatility models. While these models do capture vol clustering effects, using them to on longer time scales generally invovles estimating a very large number of coefficients and/or tracking a very large number of states.

Consequently, we consider a multiscale model illustrated below. At each level, we track a variance term which is effected by the previous variance at that level, the previous returns from the finer level and the variance from the higher level. Thus, the variance for month i is a contribution of the previous variance at that level (the variance for month i-1), the variance for year i, and the previous month's return. This continues all the way down to the realized returns.

![http://pyvol.googlecode.com/svn/wiki/MultiClusterModel.attach/MultiClusterModel.png](http://pyvol.googlecode.com/svn/wiki/MultiClusterModel.attach/MultiClusterModel.png)

By setting the alpha, beta, and omega parameters which control how the previous returns, previous variance, and previous higher level contribution are weighted, it is possible to recover a variety of simpler models such as constant variance, small GARCH-like models, etc. Furthermore, by setting the parameters appropriately, one can induce dependence across weeks, months, quarters, or years with a relatively small number of states. Since the previous figures seem to indicate that volatility clustering happens simultaneously at all these scales, this may be valuable.

# Contest Usage #

Since the multi cluster model produces vol clustering at a variety of scales, it provides the opportunity to explore the effectiveness of a wide variety of estimation algorithms and is thus useful in contents. The contest organizer can choose a reasonable set of parameters and generate some example data to provide to submitters. Submitters can then explore a range of estimation algorithms from simple ideas that only focus on daily returns to more sophisticated algorithms which use tools from graphical models to understand effects at different scales.