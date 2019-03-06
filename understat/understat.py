import asyncio
import re

import aiohttp
from bs4 import BeautifulSoup

from understat.constants import LEAGUE_URL, PATTERN
from understat.utils import decode_data, fetch, find_match, to_league_name


class Understat():
    def __init__(self, session):
        self.session = session

    async def get_teams(self, league_name, season):
        """Returns a dictionary containing information about all the teams in
        the given league in the given season.

        :param league_name: The league's name.
        :type league_name: str
        :param season: The season.
        :type season: str or int
        :return: A dictionary of the league's table as seen on Understat.
        :rtype: dict
        """

        league_name = to_league_name(league_name)
        url = LEAGUE_URL.format(league_name, season)

        html = await fetch(self.session, url)
        soup = BeautifulSoup(html, "html.parser")
        scripts = soup.find_all("script")

        pattern = re.compile(PATTERN.format("teamsData"))
        match = find_match(scripts, pattern)
        team_data = decode_data(match)

        return team_data

    async def get_players(self, league_name, season):
        league_name = to_league_name(league_name)
        url = LEAGUE_URL.format(league_name, season)

        html = await fetch(self.session, url)
        soup = BeautifulSoup(html, "html.parser")
        scripts = soup.find_all("script")

        pattern = re.compile(PATTERN.format("playersData"))
        match = find_match(scripts, pattern)
        players_data = decode_data(match)

        return players_data

    async def get_results(self, league_name, season):
        league_name = to_league_name(league_name)
        url = LEAGUE_URL.format(league_name, season)

        html = await fetch(self.session, url)
        soup = BeautifulSoup(html, "html.parser")
        scripts = soup.find_all("script")

        pattern = re.compile(PATTERN.format("datesData"))
        match = find_match(scripts, pattern)
        results_data = decode_data(match)

        results = [result for result in results_data if result["isResult"]]
        return results

    async def get_fixtures(self, league_name, season):
        league_name = to_league_name(league_name)
        url = LEAGUE_URL.format(league_name, season)

        html = await fetch(self.session, url)
        soup = BeautifulSoup(html, "html.parser")
        scripts = soup.find_all("script")

        pattern = re.compile(PATTERN.format("datesData"))
        match = find_match(scripts, pattern)
        fixtures_data = decode_data(match)

        fixtures = [fixture for fixture in fixtures_data
                    if not fixture["isResult"]]

        return fixtures
