# secure settings example. change name to settings.py once options have been set

class Settings:
    def __init__(self):
        self.first_name = "" # first name to set for the ms account
        self.last_name = "" # last name to set for the ms account
        self.pfp_url = None # optional, url for a pfp link like a png to set on secured microsoft accounts
        self.dob_day = "" # day of date of birth to set
        self.dob_month = "" # month of date of birth to set, january being 1 and december being 12
        self.dob_year = "" # year of date of birth to set based on american calendar or wtv, 4 digits, eg. 1989
        self.region = "" # region by country code, eg. US as united states
        self.primary_prefix = "" # prefix to set for the new primary alias
        self.primary_amount = 1 # primary alias count
        
        # securing options, 0 is false and 1 is true
        self.tfa = 1 # toggle two factor authentication
        self.change_ign = 1 # change the minecraft ign by adding an _ to the end, eg. asa -> asa_ doesn't work when unavailable
        self.change_name = 1 # change microsoft name
        self.change_pfp = 1 # change microsoft profile picture
        self.change_dob = 1 # change microsoft date of birth
        self.multiplayer = 1 # toggle multiplayer via xbox settings
        self.secureifnomc = 1 # secure the account regardless of if it has minecraft or not
        self.domain = "" # domain for security email auto generation. must create mail records bound to the host for it to work.
        self.devices = 1 # toggle devices
        self.family = 1 # toggle microsoft family
        self.sign_out = 1 # sign out from all locations on microsoft
        self.windows_keys = 1 # clear all windows keys bound to the microsoft account
        self.oauths = 1 # clear oauth keys from linked applications, recommended for revoking access from seller to prevent pullbacks.

settings = Settings()
