from gap_inventory.libraries import const

#OS Names
const.IOS_OS_NAME = "iOS"
const.ANDROID_OS_NAME = "Android"

#Custom messages
const.MESSAGE_EMERGENCY_RETURN = "Current device is required by %s"
const.MESSAGE_REMINDER_CHECK_IN = "Please check in the device, after you use it"
const.MESSAGE_REMINDER_CHECK_OUT = "Please check out the device, before you use it"
const.MESSAGE_ERROR_NOTIFICATION_SERVICE = "Error device %s has no notification service"
const.MESSAGE_ERROR_NO_TOKEN = "Current device has no token registered"
const.MESSAGE_ERROR_NO_TOKEN_BUT_EMAIL = const.MESSAGE_ERROR_NO_TOKEN \
                                         + "but, an email was sent to the borrower's account"
const.MESSAGE_ERROR_CHECK_NO_ASSET_ID = "There was en error when trying to check a device status - No Asset Id provided"
const.MESSAGE_ERROR_CHECK_DEVICE = "There was en error when trying to check a device status --AssetId: #%s"

const.MESSAGE_ERROR_UPDATE_DEVICE = "There was en error when trying to update a device status --AssetId: #%s"
const.MESSAGE_ERROR_UPDATE_DEVICE_NO_ASSET = "There was en error when trying to update a device status"
const.RESPONSE_FORMAT_CHECK_STATUS = '{"%s": "%s"}'
const.MESSAGE_NOTIFYING = "Notified to %s %s"

#Custom Messages Keys
const.KEY_PLATFORM = "platform"
const.KEY_MESSAGE = "message"
const.KEY_TOKEN = "token"
const.KEY_BADGE = "badge"
const.KEY_CHECK_STATE = "checkState"
const.KEY_EMAIL = "email"
const.KEY_ASSET_ID = "assetID"
const.KEY_TOKEN_ID = "tokenId"
const.KEY_OS_VERSION = "osVersion"
const.KEY_OS_NAME = "osName"
const.KEY_STATUS = "status"
const.KEY_LOGGED_USER = "loggedUser"

#Custom value keys
const.VALUE_NO_USER = "NO_USER"

#Custom Email
const.EMAIL_SENDER = "MobileGap Support <rmadrigal@growthaccelerationpartners.com>"
const.EMAIL_SUBJECT = "Device is required as soon as possible"
const.EMAIL_DOMAIN = "@growthaccelerationpartners.com"


#GCM Config attributes
const.GCM_API_KEY = "AIzaSyCowbX6-W9JzxrH9uJDBv_lqfAmxte-yxA"
const.GCM_MULTICAST_LIMIT = 1000

#iOS APNs Config Attributes
const.APNS_MULTICAST_LIMIT = 1000
const.APNS_TEST_MODE = True
const.APNS_SANDBOX_CERT = "-----BEGIN CERTIFICATE-----".join([
"MIIFjTCCBHWgAwIBAgIIWtMneiNSyeYwDQYJKoZIhvcNAQEFBQAwgZYxCzAJBgNV" ,
"BAYTAlVTMRMwEQYDVQQKDApBcHBsZSBJbmMuMSwwKgYDVQQLDCNBcHBsZSBXb3Js" ,
"ZHdpZGUgRGV2ZWxvcGVyIFJlbGF0aW9uczFEMEIGA1UEAww7QXBwbGUgV29ybGR3" ,
"aWRlIERldmVsb3BlciBSZWxhdGlvbnMgQ2VydGlmaWNhdGlvbiBBdXRob3JpdHkw" ,
"HhcNMTMxMDE1MjExNDUwWhcNMTQxMDE1MjExNDUwWjCBjDEkMCIGCgmSJomT8ixk" ,
"AQEMFGNvbS5nYXAuZGV2aWNlbG9nZ2VyMUIwQAYDVQQDDDlBcHBsZSBEZXZlbG9w" ,
"bWVudCBJT1MgUHVzaCBTZXJ2aWNlczogY29tLmdhcC5kZXZpY2Vsb2dnZXIxEzAR" ,
"BgNVBAsMCjVIN1dIWEpNVjUxCzAJBgNVBAYTAlVTMIIBIjANBgkqhkiG9w0BAQEF" ,
"AAOCAQ8AMIIBCgKCAQEAnkD/mRAUt8UZ7N17StPkgcC5d7l3MSAGapzLxNylTcHU" ,
"zLVqDxiTwHtAoy47Dnk26AZBCs+km9DmS9iFf+Oxv1hfnZZr2puUPGbamOobSAoH" ,
"HtFR0Ig+MLJR1RuYYl8CpBFFtqkBzhcoa03oYutjLiQMkGurNRJkVaSgPwyIawfm" ,
"YATzaCqBc6Oe5OaPqjkH3PERqxYeFFxbT6Tina4jW8UoKIL3x9rBmVet0gzQY8im" ,
"bPGcdaIklgWZwryzzngNaDftEkVw4XQTUeIjIVyKxd639Jcr1lrNHZ2BwwKpz9OF" ,
"C/HKpAYXIaHXwwdQyg5AEzt7/ej0vSCq4VmQ9WuCMwIDAQABo4IB5TCCAeEwHQYD" ,
"VR0OBBYEFG03Ylfr1H5xT6S+WLSuwJovvhpbMAkGA1UdEwQCMAAwHwYDVR0jBBgw" ,
"FoAUiCcXCam2GGCL7Ou69kdZxVJUo7cwggEPBgNVHSAEggEGMIIBAjCB/wYJKoZI" ,
"hvdjZAUBMIHxMIHDBggrBgEFBQcCAjCBtgyBs1JlbGlhbmNlIG9uIHRoaXMgY2Vy" ,
"dGlmaWNhdGUgYnkgYW55IHBhcnR5IGFzc3VtZXMgYWNjZXB0YW5jZSBvZiB0aGUg" ,
"dGhlbiBhcHBsaWNhYmxlIHN0YW5kYXJkIHRlcm1zIGFuZCBjb25kaXRpb25zIG9m" ,
"IHVzZSwgY2VydGlmaWNhdGUgcG9saWN5IGFuZCBjZXJ0aWZpY2F0aW9uIHByYWN0" ,
"aWNlIHN0YXRlbWVudHMuMCkGCCsGAQUFBwIBFh1odHRwOi8vd3d3LmFwcGxlLmNv" ,
"bS9hcHBsZWNhLzBNBgNVHR8ERjBEMEKgQKA+hjxodHRwOi8vZGV2ZWxvcGVyLmFw" ,
"cGxlLmNvbS9jZXJ0aWZpY2F0aW9uYXV0aG9yaXR5L3d3ZHJjYS5jcmwwCwYDVR0P" ,
"BAQDAgeAMBMGA1UdJQQMMAoGCCsGAQUFBwMCMBAGCiqGSIb3Y2QGAwEEAgUAMA0G" ,
"CSqGSIb3DQEBBQUAA4IBAQBhnORGg6EnOHOLUd1Ys56PcmCsqFP0UC1ImpE84C02" ,
"orQLbpRmVKosDmf3e1cnrnXSMELHIUAr1SG2lEWbBNKP3uCcsRdys2ks6H0C3rQV" ,
"zPn9u1A1lWcWSM8EEnBL/e4/XfYEwFKvP+0qqN2F50sLtzD1Am+Xl1e9xp3VGOQ6" ,
"5RODQEOcpLYI8pagWdLJNGG5UthtHMdo95pHgOWrmW5favSoHHUi/w9Xq+8jq7U8" ,
"aRUFl/sjslbCtBBgC0yJ0XAil5OFictNrTzbjhqt3uhS/ai60WUV44rn6kfMOJ7m" ,
"p74RiTtHevr92JUGquJE45s+/lP7aaC8CCx5Lp59coSC" ,
"-----END CERTIFICATE-----"])

const.APNS_SANDBOX_KEY = "-----BEGIN RSA PRIVATE KEY-----".join([
"Proc-Type: 4,ENCRYPTED",
"DEK-Info: DES-EDE3-CBC,9E4FECF939EC64B4",

"iwspQCZze/jeJyStlJ2c6+rYWzfA6bqBl8nmFmVzhM4bSGJxLP7A8HhL0ZbdfnHE",
"jk/dxDkxQBD1x3sT2I8tNfETKbgCELwD84ykWbg7/GodkgyikVkrRlWT+BJoKovd",
"dE9uHKH8oMPWufDP8seH1/lGPG6ll4YV0zIIePMgBuFcu07a60LGlINMPxPp3wM5",
"fLFG/ONPA6D0yeaGee1sv69AT372Y/QleFiS663gQ0FTJlTM6De3MXeFTgB8MnWG",
"GVjGFP7moukIZ9tzobD5EcfcLb2JLymxQW99I6IAuxHwclMRsEVW2oeCcfOm8as5",
"SpsUozQhipLRaYS/iannOxaRxvpulkoSLbau167/vUWhYzKfYA8FvMB1JNgHo1SP",
"jscnlVN/eN4n2Zex0ccS2p9Bxkm/6ZMRbONA1admGbvQyDtK3BV+t3coQdrrw3HG",
"BympRI1CNIXzA1tyxUg4MsxmsUmmhvH9f5qG+GW+k+yJ6AlnEg6KU5Dew4SuPHSO",
"Dj0DT0VQfHXTFnOLjitvAFIn6WjFkJVKw0jUN+uQsMpN0HgKMmlhwCH+OcnV8UAY",
"eG+UKIjVtTfgr6xB/wM2/ErmqjaTY94BHMNUdKrhFVUgbLlquqvYSBgtqhK1rfkl",
"qNn/Ws47oykEnZA5UHOBW8SV8Czy/6VLZ8yflK7jeu5yXnY/rJhaVi6wRtbksB7v",
"umOdVnwuHVjVXrvi3QbUccZd9V/MOEs1kq0w8cZqOqlXdsjSauwJzGzfeuyAadIn",
"PXHEMOxHjIb2Yv5omtUsfFvHGD55GLNOMbZu+2+wn/pGFzQgSqmzIcflvc9+RuBU",
"eyq1vWiBCKyYmxCUVMHGU2P1bkc7P1R+VtmKSjwo2a7t2pxECtp2WT4qncNpR7IK",
"LRQsGL3AjRwrx4AxF636GCGaUebOwOCha9NIl1lPHjDMuyKQFHsSk/AS2xlX9mQQ",
"kzPa+UNyR218rjVTyzF80it8NSbI0StygMXrnTU919WHvz+FAj+0UJ7O8O+u5dn2",
"oSdM3k/zTPY3Y8Q7HDKF4J7tUKFoIp1rOZ6qCyZnnDFX9mga0FD9oIL812G6oVZZ",
"p2qPxOyRei/SDzZ42mlXspdwRDHI3A3uaakckwssRKXvgxZptpg9Xwq9XBl7vtKG",
"nqVbQfcTK+xhWtOD9qARySRrFNyFJkVH03FE6IXawnhtFs2zW/rc/CvbfCq1xYd5",
"TCFsTXtYLV2PqrGAK2+mB3DNbZkfCeCTMQXuxonZc+wGp3LwlIaB0Q9B6BZOXAuv",
"BVM3PiX+xBlKN28LARtlx8cj/5eGR+zS7k5QNjx1CPA06/WnB+1jN2yVq2tomEIl",
"nYcma7d0DE+gzioAkcGXHM/l43jn3h+oMLe7SgDPUgOZUT8Hk7IFhRDq2d5XRZRH",
"IRyx44ls1Kj/vyedj4KCx7DOaxcUs6dFJ276O8KZzs1360BFGFjhzhK5nwrvrXiD",
"mD8O4lpJZYIu0D9+kE8iyuL6xk6x1QwqgcdxkS/Jtkz/BF6jyFkLKQ/fGl/m/2Bk",
"iGX2iO0z7OuP9Ipc513kVvDSBXY1Xeqh/AUAAoaAskYYf6HhHkg32w==",
"-----END RSA PRIVATE KEY-----"])
const.APNS_CERT = "<pem certificate string>"
const.APNS_KEY = "<pem private key string>"

