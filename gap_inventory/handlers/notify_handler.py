__author__ = 'rmadrigal'

import webapp2
from gap_inventory.utils import const
from gap_inventory import models
from google.appengine.ext.webapp import template
from google.appengine.api import users
from external.apnsclient import apns

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

            if (const.ANDROID_OS_NAME == device.os):
                response = notify_to_android(device)
            elif (const.IOS_OS_NAME == device.os):
                response = notify_to_ios(device)

            self.response.out.write(response)
            #TODO: Also, notify by sending an email to device.borrower

            self.response.set_status(202)

def notify_to_android(device):
    return "Notifying to Android: %s" % device.get_os_details()

def notify_to_ios(device):
    con = apns.Session.new_connection("feedback_sandbox", cert_file="sandbox.pem")
    #con = session.get_connection("push_sandbox", cert_file="sandbox.pem")

    # New message to 3 devices. You app will show badge 1 over app's icon.
    message = apns.Message([device.token_id], alert="User %s needs the device asap" % users.get_current_user().nickname(), badge=1)

    # Send the message.
    srv = apns.APNs(con)
    res = srv.send(message)

    # Check failures. Check codes in APNs reference docs.
    for token, reason in res.failed.items():
        code, errmsg = reason
        print "Device failed: {0}, reason: {1}".format(token, errmsg)

    # Check failures not related to devices.
    for code, errmsg in res.errors:
        print "Error: ", errmsg

    # Check if there are tokens that can be retried
    if res.needs_retry():
        # repeat with retry_message or reschedule your task
        retry_message = res.retry()

    #Close session
    con.shutdown()

    return "Notifying to iOS: %s" % device.get_os_details()

def notify_to_error(device):
    return "Error device %s has no notification service" % device.get_os_details()