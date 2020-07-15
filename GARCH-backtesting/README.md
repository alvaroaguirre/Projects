# GARCH backtesting in Julia and Python

Simple comparison between computing time in Julia and Python for GARCH estimations.

Packages used are [ARCHModels](https://s-broda.github.io/ARCHModels.jl/stable/) for Julia by Simon Broda and [ARCH](https://github.com/bashtage/arch/) by Kevin Sheppard

Working with an Estimation Window of 2000 observations, Julia proved itself an average of 4x faster than Python