# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['AddVoteTestCase::test_add_vote 1'] = {
    'data': {
        'addVote': None
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 3,
                    'line': 3
                }
            ],
            'message': 'UserProfile matching query does not exist.',
            'path': [
                'addVote'
            ]
        }
    ]
}

snapshots['AnimeQLTestCase::test_anime 1'] = {
    'data': {
        'allAnime': {
            'edges': [
            ]
        }
    }
}

snapshots['FindWinnerTestCase::test_find_winner 1'] = {
    'data': {
        'winner': {
            'animeAwards': [
            ]
        }
    }
}
