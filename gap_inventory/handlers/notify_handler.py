__author__ = 'rmadrigal'

import webapp2
from gap_inventory import models
from google.appengine.ext.webapp import template
from google.appengine.api import users
from external.appengine_push_service import push
from gap_inventory.libraries import const


class NotifyHandler(webapp2.RequestHandler):

    def post(self):
        device_id = self.request.get("device_id")

        if not device_id or not device_id.isdigit():
            self.response.set_status(400)
        else:
            device = models.Device.get_by_id([int(device_id)])[0]
            device.borrower = users.get_current_user().nickname()
            device.borrower_email = users.get_current_user().email()

            response = notify_to_error(device)

            print "Notifying to Android: %s" % device.get_os_details()
            if (const.ANDROID_OS_NAME == device.os):
                response = notify_to_android(device)
            elif (const.IOS_OS_NAME == device.os):
                response = notify_to_ios(device)

            self.response.out.write(response)
            #TODO: Also, notify by sending an email to device.borrower

            self.response.set_status(202)

def notify_to_android(device):

    request = {}
    request["platform"] = const.ANDROID_OS_NAME,
    request["message"] = "User %s needs the device asap" % users.get_current_user().nickname(),
    request["token"] = device.token_id

    push.sendMessage(request)

    return "Notifying to Android: %s" % device.get_os_details()

def notify_to_ios(device):
    request = {}
    request["platform"] = const.IOS_OS_NAME,
    request["ios_message"] = "User %s needs the device asap" % users.get_current_user().nickname(),
    request["token"] = device.token_id
    request["ios_badge"] = "1"

    push.sendMessage(request)

    return "Notifying to iOS: %s" % device.get_os_details()

def notify_to_error(device):
    return "Error device %s has no notification service" % device.get_os_details()