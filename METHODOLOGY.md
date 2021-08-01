
## Interpretation of Elo ratings:

Using an F-factor of 1000, one can interpret Elo rating differences as the probability that one model will outperform the other, as measured by root mean square error, when
tasked with fifty consecutive k-step ahead forecasts. Both models are supplied 400 prior data points to warm up on. If the errors are within one percent of each other, a draw is declared. 

       P(win) = 1. / (1 + 10 ** (rating difference / 1000))

Consult the [eloformulas.py](https://github.com/microprediction/timemachines/blob/main/timemachines/skatertools/comparison/eloformulas.py) for
the conversion from Elo difference to winning probability, just in case it has changed, but at time of writing we have:

    


