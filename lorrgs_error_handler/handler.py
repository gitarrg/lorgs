"""Small Function to send lambda error messges to Discord.

Ref: https://aws.amazon.com/blogs/mt/get-notified-specific-lambda-function-error-patterns-using-cloudwatch/

"""

import base64
import gzip
import json


from lorrgs_error_handler import discord


def parse_event(event):
    """Parse the Log Payload from an Cloudwatch Event."""
    compressed_payload = base64.b64decode(event['awslogs']['data'])
    uncompressed_payload = gzip.decompress(compressed_payload)
    log_payload = json.loads(uncompressed_payload)
    return log_payload


def handler(event, *_, **__):
    """Handle Lambda Events."""
    payload = parse_event(event)
    discord.send_message(payload)


# Uncomment in Case of Development
# def test():
#     event = {'awslogs': {'data': 'H4sIAAAAAAAAAO1Xa2vjRhT9K4MoxFlsvZ+GfnBZd7+0LCSGQuMgRtJ1LCLNqDMjJ2bZ/94ryQ8pa2+IN6VQCv4gz4zuuefcM3dGX7QSpKQPsNhWoE21j7PFLP59fns7+zTXxhp/YiBwOHD9yLLtwI1sG4cL/vBJ8LrCGYM+SaOgZZJRo+BCPMgJrfJuza0SQEtcZJu2bVimYUfG3U+/zRbz28W9GyShCxF1ArDcBMLISXzPp67tRJG38jIMIetEpiKvVM7Zr3mhQEhteqfNheD4dN9izDfAVDP8RcszhHICKwgc0wss37FMJ/IsJwzCwMcn3wwD03Mty/UiFxn5kesFroOkLNtCOJWjFoqWSMvy/cAMQ9P1TM8f7zXC8Hfzm5vPN/dL1VCaWObEMRemOcWf6+mm6/65VIll+iuPhpPUyVYTFxxzEmVeOskCSi0zcN3EhqWaMQIND8LTtBYCMiJqxnL2QNQaCK2qIk9pQ1xfsoWgKSQ0fSSjkktFBKRImqS0KEhBpbqeLhkhqBCQpWbwShnVVq05Myjb5tyQbRmkUULJxVavtkttTIqcAYncMclZGy/fQBOE4B9VC0YkFCt9NxEz/kRzNbq+ECaM+jC7aDs0mksgf/C6yH4pePq4ZG0wvT+yZB9r0Sizpiwrmge+6lRK+AYIPKfQWmRMKOM4Lo5DB3WnTZiLdURXiAKUAqPMs6yAJyrASKiEPkvXaVk20WIGzzuCO+uQnwltWDeYm7iTai/vxbqik0/Ur1V0zrLPq27/7SUdDP37mpaUPdSlUQmueMoLaayVqvrsvLAjV7OOWKcf7oxR602Z8grGA5/u/klg2TlJV5gS9iejt8FkH9QOzBY1jts6xn1oWVcgRtf6fm60S6GHfh74aKFz0JbtnodueB29hwZCxS/E71m47UDDJMJTSXSeQgf8YHDf/j7DtrgvSMVvZvVyYwanUAXICgtw3JhtAlkuK6rSdbyqWToS8FeNJ8L4uKcHeWyoMBSVj7tzL258dUxDGilN1xAfRwY+68xNsyzOYEXrQsXd8pQzJXhxJslDIvvcfkgY1z/VsbpiYyniNxb8ZXhnF54L/v1Kt0z0gY33LfK/WXzrUHxsfymeEHFz94jXQDMQ/5f+wtIfTqhB0wm8d2toJ+P7r3TtUz2toQbitTOqB03llqXwnKu28Z/w0kl67xHfCi+j93rl8ANC4cVjoGV4/vRtloPeXlfg/RDtnT26uP8wuw4KY57Z4v2+85o5TnFxrBcA9Cn+BgTvUzEyqHjOVNvpGkeP3o5m+eb+fvZtvMGnRIebQYXLKFN6U9vRhw8bWiDRV5tqW3eJt6Ycz8ayigVlj5jKYA9GXSrNq3HBaTZcObw+5nGzTOopNhmF523B6+yQdzuHYsyUEnmCwO235pSUPKsxxatjXnqXl34IeIUekoRxQvfvkqvzGFfa1/uvfwP2UBGOfQ8AAA=='}}
#     handler(event=event)
# 
# if __name__ == "__main__":
#     test()
