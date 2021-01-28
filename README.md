# pymsteams
This module provides wrapper for [pymsteams](https://pypi.org/project/pymsteams/).

## Installation
```bash
pip install takeme-pymsteams
```

## Usage
```python
import takeme_pymsteams

SP_SITE = 'https://xxxx.sharepoint.com'
SITE_NAME = 'XXXX'
SP_ID = 'user'
SP_PWD = 'abcd'
TEAMS_CHANNEL = 'https://outlook.office.com/webhook/xxxxx/IncomingWebhook/xxx/xxxx/xxxx'

teams = takeme_pymsteams.Teams()
try:
    teams.connect_to_share_point(
        share_point_site=SP_SITE,
        site_name=SITE_NAME,
        user_name=SP_ID,
        password=SP_PWD
    )
    teams.send(
        channel=TEAMS_CHANNEL,
        text='Hello Microsoft Teams!',
        file='Hello.xlsx'
    )
except Exception as ex:
    print(str(ex))
```
