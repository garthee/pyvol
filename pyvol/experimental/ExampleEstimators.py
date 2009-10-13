"""Module containing example estimators illustrating how to write your own.
"""

import math
from pyvol.est.CovEst import CovEstimator

class FullHistoryCovEstimator(CovEstimator):
    """Simple example covariance estimator using full history of the data.

    NOTE: This estimator is *SLOW* because it looks at all the past data.

    The following illustrates example usage and evaluating of this estimator:

>>> import random, datetime
>>> import ExampleEstimators
>>> from pyvol.sims import DataSimulator, SimAPI
>>> from pyvol.est import CovEst
>>> seed = 64
>>> random.seed(seed)
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

    """

    def __init__(self, *args, **kw):
        "Initializer just passes args onto CovEstimator.__init__."
        CovEstimator.__init__(self, *args, **kw)

    def Estimate(self, args, query, line):
        """Override Estimate as required by CovEstimator class

        Here is the function where we do the actual work. In this case,
        we simply look at the sample variance for all data.
        """
        
        _ignore = args  # this estimator doesn't use args so ignore them
        if (line < 10): # Wait until we have a few data points to do an estimate
            return None 
        returns = [row[self.returnCol] for row in query.data[0:line]]
        volEst = math.sqrt(sum([r*r for r in returns])/float(len(returns)))
        return volEst

class ExponentialCovEstimator(CovEstimator):
    """Covariance estimator with an exponetial averaging estimate.

    The following illustrates example usage and evaluating of this estimator:

>>> import random, datetime
>>> import ExampleEstimators
>>> from pyvol.sims import DataSimulator, SimAPI
>>> from pyvol.est import CovEst
>>> seed = 64
>>> random.seed(seed)
>>> simulator = DataSimulator.PriceSimulator()
>>> returnColName = simulator.levelParams.retNames[-1]
>>> estimator = ExampleEstimators.ExponentialCovEstimator(.95)
>>> estimator.SetReturnColName(returnColName)
>>> estimatorTx = CovEst.EstimateVols(estimator, 'estimatedVol')
>>> query = simulator.MakeSimulatedData([estimatorTx])
>>> _ignore = query.AddBlankColumns(['position'],default=1.0)
>>> from pyvol.sims import Evaluator
>>> errors = Evaluator.EvaluateQuery(
... query, 'position', 'scaledPos', 'estimatedVol',
... returnColName, simulator.levelParams.annualizedVolNames[-1],
... simulator.startDate)
>>> stats = SimAPI.MakeStats(query, simulator.levelParams)
>>> print stats
yearly    : ret = 0.026, vol = 0.195, sqCorrs = 1.000, 0.123, -0.084
quarterly : ret = 0.025, vol = 0.222, sqCorrs = 1.000, 0.103, 0.138
monthly   : ret = 0.026, vol = 0.223, sqCorrs = 1.000, 0.054, 0.158
weekly    : ret = 0.026, vol = 0.242, sqCorrs = 1.000, 0.175, 0.249
daily     : ret = 0.026, vol = 0.250, sqCorrs = 1.000, 0.422, 0.276
>>> print (
... 'targErr= %.5f, spreadErr= %.5f, naiveError= %.5f, minPossible=%.5f'%(
... errors))
targErr= 0.01283, spreadErr= 53.26522, naiveError= 7.92135, minPossible=2.06377
    """

    def __init__(self, smoothing, *args, **kw):
        """Initializer.
        
        INPUTS:
        
        -- smoothing:   Smoothing parameter between 0 and 1 to use in
                        doing exponential average.
        
        -- *args, **kw:  Passed to CovEstimator.__init__.
        
        """
        self.smoothing = smoothing
        self.state = None
        CovEstimator.__init__(self, *args, **kw)

    def Startup(self, query):
        "Reset state on startup"
        
        _ignore = query
        self.state = None
        CovEstimator.Startup(self, query) # call parent version too

    def Estimate(self, args, query, line):
        """Override Estimate as required by CovEstimator class

        Here is the function where we do the actual work. In this case,
        we simply look at the sample variance for data from self.lookback
        to the current line (not including current line).
        """
        
        _ignore = args
        if (line == 0):
            return None # no data yet
        squaredReturn = query.data[line-1][self.returnCol]**2
        if (self.state is None):
            self.state = squaredReturn
        else:
            self.state = ((1 - self.smoothing) * self.state
                          + self.smoothing * squaredReturn)
            
        return math.sqrt(self.state) if self.state > 0 else None
