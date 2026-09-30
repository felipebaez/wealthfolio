# Commercial and Czech/EU review readiness

Audit date: 2026-09-30.
[Issue #5](https://github.com/felipebaez/wealthfolio/issues/5), parent
[#1](https://github.com/felipebaez/wealthfolio/issues/1). Source baseline:
`6ee11b1278eff8b5123280e740fa6983b501952b`. **Documentation and investigation
only; this is not legal approval.** Every external source below was accessed
2026-09-30; displayed update dates are recorded where available.

## Executive recommendation

**Inferred recommendation:** the AGPL code is a plausible foundation for a paid
advisory service, subject to its license conditions, but the current application
and its optional services do not establish commercial launch readiness. Use an
independently named offering with an exact deployed-source publication process,
reviewed dependency notices, approved data-provider rights and a qualified
Czech/EU review of the actual business. The accepted target is **more than 50
clients on one private server/VM**. That increases operating and data-governance
work; it does not itself settle legal classifications or capacity.

**Confirmed commercial gate:** current Connect terms expressly restrict
unauthorized commercial use; personal/household subscription availability does
not grant this advisory use. Market-data rights also need examination even where
source defaults enable no-key providers. Keep these capabilities out of the
proposed commercial launch until their contractual scope is established. A
manual-file-import route avoids bank API registration as an implementation
dependency, but does not remove GDPR, advisory regulation or market-data
licensing questions.

See [operations](operations.md) for deployment/recovery gates. Privacy and
authorization decisions belong with
[security audit #3](https://github.com/felipebaez/wealthfolio/issues/3); Czech
account/investment connectivity details belong with
[bank audit #4](https://github.com/felipebaez/wealthfolio/issues/4). Commercial
review is a separate gate from a successful build or isolation test.

**Architecture impact:** no code, runtime/network calls, storage, events,
workers, retries or permission changes. Later branding/source-offer work changes
presentation/distribution. Provider selection changes outbound
data/dependencies; bank automation and advisor access change legal and
permission boundaries and require explicit human direction.

## Source license, attribution and brand

### COM-01 — High launch gate: source availability must match the deployed fork

**Confirmed:** the actual root
[LICENSE](https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/LICENSE)
is GNU AGPL version 3 dated 19 November 2007, not a proprietary-hosting ban. Its
sections 2 and 4 permit running and charging for copies/support subject to
conditions. Sections 4–6 cover preservation of notices, modification notices and
applicable corresponding-source delivery when conveying covered code. Section 1
includes the scripts needed to build/install/run the covered work; section 13
requires a prominent no-charge corresponding-source opportunity for remote users
of a modified network version.

**Verification:** read LICENSE sections 1, 2, 4–6 and 13 and root/crate license
declarations. The existing
[About page source button](https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/apps/frontend/src/pages/settings/about/about-page.tsx#L125)
links upstream. **Inferred impact:** once this fork changes the covered
application, an upstream-only link cannot supply the actual modified version.
Shipping browser bundles/container/binary artifacts also needs an applicable
object-code/source mechanism; counsel should determine covered-work scope,
including addons and separately integrated services.

**Proposed action:** maintain a prominent source offer for the exact deployed
fork revision, a reproducible source/build-instructions archive and
license/copyright/warranty/modification notices. Version every client's deployed
image-to-source association. Do not include client databases, vaults,
credentials or environment secrets in source delivery. Access to source must not
be conditioned on additional secrecy restrictions that conflict with license
rights. Publicly hosting source is one practical route; this audit does not
assert public GitHub publication is the only lawful mechanism.

**Unknown:** complete compliance of a future product distribution or addon
boundary. No incompatibility or current deployment violation is asserted. The
remote-use clause is tied to a modified version; it should not be summarized as
a blanket obligation newly created by every unmodified hosting arrangement. The
official GNU web copy could not be retrieved through browsing here; the actual
repository LICENSE is the direct evidence.

### COM-02 — High for modified offering: trademarks require distinct presentation

**Confirmed:** actual
[TRADEMARKS.md](https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/TRADEMARKS.md)
separately governs marks. Modified builds/forks must use a different name,
remove Wealthfolio logos/brand assets and avoid implying official status. It
allows accurate descriptive references and upstream attribution with a
disclaimer. Trademark references require: “Wealthfolio is a trademark of Teymz
Inc.” Third-party ticker/company marks are separately owned; the code license
does not authorize a standalone logo collection.

**Verification:** compare policy sections “Allowed,” “Not allowed,” “Forks and
modified builds,” “Attribution” and “Third-party trademarks” with existing About
UI/assets. **Inferred impact:** using the official brand for a paid modified
hosted offering risks breaching this stated policy even if source obligations
are satisfied.

**Proposed action:** choose an independent service name/domain, inventory app
icons, PWA/native assets, login/About pages, emails, links and marketing,
preserve descriptive attribution and copyright notices, and review third-party
mark use with counsel. Rebranding is future implementation, not performed in
this audit. Written permission may be an alternative; no request/contact is
authorized or made.

### COM-03 — Medium: dependency declarations are not a license inventory

**Confirmed:** root
[Cargo.toml](https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/Cargo.toml)
and main application/core/storage crates declare `AGPL-3.0`. Shared
[UI](https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/packages/ui/package.json),
[addon SDK](https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/packages/addon-sdk/package.json)
and
[addon development tools](https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/packages/addon-dev-tools/package.json)
declare MIT; SDK includes its own
[MIT LICENSE](https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/packages/addon-sdk/LICENSE).
[Dockerfile](https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/Dockerfile)
bundles a server/frontend/Alpine runtime; SQLCipher/OpenSSL build dependencies
and assets need inclusion in the actual shipped-artifact inventory. Lockfiles do
not supply a complete notices/compliance decision.

**Verification:** inspect manifest/license files and build/package/CI scripts.
No dedicated SBOM/license review workflow was found in the inspected
scripts/workflows. **Unknown:** every transitive license, precise binary
composition/crypto version, notices completeness and license compatibility of
the future artifact; no dependency installation/license scanner ran and no
incompatibility was demonstrated.

**Proposed action:** inventory exact pnpm/Cargo/native/container/asset
dependencies for each deployed artifact; retain license texts/copyright notices
and review exceptions, copyleft/linking obligations, embedded fonts/icons/ticker
logos, addon packaging and later version changes. An SBOM is an inventory input,
not legal approval. MIT package declarations do not turn the combined
application into a wholly MIT product. Reuse lockfiles and the existing release
build rather than inventing a separate dependency graph.

## Proprietary cloud services and market data

### COM-04 — High: Connect entitlement for advisory hosting is not established

**Confirmed:**
[Connect Terms](https://wealthfolio.app/connect/legal/terms-of-use/), updated
**2026-09-23**, §§5.1 and 6 describe personal/household plans and prohibit
commercial purposes without express authorization. §4.1 identifies SnapTrade,
Stripe and Supabase and additional third-party terms. The
[general terms](https://wealthfolio.app/legal/terms-of-use/), updated
**2026-08-21**, distinguish AGPL software from proprietary services.

**Verification:** read the dated terms and trace
[server Connect calls](https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/apps/server/src/api/connect.rs),
[scheduler](https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/apps/server/src/scheduler.rs)
and
[Docker build configuration](https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/Dockerfile).
**Inferred impact:** a subscription, client consent or public configuration key
is insufficient evidence of entitlement for this offering; service
restriction/suspension is a dependency risk.

**Proposed action:** require written commercial scope and
processor/subprocessor/transfer terms before use; keep provider-specific
entitlements distinct from application tenancy. No vendor contact, purchase or
live account verification occurred. Service availability is not an operator SLA.

### COM-05 — High: source-enabled provider access is not commercial redistribution permission

**Confirmed source:**
[provider construction](https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/crates/core/src/quotes/client.rs#L254)
includes Yahoo, Marketdata.app, Alpha Vantage, MetalpriceAPI, Finnhub, OpenFIGI,
calculated US Treasury and Börse Frankfurt.
[Quote service](https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/crates/core/src/quotes/service.rs#L751)
filters enabled provider settings; keyed providers require a nonempty
SecretStore key. Fresh defaults come from
[initial migration](https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/crates/storage-sqlite/migrations/2025-06-27-145729_create_market_data_providers_table/up.sql),
[Finnhub migration](https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/crates/storage-sqlite/migrations/2026-01-01-000001_quotes_market_data/up.sql#L140),
[additional providers](https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/crates/storage-sqlite/migrations/2026-03-03-000001_add_phase2_providers/up.sql)
and
[custom dispatcher](https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/crates/storage-sqlite/migrations/2026-03-25-000001_custom_provider_sources/up.sql#L8).
Actual persisted settings/contracts of a running deployment are **unknown**.

| Implemented provider / fresh default                            | Official current evidence, accessed 2026-09-30                                                                                                                                                                                                                                                                                                 | Advisory-hosting consequence / uncertainty                                                                                                                                                                                                                                                                                                                                    |
| --------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Yahoo / enabled, no key                                         | [Yahoo general terms](https://legal.yahoo.com/us/en/yahoo/terms/otos/index.html?ncid=mbr_idnedulnk00000001), official indexed retrieval; direct opening returned HTTP 999. Automated collection requires express prior permission. No displayed update date was verified.                                                                      | **Unknown** commercial Finance endpoint/display/export rights. [Source](https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/crates/market-data/src/provider/yahoo/mod.rs) uses cookies/crumb and query1/query2 Finance APIs. Technical access is not evidence of a commercial license; counsel/vendor terms clarification required.       |
| Börse Frankfurt / enabled, no key                               | [Deutsche Börse disclaimer](https://live.deutsche-boerse.com/disclaimer), no displayed update date recorded: commercialization of downloaded FWB price history, including a fee for a broader service/value-added offering, requires a separate paid license.                                                                                  | **Confirmed restriction for the documented download service; unknown** precise applicability/contract for [repository JSON API](https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/crates/market-data/src/provider/boerse_frankfurt/mod.rs). Do not assume free commercial rights.                                                       |
| OpenFIGI / enabled, no key                                      | [Terms](https://www.openfigi.com/docs/terms-of-service), **2018-11-27**, permit commercial use/redistribution of FIGI identifiers; [FAQ](https://www.openfigi.com/about/faq) discusses proprietary third-party identifiers.                                                                                                                    | **Confirmed** FIGI permission; **unknown** additional rights needed for upstream third-party ISIN/CUSIP fields. Open symbology does not license market prices or every mapped identifier.                                                                                                                                                                                     |
| US Treasury calculated / enabled, no key                        | [TreasuryDirect terms](https://www.treasurydirect.gov/legal-information/terms/), no update date recorded, distinguish government works from protected material.                                                                                                                                                                                | [Source](https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/crates/market-data/src/provider/us_treasury_calc/mod.rs) retrieves securities information and Treasury.gov yield curves. Endpoint-specific rights/attribution/non-endorsement and calculated-price presentation **unknown**; do not assume the entire site is public domain. |
| Alpha Vantage / disabled, key needed                            | [Terms §2](https://www.alphavantage.co/terms_of_service/), no update date recorded: personal/noncommercial grant absent a separate written agreement; business use/sharing is commercial.                                                                                                                                                      | **Confirmed** commercial agreement gate, including multi-client use and derived analytics/export scope. A client's own key does not prove the hosting business is covered.                                                                                                                                                                                                    |
| MarketData.app / disabled, key needed                           | [Redistribution policy](https://www.marketdata.app/docs/account/data-policies/data-redistribution/), **2026-09-03**; [commercial addendum](https://www.marketdata.app/terms/commercial-use-addendum/), **2025-10-26**. Hosted recent data can be redistribution requiring exchange licenses; downstream display and API/CSV/SQL rights differ. | **Confirmed** contract/exchange and downstream-use gate. Review fees, user reporting, retention/deletion and export permissions. The app's data/portable export capability cannot silently override a display-only entitlement.                                                                                                                                               |
| Finnhub / disabled, key needed                                  | [Terms](https://finnhub.io/terms-of-service), no update date displayed: personal plans cannot serve business use even internally without written approval; redistribution/derived-result sharing needs approval; termination has deletion duties.                                                                                              | **Confirmed** agreement gate. Establish commercial user/key/rate limits, data/analytics distribution and backup retention rights before enabling.                                                                                                                                                                                                                             |
| MetalpriceAPI / disabled, key needed                            | [Terms](https://metalpriceapi.com/terms), **2026-07-01**: free plan noncommercial; active subscription permits commercial website display with other copying/resale restrictions.                                                                                                                                                              | **Confirmed** some paid commercial display permission, **unknown** entitlement for this client's export/caching/backup workflow and continued use after cancellation; written scope clarification needed.                                                                                                                                                                     |
| Custom scraper / dispatcher enabled, sources must be configured | No single terms contract; each URL/source and extraction method needs review.                                                                                                                                                                                                                                                                  | **Unknown** rights. Scraper configuration is an external-input/network capability, not a commercial data license.                                                                                                                                                                                                                                                             |

**Verification:** source enumeration/migrations plus dated official terms
review; no provider calls, paid plan login, contract/access entitlement or
exchange-license check. FinancialModelingPrep was not found as an implemented
provider and is not treated as one. The defaults are source facts, not a
guarantee that the reviewed settings are the only possible outbound sources.

**Inferred impact:** charging for access bundled with advice can still be
commercial use/redistribution; derived performance, holdings valuations,
historical caches, exports, backups and advisor display can have different
rights from personal screen display. More than 50 users can change vendor
licensing/reporting/quota obligations. **Proposed action:** create a rights
matrix for every chosen provider: actual legal entity and plan,
instruments/regions/latency, licensed user counts, advisor/client display,
derived data, redistribution/export, retention after cancellation, backups,
attribution, quotas and termination. Keep unknown sources disabled for the
commercial service until approved, then verify that disabled sources receive
zero requests in synthetic staging. Do not merge client API keys into one
business key without a contractual and privacy decision.

### COM-06 — High: own infrastructure does not imply exclusive local processing

**Confirmed:** optional Connect/broker/device sync and external quote providers
make outbound requests; optional AI/custom providers/addons add further data
flows. [Connect Privacy](https://wealthfolio.app/connect/legal/privacy-policy/),
updated **2026-09-26**, identifies potential US/Canada processing. Source
vault/database encryption protects stored material with operator-held keys; it
does not demonstrate that the operator cannot read financial data.

**Verification:** inspect server/scheduler/provider paths and dated privacy
text; use architecture/security lanes for the complete flow map. **Inferred
impact:** a self-hosting promise can be misleading if it implies no
vendors/foreign transfers/operator access while optional functions are active.

**Proposed action:** declare every activated recipient, purpose, transmitted
fields, credentials, residency, retention and controller/processor relationship;
decide acceptable data flows before enabling integrations. Review addon/network
and AI tool access, including market-symbol queries that may reveal investment
interests. Verify selected deployment contracts and actual subprocessors rather
than treating public SCC/DPF statements as proof. **Unknown:** actual vendor
locations, signed transfer agreements, keys/consents or deployment egress; no
real account data was used.

## Qualified Czech/EU review brief

These are questions for counsel and the business; cited official materials
orient the review. They do not certify the business's status or replace the
security/connectivity audits. Do not equate a software disclaimer, client
consent or upstream service policy with regulatory permission.

| Review area                     | Question and required business evidence                                                                                                                                                                                                                                                                                                                                                                       | Official source / dated context                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Advisory activity               | What exact paid services, instruments, personal recommendations, portfolio monitoring/rebalancing and execution/referral activities will be offered? Which CNB license/registration, tied-agent arrangement, suitability/appropriateness, conflict, records, complaints and disclosure obligations apply? Can an advisor use the app to communicate recommendations, and how is authorization recorded?       | [CNB investment-firm/intermediary licensing](https://www.cnb.cz/en/supervision-financial-market/conduct-of-supervision/licensing-and-approval-proceedings/licensing-and-approval-proceedings-investment-firms-investment-intermediaries/?flavour=mobile), current page accessed 2026-09-30; [CNB RS2018-08](https://www.cnb.cz/cs/dohled-financni-trh/legislativni-zakladna/stanoviska-k-regulaci-financniho-trhu/RS2018-08), 2018 opinion on personal recommendations, including internet context. Actual planned conduct is **unknown**. |
| GDPR roles/contracts            | Who determines purposes and essential means for client portfolios, advisor access, infrastructure, support, identity, backups, AI, market providers and Connect? Which controller/processor/joint-controller relationships and Article 28 terms are required? Who can instruct the trusted operator?                                                                                                          | [EDPB Guidelines 07/2020](https://www.edpb.europa.eu/documents/guideline/guidelines-072020-on-the-concepts-of-controller-and-processor-in-the-gdpr_en), final **2021-07-07**. Roles follow actual conduct, not a “self-hosted” label.                                                                                                                                                                                                                                                                                                      |
| Lawful processing/notices       | What legal basis supports each purpose: core service, optional advisor grants, import/categorization, support access, retention, analytics and third-party transfer? Which Czech-language notices/terms and records must clients receive? How are consent withdrawal and statutory retention separated?                                                                                                       | [Commission GDPR principles](https://commission.europa.eu/law/law-topic/data-protection/information-business-and-organisations/principles-gdpr_en), current official page accessed 2026-09-30. No legal basis is selected by this audit.                                                                                                                                                                                                                                                                                                   |
| DPIA/profiling/sensitive fields | Does the intended financial profiling, scale, integration or risk require a DPIA or other consultation? Can transaction descriptions reveal health/religion or involve nonclient counterparties? What minimization and access controls apply? Does any AI activity constitute automated decision-making with legal/significant effects?                                                                       | [EDPB PSD2/GDPR Guidelines 06/2020](https://www.edpb.europa.eu/sites/default/files/files/file1/edpb_guidelines_202006_psd2_afterpublicconsultation_en.pdf), final **2020-12-15**, §§4–5; [ÚOOÚ DPIA methodology](https://uoou.gov.cz/profesional/metodiky-a-doporuceni-pro-spravce/posouzeni-vlivu-na-ochranu-osobnich-udaju), current accessed 2026-09-30. Financial data is not automatically Article 9 data; a count over 50 alone does not decide DPIA applicability.                                                                  |
| Bank access                     | Does direct or aggregator read-only access constitute AIS, technical outsourcing or another regulated/contractual relationship? Who holds registration, certificates, bank consents, authentication and liability? What can be delegated to a licensed aggregator and what remains this business's duty?                                                                                                      | [CNB payment-service licensing](https://www.cnb.cz/en/supervision-financial-market/conduct-of-supervision/licensing-and-approval-proceedings/licensing-and-approval-proceedings-payment-institutions/index.html) and EDPB 06/2020, accessed 2026-09-30. PSD2 consent and GDPR legal basis are distinct. Payment-account AIS does not establish investment-data coverage; payment initiation remains excluded.                                                                                                                              |
| Transfers/subprocessors         | Which contracting entities, regions, remote support/backup locations and transfer safeguards actually apply? Are signed SCCs or other applicable mechanisms, transfer assessments and current subprocessor details adequate for this use?                                                                                                                                                                     | [Commission SCC Q&A](https://commission.europa.eu/law/law-topic/data-protection/international-dimension-data-protection/new-standard-contractual-clauses-questions-and-answers-overview_en), accessed 2026-09-30; Connect privacy date above. Actual contracts are **unknown**.                                                                                                                                                                                                                                                            |
| Retention/export/offboarding    | Reconcile applicable advisory/accounting records with deletion/access/portability requests and provider data-deletion clauses. What financial objects, import provenance, AI chats, audit logs and counterparties must be exported? What remains in backups/legal holds, for how long, and how is deleted data kept from returning on restore?                                                                | [Commission obligations](https://commission.europa.eu/law/law-topic/data-protection/information-business-and-organisations/obligations_en), accessed 2026-09-30; technical inventory in operations. No retention durations are legally approved here.                                                                                                                                                                                                                                                                                      |
| Security/incident duties        | What risk-appropriate technical/organizational evidence, operator access controls, recovery drills, incident triage, vendor notification and client communication are required? Which events require supervisory notification, potentially within 72 hours after awareness, or affected-person notification? Does the chosen regulated-business classification introduce further ICT/outsourcing obligations? | Commission obligations above. Notification conditions need counsel/incident facts; no blanket notification duty for every incident is asserted.                                                                                                                                                                                                                                                                                                                                                                                            |
| Commercial client contract      | How should client access, explicit advisor delegation/revocation, shared-host outage risk, data accuracy/source delay, export/termination, support promises, liability and consumer rules be expressed? Are the intended license/source/branding/provider notices adequate?                                                                                                                                   | Actual LICENSE/TRADEMARKS and provider terms above. Software “as is” language does not decide obligations of the paid advisory service.                                                                                                                                                                                                                                                                                                                                                                                                    |

## Proposed backlog and dependencies

All work awaits human direction; no implementation issues or vendor/legal
contact were created. Engineering/preparation person-day ranges exclude unknown
legal/vendor lead time.

| Key / priority            | Proposed deliverable and dependencies                                                                                          | Effort / confidence                                                                       | Acceptance and validation                                                                                                                                                                                                      |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| COM-B1 / launch gate      | Brand/attribution and exact deployed-source package; choose name, distribution and final fork scope; reuse About/release paths | 2–5 days / high for scope, medium for full inventory                                      | Modified offering uses distinct name/assets; prominent exact source archive/build scripts/notices available to every remote user; archive builds selected version without data/secrets; counsel reviews covered-work mechanism |
| COM-B2 / launch gate      | Exact-artifact dependency/native/asset license inventory; depends on immutable build and chosen addon/runtime packages         | 2–4 days / medium                                                                         | SBOM and notices trace to deployed digest; unresolved license issues documented/resolved by reviewer; MIT/AGPL and third-party marks kept distinct; no unscanned transitive “compliant” claim                                  |
| COM-B3 / launch gate      | Provider and Connect commercial rights/recipient matrix; depends on features, >50 users, advisor permissions and exported data | 1–3 preparation days + unknown external time / high for need, low for entitlement outcome | Written permissions cover actual business use, display/derived/export/backups/retention/quotas; unapproved sources disabled and no-request behavior tested; no purchase/contact without further authorization                  |
| COM-B4 / launch gate      | Czech/EU service/privacy/contract counsel pack; depends on product/advice scope, isolation model, host region and roles        | 2–5 preparation days + counsel time / medium                                              | Business classification, registrations/obligations, purposes/legal bases, recipient/transfer contracts, DPIA decision, notices, retention and incident responsibilities recorded by qualified reviewers                        |
| COM-B5 / before expansion | Operational evidence for client promises and offboarding; reuse operations recovery/access/export procedures                   | 2–4 days / medium; overlaps OPS-B3/B4                                                     | Synthetic >50-client deployment evidence or documented blocker, measured recovery/support assumptions, full data inventory/export/deletion/restore reconciliation and approved vendor retention treatment                      |

## Business decisions and limitations

Decide the legal business entity and precise advice scope; desired independent
name and source distribution; client/advisor/operator permissions; optional
services and outbound recipients; hosting/backup region and support operators;
provider rights/budget/user model; retention and service commitments. **Accepted
planning facts:** >50 clients and one private server/VM. Hardware, simultaneous
activity, portfolio volume, vendor agreements and business licensing status
remain unknown. Qualified review and provider approval time cannot be estimated
as engineering days.

**Confirmed work:** actual LICENSE, TRADEMARKS, manifests, provider
factories/default migrations, About source link and cloud configuration traced
at the pinned source SHA; current official sources reviewed on the audit date.
No financial client data, paid provider credentials, production host, signed
agreements or counsel opinion was available. Yahoo direct retrieval was blocked
(HTTP 999), so its indexed official general terms are a limitation, not a
Finance-license determination. GNU and EUR-Lex direct browsing did not yield
usable pages; repository AGPL text and official CNB/EDPB/Commission/ÚOOÚ sources
support the scoped statements/questions.

**Checks:** source/path/reference and documentation diff review; the operations
document records four passing Node script tests and 22 passing Python script
tests in this worktree, which do not establish legal compliance, live
encryption, commercial entitlements or operational readiness. No application
dependencies or broad system tools were installed; only standalone Prettier
3.8.1 was fetched in the npm cache for audit formatting. No application code
changed. Dependency-license, CVE, legal/contract and full runtime validation
remain **unknown/not performed**. Findings distinguish confirmed restrictions
from inferred consequences and unresolved applicability.
