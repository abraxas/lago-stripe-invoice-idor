<p align="center">
  <img src="header.png" alt="Abraxas Labs — lago-stripe-invoice-idor" width="100%">
</p>

<p align="center">
  <a href="https://abraxaslabs.tech"><strong>abraxaslabs.tech</strong></a>
  &nbsp;·&nbsp;
  <a href="https://github.com/abraxas">github.com/abraxas</a>
  &nbsp;·&nbsp;
  <a href="https://x.com/abraxas_null">@abraxas_null</a>
  &nbsp;·&nbsp;
  <a href="https://github.com/abraxas/lago-stripe-invoice-idor">lago-stripe-invoice-idor</a>
</p>

# lago-stripe-invoice-idor

**Lago** `v1.53.0` — GetLago

Unpublished Lago source finding: Stripe one-time webhook loads invoice by UUID with no organization_id, so another tenant can mark a victim invoice paid. handle_missing_payment is scoped; the one-time path skips it. Distinct from Adyen invoice webhooks which check organization_id.

| | |
|---|---|
| ID | Unpublished Lago source finding #2 (no CVE yet) |
| CWE | [CWE-639, CWE-345](https://cwe.mitre.org/data/definitions/345.html) |
| CVSS | **High: 7.7** `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:H/A:N` |
| Product | [Lago](https://github.com/getlago/lago) |
| Affected | all versions **through v1.53.0** (inclusive) |
| Patched | vendor patch — see references |
| Auth | authenticated (see source map) |
| License | [GNU Affero GPL v3.0](LICENSE) |
| Lab | `127.0.0.1` only · vendor/client disclosure pack, not a scanner |

---

## Advisory (from the source map)

webhooks_controller.rb 4-16. stripe_service.rb 23-25 one-time create_payment; 115-116 Invoice.find_by(id) unscoped; 235-241 handle_missing_payment IS scoped. Adyen invoices scoped (control).

---

## Entry

- **Method:** `POST`
- **Path:** `/webhooks/stripe/:organization_id`
- **Router:** InboundWebhooks::CreateService verifies attacker org webhook_secret. ProcessJob -&gt; HandleEventJob -&gt; PaymentIntentSucceededService -&gt; Invoices::Payments::StripeService#update_payment_status. one-time branch Invoice.find_by(id:) unscoped.
- **Notes:** Logged-in tenant unpublished Lago #2 CWE-639 v1.53.0. Attacker org Stripe webhook secret. Victim invoice UUID. Witness: victim payment_status succeeded. Control without payment_type stays pending. Not eval. Not a reverse shell. Disclose security@getlago.com, not a public GitHub issue.

### Call chain

- `POST /graphql registerUser attacker + victim orgs`
- `Seed StripeProvider webhook_secret on attacker; stripe_customer on victim`
- `POST /api/v1/invoices skip_psp victim unpaid invoice`
- `POST /webhooks/stripe/&lt;attacker_org&gt; signed payment_intent.succeeded payment_type=one-time lago_invoice_id=victim`
- `GET /api/v1/invoices/&lt;victim&gt; payment_status=succeeded`

### Lab preconditions

- Lago v1.53.0 shared database (Cloud / Embedded / multi-org)
- Attacker org has Stripe provider webhook_secret
- Victim unpaid invoice UUID
- Victim customer has stripe_customer + Stripe provider

### Witness

victim invoice payment_status=succeeded and total_paid_amount_cents matches; control webhook without payment_type stays pending

### Not success

- eval/base64/system payload
- reverse shell
- create_payment requires organization_id
- control without payment_type also succeeds
- invoice stays pending

---

## Patch / remediation

**Do this first:** Apply the vendor patch for **Lago**. See references.

**Verify after upgrade**

- Re-run `lago-stripe-invoice-idor-Abraxas-Labs.py` against the patched build: the mapped witness must **not** appear.
- Confirm the vendor advisory / changeset in the deployed tree (see references).
- A WAF signature is delay, not a patch.

**If you cannot update immediately**

- Disable or isolate the affected component.
- Hunt for the witness condition on production (new privileged users, unexpected files, injected rows — whatever this CVE's map names).

---

## Reproduction (authorized lab)

Target **only** `http://127.0.0.1:13001` (or the loopback you bound). Do not point this script at the internet.

```bash
python3 lago-stripe-invoice-idor-Abraxas-Labs.py
```

Success is the **witness** above in the response body. Generic 200 HTML is not it.

---

## Lab images

Loopback stack used to reproduce. Official images unless a `Dockerfile` in this folder builds from source.

- [`lab/docker-compose.yml`](lab/docker-compose.yml)
- [`lab/Dockerfile`](lab/Dockerfile)
- [`lab/run.sh`](lab/run.sh)
- [`lab/seed_stripe.rb`](lab/seed_stripe.rb)

Official image `getlago/lago:v1.53.0` on loopback `:13001`. Then:

```bash
cd lab
./run.sh
```

Publish nothing except `127.0.0.1`.

---

## References

- [github.com/getlago/lago](https://github.com/getlago/lago) tag v1.53.0
- [github.com/getlago/lago-api](https://github.com/getlago/lago-api)
- Vendor intake: [security@getlago.com](mailto:security@getlago.com) ([policy](https://www.getlago.com/company/security)). Do **not** open a public GitHub issue.

- Abraxas Labs: [abraxaslabs.tech](https://abraxaslabs.tech) · [github.com/abraxas](https://github.com/abraxas) · [@abraxas_null](https://x.com/abraxas_null)

---

## Records (structured)

```
# Lago unpublished #2 — Stripe one-time webhook unscoped invoice

CWE: CWE-639, CWE-345
Severity: High (HTTP lab SUCCESS, 95%)

## Description

`POST /webhooks/stripe/:attacker_org` verifies the attacker’s Stripe signing secret. If metadata `payment_type=one-time`, `create_payment` does `Invoice.find_by(id: lago_invoice_id)` with no `organization_id`. The org-scoped `handle_missing_payment` path is skipped.

## Product

Lago v1.53.0. Lab oracle: victim invoice `payment_status=succeeded` and `total_paid_amount_cents=1000` after a dummy signed event. Control without `payment_type` stayed pending.
```

---

## License

This disclosure pack is licensed under the **GNU Affero General Public License v3.0**. See [LICENSE](LICENSE).

---

## Disclaimer

This pack is for **the vendor, the site owner, and licensed labs**. The script talks to `127.0.0.1`. Using it against systems you do not own is not authorized by Abraxas Labs. No warranty.

<p align="center">
  <a href="https://abraxaslabs.tech">abraxaslabs.tech</a> ·
  <a href="https://github.com/abraxas">github.com/abraxas</a> ·
  <a href="https://x.com/abraxas_null">@abraxas_null</a>
</p>
