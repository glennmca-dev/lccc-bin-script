# lccc-bin-script
A simple script to alert you when the bins need to be left out. Created for residents of Lisburn Castlereagh City Council
## Prerequisites
1) You must be able to find your address and see an output on [The LCCC bin collection information site](https://lisburn.isl-fusion.com/) - If your address is available you should have a link that looks something like: `https://lisburn.isl-fusion.com/view/asdkh2298hhj` (this one isn't real) - save your link for later
2) You must run this script using python 10 due to the new case matching syntax
3) You must have an account with [MyNotifier](https://www.mynotifier.app/) and have access to your API key, it will be needed later. Mynotifier allows sending 25 notifications per month free of charge.
---
## Installation
###### Clone this repo
```sh
git clone https://github.com/glennmca-dev/lccc-bin-script.git
```
###### install the requirements
```sh
pip install -r requirements.txt
```
###### replace placeholders
In the script there are two placeholders that will need to be replaced.
You may need to replace the shebang on line 1 if using a venv rather than a global installation of python... At least I had to put it there.
The required replacements are described below.

|Placeholder|Replacement|
|-----------|-----------|
|Shebang on line 1|Replace with a shebang for your own VENV if applicable, or delete.|
|`YOUR_URL`| The URL described in Prerequisite 1 |
|`YOUR_API_KEY`| The API key described in Prerequisite 3 |

##### Setup crontab
Run `crontab -e` (this will open your cronjob list in vim by default) and insert the following to have the script run at 7pm every day.
```crontab
0 19 * * *  /path/to/python /path/to/script
```
---

## Limitations
Currently the script only deals with formatting:
- Black/residual Bin
- Green/Recycling Bin
- Brown/Compost Bin

Any other bin 'names' will not be nicely formatted in the sent notification.