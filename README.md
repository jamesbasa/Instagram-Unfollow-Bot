# Instagram-Unfollow-Bot
## To run
First, download ChromeDriver [here](https://chromedriver.chromium.org/downloads).
- I chose to download "ChromeDriver 89.0.4389.23" > "chromedriver_mac64.zip"
Second, download the dependencies from a shell:
```sh
pip3 install -r requirements.txt
```
Third, create a file `instagram_login.py` inside this folder and insert
the following (with your username and password inserted):
```
username = 'yourUsername'
password = 'yourPassword'
```
Lastly, run the app from a shell:
```sh
python3 app.py
```

## Selenium & ChromeDriver
[Documentation](https://chromedriver.chromium.org/getting-started)

The Selenium package is used for automating web browser interaction.
The ChromeDriver tool is used for navigating to web pages, user input,
JavaScript execution, and more.
Selenium uses ChromeDriver to control Google Chrome.
