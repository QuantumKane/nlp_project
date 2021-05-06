"""
A module for obtaining repo readme and language data from the github API.
Before using this module, read through it, and follow the instructions marked
TODO.
After doing so, run it like this:
    python acquire.py
To create the `data.json` file that contains the data.
"""
import os
import json
from typing import Dict, List, Optional, Union, cast
import requests

from env import github_token, github_username

# TODO: Make a github personal access token.
#     1. Go here and generate a personal access token https://github.com/settings/tokens
#        You do _not_ need select any scopes, i.e. leave all the checkboxes unchecked
#     2. Save it in your env.py file under the variable `github_token`
# TODO: Add your github username to your env.py file under the variable `github_username`
# TODO: Add more repositories to the `REPOS` list below.

REPOS = [
    'freeCodeCamp/chapter', 'freeCodeCamp/freeCodeCamp', 'freeCodeCamp/nginx-config', 'freeCodeCamp/chat-config',
    'freeCodeCamp/devdocs', 'freeCodeCamp/news-theme', 'freeCodeCamp/testable-projects-fcc', 
    'freeCodeCamp/boilerplate-project-issuetracker','freeCodeCamp/demo-projects', 'freeCodeCamp/boilerplate-project-library',
    'freeCodeCamp/boilerplate-npm', 'freeCodeCamp/scripts', 'freeCodeCamp/coderadio-client', 'freeCodeCamp/ghost-config',
    'freeCodeCamp/how-to-contribute-to-open-source', 'freeCodeCamp/boilerplate-project-american-british-english-translator', 
    'freeCodeCamp/news-translation', 'freeCodeCamp/boilerplate-project-timestamp', 'freeCodeCamp/boilerplate-infosec',
    'freeCodeCamp/boilerplate-bcrypt', 'freeCodeCamp/boilerplate-neural-network-sms-text-classifier', 
    'freeCodeCamp/boilerplate-linear-regression-health-costs-calculator', 'freeCodeCamp/boilerplate-express',
    'freeCodeCamp/boilerplate-project-messageboard', 'freeCodeCamp/boilerplate-project-stockchecker', 
    'freeCodeCamp/boilerplate-project-filemetadata', 'freeCodeCamp/boilerplate-cat-and-dog-image-classifier',
    'freeCodeCamp/boilerplate-project-exercisetracker', 'freeCodeCamp/forum-theme', 'freeCodeCamp/boilerplate-mochachai',
    'freeCodeCamp/boilerplate-project-sudoku-solver', 'freeCodeCamp/boilerplate-time-calculator', 
    'freeCodeCamp/boilerplate-mongomongoose','freeCodeCamp/boilerplate-project-metricimpconverter', 
    'freeCodeCamp/boilerplate-budget-app', 'freeCodeCamp/boilerplate-project-urlshortener', 'freeCodeCamp/design-style-guide', 
    'freeCodeCamp/boilerplate-advancednode', 'freeCodeCamp/boilerplate-project-headerparser', 
    'freeCodeCamp/100DaysOfCode-twitter-bot','freeCodeCamp/template', 'freeCodeCamp/infra', 
    'freeCodeCamp/boilerplate-medical-data-visualizer','freeCodeCamp/boilerplate-demographic-data-analyzer',
    'freeCodeCamp/boilerplate-probability-calculator','freeCodeCamp/boilerplate-project-secure-real-time-multiplayer-game', 
    'freeCodeCamp/boilerplate-page-view-time-series-visualizer','freeCodeCamp/cdn',
    'freeCodeCamp/boilerplate-book-recommendation-engine', 'freeCodeCamp/boilerplate-sea-level-predictor', 
    'freeCodeCamp/boilerplate-mean-variance-standard-deviation-calculator','freeCodeCamp/boilerplate-SHA-1-password-cracker',
    'freeCodeCamp/boilerplate-polygon-area-calculator','freeCodeCamp/boilerplate-port-scanner',
    'freeCodeCamp/boilerplate-rock-paper-scissors','freeCodeCamp/boilerplate-arithmetic-formatter','freeCodeCamp/auth0-templates',
    'freeCodeCamp/error-pages','freeCodeCamp/demo-projects-nginx-config','freeCodeCamp/freeCatPhotoApp', 
    'freeCodeCamp/forum-users-nav', 'freeCodeCamp/CurriculumExpansion','freeCodeCamp/boilerplate-socketio',
    'freeCodeCamp/boilerplate-socialauth', 'freeCodeCamp/fcc-express-bground-pkg',
    'freeCodeCamp/2017-new-coder-survey', 'freeCodeCamp/multiple-choice-questions', 'freeCodeCamp/osfg-dir-server',
    'freeCodeCamp/fcc-github-syncing-service', 'freeCodeCamp/open-source-for-good-directory', 
    'freeCodeCamp/math-for-programmers-prototype','freeCodeCamp/2016-new-coder-survey', 'freeCodeCamp/mongodb-statsd',
    'freeCodeCamp/open2017','freeCodeCamp/conference-for-good','freeCodeCamp/donate-page',
    'freeCodeCamp/gsoc','freeCodeCamp/react-freecodecamp-search','freeCodeCamp/search','freeCodeCamp/donations-for-good',
    'freeCodeCamp/TranslationExpansion','freeCodeCamp/news','freeCodeCamp/cz-freecodecamp','freeCodeCamp/persist',
    'freeCodeCamp/ZiplineStatusChecker','freeCodeCamp/wiki-generator','freeCodeCamp/pm2-pager',
    'freeCodeCamp/actual-react-router-bootstrap','freeCodeCamp/camper-gh-bot','freeCodeCamp/camper-gitter-bot',
    'freeCodeCamp/home','freeCodeCamp/store.js','freeCodeCamp/react-notification','freeCodeCamp/arcade-mode',
    'freeCodeCamp/camper-probot','freeCodeCamp/react-bootstrap','freeCodeCamp/classroom-mode',
    'freeCodeCamp/wiki','freeCodeCamp/events','freeCodeCamp/curriculum','freeCodeCamp/terms-of-service',
    'freeCodeCamp/outreach-for-good','freeCodeCamp/gatsby-source-filesystem','freeCodeCamp/jamstack-hackathon',
    'freeCodeCamp/open-data'
]

headers = {"Authorization": f"token {github_token}", "User-Agent": github_username}

if headers["Authorization"] == "token " or headers["User-Agent"] == "":
    raise Exception(
        "You need to follow the instructions marked TODO in this script before trying to use it"
    )


def github_api_request(url: str) -> Union[List, Dict]:
    response = requests.get(url, headers=headers)
    response_data = response.json()
    if response.status_code != 200:
        raise Exception(
            f"Error response from github api! status code: {response.status_code}, "
            f"response: {json.dumps(response_data)}"
        )
    return response_data


def get_repo_language(repo: str) -> str:
    url = f"https://api.github.com/repos/{repo}"
    repo_info = github_api_request(url)
    if type(repo_info) is dict:
        repo_info = cast(Dict, repo_info)
        return repo_info.get("language", None)
    raise Exception(
        f"Expecting a dictionary response from {url}, instead got {json.dumps(repo_info)}"
    )


def get_repo_contents(repo: str) -> List[Dict[str, str]]:
    url = f"https://api.github.com/repos/{repo}/contents/"
    contents = github_api_request(url)
    if type(contents) is list:
        contents = cast(List, contents)
        return contents
    raise Exception(
        f"Expecting a list response from {url}, instead got {json.dumps(contents)}"
    )


def get_readme_download_url(files: List[Dict[str, str]]) -> str:
    """
    Takes in a response from the github api that lists the files in a repo and
    returns the url that can be used to download the repo's README file.
    """
    for file in files:
        if file["name"].lower().startswith("readme"):
            return file["download_url"]
    return ""


def process_repo(repo: str) -> Dict[str, str]:
    """
    Takes a repo name like "gocodeup/codeup-setup-script" and returns a
    dictionary with the language of the repo and the readme contents.
    """
    contents = get_repo_contents(repo)
    readme_download_url = get_readme_download_url(contents)
    if readme_download_url == "":
        readme_contents = None
    else:
        readme_contents = requests.get(readme_download_url).text
    return {
        "repo": repo,
        "language": get_repo_language(repo),
        "readme_contents": readme_contents,
    }


def scrape_github_data() -> List[Dict[str, str]]:
    """
    Loop through all of the repos and process them. Returns the processed data.
    """
    return [process_repo(repo) for repo in REPOS]


if __name__ == "__main__":
    data = scrape_github_data()
    json.dump(data, open("data.json", "w"), indent=1)