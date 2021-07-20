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
        pypi_url = '<a href="'+pypi+'">+pypi+'</a>'
        data_dict[name] = (rating,count, active, pypi_url, scnds )

    data_dict = dict(sorted(data_dict.items(), key=lambda item: item[1], reverse=True))

    html = "<tr><th>Name</th><th>Rating</th><th>Games</th><th>Active</th><th>Seconds</th><th>Package</th> </tr>"
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
        <h1>Ongoing Performance Comparison of Python Time-Series Forecasting Techniques</h1>
Ratings are produced by <a href="https://github.com/microprediction/timeseries-elo-ratings">timeseries-elo-ratings</a> and 
based on k-step ahead prediction duels using <a href="https://www.microprediction.org/browse_streams.html">live time series data</a> taken from 
<a href="www.microprediction.com">microprediction.com</a>. 
<p>
All algorithms shown here can be found in the <a href="https://github.com/microprediction/timemachines">TimeMachines</a> Python package. However as indicated some of
these draw their essential functionality from
from <a href="https://www.microprediction.com/blog/popular-timeseries-packages">popular Python time-series packages</a> like Facebook Prophet, Statsmodels TSA, Flux, PmdArima, Uber Orbit and <a href="https://github.com/microprediction/timemachines/tree/main/timemachines/skaters">more</a>. If you have a suggestion
please file a <a href="https://github.com/microprediction/timemachines/issues">issue<a/> or, even better, add a 
<a href="https://github.com/microprediction/timemachines/tree/main/timemachines/skaters">skater</a> and make a pull request. There is 
a <a href="https://github.com/microprediction/timemachines/blob/main/CONTRIBUTE.md">guide for contributors</a> willing to make autonomous univariate
time series prediction functions. 
        <p>
Wins and losses and the occasional draw are based on RMSE with 400 training points and 50 out of sample predictions. Residual streams use data from probability integral 
transforms (as explained in <a href="https://www.linkedin.com/pulse/short-introduction-z-streams-peter-cotton-phd/">An Introduction to Z-Streams</a>). 
<p>
Some of these methods are used in real-time to predict live data. That live data can in turn be published by anyone. See the <a href="https://github.com/microprediction/microprediction/tree/master/crawler_examples">example crawlers</a> folder
for examples of live algorithms. See the <a href="https://www.microprediction.com/knowledge-center">knowledge center</a> or <a href="https://github.com/microprediction/timemachines/blob/main/CONTRIBUTE.md">contributor guide</a> for instructions
on publishing live data that can influence these ratings. Further motivation for the project is explained at <a href="https://www.microprediction.com/">microprediction.com</a>. 
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

if __name__ == '__main__':
    if True:
        jsons = load_all_games()

        HTML_DIR = os.path.join(THIS_PATH, "docs", "html_leaderboards")
        if not os.path.exists(HTML_DIR):
            os.mkdir(HTML_DIR)

        with open(os.path.join(THIS_PATH, "docs", "index.html"), "w") as f:
            f.write(get_index_html_str(jsons.keys()))

        navbar = get_html_navbar(jsons.keys())
        for file, data in jsons.items():
            file_html = file.replace(".json", ".html")
            with open(os.path.join(HTML_DIR, file_html), "w") as f:
                if file == "overall.json":
                    f.write(get_overall_html_str(file, data, navbar))
                else:
                    f.write(get_html_str(file, data, navbar))
