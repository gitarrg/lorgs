
import json
from mock import patch
from pprint import pprint

import dotenv
dotenv.load_dotenv() # pylint: disable=wrong-import-position


from lorrgs_sqs import helpers
from lorrgs_sqs.handler import handler



TEST_EXPANDERS_BOSS_NAME = {
    "boss_name":["bossA", "bossB", "bossC"]
}

TEST_EXPANDERS_BOSS_AND_SPEC = {
    "boss_name":["bossA", "bossB"],
    "spec_name":["specA", "specB", "specC"],
}


@patch("lorrgs_sqs.utils.PAYLOAD_EXPANDERS", TEST_EXPANDERS_BOSS_NAME)
def test_expand_boss():
    payload = {"boss_name": "all"}
    payloads = helpers.expand_keywords(payload)
    assert len(payloads) == 3


@patch("lorrgs_sqs.utils.PAYLOAD_EXPANDERS", TEST_EXPANDERS_BOSS_AND_SPEC)
def test_expand_two_expands():
    payload = {
        "boss_name": "all",
        "spec_name": "all",
    }

    payloads = helpers.expand_keywords(payload)
    assert len(payloads) == 6  # 2*3


@patch("lorrgs_sqs.utils.PAYLOAD_EXPANDERS", TEST_EXPANDERS_BOSS_AND_SPEC)
def test_expand_cap():
    payload = {
        "boss_name": "all",
        "spec_name": "all",
        "difficulty": "all",
    }

    payloads = helpers.expand_keywords(payload, cap=1)
    assert len(payloads) == 3
    print(payloads)


def test_resubmit():

    # handler({
    #     "Records": [{
    # 
    #         "messageAttributes": {
    #             "task": { "DataType": "String", "StringValue": "Test" },
    #         },
    # 
    #         "messageGroupId": "test",
    # 
    #         "body": json.dumps({
    #             "boss_name": "all",
    #             "spec_name": "test",
    #         })
    #         
    #     }]
    # })

    print("X", json.dumps({"boss_name": "all", "test": 2}))

    event = {
        "Records": [
            {
            "messageId": "1234-5678",
            "body": '{"boss_name": "all", "test": 2}',
            "messageGroupId": "test"
            }
        ]
    }
    handler(event)



if __name__ == "__main__":
    # test_expand_boss()
    # test_expand_two_expands()
    # test_expand_cap()
    test_resubmit()

    # payload = {"boss_name": "all", "test": 2}
    # print(json.dumps(payload))

#
###
##
