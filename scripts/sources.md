# Authentic public sources for the corpus

All sources below are public, free, and require no manual approval or payment.
We respect rate limits and User-Agent etiquette. Per the user's brief, this
project is non-commercial; still, we never republish copyrighted commentary
verbatim — only primary law (statutes, judgments) and public administrative
documents.

## Central statutes

- **India Code** — https://www.indiacode.nic.in/  (`scripts/scrape_indiacode.py`)
  - Bare acts as PDFs and HTML.
  - BNS, BNSS, BSA, IPC, CrPC, Indian Evidence Act, Contract Act, Companies Act,
    DPDP Act, Consumer Protection Act, Arbitration & Conciliation Act,
    NI Act, TP Act, Specific Relief Act, Limitation Act, RTI Act,
    POSH Act, IT Act, Trade Marks Act, Patents Act, Copyright Act,
    Income Tax Act, CGST Act, IGST Act, SGST Acts, Hindu Marriage Act,
    Indian Succession Act, Hindu Succession Act, Muslim Personal Law (Shariat) Application Act,
    Special Marriage Act, etc.

## Constitution

- **Constitution of India** — https://legislative.gov.in/constitution-of-india/
  - Authoritative current text (as amended).

## State statutes (Phase: MH, DL, KA + remainder by population)

- **Maharashtra** — https://www.maharashtra.gov.in/ (Law and Judiciary Department),
  https://lj.maharashtra.gov.in/
  - Maharashtra Rent Control Act, 1999
  - Maharashtra Co-operative Societies Act
  - Bombay Stamp Act / Maharashtra Stamp Act
- **Delhi** — https://lawmin.gov.in/ (selected) and https://delhi.gov.in/
  - Delhi Rent Control Act, 1958
- **Karnataka** — https://dpal.karnataka.gov.in/
  - Karnataka Rent Act, 1999
- **All states** — listed at https://www.indiacode.nic.in/  → State Acts

## Supreme Court of India judgments

- **SCI Judgment Search** — https://main.sci.gov.in/judgments
- **SCI eCourts** — https://judgments.ecourts.gov.in/

## High Court judgments (one or more per state)

- Bombay HC: https://bombayhighcourt.nic.in/
- Delhi HC: https://delhihighcourt.nic.in/
- Karnataka HC: https://karnatakajudiciary.kar.nic.in/
- Madras HC: https://www.hcmadras.tn.nic.in/
- Allahabad HC: https://www.allahabadhighcourt.in/
- Calcutta HC: https://www.calcuttahighcourt.gov.in/
- All HCs aggregated in eCourts: https://hcservices.ecourts.gov.in/

## Aggregator (last resort, public domain content only)

- **Indian Kanoon** — https://indiankanoon.org/  (`scripts/scrape_indiankanoon.py`)
  - Public-domain primary text of Indian judgments. Respect their rate limits;
    they explicitly request no aggressive scraping. Use their docfragment API
    where available and cache locally.

## Notifications, circulars

- **RBI** — https://www.rbi.org.in/  (notifications, circulars, master directions)
- **SEBI** — https://www.sebi.gov.in/legal/regulations.html
- **CBIC** — https://www.cbic.gov.in/  (GST notifications)
- **Ministry of Corporate Affairs** — https://www.mca.gov.in/

## Procedural

- **eCourts** — https://ecourts.gov.in/
- **Bar Council of India** — https://www.barcouncilofindia.org/

## Ingest hygiene rules (followed by all scrapers)

1. User-Agent: `AILawyerIndia/0.1 (research; contact: <maintainer-email>)`.
2. `robots.txt` honored.
3. Rate limit: 1 request / 2 seconds per host (configurable via
   `RATE_LIMIT_HZ`).
4. Retries on 429/5xx with exponential backoff, capped.
5. Content cached locally under `corpus/raw/<source>/<sha1>.<ext>` so re-runs
   don't re-fetch.
6. We attribute every chunk to its original public URL in `legal_documents.source_url`.
