from django.test import TestCase
from .models import User, UsersList, Tournament

class TournamentTestCase(TestCase):
    def setUp(self):
        test_users_list = UsersList.objects.create(
            name = 'Test_users_list',
        )

        User.objects.create(
            name = 'Test_user_1',
            list = test_users_list,
        )

    def test_tournament_fill_in(self):
        test_user = User.objects.get(name='Test_user_1')

        test_tournament = Tournament(
            name = 'Test_tournament',
            host = test_user,
            players_count = 2,
        )

        test_tournament.add_leaderboard_user('TOTO')
        self.assertEqual('TOTO', test_tournament.leaderboard[0])

        test_tournament.add_leaderboard_user('TATA')
        self.assertEqual('TATA', test_tournament.leaderboard[1])