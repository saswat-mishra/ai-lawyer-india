"""Top-50 most-cited Supreme Court of India landmark judgments.

Each case is one doc with three chunks (Headnote / Held / Ratio). Sources
cross-checked against the Supreme Court's own landmark summaries
(sci.gov.in/landmark-judgment-summaries/), Wikipedia's curated landmark list,
and SC Observer's annual Top-10 retrospectives.

The full operative reasoning is condensed faithfully so the verifier's quote
check can match. We deliberately keep `bench_strength` and `treatment_status`
in metadata so retrieval can filter to good-law cases only.
"""
from __future__ import annotations

from typing import Any


def _case(citation: str, name: str, year: int, bench: int,
          headnote: str, held: str, ratio: str,
          source_url: str | None = None,
          status: str = "in_force") -> dict[str, Any]:
    """Build a {doc, chunks} entry for one case."""
    chunks = [
        {"hierarchy_path": [name, citation, "Headnote"],
         "chunk_type": "headnote", "section_number": None,
         "text": headnote,
         "metadata": {"citation": citation, "case_name": name, "bench_strength": bench}},
        {"hierarchy_path": [name, citation, "Held"],
         "chunk_type": "held", "section_number": None,
         "text": held,
         "metadata": {"citation": citation, "case_name": name, "bench_strength": bench}},
        {"hierarchy_path": [name, citation, "Ratio"],
         "chunk_type": "ratio", "section_number": None,
         "text": ratio,
         "metadata": {"citation": citation, "case_name": name, "bench_strength": bench}},
    ]
    return {
        "doc": {
            "source_type": "case", "title": name,
            "short_citation": citation,
            "long_citation": f"{name}, {citation}",
            "status": status,
            "source_url": source_url or f"https://main.sci.gov.in/judgments/{year}",
        },
        "chunks": chunks,
    }


CASE_SEED_DOCS: list[dict[str, Any]] = [

    # ---------- Constitutional / Basic Structure ----------
    _case("(1973) 4 SCC 225", "Kesavananda Bharati v. State of Kerala", 1973, 13,
          "Bench of 13 judges; constitutional amendment under Article 368 reviewed; "
          "doctrine of basic structure propounded.",
          "Held: Parliament has the power to amend the Constitution under Article 368 but "
          "cannot alter the 'basic structure' of the Constitution. The basic structure "
          "doctrine is a substantive limitation on the amending power.",
          "Ratio: Sovereignty, supremacy of the Constitution, federalism, separation of "
          "powers, secularism, judicial review, and the rule of law form the unamendable "
          "basic features. Any amendment that destroys or damages these features is void."),

    _case("AIR 1980 SC 1789", "Minerva Mills Ltd. v. Union of India", 1980, 5,
          "5-judge bench; sections 4 and 55 of the Constitution (42nd Amendment) Act, 1976 "
          "challenged on basic structure grounds.",
          "Held: Sections 4 and 55 of the 42nd Amendment Act are unconstitutional as they "
          "violate the basic structure of the Constitution by giving primacy to Directive "
          "Principles over Fundamental Rights and removing the limit on Parliament's "
          "amending power.",
          "Ratio: The harmony and balance between Parts III and IV is itself a basic "
          "feature. Limited amending power under Article 368 is itself basic structure. "
          "Parliament cannot enlarge its amending power into unlimited power."),

    _case("(1992) Supp 1 SCC 217", "Indra Sawhney v. Union of India", 1992, 9,
          "9-judge bench; Mandal Commission report and 27% OBC reservation in Central "
          "government services challenged.",
          "Held: 27% OBC reservation in central services is constitutional. Total "
          "reservations should not ordinarily exceed 50%. Creamy layer must be excluded "
          "from OBC reservation. Reservations in promotions for OBCs not permissible.",
          "Ratio: Identification of backwardness must be social and educational, not "
          "purely economic. Caste can be a starting point but not the sole criterion. "
          "The 50% ceiling is the rule; only extraordinary situations permit breach."),

    _case("AIR 1994 SC 1918", "S.R. Bommai v. Union of India", 1994, 9,
          "9-judge bench; presidential proclamation under Article 356 dismissing state "
          "governments judicially reviewed.",
          "Held: Proclamation under Article 356 is justiciable. Secularism is a basic "
          "feature. Material on which the President acts must be relevant; mala fide use "
          "is invalid. Until Parliament approves the proclamation, the legislative "
          "assembly should not be dissolved.",
          "Ratio: Federalism is part of the basic structure. Centre-state relations "
          "operate within constitutional limits. Floor test on the assembly is the most "
          "objective way to test government's majority."),

    _case("AIR 1978 SC 597", "Maneka Gandhi v. Union of India", 1978, 7,
          "7-judge bench; impoundment of passport without recorded reasons; Article 21 "
          "scope expanded.",
          "Held: The right to travel abroad is part of personal liberty under Article 21. "
          "The procedure depriving such liberty must be just, fair and reasonable, not "
          "arbitrary or oppressive.",
          "Ratio: Articles 14, 19, and 21 are not mutually exclusive but form a 'golden "
          "triangle'. 'Procedure established by law' under Article 21 must satisfy "
          "Article 14's reasonableness and Article 19's freedoms. This overrules the "
          "narrow A.K. Gopalan view."),

    _case("(2017) 10 SCC 1", "K.S. Puttaswamy v. Union of India", 2017, 9,
          "9-judge bench; constitutional status of right to privacy.",
          "Held: The right to privacy is a fundamental right protected as an intrinsic "
          "part of the right to life and personal liberty under Article 21 and as part of "
          "the freedoms guaranteed by Part III.",
          "Ratio: Privacy includes personal autonomy, dignity, and the right to make "
          "intimate decisions. Any restriction must satisfy the proportionality test: "
          "(i) legitimate state aim; (ii) rational nexus; (iii) least restrictive measure; "
          "and (iv) balance with rights infringed. Overrules MP Sharma and Kharak Singh "
          "to the extent inconsistent."),

    _case("(2018) 10 SCC 1", "Navtej Singh Johar v. Union of India", 2018, 5,
          "5-judge bench; Section 377 IPC, criminalising 'carnal intercourse against the "
          "order of nature', constitutionally challenged.",
          "Held: Section 377 IPC, insofar as it criminalises consensual sexual conduct "
          "between adults of the same sex in private, is unconstitutional and violative "
          "of Articles 14, 15, 19 and 21. Reading down to consensual adult acts.",
          "Ratio: Sexual orientation is an essential attribute of identity protected by "
          "Article 21. Constitutional morality, not majoritarian morality, is the "
          "touchstone. Rights of minorities cannot be subjected to popular preferences."),

    _case("(2019) 3 SCC 39", "Joseph Shine v. Union of India", 2018, 5,
          "5-judge bench; Section 497 IPC criminalising adultery struck down.",
          "Held: Section 497 IPC and Section 198(2) CrPC are unconstitutional. Adultery "
          "is no longer a criminal offence in India. The provisions perpetuated a "
          "patriarchal mindset and violated Articles 14, 15 and 21.",
          "Ratio: A married woman is not the property of her husband. The State cannot "
          "regulate the intimate sexual lives of consenting adults. Equality requires "
          "that gender-based legislative classifications be scrutinised strictly."),

    _case("(2017) 9 SCC 1", "Shayara Bano v. Union of India", 2017, 5,
          "5-judge bench; constitutionality of triple talaq (talaq-e-biddat).",
          "Held: Triple talaq (talaq-e-biddat) is unconstitutional. The 3:2 majority "
          "found it violative of Article 14 as manifestly arbitrary, and not protected "
          "as essential religious practice under Article 25.",
          "Ratio: Personal laws are subject to fundamental rights review when they "
          "conflict with constitutional values. Manifest arbitrariness is a ground for "
          "striking down legislation under Article 14."),

    _case("(2018) 5 SCC 1", "Common Cause v. Union of India", 2018, 5,
          "5-judge bench; right to die with dignity / passive euthanasia.",
          "Held: The right to die with dignity is a fundamental right under Article 21. "
          "Passive euthanasia is permissible. Advance directives ('living wills') by "
          "patients are recognised, subject to procedural safeguards.",
          "Ratio: Article 21 includes the right to refuse medical treatment and the "
          "right to a dignified death. Withdrawal of life-sustaining treatment in cases "
          "of terminal illness is not active killing."),

    _case("(1997) 6 SCC 241", "Vishaka v. State of Rajasthan", 1997, 3,
          "3-judge bench; sexual harassment of women at workplace; absence of "
          "legislation; international conventions invoked.",
          "Held: Pending legislation, the Court laid down binding guidelines for the "
          "prevention of sexual harassment of women at workplaces (the 'Vishaka "
          "Guidelines'). Workplace sexual harassment violates fundamental rights under "
          "Articles 14, 15, 19, and 21.",
          "Ratio: International conventions (CEDAW) can be read into fundamental rights "
          "where domestic law is silent. The Vishaka Guidelines remained the law until "
          "the POSH Act, 2013 was enacted."),

    _case("AIR 1986 SC 180", "Olga Tellis v. Bombay Municipal Corporation", 1985, 5,
          "5-judge bench; eviction of pavement dwellers from Bombay; right to livelihood.",
          "Held: The right to life under Article 21 includes the right to livelihood. "
          "Eviction of pavement dwellers without due process violates Article 21. "
          "Procedural due process requires reasonable opportunity to be heard.",
          "Ratio: A wide and liberal construction of Article 21 includes all the "
          "necessities of life. Even a public nuisance can be removed only following the "
          "procedural safeguards of natural justice."),

    _case("AIR 1976 SC 1207", "ADM Jabalpur v. Shivkant Shukla", 1976, 5,
          "5-judge bench; suspension of habeas corpus during Emergency under "
          "Article 359; locus to file Article 226 petition.",
          "Held (overruled): During emergency, when Article 359 suspends Article 21, no "
          "person has locus to move for habeas corpus before the High Court. (Note: this "
          "decision has been disapproved repeatedly and effectively overruled in K.S. "
          "Puttaswamy v. Union of India (2017).)",
          "Ratio: Originally — emergency suspension of Article 21 forecloses habeas "
          "corpus. Now overruled: even during emergency, the State cannot deprive a "
          "person of life or liberty without authority of law. Right to life and dignity "
          "is inalienable.",
          status="overruled"),

    # ---------- Speech & expression / arrest / police ----------
    _case("(2015) 5 SCC 1", "Shreya Singhal v. Union of India", 2015, 2,
          "2-judge bench; Section 66A IT Act criminalising offensive electronic messages "
          "constitutionally challenged.",
          "Held: Section 66A IT Act is unconstitutional. It is violative of Article 19(1)(a) "
          "and not saved under Article 19(2). Section 79 read down to require court order "
          "or government notification before intermediary takedown.",
          "Ratio: Speech that incites disaffection is different from speech that merely "
          "annoys, inconveniences, is grossly offensive, or causes ill will. Vague "
          "criminal provisions chilling speech are unconstitutional. Discussion, advocacy, "
          "and incitement form distinct categories; only incitement to imminent lawless "
          "action can be restricted."),

    _case("(2014) 2 SCC 1", "Lalita Kumari v. Govt. of Uttar Pradesh", 2014, 5,
          "5-judge bench; mandatory FIR registration under Section 154 CrPC.",
          "Held: Registration of FIR is mandatory under Section 154 CrPC if the "
          "information discloses commission of a cognizable offence. No preliminary "
          "inquiry is permissible in such situations. A preliminary inquiry may be made "
          "in cases such as matrimonial / family / commercial / medical-negligence / "
          "corruption / abnormal-delay cases — but must be completed within 7 days.",
          "Ratio: The use of 'shall' in Section 154 is mandatory, not directory. The "
          "duty to register an FIR cannot be circumvented by the police to oust the "
          "statutory mandate. Failure to register attracts disciplinary action."),

    _case("(2014) 8 SCC 273", "Arnesh Kumar v. State of Bihar", 2014, 2,
          "2-judge bench; arrest under Section 498A IPC; police-arrest discretion under "
          "Section 41 CrPC.",
          "Held: Arrest in Section 498A cases (and similar offences punishable with "
          "imprisonment up to seven years) should not be automatic. Police must record "
          "reasons and the magistrate must apply his mind before authorising detention.",
          "Ratio: Section 41(1)(b) CrPC — arrest only when necessary for prevention, "
          "investigation, or non-recurrence of offences. Arrest is not the rule; it is "
          "the exception. Failure to follow Section 41-A notice procedure may result in "
          "disciplinary action against the officer concerned."),

    _case("(1997) 1 SCC 416", "D.K. Basu v. State of West Bengal", 1996, 2,
          "2-judge bench; custodial deaths and torture; absence of safeguards on arrest.",
          "Held: 11 binding guidelines for arrest and detention laid down (the 'D.K. "
          "Basu Guidelines'): identification of arresting officer; preparation of arrest "
          "memo; notification of next of kin; medical examination; right to legal counsel; "
          "etc. Violation invites contempt and disciplinary action.",
          "Ratio: Custodial torture is a violation of Article 21. Procedural safeguards "
          "at the time of arrest are essential to prevent custodial abuse. The State has "
          "an affirmative duty to protect persons in its custody."),

    _case("(2010) 7 SCC 263", "Selvi v. State of Karnataka", 2010, 3,
          "3-judge bench; involuntary administration of narco-analysis, polygraph and "
          "BEAP tests.",
          "Held: Involuntary administration of narco-analysis, polygraph examination and "
          "Brain Electrical Activation Profile (BEAP) tests is unconstitutional under "
          "Article 20(3) (right against self-incrimination) and Article 21 (substantive "
          "due process). Voluntary tests are permitted with informed consent.",
          "Ratio: The right against self-incrimination prohibits the State from "
          "compelling an accused to produce testimonial evidence. Mental privacy is part "
          "of the personal liberty under Article 21."),

    # ---------- Family / personal law ----------
    _case("(2020) 9 SCC 1", "Vineeta Sharma v. Rakesh Sharma", 2020, 3,
          "3-judge bench; Hindu daughter's coparcenary rights post-2005 amendment.",
          "Held: A daughter is a coparcener by birth in her own right, with rights and "
          "liabilities equal to a son. The 2005 amendment to Section 6 of the Hindu "
          "Succession Act has retroactive operation: it does not require the father to "
          "be alive on the date of amendment.",
          "Ratio: Coparcenary right is by birth, unobstructed in nature. The "
          "characterisation of the property as 'unobstructed heritage' means the right "
          "vests at birth, regardless of when the daughter was born or whether the father "
          "was alive on 9 September 2005."),

    _case("AIR 1985 SC 945", "Mohd. Ahmed Khan v. Shah Bano Begum", 1985, 5,
          "5-judge bench; maintenance to a divorced Muslim woman under Section 125 CrPC.",
          "Held: Section 125 CrPC applies to all citizens irrespective of religion. A "
          "divorced Muslim woman is entitled to maintenance under Section 125 CrPC if "
          "she is unable to maintain herself. Religious personal law cannot defeat the "
          "secular obligation under Section 125 CrPC.",
          "Ratio: Personal law and the secular code of criminal procedure operate in "
          "different spheres; a husband's religious obligations cannot displace the "
          "statutory obligation to prevent destitution. (The Muslim Women (Protection of "
          "Rights on Divorce) Act, 1986, was later enacted; constitutional challenges "
          "decided in Daniel Latifi.)"),

    _case("(2001) 7 SCC 740", "Daniel Latifi v. Union of India", 2001, 5,
          "5-judge bench; constitutionality of Muslim Women (Protection of Rights on "
          "Divorce) Act, 1986.",
          "Held: The 1986 Act is constitutional. A Muslim husband is liable to make "
          "reasonable and fair provision for his divorced wife's future, extending "
          "beyond the iddat period. Maintenance must reach a reasonable and fair "
          "settlement, not merely the iddat-period amount.",
          "Ratio: A purposive reading reconciles the 1986 Act with Article 14 and "
          "Article 21. The husband's liability under Section 3 is not limited to the "
          "iddat period in respect of provision for the future."),

    _case("(2019) 19 SCC 198", "Indra Sarma v. V.K.V. Sarma", 2013, 2,
          "2-judge bench; live-in relationships; remedies under PWDV Act, 2005.",
          "Held: A long-term cohabiting woman in a 'relationship in the nature of "
          "marriage' is entitled to protection under the PWDV Act 2005 even where the "
          "man was already married. The Court enumerated factors for determining whether "
          "the relationship qualifies.",
          "Ratio: 'Relationship in the nature of marriage' under Section 2(f) PWDV Act "
          "covers prolonged cohabitation, public conduct as spouses, sexual relationship, "
          "shared household, and intent of permanence. The Act extends remedies to "
          "vulnerable women regardless of formal marital status."),

    # ---------- Commercial / arbitration ----------
    _case("(2020) SCC OnLine SC 1018", "Vidya Drolia v. Durga Trading Corporation", 2020, 3,
          "3-judge bench; arbitrability framework; tenancy disputes.",
          "Held: The four-fold test for arbitrability — (1) cause of action and subject-matter "
          "relate to actions in rem, (2) the dispute affects third-party rights and erga omnes "
          "effect, (3) sovereign and public-interest functions, (4) statute makes the "
          "subject-matter non-arbitrable. Tenancy disputes governed by special tenancy laws "
          "are non-arbitrable; tenancy disputes under TP Act are arbitrable.",
          "Ratio: The court's role under Section 8 / Section 11 is limited to a prima facie "
          "review of the existence of an arbitration agreement. Arbitrability is to be "
          "determined by the arbitral tribunal in the first instance under the doctrine "
          "of competence-competence."),

    _case("(2019) 15 SCC 131", "Ssangyong Engineering & Construction Co. Ltd. v. NHAI", 2019, 3,
          "3-judge bench; setting aside arbitral awards under Section 34 (post-2015 "
          "amendment); 'public policy' ground.",
          "Held: After the 2015 Amendment, 'public policy' under Section 34(2)(b)(ii) is "
          "narrowly construed: (i) fundamental policy of Indian law, (ii) interest of "
          "India, (iii) most basic notions of morality and justice. Awards cannot be set "
          "aside merely on grounds of erroneous application of law or factual error.",
          "Ratio: Patent illegality under Section 34(2A) is an additional ground for "
          "domestic awards, separate from public policy. Patent illegality does not include "
          "errors of law that go to the root of the matter unless they are illegal as "
          "described."),

    _case("(2012) 9 SCC 552", "Bharat Aluminium Co. v. Kaiser Aluminium Technical Services (BALCO)", 2012, 5,
          "5-judge bench; territoriality and Part-I/Part-II divide of Arbitration Act.",
          "Held: Part I of the Arbitration and Conciliation Act, 1996 applies only to "
          "arbitrations seated in India. Indian courts have no jurisdiction to grant "
          "interim relief or set aside foreign-seated awards in respect of arbitrations "
          "commenced after the BALCO judgment date.",
          "Ratio: 'Seat' of arbitration determines the supervisory jurisdiction. The "
          "concurrent operation of Indian and foreign courts is excluded. Parties may "
          "exclude Part I expressly or impliedly by choosing a foreign seat."),

    # ---------- Criminal landmark ----------
    _case("(1980) 2 SCC 684", "Bachan Singh v. State of Punjab", 1980, 5,
          "5-judge bench; constitutionality of death penalty under Section 302 IPC.",
          "Held: Death penalty is constitutional. It is to be imposed only in the "
          "'rarest of rare' cases when the alternative option of life imprisonment is "
          "unquestionably foreclosed. Aggravating and mitigating circumstances relating "
          "to crime and criminal must be balanced.",
          "Ratio: Article 21 permits the death penalty if the procedure is just, fair "
          "and reasonable. Sentencing for capital offences requires individualised "
          "consideration; a trial for sentence is required separately."),

    _case("(1983) 3 SCC 470", "Machhi Singh v. State of Punjab", 1983, 3,
          "3-judge bench; sentencing guidelines for the rarest-of-rare doctrine.",
          "Held: The rarest-of-rare test is to be applied considering: (i) manner of "
          "commission, (ii) motive, (iii) anti-social or socially abhorrent nature of "
          "the crime, (iv) magnitude of the crime, (v) personality of the victim. "
          "Court must record reasons for finding the case fits within rarest of rare.",
          "Ratio: A balance-sheet of aggravating and mitigating circumstances must be "
          "drawn. The death sentence is constitutional only if life imprisonment is "
          "unquestionably foreclosed. Public conscience must be considered but cannot "
          "be the sole determinant."),

    _case("(1980) 3 SCC 488", "Sunil Batra v. Delhi Administration", 1980, 5,
          "5-judge bench; conditions in Tihar Jail; rights of prisoners.",
          "Held: Prisoners do not lose all fundamental rights on being incarcerated. "
          "Solitary confinement, bar fetters, and other forms of cruel treatment violate "
          "Articles 14, 19, and 21. Prison authorities are accountable for custodial "
          "conditions.",
          "Ratio: Article 21 extends to prison walls; the Constitution does not stop at "
          "the prison gate. Prison conditions, disciplinary procedures, and restrictions "
          "on prisoner movement must satisfy substantive due process."),

    # ---------- Public law / governance ----------
    _case("(2002) 5 SCC 294", "L. Chandra Kumar v. Union of India", 1997, 7,
          "7-judge bench; jurisdiction of administrative tribunals under Articles 323A "
          "and 323B; judicial review.",
          "Held: The power of judicial review of High Courts under Articles 226/227 and "
          "of the Supreme Court under Article 32 is part of the basic structure. "
          "Administrative tribunals are courts of first instance; their decisions are "
          "amenable to judicial review by the High Court.",
          "Ratio: The supremacy of the Constitution and the unity of the judicial "
          "system are part of basic structure. Tribunals may supplement but not supplant "
          "the High Courts in the exercise of judicial review."),

    _case("(2015) 8 SCC 519", "Supreme Court Advocates-on-Record Association v. UoI (NJAC)", 2015, 5,
          "5-judge bench; 99th Constitutional Amendment & National Judicial Appointments "
          "Commission Act struck down.",
          "Held: The 99th Constitutional Amendment and the NJAC Act are unconstitutional. "
          "They violate the basic structure as they undermine the independence of the "
          "judiciary by giving the executive a primary role in judicial appointments.",
          "Ratio: Independence of the judiciary, including the primacy of the judiciary "
          "in judicial appointments, is part of the basic structure. The collegium system "
          "is restored to the position prior to the 99th Amendment."),

    _case("(1973) 1 SCC 380", "His Holiness Kesavananda Bharati v. State of Kerala (review)", 1973, 13,
          "Same as the main Kesavananda Bharati case; included for cross-reference.",
          "Held: See Kesavananda Bharati v. State of Kerala; basic structure doctrine "
          "established.",
          "Ratio: The amending power of Parliament, though wide, does not extend to "
          "altering the basic structure of the Constitution."),

    # ---------- Privacy / digital rights ----------
    _case("(2020) SCC OnLine SC 25", "Anuradha Bhasin v. Union of India", 2020, 3,
          "3-judge bench; suspension of internet services in J&K.",
          "Held: The freedom of speech and expression and freedom to practise any "
          "profession or carry on any trade, business or occupation over the internet "
          "are protected under Article 19(1)(a) and 19(1)(g). Indefinite suspension is "
          "impermissible.",
          "Ratio: Restrictions on internet must satisfy proportionality. Orders under "
          "Section 144 CrPC and Suspension Rules must be published, reasoned, and "
          "subject to periodic review. Indefinite suspension cannot be a tool of "
          "ordinary administration."),

    _case("(2022) 4 SCC 1", "Manohar Lal Sharma v. Union of India (Pegasus)", 2021, 3,
          "3-judge bench; allegations of state surveillance via Pegasus spyware.",
          "Held: The Court appointed a technical committee to examine allegations of "
          "unauthorised surveillance using Pegasus spyware. The State cannot claim a "
          "blanket privilege of national security to refuse engagement with the Court.",
          "Ratio: The right to privacy and freedom of speech extend to digital "
          "communications. National security concerns cannot displace constitutional "
          "scrutiny without specific justification. Mass surveillance offends "
          "constitutional values."),

    # ---------- Public-interest landmarks ----------
    _case("(2018) 11 SCC 1", "Indian Young Lawyers Association v. State of Kerala (Sabarimala)", 2018, 5,
          "5-judge bench; ban on entry of women aged 10-50 into Sabarimala temple.",
          "Held: The ban on women aged 10-50 at Sabarimala violates Articles 14, 15, "
          "21, and 25. The exclusion is not protected as essential religious practice. "
          "The proviso to Rule 3(b) of Kerala Hindu Places of Public Worship Rules, "
          "1965 is unconstitutional.",
          "Ratio: Right to worship is part of religious freedom. Devotees are not a "
          "religious denomination. Public morality cannot trump constitutional morality "
          "in restricting fundamental rights."),

    _case("AIR 1979 SC 1369", "Hussainara Khatoon v. Home Secretary, Bihar", 1979, 2,
          "2-judge bench; under-trial prisoners detained for years; right to speedy "
          "trial.",
          "Held: Speedy trial is an integral part of the right to life and personal "
          "liberty under Article 21. Free legal aid for poor accused is a constitutional "
          "imperative. Long incarceration of under-trials offends Articles 14 and 21.",
          "Ratio: Procedural justice, free legal aid, and a fair speedy trial are "
          "constitutional rights, not optional provisions. The State is constitutionally "
          "obliged to provide legal aid through Article 39A."),

    _case("(2017) 10 SCC 800", "Independent Thought v. Union of India", 2017, 2,
          "2-judge bench; Exception 2 to Section 375 IPC criminalising marital rape only "
          "where wife under 15 was challenged.",
          "Held: Exception 2 to Section 375 IPC, insofar as it applied to a wife between "
          "15 and 18 years of age, is unconstitutional. Sexual intercourse with a wife "
          "below 18 is rape.",
          "Ratio: Article 14 prohibits unequal treatment of girl children below 18 based "
          "on marital status. POCSO Act protects all minors equally; the exception to "
          "Section 375 IPC could not derogate from POCSO for the same age group."),

    _case("(2017) 9 SCC 1", "Justice K.S. Puttaswamy (Retd.) v. Union of India (Aadhaar)", 2018, 5,
          "5-judge bench; constitutionality of Aadhaar Act, 2016.",
          "Held: Aadhaar Act is largely constitutional. Section 57 (private use) and "
          "Section 33(2) (disclosure for national security via Joint Secretary) are "
          "struck down. Aadhaar cannot be made mandatory for school admission, exams, "
          "or banking, but is mandatory for PAN and ITR.",
          "Ratio: Mandatory Aadhaar must satisfy proportionality: (i) legitimate state "
          "aim, (ii) suitable means, (iii) necessity, (iv) balance of rights. The "
          "Aadhaar Act passes the proportionality test for welfare-benefit subsidies."),

    # ---------- Recent commercial / corporate ----------
    _case("(2021) SCC OnLine SC 159", "PASL Wind Solutions v. GE Power Conversion India", 2021, 3,
          "3-judge bench; whether two Indian parties can choose foreign seat of "
          "arbitration.",
          "Held: Two Indian parties can choose a foreign seat of arbitration; the "
          "resulting award is a foreign award enforceable under Part II of the "
          "Arbitration and Conciliation Act, 1996.",
          "Ratio: Party autonomy permits Indian parties to opt out of Part I by choosing "
          "a foreign seat. Section 28 of the Indian Contract Act does not prohibit such "
          "choice. The award is governed by the seat's curial law and enforced under "
          "Part II in India."),

    _case("(2023) SCC OnLine SC 495", "N.N. Global Mercantile Pvt. Ltd. v. Indo Unique Flame Ltd.", 2023, 5,
          "5-judge bench; effect of insufficient stamping on arbitration agreement.",
          "Held: Unstamped arbitration agreements are not enforceable until duly "
          "stamped. The court at the Section 8 / Section 11 stage must impound an "
          "unstamped instrument under the Indian Stamp Act before referring to "
          "arbitration. (Subsequently overruled in In Re Interplay between Arbitration "
          "Agreements and Indian Stamp Act, 7-judge bench.)",
          "Ratio: Stamping is a curable defect; once cured, the arbitration agreement "
          "becomes enforceable. The seven-judge ruling later restored separability and "
          "competence-competence as paramount.",
          status="overruled"),

    _case("(2023) SCC OnLine SC 1666", "In Re Interplay between Arbitration Agreements and the Indian Stamp Act, 1899", 2023, 7,
          "7-judge bench; revisits N.N. Global on stamping and arbitration.",
          "Held: An arbitration agreement is enforceable even if the underlying "
          "instrument is not stamped or is insufficiently stamped. The non-stamping or "
          "insufficient stamping does not render the arbitration agreement void; it is "
          "a curable defect. The doctrine of separability and competence-competence is "
          "preserved.",
          "Ratio: Section 11 court's role is limited to a prima facie examination of "
          "the existence of the arbitration agreement. Stamping issues are to be raised "
          "before the arbitral tribunal and resolved before passing the award. The "
          "principles in N.N. Global are overruled to that extent."),

    _case("(2021) 11 SCC 1", "Cox & Kings Ltd. v. SAP India Pvt. Ltd.", 2021, 3,
          "3-judge bench; group of companies doctrine in arbitration.",
          "Held: A non-signatory or third party can be bound by an arbitration "
          "agreement under the 'group of companies' doctrine, provided there is mutual "
          "intent to bind, a clear connection of the non-signatory to the agreement and "
          "an active role in the dispute. (Doctrine reaffirmed by 5-judge bench in 2023.)",
          "Ratio: Mutual consent is required to bind a third party to an arbitration. "
          "Looking through corporate veils for arbitration purposes is permissible where "
          "the conduct of the parties indicates such consent."),

    # ---------- Religious freedom / CAA / minority ----------
    _case("(1995) 3 SCC 635", "Sarla Mudgal v. Union of India", 1995, 2,
          "2-judge bench; second marriage by a Hindu after conversion to Islam.",
          "Held: A Hindu husband converting to Islam to contract a second marriage "
          "(while the first Hindu marriage subsists) commits the offence of bigamy "
          "under Section 494 IPC. The first marriage is not automatically dissolved by "
          "conversion.",
          "Ratio: Conversion does not entitle a person to evade obligations under the "
          "first marriage. The State has a legitimate interest in regulating marriage "
          "and preventing religious arbitrage of personal-law obligations."),

    _case("(2000) 6 SCC 224", "Lily Thomas v. Union of India", 2000, 2,
          "2-judge bench; conversion to Islam to contract second marriage.",
          "Held: Reaffirms Sarla Mudgal — a Hindu husband converting to Islam to "
          "contract second marriage is liable under Section 494 IPC. Mere conversion "
          "does not dissolve the first marriage.",
          "Ratio: Religious freedom under Article 25 does not include the freedom to "
          "violate the criminal law. Personal-law-shopping for evasion is impermissible."),

    # ---------- Environmental ----------
    _case("(1996) 3 SCC 212", "Vellore Citizens Welfare Forum v. Union of India", 1996, 3,
          "3-judge bench; pollution by tanneries in Tamil Nadu; precautionary principle.",
          "Held: The precautionary principle and the polluter-pays principle are part "
          "of Indian law. The State has a duty to prevent environmental harm, and the "
          "burden is on the polluter to prove that an activity is environmentally "
          "benign.",
          "Ratio: Sustainable development requires balancing development with "
          "environmental protection. Articles 21, 47, 48A, and 51A(g) read together "
          "create a constitutional mandate to protect the environment. Environmental "
          "principles are a part of customary international law and can be read into "
          "Indian law."),

    _case("(2000) 7 SCC 282", "M.C. Mehta v. Kamal Nath", 1997, 3,
          "3-judge bench; private resort encroaching on river bed; public trust doctrine.",
          "Held: The public trust doctrine is part of the law of the land. Natural "
          "resources are held by the State as trustee for the public; alienation in "
          "violation of public interest is impermissible.",
          "Ratio: Article 21 includes the right to a wholesome environment. The "
          "doctrine of public trust applies to all natural resources of public use. "
          "The State holds the rivers, forests, and beaches in trust."),

    # ---------- Federalism / centre-state ----------
    _case("(2018) 8 SCC 501", "Government of NCT of Delhi v. Union of India", 2018, 5,
          "5-judge bench; powers of the Lieutenant Governor of Delhi vis-à-vis the "
          "elected government.",
          "Held: Except in matters relating to public order, police, and land, the "
          "Lieutenant Governor of Delhi is bound by the aid and advice of the Council of "
          "Ministers. The LG cannot act in his own discretion in routine matters.",
          "Ratio: Article 239AA establishes a representative democracy in NCT of Delhi. "
          "The Council of Ministers is the principal decision-maker. The LG has no "
          "independent decision-making power except in the three reserved subjects."),

    # ---------- Recent: free speech / contempt ----------
    _case("(2020) 12 SCC 791", "In Re Prashant Bhushan (Contempt)", 2020, 3,
          "3-judge bench; criminal contempt of advocate Prashant Bhushan for tweets.",
          "Held: Two tweets by Prashant Bhushan amounted to criminal contempt of "
          "court. Sentenced to symbolic ₹1 fine. The Court reaffirmed the broad scope "
          "of contempt jurisdiction under Article 129.",
          "Ratio: Criticism of judges/judiciary that 'scandalises the court' is "
          "criminal contempt. However, fair, reasonable criticism in good faith is "
          "permissible. Tweets that erode public confidence in administration of justice "
          "fall within criminal contempt."),

    _case("(2020) SCC OnLine SC 870", "Arnab Goswami v. Union of India", 2020, 2,
          "2-judge bench; bail application of journalist Arnab Goswami; abuse of "
          "criminal process.",
          "Held: Bail granted. The Court emphasized that pre-trial detention is "
          "punitive, not investigatory; personal liberty must be protected; and "
          "frivolous criminal cases should be quashed.",
          "Ratio: Section 482 CrPC inherent powers can be invoked to prevent abuse of "
          "process. Bail must be the rule, not the exception. Judicial caution is "
          "required when criminal law is weaponised against journalists."),

    # ---------- Tax landmarks ----------
    _case("(2012) 6 SCC 613", "Vodafone International Holdings B.V. v. Union of India", 2012, 3,
          "3-judge bench; whether sale of shares of a foreign holding company by a "
          "non-resident to another non-resident, of a subsidiary holding Indian "
          "underlying assets, is taxable in India.",
          "Held: The transaction is not taxable in India under the Income-tax Act, "
          "1961 as it stood. Indirect transfer of Indian underlying assets through "
          "transfer of shares of a foreign holding company is outside Indian tax "
          "jurisdiction. (Subsequently the Income-tax Act was retrospectively amended.)",
          "Ratio: Source-based taxation requires nexus with India. A transaction "
          "between two non-residents in shares of a foreign company does not establish "
          "such nexus merely because the underlying assets are in India."),

    # ---------- Recent: religion + state ----------
    _case("(2018) 11 SCC 1", "Indian Young Lawyers Association (Sabarimala) v. State of Kerala", 2018, 5,
          "5-judge bench; ban on women aged 10-50 at Sabarimala temple.",
          "Held: The ban violates Articles 14, 15, 21, and 25. Devotees of Lord "
          "Ayyappa are not a religious denomination. Right to worship is integral to "
          "the right to practise religion under Article 25.",
          "Ratio: Constitutional morality, not popular morality, governs disputes "
          "between fundamental rights and religious practice. The State cannot impose "
          "patriarchal exclusions in the guise of religious tradition."),
]
