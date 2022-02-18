# Lorrgs

simple webapp to analyze and compare cooldown usage in top logs by spec/comp.

## Link

👉 [lorrgs.nw.r.appspot.com](https://lorrgs.nw.r.appspot.com/).


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)



# CI Setup

Store GH Secret
```
    base64 -i google_creds.json -o google_creds_base64.json
    gh secret set GOOGLE_APPLICATION_CREDENTIALS_BASE64 < google_creds_base64.json
    rm google_creds_base64.json
```
