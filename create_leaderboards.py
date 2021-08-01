import json
import os
from pprint import pprint


THIS_PATH = os.path.dirname(os.path.realpath(__file__))
ELO_PATH = THIS_PATH + os.path.sep + 'ratings'


def load_all_games():
    def load_json(file):
        with open(os.path.join(ELO_PATH, file), "r") as f:
            ret = json.load(f)
        return ret

    games = list()
    i = 0
    leaderboard_jsons = dict(
        (file, load_json(file)) for file in os.listdir(ELO_PATH) if os.path.isfile(
            os.path.join(ELO_PATH, file)
        ) and os.path.join(ELO_PATH, file).endswith(".json")
    )
    return leaderboard_jsons               # "name" and "rating" keys are important


def get_html_table_rows(data):
    data_dict = {}
    for name, rating, count, active, pypi, scnds in zip(data["name"], data["rating"], data["count"], data["active"], data["pypi"], data['seconds']):
        pypi_name = pypi.split('/project/')[-1]
        pypi_url = '<a href="'+pypi+'">' + pypi_name + '</a>'
        tm_url = '<a href="https://github.com/microprediction/timemachines">timemachines</a>'
        if 'timemachines' not in pypi_url:
            pypi_url = pypi_url + ' , '+tm_url
        data_dict[name] = (rating,count, active, pypi_url, scnds )

    data_dict = dict(sorted(data_dict.items(), key=lambda item: item[1], reverse=True))

    html = "<tr><th>Name</th><th>Rating</th><th>Games</th><th>Active</th><th>Seconds</th><th>Dependencies</th> </tr>"
    for name, (rating,count,active,pypi,scnds) in data_dict.items():
        active_str = 'yes' if active else 'no'
        html += f"<tr><td>{name.replace('_cube','')}</td><td>{round(rating, 0)}</td><td>{round(count, 0)}</td><td>{active_str}</td><td>{round(10*scnds)/10}</td><td>{pypi}</td></tr>"
    return html


# For overall.json
def get_overall_html_str(file, data, navbar):
    return f"""<html>
<head><link rel="stylesheet" href="../style.css" type="text/css"></head>
<body>
    <div class="left">{navbar}</div>
    <div class="right">
        <h1>Overall Elo Leaderboard for {file}</h1>
        <table class="default-table">
            {get_html_table_rows(data)}
        </table>
    </div>
</body>
</html>"""

# For all the other jsons
def get_html_str(file, data, navbar):
    parse_file = file.replace(".json", "")
    args = parse_file.split("_")


    return f"""<html>
<head><link rel="stylesheet" href="../style.css" type="text/css"></head>
<body>
    <div class="left">{navbar}</div>
    <div class="right">
        <h1>Accuracy and Speed of Some Short Term Automated Time-Series Forecasting Approaches (Python Packages only)</h1>
The Elo Ratings in this table are produced transparently in the repo <a href="https://github.com/microprediction/timeseries-elo-ratings">timeseries-elo-ratings</a> and 
based on k-step ahead prediction duels using <a href="https://www.microprediction.org/browse_streams.html">live time series data</a>. See <a href="https://github.com/microprediction/timeseries-elo-ratings/blob/main/METHODOLOGY.md">METHODOLOGY.md</a> for 
interpretation of Elo ratings. The table named <a href="https://microprediction.github.io/timeseries-elo-ratings/html_leaderboards/univariate-k_002.html">univariate-k_002</a> refers to 2-step ahead prediction, 
and so forth. Residual leaderboards use so-called z-streams (as explained in <a href="https://www.linkedin.com/pulse/short-introduction-z-streams-peter-cotton-phd/">An Introduction to Z-Streams</a>). 
<p>
There is some motivation in the blog post <a href="https://www.microprediction.com/blog/fast">Fast Python Time-Series Forecasting</a>. All algorithms
utilized here can be called the same way using the <a href="https://github.com/microprediction/timemachines">TimeMachines</a> Python package. However, as indicated
in the table, some of
these draw an important part of their functionality (if not all) from other packages such as Facebook Prophet,
Statsmodels TSA, Flux, PmdArima, Uber Orbit and <a href="https://github.com/microprediction/timemachines/tree/main/timemachines/skaters">more</a>. Take relative performance
with with a grain of salt, since many packages don't intend completely autonomous use and some are aimed at longer term seasonal forecasts. If you have a suggestion for a package or technique that should be included, please file an <a href="https://github.com/microprediction/timemachines/issues">issue<a/> or, even better, add a 
<a href="https://github.com/microprediction/timemachines/tree/main/timemachines/skaters">skater</a> and make a pull request. There is
a <a href="https://github.com/microprediction/timemachines/blob/main/CONTRIBUTE.md">guide for contributors</a> and a long list of <a href="https://www.microprediction.com/blog/popular-timeseries-packages">popular time-series packages</a>. 
<p>
Some of these methods are used in real-time to provide free prediction to anyone who publishes public data using 
a <a href="http://api.microprediction.org/">community API</a> explained at <a href="https://www.microprediction.com">microprediction.com</a>. See the <a href="https://github.com/microprediction/microprediction/tree/master/crawler_examples">example crawlers</a> folder
for examples of algorithms calling the timemachines package. See the <a href="https://www.microprediction.com/knowledge-center">knowledge center</a> or <a href="https://github.com/microprediction/timemachines/blob/main/CONTRIBUTE.md">contributor guide</a> for
instructions on publishing live data that can influence these ratings. 
        <p>
        <table class="default-table">
            {get_html_table_rows(data)}
        </table>
    </div>
</body>
</html>"""

def get_html_navbar(json_names):
    div = "<h3>Leaderboards</h3>"
    for name in json_names:
        name_html = name.replace(".json", ".html")
        div += f"<a href='{name_html}'>{name.replace('.json','')}</a>"
    return div

# For index.html
def get_index_html_str(json_names):
    navbar = "<h3>Leaderboards</h3>"
    for name in json_names:
        name_html = name.replace(".json", ".html")
        navbar += f"<a href='html_leaderboards/{name_html}'>{name}</a>"
    return f"""<html>
<head><link rel="stylesheet" href="style.css" type="text/css"></head>
<body>
    <div class="left">
        {navbar}
    </div>
</body>
</html>"""


def add_overall_json(json_lbs):
    from momentum.objects import RunningVariance
    all_names_set = set()
    for lb_name, lb_data in json_lbs.items():
        for nm in lb_data['name']:
            all_names_set.add(nm)
    all_names = list(all_names_set)
    all_elo = dict([ (nm, RunningVariance()) for nm in all_names ])
    all_seconds = dict([(nm, RunningVariance()) for nm in all_names])
    all_pypi = dict([(nm, '') for nm in all_names])
    all_counts = dict([(nm,0) for nm in all_names])
    all_active = dict([(nm,False) for nm in all_names])
    for lb_name, lb_data in json_lbs.items():
        for nm,rtg,cnt,snds,url,act in zip( lb_data['name'],lb_data['rating'],lb_data['count'],lb_data['seconds'],lb_data['pypi'],lb_data['active'] ):
            if cnt>=10:
                all_elo[nm].update(value=rtg)
                all_seconds[nm].update(value=snds)
                all_pypi[nm] = url
                all_counts[nm] += cnt
                all_active[nm] = all_active[nm] or act

    overall = {
            'name':all_names,
            'rating':[all_elo[nm].mean for nm in all_names],
            'count':[all_counts[nm] for nm in all_names],
            'seconds':[all_seconds[nm].mean for nm in all_names],
            'active':[True for _ in all_names],
            'pypi':[all_pypi[nm] for nm in all_names]
    }
    json_lbs['overall.json'] = overall
    overall_fast = dict( [ (ky,[v for v,sc in zip(vl, overall['seconds']) if 0<sc<1 ]) for ky, vl in overall.items() ] )
    json_lbs['fastest.json'] = overall_fast
    overall_moderate = dict(
        [(ky, [v for v, sc in zip(vl, overall['seconds']) if 0 < sc < 30]) for ky, vl in overall.items()])
    json_lbs['faster.json'] = overall_moderate

    return json_lbs


if __name__ == '__main__':
    if True:
        unsorted_json_lbs = load_all_games()
        unsorted_json_lbs = add_overall_json(json_lbs=unsorted_json_lbs)
        json_lbs = {k: v for k, v in sorted(unsorted_json_lbs.items(), key=lambda item: item[0])}

        HTML_DIR = os.path.join(THIS_PATH, "docs", "html_leaderboards")
        if not os.path.exists(HTML_DIR):
            os.mkdir(HTML_DIR)

        with open(os.path.join(THIS_PATH, "docs", "index.html"), "w") as f:
            f.write(get_index_html_str(json_lbs.keys()))

        navbar = get_html_navbar(json_lbs.keys())
        for file, data in json_lbs.items():
            file_html = file.replace(".json", ".html")
            with open(os.path.join(HTML_DIR, file_html), "w") as f:
                 f.write(get_html_str(file, data, navbar))

