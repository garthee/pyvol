# Introduction #

One complication of volatility estimation is that volatility is latent: we observe returns but can only infer volatility. This can lead to a variety of subtle difficulties. We adopt two simple measures of effectiveness which we call the targeting error and the spread error.

## Vol Targeting Error ##

The targeting error is simply the realized standard deviation vs. the target standard deviation of returns. So if the target volatility is 10% per year and the realized is 10.1% per year, the targeting error is .1%. Almost any reasonable estimator should be able to achieve a very small targeting error over a long enough period.

## Vol Spread Error ##

The vol spread error is designed to measure how consistent an algorithm is at estimating volatility. To compute the spread error, we first normalize the entire sequence of returns by dividing it by a constant so that the targeting error is zero. Next, we compute the average (n\*n - 1) where n is the normalized daily return. We view an estimation algorithm as good if it results in the lowest vol spread error.

## Software Implementation ##

These error measures are implemented in the `pyvol.sims.Evaluator` module.