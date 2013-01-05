__author__ = 'bakeneko'

import datetime
from google.appengine.ext import db
from google.appengine.api import users

class Device(db.Model):
    """
    This represents the inventory of devices itself
    """
    gap_asset_id       = db.StringProperty()
    brand              = db.StringProperty()
    family             = db.StringProperty()
    model              = db.StringProperty()
    serial_num         = db.StringProperty()
    imei               = db.StringProperty()
    password           = db.StringProperty()
    os                 = db.StringProperty()
    os_version         = db.StringProperty()
    notes              = db.StringProperty()
    current_state      = db.StringProperty()
    borrower           = db.StringProperty()
    returned           = db.DateTimeProperty()
    client             = db.StringProperty()


    def get_device_name(self):
        return "%s %s (%s)"%(self.family, self.model, self.brand)

    def get_os_details(self):
        return "%s - %s"%(self.os, self.os_version)

    def get_last_used(self):
        """ Return last time somebody used the device """
        value = " - "
        if self.returned:
            date_diff = datetime.datetime.now() - self.returned
            if date_diff.seconds < 60:
                value = "%s seconds ago"%date_diff.seconds
            elif date_diff.seconds < 3600:
                value = "%s minutes ago"%(date_diff.seconds / 60)
            elif date_diff.seconds < 86400:
                value = "%s hours ago"%(date_diff.seconds / 3600)
            else:
                value = "%s days ago"%(date_diff.seconds /  86400)

        return value

    def do_i_have_the_device(self):
        return self.borrower == users.get_current_user().nickname()

class Check_Out(db.Model):
    """
    Represent the action of take a cellphone form the storage
    """
    borrower           = db.UserProperty(auto_current_user_add=True)
    borrower_email     = db.EmailProperty()
    check_out          = db.DateTimeProperty()
    check_in           = db.DateTimeProperty()

class Queue(db.Model):
    pass

class DeviceStates:
    """
      Enum of available states for the devices
    """
    CHECKED_IN = "check_in"
    CHECKED_OUT = "check_out"
    OUT_OF_ORDER = "out_of_order"