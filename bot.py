# 𝙍𝘼𝙕𝙊𝙍 𝙓 𝘽𝙤𝙩
from telethon.errors import FloodWaitError
from telethon import TelegramClient, events, Button
from telethon.tl.types import MessageEntityCustomEmoji, ChannelParticipantBanned
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.extensions import html as thtml
import asyncio
import aiohttp
import aiofiles
import os
import random
import time
import json
import re
import string
import logging
import socket
import platform
from datetime import datetime, timedelta
from urllib.parse import urlparse, quote
from typing import Optional, List
from telethon.errors import (
    UserNotParticipantError,
    ChatAdminRequiredError,
    ChannelPrivateError,
)

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

from database import (
    init_db, db,
    ensure_user, get_user_plan, set_user_plan, is_premium_user,
    is_banned_user,
    add_proxy_db, get_all_user_proxies, get_proxy_count, get_random_proxy,
    remove_proxy_by_index, remove_proxy_by_url, clear_all_proxies,
    add_site_db, get_user_sites, remove_site_db,
    save_card_to_db, get_total_cards_count, get_charged_count, get_approved_count,
    get_all_premium_users, get_total_users, get_premium_count,
    get_total_sites_count, get_users_with_sites, get_sites_per_user, get_all_sites_detail,
    mark_user_joined, is_user_marked_joined, remove_joined_mark
)

# ====================== LOGGING ======================
log = logging.getLogger("RazorX")
log.setLevel(logging.INFO)
_log_fmt = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
_ch = logging.StreamHandler()
_ch.setLevel(logging.INFO)
_ch.setFormatter(_log_fmt)
log.addHandler(_ch)
try:
    _fh = logging.FileHandler('razor_x_bot.log', encoding='utf-8')
    _fh.setLevel(logging.INFO)
    _fh.setFormatter(_log_fmt)
    log.addHandler(_fh)
except:
    pass


def log_user(uid, action, msg, level="info"):
    getattr(log, level, log.info)(f"[USER:{uid}] [{action}] {msg}")


def log_system(action, msg, level="info"):
    getattr(log, level, log.info)(f"[SYSTEM] [{action}] {msg}")


# ====================== BOLD SANS CONVERTER ======================
_BOLD_SANS_MAP = {}
_normal_upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
_normal_lower = "abcdefghijklmnopqrstuvwxyz"
_normal_digits = "0123456789"
_bold_upper = "𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭"
_bold_lower = "𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇"
_bold_digits = "𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵"

for _i, _c in enumerate(_normal_upper):
    _BOLD_SANS_MAP[_c] = _bold_upper[_i]
for _i, _c in enumerate(_normal_lower):
    _BOLD_SANS_MAP[_c] = _bold_lower[_i]
for _i, _c in enumerate(_normal_digits):
    _BOLD_SANS_MAP[_c] = _bold_digits[_i]


def bs(text):
    if not text:
        return text
    return "".join(_BOLD_SANS_MAP.get(c, c) for c in str(text))


# ====================== CONFIG ======================
API_ID = int(os.getenv("API_ID", "26038836"))          # default as string, then int()
API_HASH = os.getenv("API_HASH", "25f462e2a8517df5014a653c39cc58ca")
BOT_TOKEN = os.getenv("BOT_TOKEN", "8894769120:AAGpUWVrxt4jhbeS1xVgXoi6HNbO66XraNA")
ADMIN_ID = json.loads(os.getenv("ADMIN_ID",7205267248 "[]"))
HIT_CHANNEL_ID = int(os.getenv("HIT_CHANNEL_ID",-1003718418094 ""))
JOIN_GROUP_ID = int(os.getenv("JOIN_GROUP_ID",-1003718418094 ""))
JOIN_CHANNEL_ID = int(os.getenv("JOIN_CHANNEL_ID",-1003718418094 ""))
JOIN_GROUP_LINK = os.getenv("JOIN_GROUP_LINK",https://t.me/cvvwasi "")
JOIN_CHANNEL_LINK = os.getenv("JOIN_CHANNEL_LINK",https://t.me/cvvwasi "")
FORCE_JOIN_IMAGES = [
    "",
    ""
]
API_BASE_URL = os.getenv("API_BASE_URL", "https://web-production-e6929.up.railway.app/shopify")
RAZORPAY_API_URL = os.getenv("RAZORPAY_API_URL", "https://rz.rcvan.indevs.in/rz")
BOT_API = f"https://api.telegram.org/bot{8894769120:AAGpUWVrxt4jhbeS1xVgXoi6HNbO66XraNA}"

# ── SEPARATE Worker Configuration (PER-USER) ──
SP_PER_USER_WORKERS = 30
MSP_PER_USER_WORKERS = 70
RZ_PER_USER_WORKERS = 30
MRZ_PER_USER_WORKERS = 50
SITE_PER_USER_WORKERS = 30
PROXY_PER_USER_WORKERS = 50
BIN_WORKERS = 20

# ── Timeout Configuration ──
API_TIMEOUT = 60
BIN_TIMEOUT = 60
PROXY_TIMEOUT = 12
RZ_TIMEOUT = 60

# ── General Settings ──
BATCH_SIZE = 60
SITE_CHECK_BATCH = 40
HIT_DELAY = 1.5
PER_USER_LIMIT = 200
LOG_CHANNEL_ID = HIT_CHANNEL_ID

FREE_SP_DAILY_LIMIT = 15
FREE_SP_COOLDOWN = 10

PLANS = {
    "plan1": {"name": bs("Core Access"), "tier": "Core", "duration_days": 7, "emoji": "🛠️", "price": "$8.00"},
    "plan2": {"name": bs("Elite Access"), "tier": "Elite", "duration_days": 15, "emoji": "👑", "price": "$14.00"},
    "plan3": {"name": bs("Root Access"), "tier": "Root", "duration_days": 30, "emoji": "⭐", "price": "$25.00"},
    "plan4": {"name": bs("X-Access"), "tier": "X", "duration_days": 90, "emoji": "💎", "price": "$60.00"},
}
PAID_TIERS = ["Core", "Elite", "Root", "X"]

# ── PER-USER Semaphore Factory (FULLY SEPARATED per function) ──
_USER_SEMS = {}
_BIN_SEM = asyncio.Semaphore(BIN_WORKERS)


def get_user_sem(uid, sem_type="msp"):
    key = f"{uid}_{sem_type}"
    if key not in _USER_SEMS:
        limits = {
            "sp": SP_PER_USER_WORKERS,
            "msp": MSP_PER_USER_WORKERS,
            "rz": RZ_PER_USER_WORKERS,
            "mrz": MRZ_PER_USER_WORKERS,
            "site": SITE_PER_USER_WORKERS,
            "proxy": PROXY_PER_USER_WORKERS,
        }
        _USER_SEMS[key] = asyncio.Semaphore(limits.get(sem_type, 30))
    return _USER_SEMS[key]


def cleanup_user_sem(uid):
    keys_to_remove = [k for k in _USER_SEMS if k.startswith(f"{uid}_")]
    for k in keys_to_remove:
        del _USER_SEMS[k]


CE = {
    "crown": 5039727497143387500, "bolt": 5042334757040423886,
    "brain": 5040030395416969985, "shield": 5042328396193864923,
    "star": 5042176294222037888, "gem": 5042050649248760772,
    "check": 5039793437776282663, "fire": 5039644681583985437,
    "party": 5039778134807806727, "search": 5039649904264217620,
    "chart": 5042290883949495533, "pin": 5039600026809009149,
    "joker": 5039998939076494446, "plus": 5039891861246838069,
    "cross": 5040042498634810056, "info": 5042306247047513767,
    "gift": 5041975203853239332, "eyes": 5039623284056917259,
    "trash": 5039614900280754969, "tick": 5039844895779455925,
    "stop": 5039671744172917707, "warn": 5039665997506675838,
    "link": 5042101437237036298, "globe": 5042186567783809934,
    "restart": 5413554170668032766, "online": 5413813953685923984,
    "declined": 4956612582816351459,
}
PE = "⭐"

ACTIVE_SESSIONS = {}
ACTIVE_MTXT_PROCESSES = {}
ACTIVE_MRZ_PROCESSES = {}
ACTIVE_ADD_PROCESSES = {}
PENDING_ADD_SITES = {}
PENDING_SITE_CHECK = {}
USER_APPROVED_PREF = {}
MAINTENANCE_FILE = "maintenance.json"
_MAINTENANCE_CACHE = {"enabled": None, "last_check": 0}
_JOIN_CACHE = {}
_FREE_SP_USAGE = {}
_FREE_SP_LAST_USE = {}

BOT_START_TIME = time.time()

HIT_BUTTON = [[Button.url(bs("Razor X"), "https://t.me/Razor_x_1998_bot")]]

# ── SEPARATE PER-USER HTTP Session Pools ──
_USER_HTTP_SESSIONS = {}
_GLOBAL_BIN_SESSION = None
_GLOBAL_PROXY_SESSION = None


async def get_user_http_session(uid, purpose="general"):
    key = f"{uid}_{purpose}"
    session = _USER_HTTP_SESSIONS.get(key)
    if session is None or session.closed:
        timeout_val = RZ_TIMEOUT if purpose in ("rz", "mrz") else API_TIMEOUT
        connector = aiohttp.TCPConnector(
            limit=150,
            limit_per_host=50,
            ttl_dns_cache=300,
            use_dns_cache=True,
            keepalive_timeout=30,
            enable_cleanup_closed=True,
        )
        session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=timeout_val, connect=10),
            connector=connector,
        )
        _USER_HTTP_SESSIONS[key] = session
    return session


async def cleanup_user_http_session(uid, purpose="general"):
    key = f"{uid}_{purpose}"
    session = _USER_HTTP_SESSIONS.pop(key, None)
    if session and not session.closed:
        try:
            await session.close()
        except:
            pass


async def get_bin_session():
    global _GLOBAL_BIN_SESSION
    if _GLOBAL_BIN_SESSION is None or _GLOBAL_BIN_SESSION.closed:
        _GLOBAL_BIN_SESSION = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=BIN_TIMEOUT, connect=5),
            connector=aiohttp.TCPConnector(limit=50, limit_per_host=20, ttl_dns_cache=300, use_dns_cache=True)
        )
    return _GLOBAL_BIN_SESSION


async def get_proxy_session():
    global _GLOBAL_PROXY_SESSION
    if _GLOBAL_PROXY_SESSION is None or _GLOBAL_PROXY_SESSION.closed:
        _GLOBAL_PROXY_SESSION = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=PROXY_TIMEOUT, connect=15),
            connector=aiohttp.TCPConnector(limit=30, limit_per_host=10, ttl_dns_cache=300, use_dns_cache=True)
        )
    return _GLOBAL_PROXY_SESSION


# ====================== FREE USER DAILY TRACKER ======================
def _get_today_key():
    return datetime.now().strftime("%Y-%m-%d")


def get_free_sp_usage(user_id):
    today = _get_today_key()
    entry = _FREE_SP_USAGE.get(user_id)
    if not entry or entry.get("date") != today:
        _FREE_SP_USAGE[user_id] = {"date": today, "count": 0}
        return 0
    return entry["count"]


def increment_free_sp_usage(user_id):
    today = _get_today_key()
    entry = _FREE_SP_USAGE.get(user_id)
    if not entry or entry.get("date") != today:
        _FREE_SP_USAGE[user_id] = {"date": today, "count": 1}
    else:
        _FREE_SP_USAGE[user_id]["count"] += 1


def get_free_sp_cooldown_remaining(user_id):
    last = _FREE_SP_LAST_USE.get(user_id, 0)
    elapsed = time.time() - last
    if elapsed >= FREE_SP_COOLDOWN:
        return 0
    return round(FREE_SP_COOLDOWN - elapsed, 1)


def set_free_sp_last_use(user_id):
    _FREE_SP_LAST_USE[user_id] = time.time()


# ====================== SMART ROTATION ENGINE ======================
class SmartRotator:
    def __init__(self):
        self._site_fails = {}
        self._proxy_fails = {}
        self._site_idx = 0
        self._proxy_idx = 0

    def pick_site(self, sites, exclude=None):
        if not sites:
            return None
        exclude = exclude or set()
        available = [s for s in sites if s not in exclude and self._site_fails.get(s, 0) < 5]
        if not available:
            available = [s for s in sites if s not in exclude]
        if not available:
            available = list(sites)
        self._site_idx = (self._site_idx + 1) % len(available)
        return available[self._site_idx]

    def pick_proxy(self, proxies, exclude=None):
        if not proxies:
            return None
        exclude = exclude or set()
        available = [p for p in proxies if p.get('proxy_url') not in exclude and self._proxy_fails.get(p.get('proxy_url'), 0) < 5]
        if not available:
            available = [p for p in proxies if p.get('proxy_url') not in exclude]
        if not available:
            available = list(proxies)
        self._proxy_idx = (self._proxy_idx + 1) % len(available)
        return available[self._proxy_idx]

    def report_site_ok(self, site):
        self._site_fails[site] = 0

    def report_site_fail(self, site):
        self._site_fails[site] = self._site_fails.get(site, 0) + 1

    def report_proxy_ok(self, proxy_url):
        if proxy_url:
            self._proxy_fails[proxy_url] = 0

    def report_proxy_fail(self, proxy_url):
        if proxy_url:
            self._proxy_fails[proxy_url] = self._proxy_fails.get(proxy_url, 0) + 1

    def get_site_fails(self, site):
        return self._site_fails.get(site, 0)

    def get_dead_sites(self, threshold=5):
        return {s for s, c in self._site_fails.items() if c >= threshold}


# ====================== SITE ERROR DETECTION ======================
SITE_ERROR_KEYWORDS = [
    'r4 token empty', 'payment method is not shopify', 'r2 id empty', 'product id is empty',
    'py id empty', 'clinte token', 'receipt_empty', 'receipt id is empty', 'receipt empty',
    'site requires login', 'failed to get token', 'no valid products', 'not shopify',
    'failed to get checkout', 'failed to detect product', 'failed to create checkout',
    'failed to get proposal data', 'site not supported', 'site error! status: 429',
    'token not found', 'handle is empty', 'payment method identifier is empty',
    'failed to get session token', 'failed to tokenize card', 'no_session_token',
    'no session token', 'no checkout token found',
    'checkout token not found', 'no checkout token', 'checkout token is empty',
    'tokenize_fail', 'tokenize fail', 'tax ammount empty', 'tax amount empty',
    'tax amount is empty', 'del ammount empty', 'site not supported for now',
    'payment base card not supported', 'no product found', 'checkout is not available',
    'cart is empty', 'cart add failed after retries', 'checkout_expired',
    'checkout_not_found', 'no shipping methods available', 'site error', 'site dead',
    'site errors', 'server error', 'internal server error',
    'internal_server_error', 'application error', 'unexpected error',
    'something went wrong', 'error in 1st req', 'error in 1 req',
    'error processing card', 'we could not process', 'unable to process',
    'payment provider error', 'payment gateway error', 'session expired',
    'session invalid', 'failed after retries', 'max retries exceeded',
    'all sites dead', 'all sites unavailable', 'processinf error', 'handle error',
    'nonetype', "nonetype' object has no attribute 'get", 'unknown error',
    'unknown_error', 'unknown_result', 'utm_source', 'shop is unavailable',
    'store is unavailable', 'store not found', 'page not found',
    'this store is unavailable', 'this shop is currently unavailable',
    'password protected', 'enter store using password', 'storefront is password protected',
    'shop closed', 'store closed', 'delivery_delivery_line_detail_changed',
    'delivery_address2_required', 'delivery_line_detail_changed', 'delivery_line',
    'delivery_address', 'address_required', 'submit_rejected',
    'submit rejected:', 'change proxy or site', 'change site',
    'fake charge gate', 'fake gate',
    'hcaptcha detected', 'hcaptcha_detected', 'captcha at checkout',
    'captcha_required', 'captcha required', 'cloudflare',
    'access denied', 'permission denied',
    'connection error', 'connection failed', 'timed out', 'timeout',
    'could not resolve host', 'connect tunnel failed', 'unreachable',
    'network error', 'connection reset', 'empty reply from server',
    'tlsv1 alert', 'ssl routines', 'openssl ssl_connect', 'api_timeout',
    'http error', 'httperror504', '502', '503', '504',
    'bad gateway', 'service unavailable', 'gateway timeout',
    'site error! status: 404', 'site error! status: 401',
    'amount_too_small', 'amount too small', 'merchandise_not_enough_stock',
    'product out of stock', 'malformed input', 'url rejected',
    'invalid_response',
    'cart failed with status', 'invalid json response', 'invalid json',
    'inventoryreservationfailure', 'inventory_reservation_failure',
    'payments_positive_amount_expec', 'payments_payment_flexibility_t',
    'payments_credit_card_brand_not', 'buyer_identity_presentment_currency',
    "'products'", "error:", "error: '",
    'unable to get payment token',
    'empty submit response',
    'empty submit',
    'order_total_changed',
    'order total changed',
    'invalid_payment_method',
    'invalid payment method',
    'validation_custom',
    'validation custom',
    'ARTIFACT_DISSATISFACTION',
    'artifact_dissatisfaction',
    'TAX_NEW_TAX_MUST_BE_ACCEPTED',
    'tax_new_tax_must_be_accepted',
    'PROCESSING_ERROR',
    'processing_error',
    'DELIVERY_COMPANY_REQUIRED',
    'delivery_company_required',
    'DECISION_RULE_BLOCK',
    'decision_rule_block',
    'timeout'
]

PROXY_ERROR_KEYWORDS = [
    'proxy dead', 'proxy error', 'proxy timeout',
    'proxy connection failed', 'proxy refused',
]

# Razorpay-specific retry keywords
RZ_RETRY_KEYWORDS = [
    'payment id not found', 'payment_id_not_found',
    'timeout', 'timed out', 'connection error',
    'connection failed', 'connection reset',
    'server error', 'internal server error',
    '502', '503', '504', 'bad gateway',
    'service unavailable', 'gateway timeout',
    'empty reply', 'invalid json',
    'could not resolve host', 'network error',
    'ssl routines', 'unreachable',
    'proxy dead', 'proxy error', 'proxy timeout',
    'DEAD | Payment ID not found', 'timeout',
]


def is_site_error(text):
    if not text:
        return True
    lower = text.lower().strip()
    if lower == 'na':
        return True
    return any(kw in lower for kw in SITE_ERROR_KEYWORDS)


def is_proxy_error(text):
    if not text:
        return False
    return any(kw in text.lower().strip() for kw in PROXY_ERROR_KEYWORDS)


def is_rz_retry_error(text):
    if not text:
        return True
    lower = text.lower().strip()
    return any(kw in lower for kw in RZ_RETRY_KEYWORDS)


def is_truly_alive(response, price):
    if not response:
        return False
    lower = response.lower().strip()
    pc = str(price).replace('$', '').strip() if price else '0'
    try:
        pv = float(pc)
    except:
        pv = 0.0
    bad = ['error:', 'error: ', "error: '", 'cart failed', 'invalid json',
           'inventoryreservationfailure', 'payments_positive_amount',
           'payments_payment_flexibility', 'payments_credit_card_brand']
    for b in bad:
        if b in lower:
            return False
    if pv == 0.0:
        normal = ['card_declined', 'card declined', 'generic_decline', 'generic decline',
                   'do_not_honor', 'do not honor', 'insufficient_funds', 'insufficient funds',
                   'stolen_card', 'lost_card', 'expired_card', 'expired card',
                   'otp_required', 'otp required', '3d', 'authentication',
                   'cvc', 'ccn', 'generic_error', 'generic error',
                   'restricted_card', 'fraudulent', 'not_permitted',
                   'transaction_not_allowed', 'card_not_supported']
        if not any(n in lower for n in normal):
            return False
    return True


# ====================== URL NORMALIZATION ======================
def normalize_site_url(url):
    url = url.strip().lower()
    url = re.sub(r'^https?://', '', url)
    url = url.rstrip('/')
    if url.startswith('www.'):
        url = url[4:]
    if '/' in url:
        url = url.split('/')[0]
    return url


# ====================== MESSAGE SYSTEM ======================
client_instance = None


def build_entities(html_text, emoji_ids=None):
    text, entities = thtml.parse(html_text)
    if emoji_ids:
        idx, utf16_pos = 0, 0
        for ch in text:
            if ch == PE and idx < len(emoji_ids):
                entities.append(MessageEntityCustomEmoji(offset=utf16_pos, length=1, document_id=emoji_ids[idx]))
                idx += 1
            utf16_pos += 2 if ord(ch) > 0xFFFF else 1
    return text, sorted(entities, key=lambda e: e.offset)


async def styled_reply(event, html_text, buttons=None, emoji_ids=None, file=None):
    try:
        text, entities = build_entities(html_text, emoji_ids)
        return await asyncio.wait_for(
            event.reply(text, formatting_entities=entities, buttons=buttons, file=file, link_preview=False),
            timeout=15
        )
    except asyncio.TimeoutError:
        return None
    except:
        try:
            return await asyncio.wait_for(
                event.reply(html_text[:4000], parse_mode='html', link_preview=False),
                timeout=10
            )
        except:
            return None


async def styled_send(chat_id, html_text, buttons=None, emoji_ids=None, file=None):
    try:
        text, entities = build_entities(html_text, emoji_ids)
        return await asyncio.wait_for(
            client_instance.send_message(chat_id, text, formatting_entities=entities, buttons=buttons, file=file, link_preview=False),
            timeout=15
        )
    except:
        return None


async def styled_edit(msg, html_text, buttons=None, emoji_ids=None):
    try:
        text, entities = build_entitie
