


WCL Auth Token
```bash
source venv/bin/activate
export PYTHONPATH=.
python scripts/get_wcl_auth_token.py
```


Insomnia:
=========
 
- Manage Envs (Ctrl+E)
- "TOKEN: <value>" (only TOKEN. Remove the "Bearer" Keyword)

- Request:
    - URL: https://www.warcraftlogs.com/api/v2/client
    - Auth: Bearer
    - Ctrl+Space --> `_.TOKEN`


Docs:
=====
https://www.warcraftlogs.com/v2-api-docs/warcraft/





