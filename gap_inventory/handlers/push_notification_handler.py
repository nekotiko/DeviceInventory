__author__ = 'rmadrigal'

import webapp2
from gap_inventory import models
from google.appengine.ext.webapp import template
from google.appengine.api import users
from external.appengine_push_service import push
from gap_inventory.libraries import const
from google.appengine.api import mail
import logging

class PushNotificationHandler(webapp2.RequestHandler):

    def post(self):
        try:
            device_id = self.request.get("device_id")

            if not device_id or not device_id.isdigit():
                self.response.set_status(400)
            else:
                device = models.Device.get_by_id([int(device_id)])[0]

                if device.token_id:
                    response = notify_to_error(device)
                    message = const.MESSAGE_EMERGENCY_RETURN % users.get_current_user().nickname()
                    if (const.ANDROID_OS_NAME == device.os):
                        response = notify_to_device(device, const.ANDROID_OS_NAME, message)
                    elif (const.IOS_OS_NAME == device.os):
                        response = notify_to_device(device, const.IOS_OS_NAME, message)
                else:
                    response = const.MESSAGE_ERROR_NO_TOKEN

                if response == const.MESSAGE_ERROR_NO_TOKEN and \
                   notify_by_email(device, users.get_current_user().email(), device.borrower):
                    self.response.out.write(const.MESSAGE_ERROR_NO_TOKEN_BUT_EMAIL)
                else:
                    self.response.out.write(response)

                self.response.set_status(202)
        except:
            logging.error("There was an error when trying to notify by push notification")
            self.response.set_status(404)
            pass

class CheckInGlobalNotifierHandler(webapp2.RequestHandler):

    def get(self):

        print "Cron task: Notifying to checked in devices: \n"
        for device in models.Device.gql("WHERE current_state = :1 order by family", models.DeviceStates.CHECKED_OUT).run():
            print device.get_os_details()
            try:
                if (const.ANDROID_OS_NAME == device.os):
                    print notify_to_device(device, const.ANDROID_OS_NAME, const.MESSAGE_REMINDER_CHECK_IN)
                elif (const.IOS_OS_NAME == device.os):
                    print notify_to_device(device, const.IOS_OS_NAME, const.MESSAGE_REMINDER_CHECK_IN)
            except:
                pass

class CheckOutGlobalNotifierHandler(webapp2.RequestHandler):

    def get(self):

        print "Cron task: Notifying to checked out devices: \n"
        for device in models.Device.gql("WHERE current_state = :1 order by family", models.DeviceStates.CHECKED_IN).run():
            try:
                if (const.ANDROID_OS_NAME == device.os):
                    print notify_to_device(device, const.ANDROID_OS_NAME, const.MESSAGE_REMINDER_CHECK_OUT)
                elif (const.IOS_OS_NAME == device.os):
                    print notify_to_device(device, const.IOS_OS_NAME, const.MESSAGE_REMINDER_CHECK_OUT)
            except:
                pass


def notify_to_device(pDevice, pOS, pMessage):

    request = {}
    request[const.KEY_PLATFORM] = pOS
    request[const.KEY_MESSAGE] = pMessage
    request[const.KEY_TOKEN] = pDevice.token_id
    request[const.KEY_BADGE] = "1"

    push.send_message(request)

    return const.MESSAGE_NOTIFYING % (pDevice.get_device_name(), pDevice.get_os_details())

def notify_to_error(device):
    return const.MESSAGE_ERROR_NOTIFICATION_SERVICE % device.get_os_details()

def notify_by_email(device, pFromUser, pToUserEmail):
    try:
        message = mail.EmailMessage(sender=const.EMAIL_SENDER, subject=const.EMAIL_SUBJECT)
        userNickname = pToUserEmail
        if pToUserEmail.find("@") == -1 :
            pToUserEmail = userNickname + const.EMAIL_DOMAIN
        else:
            userNickname = pToUserEmail[0:pToUserEmail.find("@")]

        message.to = "%s <%s>" % (userNickname, pToUserEmail)
        message.body = """
        Dear %s:

        The following device that you are using is required by %s:

        Gap Asset ID: %s %s %s

        Please do check-in this device as soon as possible, or contact the requester.

        --MobileGap Team
        """ % (userNickname.capitalize(), pFromUser, device.gap_asset_id, device.get_device_name(), device.get_os_details())

        message.send()
        return True
    except:
        logging.error("There was an error when trying to send an email to %s" % pToUserEmail)
        pass
        return False