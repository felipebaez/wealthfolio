# Czech bank exports and read-only connectivity

Audit date: 2026-09-30.
[Issue #4](https://github.com/felipebaez/wealthfolio/issues/4),
[parent #1](https://github.com/felipebaez/wealthfolio/issues/1). Baseline
source: `6ee11b1278eff8b5123280e740fa6983b501952b`. Implementation-path
findings, checks and proposed backlog: [imports.md](imports.md).

**Executive recommendation — inferred:** make the first advisory pilot a
reviewed file-import service. George has the clearest current general-purpose
export documentation; KB+ explicitly documents business CSV eligibility; RB
business CSV is documented but variants change; ČSOB CEB publishes several
structured statement formats. Choose actual clients' products before choosing
parsers. Fix shared accuracy/provenance/reconciliation gaps, verify one format,
then expand. Bank transaction data is useful for cash and transfers; it does not
reconstruct securities positions or returns. Keep investment statements and
automated connectivity as separate workstreams.

**Decision status:** investigation complete for the accessible public evidence,
documentation awaiting consolidation review. No bank/product importer is
certified. No production account/API access, client consent, bank contact,
subscription, payment initiation or product change was performed or authorized
by this audit. Provider contract and legal feasibility remain outside a
technical source audit.

**Architecture impact:** this documentation makes no runtime changes. File
imports should reuse existing local parser/templates, core service, SQLite and
events; future automatic access adds opt-in financial-data transmission and
per-client secrets/consent/checkpoints and requires explicit boundary review.
Proposed implementation is pending human direction.

## Evidence conventions

**Confirmed** means an official source states the capability or source code
demonstrates it. It does not mean tested on a client's account. **Inferred** is
an engineering recommendation or consequence. **Unknown** means not established
from current accessible evidence. “Unknown” is not “unsupported by the bank”;
“not supported by the present CSV path” is a specific application limit.

All official external sources below were consulted on **2026-09-30**. Where a
publication/version date is shown, it is recorded separately; an undated live
page's access date is not its publication date. No authentic bank export was
obtained. Documentation screenshots, sample API JSON or statement format
descriptions are not representative files accepted by the current application.
Search results for other countries, payment gateways, merchant settlement or
bank aggregate fund portfolios were excluded as evidence of Czech customer
bank-account support.

## Bank-by-bank file and investment matrix

| Institution / product / channel                                                | Confirmed available exports or records                                                                                                                                                          | Retail / business eligibility                                                                                                                                                    | Sample and application status                                                                                                                                                                                                                   |
| ------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| KB — KB+ accounting data                                                       | CSV with/without headers, XML, BEST KB `.OKM/.KMO`, compatible media `.GPC`; a download may be ZIP. Maximum 31-day range per download, up to 24 months back. [KB-1]                             | Owner/disponent of business current account with Standard Business tariff or higher. This source does not establish equivalent retail KB+ CSV access.                            | **Unknown:** current retail machine-readable exports, exact columns/encoding/date/sign semantics and authentic files. CSV is a template candidate after samples; other formats/ZIP need explicit local parsing and limits.                      |
| KB — Amundi-distributed funds / investment portfolio                           | Quarterly investment statements and online portfolio visibility documented; online visibility after trades can lag processing. [KB-2]                                                           | Documented fund customer context; exact customer contract/product determines access. Business versus retail export schema not established.                                       | Statement existence **confirmed**; CSV/XLSX/XML investment export, ISIN/quantity/fees/tax completeness and sample availability **unknown**. Do not infer securities trades from the current-account payment export.                             |
| KB — Online Portfolio / capital-market portfolio account                       | Monthly or quarterly portfolio-account statements, online portfolio information. [KB-3]                                                                                                         | Reviewed page is corporate/institutional; do not apply to every retail fund account.                                                                                             | Machine-readable trade/holdings format and sample **unknown**; separate from Amundi and KB+ payment-account data.                                                                                                                               |
| Raiffeisenbank CZ — entrepreneur/business internet banking transaction history | CSV and PDF movement export documented. [RB-1] Corporate FAQ acknowledges changes to CSV column ordering/content and numeric formatting. [RB-2]                                                 | Business/entrepreneur channel confirmed. Current consumer channel/tariff availability requires verification; historical retail material is insufficient for present eligibility. | **Unknown:** actual variant/bytes/headers and authentic sample. CSV candidate after intake; avoid one positional mapping for all generations.                                                                                                   |
| Raiffeisenbank CZ — business account statements                                | PDF, ABO, Gemini and XML statement download documented separately from history CSV. [RB-3]                                                                                                      | Entrepreneur/business product page.                                                                                                                                              | Structured formats need dedicated parser, not a template-only promise. Exact exported XML schema/version, historical retrieval and samples **unknown**.                                                                                         |
| Raiffeisenbank CZ — RBroker / Raiffeisen investice / custody                   | Product terms distinguish account and asset-account information and the trading platforms. [RB-4]                                                                                               | Investment contract/platform-specific; no blanket retail/business or bank-channel equivalence.                                                                                   | Existence of statements/in-platform information **confirmed**; current export formats, trade/holding sample and coverage **unknown**. Obtain RBroker and Raiffeisen investice samples separately if required.                                   |
| ČSOB CZ — retail internet banking / Smart                                      | Public banking/help pages establish banking access; this research did not establish a current machine-readable retail transaction format.                                                       | Retail context.                                                                                                                                                                  | CSV/TXT/XLSX eligibility, exact layout and samples **unknown**. Legacy InternetBanking 24 TXT references are not current compatibility proof. Merchant SoftPOS CSV is a different product.                                                      |
| ČSOB CZ — CEB business statements / advices                                    | PDF and statement formats BBF, GPC, MT940, TXT (BB-TXT), XML (CBA); intraday advices BBF/MT942. CEB also offers tabular export. [CB-1]                                                          | Business CEB users with relevant access.                                                                                                                                         | Dedicated structured-format parser candidates after sample/spec validation. Exact tabular movement export extension/schema **unknown**. CSV of payment templates/bank connections is not transaction-history CSV.                               |
| ČSOB CZ — ČSOB Investice funds/portfolio                                       | User guide describes portfolio and a “Zprávy a výpisy” section with status statements. [CB-2]                                                                                                   | Investment customer/product permission-dependent.                                                                                                                                | Formats and trade/holdings fields/sample **unknown**. ČSOB Asset Management, Patria, pensions and DIP can involve separate providers/contracts; no blanket ČSOB investment import claim.                                                        |
| Česká spořitelna — George transaction history                                  | General FAQ lists CSV, PDF, MS Excel, JSON and MS Money with selectable period and fields. [CS-1]                                                                                               | General George help; verify actual customer's product and enabled export menu. Business George separately documents history export and file-transfer add-on. [CS-2]              | Formats **confirmed**, fixed schema **unknown** because fields/settings vary. CSV is strongest initial candidate; current importer does not directly parse XLSX/JSON/MS Money/PDF. No authentic sample.                                         |
| Česká spořitelna — business George / George Business                           | Business file-transfer add-on offers ABO standard/internal and comma/semicolon CSV. [CS-2] George Business history export offers CSV, XLSX, JSON, customizable fields/order and preview. [CS-3] | Business accounts/permissions; not interchangeable with consumer George.                                                                                                         | Distinct settings and schemas need distinct tested variants. George Business completed-history UI covers seven years, with booking date and Czech payment symbols; balance display has restrictions. [CS-4] This is not an API history promise. |
| Česká spořitelna — George asset account / investments                          | “Přehled obchodů” transaction statement and “Přehled investičního portfolia” status statement accessible in George statements. [CS-5]                                                           | Asset-account customer context; not the payment-account transaction menu.                                                                                                        | Record existence **confirmed**; machine-readable format, unit quantities/cost/charges/tax availability and real sample **unknown**. Trades and dated holdings require separate intake.                                                          |

Source-specific export notes: **confirmed**, KB-1's eligibility is a business
tariff restriction. **Confirmed**, CS-2's file-transfer data statements are
generated on a selected frequency and available one year from generation; that
window differs from the chosen history export. **Confirmed**, CS-4 describes
completed transactions only and opening/closing balance visibility for
transactions after 2025-04-30. Availability of balances in the client's chosen
CSV variant still needs a sample. **Inferred**, downloadable PDFs can be a
manual verification aid for totals but do not constitute deterministic automatic
CSV compatibility.

## Automated read-only access matrix

| Institution / product                                    | Confirmed public data/API                                                                                                                                                                                              | Access / authorization                                                                                                                                                                                                                                        | Sandbox versus production; unresolved production facts                                                                                                                                                                                                                                      |
| -------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| KB — regulated AIS CZ                                    | Accounts, balances, transactions and standing orders; bank states EU/Czech PSD2 authorization and qualified certificate requirements. [KB-4]                                                                           | PSD2 production onboarding requires registry/notified status and registered QWAC/QSEAL according to KB's process. Sandbox can be explored without licensed-TPP status using test certificate. [KB-5]                                                          | Sandbox/live distinction **confirmed**. Customer account grants, current consent duration, rate/history/page limits, balance types and retail/business edge cases require authoritative current CZ spec verification. No investment coverage established.                                   |
| KB — API Business Suite / Account Direct Access / STATDA | Developer catalog lists transaction/balance direct access and statement detail/generation/download. STATDA is explicitly KB+ account-statement retrieval. [KB-6], [KB-7]                                               | Separate premium/business route; contract/tariff, account holder/disponent authorization, app registration and exact certificate/grant model need product-specific confirmation.                                                                              | Product existence **confirmed**; exact eligibility, statement formats, history/pagination/limits/renewal and whether an advisor may host access for clients **unknown**. An own-account service must not be assumed an AISP permission to all clients.                                      |
| Raiffeisenbank CZ — Premium API                          | Accounts/currency folders, balances, posted transactions including intraday, statement list/download and FX data. [RB-5]                                                                                               | Developer app ClientID plus bank-issued PKCS#12 client certificate/password for mTLS; account/method permissions set by client in banking. [RB-6]                                                                                                             | Both sandbox and production documented. Premium own-account route is separate from regulated PSD2; exact consumer eligibility and terms for advisor-hosted third-party software **unknown**. Investment endpoints not established. See verified operating limits below.                     |
| Raiffeisenbank CZ — regulated AIS                        | Searchable bank portal includes legacy Equabank AISP sandbox artifacts; its PaymentServices 3.0.0 product is payment initiation. [RB-7], [RB-8]                                                                        | **Unknown:** current AIS production onboarding/certificate/consent detail for all RB CZ accounts. Do not substitute old Equabank sandbox or PISP product for current RB AIS.                                                                                  | Bank-specific licensed aggregator coverage or authorized current documentation needed. No AIS calls made. API rates/history/page/renewal remain **unknown** here, independently of Premium API.                                                                                             |
| ČSOB CZ — regulated account information                  | Official public open-banking page describes account balances/history with client authorization. TPP license, insurance and certificate requirements stated; developer registration for API key. [CB-3], [CB-4], [CB-5] | ČSOB Identity redirect and explicit grant; page states 180-day authentication exception, then reauthentication. This is not a blanket 180-day transaction-history or token-life guarantee.                                                                    | Production availability described; developer portal inaccessible to research tool. Sandbox process, issuer acceptance, rates, history, pagination, account/card eligibility and exact contract requirements **unknown** until accessible current specs. No investment coverage established. |
| ČSOB CZ — Business Connector / CEB                       | Automated file transfer and bank-issued communication certificate management; custom programs may implement API instead of bank app. [CB-6]                                                                            | CEB service enabled by customer; certificates controlled by customer. Bank app download requires accepting licensing agreement; no installation/acceptance performed.                                                                                         | Business contract route distinct from PSD2. Supported account access, download-only privileges, history/rate/page limits, certificate renewal/revocation and hosted-advisor eligibility **unknown**. Statements are not investment APIs.                                                    |
| Česká spořitelna — PSD2 / partner API                    | Public API Multibanking page describes accounts/balances/history and customer redirect/consent. Bank connection guide distinguishes PSD2 authorization from contractual connection routes. [CS-6], [CS-7]              | Registered application, bank approval and client authorization/token described. Applicable certificate type and read-only scopes require selected current production product/spec. A bank partnership does not automatically establish regulatory permission. | Sandbox/system-test versus live is documented in the connection guide; access to full docs can require bank approval. Rate/history/page/consent/token renewal and product eligibility **unknown**. George UI coverage does not establish API coverage. No investment endpoint verified.     |

### Verified RB Premium operating details

**Confirmed — RB-5/RB-6:** transaction `from` is limited to 90 days; pages start
at 1 and `lastPage` controls completion; empty/nonexistent page may return 204.
Payload includes entryReference, booking/value dates, amount/currency/direction,
counterparties and VS/SS/KS. Published limits are 10 requests/second and
5,000/day per operation/client; statement download 5/second and 1,500/day; rate
headers expose actual limits. Certificates can have limited validity (example
five years) and annual blocking requiring client unblocking. Sandbox description
also says production limits depend on subscription plan; use current assigned
limits rather than hard-code marketing numbers. Documented production schema
version is `1.1.20240910`, not a guarantee of current account eligibility.
Certificate renewal, blocking and historical file backfill must be part of pilot
behavior. JSON amounts typed as double need careful decimal ingestion; schema
examples are not bank-file fixtures. Payment upload is outside scope.

### Known source contradictions and limits

- **Confirmed:** KB AIS page labels its linked manual version 12 dated
  2026-06-18, while the resolved filename contains `v11_V2`. Retrieval returned
  PDF metadata but subsequent body searches failed. Treat detailed CZ limits as
  **unknown**, rather than copying the Slovak manual or relying on the filename.
  A future specification review must reconcile actual content/version.
- **Confirmed:** ČSOB's API-list summary calls production access a certificate
  “from ČNB”; its TPP manual points to a certificate authority and separates
  licensing. Treat the short label as insufficient certificate-issuer guidance;
  verify technical acceptance from the actual current onboarding specification.
- **Confirmed:** searchable RB legacy Equabank AISP sandbox and a published PISP
  product are not sufficient evidence of current RB CZ account-information
  production coverage.
- **Confirmed:** CSV exports mentioned for ČSOB payment templates/contacts,
  SoftPOS or bank-level fund portfolios describe different datasets. They must
  not be used to claim retail account or client investment CSV import support.
- **Unknown:** bank-by-bank UTF-8/Windows-1250/ISO-8859-2, exact Czech headers,
  signed amount conventions and canonical date column. Existing parser
  capabilities and Czech formatting conventions do not fill these evidence gaps.

## Direct integration versus aggregator

**Inferred decision:** self-hosting the application and keeping SQLite locally
are compatible with calling a bank directly, but direct connectivity creates
off-machine financial-data exchange and server-held authorizations. A regulated
AIS route requires the actual provider arrangement; a premium own-account
certificate route needs its terms and delegation boundaries checked. Reusing a
client's personal login or screen-scraping their internet banking is not the
proposed route.

| Option / current evidence                       | Self-hosting and privacy assessment                                                                                                                                                                                                                                                                                        | Decision gate                                                                                                                                                                                                                                                                    |
| ----------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Direct bank AIS as licensed/authorized provider | Avoids an additional aggregator; application still receives and stores bank data and must securely own client grants, certificates, callbacks and revocation. Bank onboarding differs.                                                                                                                                     | Qualified Czech/EU review of service role plus bank-specific production spec/certificate registration. No authorization obtained in this audit.                                                                                                                                  |
| Bank business/premium account authorization     | RB Premium and ČSOB Business Connector may suit business customers; KB API Business is a distinct option. **Inferred:** useful for a business-account pilot, not a general retail-client substitute.                                                                                                                       | Verify tariff, permitted hosting/delegation, read-only credential scope and client revocation. No assumption that advisory onboarding grants bank access.                                                                                                                        |
| Finbricks                                       | Official provider describes a single multi-bank interface and service for partners without their own PSD2 license, with contract before development/production. [AG-1] **Inferred:** app can remain self-hosted while data passes through a third party; this does not satisfy a strict “no aggregator processing” policy. | Verify exact four-bank/product availability, controller/processor roles, storage region/retention/subprocessors/deletion, rates/history/consent, pricing and commercial-advisory eligibility. None is established by the broad “all banks” wording. No contact or contract made. |
| Enable Banking                                  | Its official Czech market page explicitly says it currently does not provide its services to Czech-resident payment service users; TPPs operating in CZ may use its technical API. [AG-2] FAQ says it does not store/cache financial data beyond delivery. [AG-3]                                                          | **Confirmed blocker** to assuming its license covers a new unlicensed advisory service for Czech residents. A data-transit design still needs permission/contract/security review; “no storage” does not mean no processing/transmission.                                        |
| GoCardless Bank Account Data                    | Official technical docs describe authorized AISP operation and hosted consent/token handling with raw account/balance/transaction delivery. [AG-4]                                                                                                                                                                         | **Unknown:** current new-customer commercial onboarding and exact Czech bank coverage. API docs do not prove the operator can open a new account or purchase this use case. Do not recommend it as an available free solution.                                                   |
| Existing Wealthfolio Connect                    | Source default is SnapTrade and uses a configurable cloud API; see pinned traces in imports.md.                                                                                                                                                                                                                            | **Unknown:** coverage of these Czech products, terms for client-advisory use, provider privacy and commercial access. Reuse ingest infrastructure where suitable, not an unverified institution/contract assumption.                                                             |

**Proposed privacy contract requirements:** client sees exactly which bank
accounts, data fields and provider receive access; authorizes bank connection
separately from advisor viewing; no payment scopes/endpoints; callback state and
session/profile ownership enforced server-side; private keys/tokens use existing
SecretStore; no browser localStorage/plaintext/logging;
reconnect/revoke/suspend/offboard semantics documented; jobs cannot continue
under stale grants. If an aggregator is selected, declare transit/retention
explicitly and require an acceptable DPA, hosting/transfer terms, incident
handling and deletion/export process. These are proposed implementation and
legal-review requirements, not a claim that existing bank grants or tenant
controls meet them.

## Representative sample intake: external blocker

**Request for the next phase:** obtain authorized, sanitized representative
exports for each selected bank **and exact product/channel**, with the
export-settings screen transcribed. Do not put genuine client statements,
credentials, identifiers or portfolio data in public issues, PRs or logs. This
audit accepts only synthetic data; any later real-file handling needs an
approved private intake and replacement process. No bank sample was received or
invented here.

Preserve actual file structure during sanitization: exact headers and order,
delimiters/quotes/newlines, BOM/encoding, preamble/footer and date/number
formatting. Replace names, addresses, IBAN/local numbers, payment
symbols/references and investment amounts/positions consistently; reconstruct
internally consistent synthetic opening/closing balances. Do not open and
re-save in Excel before recording original byte/format facts. Distinguish vendor
public sample, safely sanitized real-shaped export and fully synthetic fixture;
none alone establishes current production eligibility.

| Intake by institution | Needed records/settings, without inventing headers                                                                                                                                                                                                                                                                         |
| --------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| KB                    | KB+ retail availability evidence separately from Standard Business accounting data. For eligible business export: header/no-header choices, period boundaries, currency and tariff; overlapping exports and balance statement. For investments: fund statement versus Online Portfolio trade/status statements separately. |
| RB CZ                 | Consumer availability evidence separately from entrepreneur/corporate CSV; current export version/settings, currency folder, statement versus movement history. Obtain RBroker and Raiffeisen investice trade/status exports separately if in pilot.                                                                       |
| ČSOB CZ               | Current retail export-menu evidence and file; CEB actual selected statement format plus official version/spec and totals; intraday advice identified separately. ČSOB Investice statement/menu evidence; identify Patria/pension/DIP provider separately.                                                                  |
| Česká spořitelna      | Consumer George versus business George versus George Business; selected fields/order/separator/period/default locale. Asset-account trade and portfolio statements separately from payment history; date, quantity and cost/charge availability recorded.                                                                  |

For all variants request examples of booked incoming/outgoing, fee/interest/tax,
reversals, pending exclusion, own-account transfers, foreign currency and
repeated equal same-day payments if the product emits them. Include two
overlapping periods and exact repeat export, no-transaction period, start/end
balances and legitimate total/count expectations. Investments need actual
evidence of ISIN/other identifiers, quantities, prices, dates,
fees/tax/corporate actions; mark missing fields rather than manufacture trades.
Include UTF-8 and any verified legacy-encoding variant only when the product
really emits it.

A named importer can be accepted only after a golden expected ledger/holdings
outcome, preview, field errors, repeat-import idempotency and balance/position
reconciliation pass through both affected runtimes. Synthetic helper tests prove
mechanics; samples establish format shape; eligibility/production authorization
requires separate evidence.

## Findings for consolidation

| ID / severity / confidence                                             | Evidence / verification                                                                                         | Impact / proposed action                                                                                                                                                                                           |
| ---------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| BANK-06 / high / confirmed evidence gap                                | File matrix and intake above; no real sample; no verified current Czech template/fixture in traced source.      | Do not advertise all four institutions compatible. Select products, collect samples, then certify each variant via BANK-01/02/03 proposals in imports.md.                                                          |
| BANK-07 / high / confirmed coverage distinction                        | KB AIS, ČSOB account-information and RB Premium describe bank account data; investment statements are separate. | Payment APIs cannot be assumed to provide trades/holdings/fees/tax or reconstruct returns. Separate cash versus securities roadmap and contracts.                                                                  |
| BANK-08 / high / confirmed provider restriction                        | Enable Banking's current official CZ market notice, AG-2.                                                       | Do not select its licensed service for Czech-resident users without resolving the stated restriction. Technical API use by an authorized TPP is a different model.                                                 |
| BANK-09 / medium / confirmed variant/eligibility risk                  | KB-1 business tariff restriction, RB-2 CSV changes, CS-1/3 selectable fields and formats.                       | A bank-name template alone is insufficient. Verify product/channel/export settings/version and fail clearly on unsupported variants.                                                                               |
| BANK-10 / medium / confirmed access barriers; legal conclusion unknown | Bank API and aggregator evidence above; detailed constraints absent/inaccessible for several products.          | Automatic pilot requires verified production rights, consent/credential isolation, rates/history/pages/renewal and privacy terms. BANK-04/05 proposals; no paid service or bank contact is approved by this audit. |

Application findings IMP-01–06 and candidate implementation backlog with
dependencies, person-day ranges, confidence, acceptance criteria and tests are
in imports.md. They are proposals for synthesis/orchestrator deduplication; no
implementation issues were created by this lane.

## Business decisions needed

1. First clients' exact products: consumer/business banking and which investment
   platforms; select the first verified file variant by demand.
2. Initial service promise: cash/transactions, dated holdings or reconstructed
   investment performance. Missing history/cost data must constrain the promise.
3. Is aggregator financial-data transit acceptable, or only direct-bank access?
   Is licensed-provider onboarding a business objective, or should a contracted
   provider handle it?
4. Who reviews/approves imports and how is separate advisor access authorized?
   File upload and bank consent do not themselves grant an advisor permission.
5. Required provenance/raw-file retention and reconciliation policy; private
   sample intake route and legal review owner. The service operator's access to
   server-held credentials/data remains a separate security decision.

## Official source register

All accessed **2026-09-30**, official bank/vendor sources. Undated unless
expressly noted. These establish published capabilities, not tested access,
provider SLA or legal approval.

- **KB-1:**
  [KB+ accounting-data download](https://www.kb.cz/cs/podpora/ucty-a-platby/jak-stahnout-ucetni-data-v-kbplus).
- **KB-2:**
  [Fund purchase/sale and statements](https://www.kb.cz/cs/podpora/investovani/jak-funguje-nakup-a-prodej-listu-podilovych-fondu).
- **KB-3:**
  [Capital-market portfolio account](https://www.kb.cz/cs/korporace-a-instituce/sporeni-a-investovani/cenne-papiry/obchodovani-na-kapitalovych-trzich).
- **KB-4:**
  [AIS CZ service](https://www.kb.cz/cs/kbapi/psd2/informace-o-uctu-ais), manual
  label version 12, 2026-06-18.
  [Resolved manual URL](https://www.kb.cz/getmedia/2439e1c8-f2c4-4439-b3dc-c708056e6031/API-Informovani-o-uctu-%28AIS%29_v11_V2.pdf);
  body/version not validated.
- **KB-5:**
  [PSD2 sandbox and production onboarding](https://www.kb.cz/cs/kbapi/psd2/).
- **KB-6:** [Developer product catalog](https://developers.kb.cz/).
- **KB-7:**
  [STATDA KB+ account statements](https://www.kb.cz/cs/kbapi/extra-sluzba-api-business/vypisy-z-uctu-pres-api-v-kb-%28statda%29);
  subsequent retrieval timed out, detailed operating constraints not confirmed.
- **RB-1:**
  [Entrepreneur internet banking](https://www.rb.cz/podnikatele/ucty-a-platebni-styk/prime-bankovnictvi/internetove-bankovnictvi?an=ft-bc).
- **RB-2:**
  [Corporate account FAQ / changed CSV](https://www.rb.cz/firmy/transakcni-bankovnictvi/elektronicke-bankovnictvi/internetove-bankovnictvi/caste-dotazy/ucty).
- **RB-3:**
  [Business batch import and statement export FAQ](https://www.rb.cz/podnikatele/ucty-a-platebni-styk/prime-bankovnictvi/internetove-bankovnictvi/caste-dotazy/import-hromadnych-plateb).
- **RB-4:**
  [Investment product conditions](https://online.rb.cz/doc_attachments/VKS_Produktove_podminky_obstaravani_obchodu_s_investicnimi_nastroji_a_jinych_sluzeb_CZ_cistopis_01082024.pdf),
  file version 2024-08-01; current applicability to a client's contract unknown.
- **RB-5:**
  [Premium production schema](https://developers.rb.cz/premium/documentation/01rbczpremiumapi),
  version `1.1.20240910`.
- **RB-6:**
  [Premium portal / sandbox and certificate lifecycle](https://developers.rb.cz/premium).
- **RB-7:**
  [Legacy Equabank AISP sandbox artifact](https://developers.rb.cz/store/apis/widget?name=AISPGetTransactionsSandbox&provider=admin&tag=Sandbox&version=2.0.4).
- **RB-8:**
  [PaymentServices 3.0.0](https://developers.rb.cz/store/apis/info?name=PaymentServices&provider=admin&version=3.0.0),
  page update 2022-01-25, PISP not AIS.
- **CB-1:**
  [ČSOB CEB / statement and advice formats](https://www.csob.cz/en/businesses/online-channels/ceb).
- **CB-2:**
  [ČSOB Investice user guide](https://www.csob.cz/documents/10710/15979913/csob-investice-uzivatelska-prirucka-pro-klienty.pdf),
  date not independently established.
- **CB-3:**
  [Public open banking and authentication renewal](https://www.csob.cz/csob/otevrene-bankovnictvi-csob/pro-verejnost).
- **CB-4:**
  [Developer API list](https://www.csob.cz/csob/otevrene-bankovnictvi-csob/pro-vyvojare/seznam-api),
  [developer entry](https://www.csob.cz/csob/otevrene-bankovnictvi-csob/pro-vyvojare).
  Linked developers.csob.cz portal inaccessible via research tool.
- **CB-5:**
  [TPP manual](https://www.csob.cz/portal/documents/10710/15236928/psd2-manual-pro-treti-strany.pdf);
  indexed official text read, direct subsequent retrieval inaccessible. Exact
  technical onboarding not verified.
- **CB-6:**
  [Business Connector](https://www.csob.cz/firmy/prehled-on-line-kanalu-a-aplikaci/business-connector),
  [custom program communication-certificate procedure](https://www.csob.cz/documents/10710/15532355/bc-postup-pro-tvorbu-komunikacniho-certifikatu.pdf).
- **CS-1:**
  [George export FAQ](https://www.csas.cz/cs/caste-dotazy/jak-z-george-exportovat-transakce).
- **CS-2:**
  [George for business / export and file-transfer eligibility](https://www.csas.cz/cs/firmy/internetove-bankovnictvi/george).
- **CS-3:**
  [George Business print/export](https://www.csas.cz/cs/george-help/george-business/transakce-a-vyhledavani/tisk-a-export/tisk-a-export-historie),
  page update 2025-02-10.
- **CS-4:**
  [George Business transaction history](https://www.csas.cz/en/george-help/george-business/transactions-and-search/transaction-history/transaction-history),
  page update 2026-06-29.
- **CS-5:**
  [George asset-account statements](https://www.csas.cz/cs/caste-dotazy/chci-znovu-zaslat-vypis-z-majetkoveho-uctu).
- **CS-6:**
  [API Multibanking](https://www.csas.cz/cs/internetove-bankovnictvi/api-multibanking).
- **CS-7:**
  [API connection guide](https://www.csas.cz/content/dam/cz/csas/www_csas_cz/dokumenty/obecne/how-to-connect-to-api-of-cs.pdf),
  [Czech guide](https://www.csas.cz/content/dam/cz/csas/www_csas_cz/dokumenty/obecne/jak-se-pripojit-do-api-cs.pdf).
  Current approved technical specs not obtained; Erste developer portal renders
  a JavaScript shell through research tool.
- **AG-1:**
  [Finbricks official product/contract process](https://www.finbricks.com/index_en.html).
- **AG-2:**
  [Enable Banking Czech market specifics](https://enablebanking.com/docs/markets/cz).
- **AG-3:**
  [Enable Banking FAQ / data handling](https://enablebanking.com/docs/faq/).
- **AG-4:**
  [GoCardless Bank Account Data technical overview](https://docs.gocardless.com/docs/bank-account-data);
  current commercial onboarding and bank-specific eligibility not verified.

## Validation limitations

Detailed source tracing and feasible isolated checks are recorded in imports.md.
Public documentation is uneven and some portals require JavaScript, registration
or approved access. No subscriptions, bank registrations or contacts were made
to resolve that. Current live bank APIs, consent/certificate renewal,
balances/holdings, provider-disabled behavior and client isolation were not
exercised. Named importers remain **unknown** until sanitized representative
exports and end-to-end checks exist. This audit is not legal approval for AIS,
commercial advisory activities or third-party financial-data processing.

[KB-1]:
  https://www.kb.cz/cs/podpora/ucty-a-platby/jak-stahnout-ucetni-data-v-kbplus
[KB-2]:
  https://www.kb.cz/cs/podpora/investovani/jak-funguje-nakup-a-prodej-listu-podilovych-fondu
[KB-3]:
  https://www.kb.cz/cs/korporace-a-instituce/sporeni-a-investovani/cenne-papiry/obchodovani-na-kapitalovych-trzich
[KB-4]: https://www.kb.cz/cs/kbapi/psd2/informace-o-uctu-ais
[KB-5]: https://www.kb.cz/cs/kbapi/psd2/
[KB-6]: https://developers.kb.cz/
[KB-7]:
  https://www.kb.cz/cs/kbapi/extra-sluzba-api-business/vypisy-z-uctu-pres-api-v-kb-%28statda%29
[RB-1]:
  https://www.rb.cz/podnikatele/ucty-a-platebni-styk/prime-bankovnictvi/internetove-bankovnictvi?an=ft-bc
[RB-2]:
  https://www.rb.cz/firmy/transakcni-bankovnictvi/elektronicke-bankovnictvi/internetove-bankovnictvi/caste-dotazy/ucty
[RB-3]:
  https://www.rb.cz/podnikatele/ucty-a-platebni-styk/prime-bankovnictvi/internetove-bankovnictvi/caste-dotazy/import-hromadnych-plateb
[RB-4]:
  https://online.rb.cz/doc_attachments/VKS_Produktove_podminky_obstaravani_obchodu_s_investicnimi_nastroji_a_jinych_sluzeb_CZ_cistopis_01082024.pdf
[RB-5]: https://developers.rb.cz/premium/documentation/01rbczpremiumapi
[RB-6]: https://developers.rb.cz/premium
[RB-7]:
  https://developers.rb.cz/store/apis/widget?name=AISPGetTransactionsSandbox&provider=admin&tag=Sandbox&version=2.0.4
[RB-8]:
  https://developers.rb.cz/store/apis/info?name=PaymentServices&provider=admin&version=3.0.0
[CB-1]: https://www.csob.cz/en/businesses/online-channels/ceb
[CB-2]:
  https://www.csob.cz/documents/10710/15979913/csob-investice-uzivatelska-prirucka-pro-klienty.pdf
[CB-3]: https://www.csob.cz/csob/otevrene-bankovnictvi-csob/pro-verejnost
[CB-4]:
  https://www.csob.cz/csob/otevrene-bankovnictvi-csob/pro-vyvojare/seznam-api
[CB-5]:
  https://www.csob.cz/portal/documents/10710/15236928/psd2-manual-pro-treti-strany.pdf
[CB-6]:
  https://www.csob.cz/firmy/prehled-on-line-kanalu-a-aplikaci/business-connector
[CS-1]: https://www.csas.cz/cs/caste-dotazy/jak-z-george-exportovat-transakce
[CS-2]: https://www.csas.cz/cs/firmy/internetove-bankovnictvi/george
[CS-3]:
  https://www.csas.cz/cs/george-help/george-business/transakce-a-vyhledavani/tisk-a-export/tisk-a-export-historie
[CS-4]:
  https://www.csas.cz/en/george-help/george-business/transactions-and-search/transaction-history/transaction-history
[CS-5]:
  https://www.csas.cz/cs/caste-dotazy/chci-znovu-zaslat-vypis-z-majetkoveho-uctu
[CS-6]: https://www.csas.cz/cs/internetove-bankovnictvi/api-multibanking
[CS-7]:
  https://www.csas.cz/content/dam/cz/csas/www_csas_cz/dokumenty/obecne/how-to-connect-to-api-of-cs.pdf
[AG-1]: https://www.finbricks.com/index_en.html
[AG-2]: https://enablebanking.com/docs/markets/cz
[AG-3]: https://enablebanking.com/docs/faq/
[AG-4]: https://docs.gocardless.com/docs/bank-account-data
