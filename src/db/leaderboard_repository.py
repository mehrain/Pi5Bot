from db import BDDB

class LeaderboardRepository:

    def __init__(self):
        self.bddb = BDDB()

    def store_leaderboards(self, leaderboards):
        self.bddb.insert_leaderboard()
        pass