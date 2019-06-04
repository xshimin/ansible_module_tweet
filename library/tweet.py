#!/usr/bin/env python
import tweepy
import os
from ansible.module_utils.basic import *

class TwitterWrapper(object):
    def __init__(self, consumer_key, consumer_secret, access_token_key,
                access_token_secret, module):
        # Authentication for Twitter API
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token_key, access_token_secret)
        self.api = tweepy.API(auth, wait_on_rate_limit = True)
        self.module = module

    def update_status(self, tweet_msg):
        try:
            self.api.update_status(tweet_msg)
        except Exception as err:
            msg = "An Error has occured. ERROR={err}".format(err=err)
            raise Exception(msg)

        msg = "api.update_status has been executed successfully."
        return 0, msg

    def me(self):
        try:
            self.api.me()
        except Exception as err:
            msg = "An Error has occured. ERROR={err}".format(err=err)
            raise Exception(msg)

        msg = "api.me has been executed successfully."
        return 0, msg

def main():
    module = AnsibleModule(
                argument_spec=dict(
                    consumer_key        = dict(required=True, type='str'),
                    consumer_secret     = dict(required=True, type='str'),
                    access_token_key    = dict(required=True, type='str'),
                    access_token_secret = dict(required=True, type='str'),
                    tweet_msg           = dict(repuired=True, type='str')
                ),
                supports_check_mode = True,
             )

    consumer_key        = module.params['consumer_key']
    consumer_secret     = module.params['consumer_secret']
    access_token_key    = module.params['access_token_key']
    access_token_secret = module.params['access_token_secret']
    tweet_msg           = module.params['tweet_msg']

    try:
        tw = TwitterWrapper(consumer_key, consumer_secret, access_token_key,
                            access_token_secret, module)
        if module.check_mode:
            rc, msg = tw.me()
        else:
            rc, msg = tw.update_status(tweet_msg)
            
    except Exception as err:
        result = {
            'changed': False,
            'rc': 1,
            'msg': err,
            'tweet_msg': tweet_msg
        }
        module.fail_json(**result)

    result = {
        'changed': True,
        'rc': rc,
        'msg': msg,
        'tweet_msg': tweet_msg
    }
    module.exit_json(**result)

if __name__ == '__main__':
    main()