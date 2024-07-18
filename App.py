from AdversaryRevulsion import CovertLister
from Components.Account import Account

Accounts: list["Account"] = []
Overt_accounts: list["Account"] = []
Covert_accounts: list["Account"] = []
Pro_accounts: list["Account"] = []

myFinder = CovertLister(Accounts)

myFinder.uncover_overt()
