# Based on source code: appengine-apns-gcm was developed by Garett Rogers <garett.rogers@gmail.com>
# Source available at https://github.com/GarettRogers/appengine-apns-gcm

import webapp2
import os
from google.appengine.ext.webapp import template
from google.appengine.ext import ndb
from gcmdata import *
from gcm import *
from apns import *
from apnsdata import *
from gap_inventory.libraries import const

def convertToGcmMessage(self, message):
    gcmmessage = {}
    gcmmessage["data"] = {}

    if 'android_collapse_key' in message["request"]:
        gcmmessage["collapse_key"] = message["request"]["android_collapse_key"]

    if 'data' in message["request"]:
        gcmmessage["Message"] = message["request"]["data"]

    return gcmmessage

def convertToApnsMessage(message):
    apnsmessage = {}
    apnsmessage["data"] = {}
    apnsmessage["sound"] = "default"
    apnsmessage[const.KEY_BADGE] = -1
    apnsmessage["alert"] = None
    apnsmessage["custom"] = None
    
    if 'ios_sound' in message:
        apnsmessage["sound"] = message["ios_sound"]
    
    if 'data' in message:
        apnsmessage["custom"] = message["data"]

    if const.KEY_BADGE in message:
        apnsmessage[const.KEY_BADGE] = message[const.KEY_BADGE]

    if const.KEY_MESSAGE in message and 'ios_button_text' in message:
        apnsmessage["alert"] = PayloadAlert(message[const.KEY_MESSAGE], action_loc_key=message["ios_button_text"])
    elif const.KEY_MESSAGE in message:
        apnsmessage["alert"] = message[const.KEY_MESSAGE]
    print "APNS MESSAGE: %s" % apnsmessage
    return apnsmessage

def getAPNs():
    if const.APNS_TEST_MODE:
        return APNs(use_sandbox=True, cert_file=const.APNS_SANDBOX_CERT, key_file=const.APNS_SANDBOX_KEY)
    else:
        return APNs(use_sandbox=False, cert_file=const.APNS_CERT, key_file=const.APNS_KEY)

def GetApnsToken(regid):

    if const.APNS_TEST_MODE:
        return ApnsSandboxToken.get_or_insert(regid)
    else:
        return ApnsToken.get_or_insert(regid)

def sendMulticastApnsMessage(apns_reg_ids, apnsmessage):
    apns = getAPNs()
    
    # Send a notification
    payload = Payload(alert=apnsmessage["alert"], sound=apnsmessage["sound"], custom=apnsmessage["custom"], badge=apnsmessage["badge"])
    apns.gateway_server.send_notifications(apns_reg_ids, payload)

    # Get feedback messages
    for (token_hex, fail_time) in apns.feedback_server.items():
        break

def sendSingleApnsMessage(message, token):
    apns_reg_ids=[token]
    sendMulticastApnsMessage(apns_reg_ids, message)


def sendMulticastGcmMessage(gcm_reg_ids, gcmmessage):

    gcm = GCM(const.GCM_API_KEY)

    # JSON request
    response = gcm.json_request(registration_ids=gcm_reg_ids, data=gcmmessage)
    if 'errors' in response:
        for error, reg_ids in response['errors'].items():
            # Check for errors and act accordingly
            if error is 'NotRegistered':
                # Remove reg_ids from database
                for reg_id in reg_ids:
                    token = GcmToken.get_or_insert(reg_id)
                    token.key.delete()
    
    if 'canonical' in response:
        for reg_id, canonical_id in response['canonical'].items():
            # Replace reg_id with canonical_id in your database
            token = GcmToken.get_or_insert(reg_id)
            token.key.delete()
            
            token = GcmToken.get_or_insert(canonical_id)
            token.gcm_token = canonical_id
            token.enabled = True
            token.put()


def send_single_gcm_message(message, token):
    gcm_reg_ids=[token]
    print "Message %s" % message
    sendMulticastGcmMessage(gcm_reg_ids, message)

def send_message(request):
    platform = ("%s" % request["platform"])
    token = ("%s" % request["token"])

    #Send a single message to a device token
    if ("%s" % platform) == const.ANDROID_OS_NAME:
        send_single_gcm_message({"data" : ("%s" % request["message"])}, token)
    elif ("%s" % platform) == const.IOS_OS_NAME:
        sendSingleApnsMessage(convertToApnsMessage(request), token)