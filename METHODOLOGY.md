
## Interpretation of Elo ratings:

Using an F-factor of 1000, one can interpret Elo rating differences as the probability that one model will outperform the other, as measured by root mean square error, when
tasked with fifty consecutive k-step ahead forecasts. 


Consult the [eloformulas.py](https://github.com/microprediction/timemachines/blob/main/timemachines/skatertools/comparison/eloformulas.py) for
the conversion from Elo difference to winning probability, just in case it has changed, but at time of writing we have:

      def elo_expected(d :float ,f :float =400 )->float:
          """ Expected points scored in a match by White player
          :param d:   Difference in rating (Black minus White)
          :param f:   "F"-Factor
          :return:
          """
          if d/ f > 8:
              return 0.0
          elif d / f < -8:
              return 1.0
          else:
              return 1. / (1 + 10 ** (d / f))




