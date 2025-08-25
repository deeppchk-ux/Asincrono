from pyrogram import Client, filters
from paquetes.plantillas import atras, gateways_menu, charged_menu, auth_menu, ccn_menu, mass_menu

# 🔹 Mostrar el menú de Gateways (corregido para coincidir con el callback_data)
@Client.on_callback_query(filters.regex(r"^gates:\d+$"))
def gates_coman(client, callback_query):
    user_id = callback_query.from_user.id
    callback_query.message.edit_text(
        """<b>あ » Tools |  GateWays | 30+

↯ » Tools      » 8
↯ » Gateways   » 25+
━ ━━━━━━━ ━
↯ » Session de comandos y manejo del bot mediante botones. Se conoce el total de los comandos actualmente estables (❗️)</b>""",
        reply_markup=gateways_menu(user_id)
    )

# 🔹 Mostrar opciones de Charged (corregido callback_data)
@Client.on_callback_query(filters.regex(r"^charged:\d+$"))
def charged_coman(client, callback_query):
    user_id = callback_query.from_user.id
    callback_query.message.edit_text(
        """<b>⚡ 𝘾𝙃𝘼𝙍𝙂𝙀𝘿 - Disponibles:

↯ » Status    » Premium 
↯ » Type    » <i>Shopify - Stripe Charged $8.99</i>
↯ » Cmmd    » /stp
↯ » Format   » <code>/stp cc|mm|yy|cvc</code> 
━━
↯ » Status    » Premium 
↯ » Type    » <i>Autorize.Net Charged $9.50 MX</i>
↯ » Cmmd    » /auth
↯ » Format   » <code>/auth cc|mm|yy|cvc</code> 
━━
↯ » Status    » Premium 
↯ » Type    » <i>Autorize.Net Charged $5.00 MX</i>
↯ » Cmmd    » /at
↯ » Format   » <code>/at cc|mm|yy|cvc</code> 
━━
↯ » Status    » Premium 
↯ » Type    » <i>Braintree Charged $7.00 MX</i>
↯ » Cmmd    » /b3
↯ » Format   » <code>/b3 cc|mm|yy|cvc</code> 
━━
↯ » Status    » Premium 
↯ » Type    » <i>Autorize.Net Charged $9.00 MX</i>
↯ » Cmmd    » /ch
↯ » Format   » <code>/ch cc|mm|yy|cvc</code> 
━━
↯ » Status    » Premium
↯ » Type    » <i>Paypal Charged 0.2$ </i>
↯ » Cmmd    » /pl
↯ » Format   » <code>/pl cc|mm|yy|cvc</code>
━━                                                                               
━━━━━━━━━━━</b>""",
        reply_markup=charged_menu(user_id)
    )

# 🔹 Mostrar opciones de Auth (corregido callback_data)
@Client.on_callback_query(filters.regex(r"^auth:\d+$"))
def auth_coman(client, callback_query):
    user_id = callback_query.from_user.id
    callback_query.message.edit_text(
        """<b>🔐 𝘼𝙐𝙏𝙃 - Disponibles:

↯ » Status    » Premium 
↯ » Type    » <i>Stripe Auth</i>
↯ » Cmmd    » /au
↯ » Format   » <code>/au cc|mm|yy|cvc</code>
━━
↯ » Status    » Premium
↯ » Type    » <i>Paypal</i>
↯ » Cmmd    » /pp
↯ » Format   » <code>/pp cc|mm|yy|cvc</code>
━━
↯ » Status    » Premium
↯ » Type    » <i>Braintree Auth Avs</i>
↯ » Cmmd    » /chk
↯ » Format   » <code>/chk cc|mm|yy|cvc</code>
━━
↯ » Status    » Premium 
↯ » Type    » <i>Payflow auth</i>
↯ » Cmmd    » /pfu
↯ » Format   » <code>/pfu cc|mm|yy|cvc</code> 
━━
↯ » Status    » Premium 
↯ » Type    » <i>Moneris Auth</i>
↯ » Cmmd    » /ms
↯ » Format   » <code>/ms cc|mm|yy|cvc</code> 
━━  
━━━━━━━━━━━</b>""",
        reply_markup=auth_menu(user_id)
    )

# 🔹 Mostrar opciones de CCN (corregido callback_data)
@Client.on_callback_query(filters.regex(r"^ccn:\d+$"))
def ccn_coman(client, callback_query):
    user_id = callback_query.from_user.id
    callback_query.message.edit_text(
        """<b>💳 𝘾𝘾𝙉 - Disponibles:

↯ » Status    » Creditos 
↯ » Type    » <i>Amazon MX</i>
↯ » Cmmd    » /amx
↯ » Format   » <code>/amx cc|mm|yy|cvc</code>
━━
 ↯ » Status    » Premium 
↯ » Type    » <i>Payeezy Charged $50.00 MX</i>
↯ » Cmmd    » /pz
↯ » Format   » <code>/pz cc|mm|yy|cvc</code> 
━━
↯ » Status    » Premium 
↯ » Type    » <i>Adyen</i>
↯ » Cmmd    » /ady
↯ » Format   » <code>/ady cc|mm|yy|cvc</code> 
━━ 
↯ » Status    » Premium 
↯ » Type    » <i>Stripe CCN</i>
↯ » Cmmd    » /str
↯ » Format   » <code>/str cc|mm|yy|cvc</code>
━━
↯ » Status    » Premium 
↯ » Type    » <i>Payflow CCN</i>
↯ » Cmmd    » /po
↯ » Format   » <code>/po cc|mm|yy|cvc</code> 
━━                                            
━━━━━━━━━━━</b>""",
        reply_markup=ccn_menu(user_id)
    )

# 🔹 Mostrar opciones de Mass
@Client.on_callback_query(filters.regex(r"^mass:\d+$"))
def mass_coman(client, callback_query):
    user_id = callback_query.from_user.id
    callback_query.message.edit_text(
        """<b>♻️ 𝙈𝘼𝙎𝙎 - Disponibles:

↯ » Status    » Premium + Créditos 
↯ » Type      » <i>Mass braintree</i>
↯ » Cmmd      » /mass
↯ » Format    » <code>/mass cc|mm|yy|cvc</code>
━━
 ↯ » Status    » Premium  + Créditos 
↯ » Type    » <i>Mass stripe</i>
↯ » Cmmd    » /mast
↯ » Format   » <code>/mast cc|mm|yy|cvc</code> 
━━
 ↯ » Status    » Premium  + Créditos
↯ » Type    » <i>Mass Paypal $0.1</i>
↯ » Cmmd    » /maspp
↯ » Format   » <code>/maspp cc|mm|yy|cvc</code> 
━━
━━━━━━━━━━━</b>""",
        reply_markup=mass_menu(user_id)
    )

# 🔹 Volver al menú de Gateways (corregido callback_data)
@Client.on_callback_query(filters.regex(r"^atras_menu:\d+$"))
def atras_menu(client, callback_query):
    user_id = callback_query.from_user.id
    callback_query.message.edit_text(
        "<b>⚡ 𝙂𝙖𝙩𝙚𝙒𝙖𝙮𝙨 - Seleccione una opción:</b>",
        reply_markup=gateways_menu(user_id)
    )