# Cisco SDWAN Custom App for China Office365 (hosted by 21Vianet)
This script reads Microsofts latest definition of Office365 hosted in 21vianet for China and creates (or updates) a custom app definition in vManage for it.  It's recommended to schedule this to run on a periodic basis to keep this app definition updated regularly.

Execution results in two custom applications; one for URLs and one for subnets.
|![vManage_Screen_Shot](https://user-images.githubusercontent.com/46031546/194152729-6f202ed6-dcac-4f11-bc32-c0364a361b43.png)|
|-|

The script reads from the JSON file linked in this Microsoft tech article:

https://learn.microsoft.com/en-us/microsoft-365/enterprise/urls-and-ip-address-ranges-21vianet?view=o365-worldwide

## Use Instructions

> git clone https://github.com/dbrown92700/21vianetO365feed

> pip install -r requirements

Add valid address and credentials to vmanage_credentials.py 

> python3 main.py
