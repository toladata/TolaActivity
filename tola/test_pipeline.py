import json

from social.exceptions import AuthException

from social.tests.models import TestUserSocialAuth, TestStorage, User
from social.tests.strategy import TestStrategy
from social.tests.actions.actions import BaseActionTest


class IntegrityError(Exception):
    pass


class UnknownError(Exception):
    pass


class IntegrityErrorUserSocialAuth(TestUserSocialAuth):
    @classmethod
    def create_social_auth(cls, user, uid, provider):
        raise IntegrityError()

    @classmethod
    def get_social_auth(cls, provider, uid):
        if not hasattr(cls, '_called_times'):
            cls._called_times = 0
        cls._called_times += 1
        if cls._called_times == 2:
            user = list(User.cache.values())[0]
            return IntegrityErrorUserSocialAuth(user, provider, uid)
        else:
            return super(IntegrityErrorUserSocialAuth, cls).get_social_auth(
                provider, uid
            )


class IntegrityErrorStorage(TestStorage):
    user = IntegrityErrorUserSocialAuth

    @classmethod
    def is_integrity_error(cls, exception):
        """Check if given exception flags an integrity error in the DB"""
        return isinstance(exception, IntegrityError)


class UnknownErrorUserSocialAuth(TestUserSocialAuth):
    @classmethod
    def create_social_auth(cls, user, uid, provider):
        raise UnknownError()


class UnknownErrorStorage(IntegrityErrorStorage):
    user = UnknownErrorUserSocialAuth


"""
Tests currently failing for unknown reason (Bad SSL Handshake)
Disabled for now 
TODO Fix
class UserPersistsInPartialPipeline(BaseActionTest):
    def test_user_persists_in_partial_pipeline(self):
        user = User(username='foobar1')
        user.email = 'foo@bar.com'

        self.strategy.set_settings({
            'SOCIAL_AUTH_PIPELINE': (
                'tola.util.redirect_after_login',
            )
        })

        #self.do_login(after_complete_checks=False)

        # Handle the partial pipeline
        self.strategy.session_set('redirect_after_login', '/testing')

        data = self.strategy.session_pop('partial_pipeline')

        idx, backend, xargs, xkwargs = self.strategy.partial_from_session(data)

        self.backend.continue_pipeline(pipeline_index=idx,
                                              *xargs, **xkwargs)

        print(self.strategy.session_get('redirect_after_login'))
        print(self.strategy.session_get('next'))
"""