# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['UserAnimeTestCase::test_update_user_anime 1'] = {
    'data': {
        'updateUserAnime': None
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 4,
                    'line': 3
                }
            ],
            'message': 'UserProfile matching query does not exist.',
            'path': [
                'updateUserAnime'
            ]
        }
    ]
}
