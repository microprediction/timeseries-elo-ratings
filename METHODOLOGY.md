
## Interpretation of Elo ratings:

Using an F-factor of 1000, one can interpret Elo rating differences as the probability that one model will outperform the other, as measured by root mean square error, when
tasked with fifty consecutive k-step ahead forecasts. Both models are supplied 400 prior data points to warm up on. If the errors are within one percent of each other, a draw is declared. The probability of the weaker model winning is

       P(win) = 1. / (1 + 10 ** (rating difference / 1000))

Consult the [eloformulas.py](https://github.com/microprediction/timemachines/blob/main/timemachines/skatertools/comparison/eloformulas.py) and the script
[skatereloupdate.py](https://github.com/microprediction/timemachines/blob/main/timemachines/skatertools/comparison/skaterelo.py) in the timemachines package if you seek more details. Constants are set in the script [update_skater_elo_ratings](https://github.com/microprediction/timeseries-elo-ratings/blob/main/update_skater_elo_ratings.py) and change from time to time.  



    


