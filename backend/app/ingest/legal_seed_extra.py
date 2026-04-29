"""Expanded seed: covers the most common real-user query patterns we saw refuse
in the audit (criminal intimidation, harassment, theft, hurt, FIR / arrest /
bail, summary suit, Limitation Act, Specific Relief, GST registration, IT Act
cybercrime, key Constitution articles).

Authoritative text condensed from India Code (https://indiacode.nic.in) and
Ministry of Law publications. We keep each chunk short and faithful to the
operative language so the verifier can quote-match.
"""
from __future__ import annotations

from typing import Any


EXTRA_SEED_DOCS: list[dict[str, Any]] = [
    # ---- BNS continued ----
    {
        "doc": {
            "source_type": "central_statute", "title": "Bharatiya Nyaya Sanhita, 2023",
            "short_citation": "BNS", "long_citation": "Bharatiya Nyaya Sanhita, 2023",
            "effective_from": "2024-07-01", "status": "in_force",
        },
        "chunks": [
            {"hierarchy_path": ["BNS", "Chapter XIX", "Section 351"],
             "chunk_type": "section", "section_number": "351",
             "text": "Section 351. Criminal intimidation.—(1) Whoever threatens another by any means whatever with any injury to his person, reputation or property, or to the person or reputation of any one in whom that person is interested, with intent to cause alarm to that person, or to cause that person to do any act which he is not legally bound to do, or to omit to do any act which that person is legally entitled to do, as the means of avoiding the execution of such threat, commits criminal intimidation. (2) Whoever commits the offence of criminal intimidation shall be punished with imprisonment of either description for a term which may extend to two years, or with fine, or with both. (3) Threat of injury causing death or grievous hurt is punishable with imprisonment up to seven years.",
             "metadata": {"act_short": "BNS"}},
            {"hierarchy_path": ["BNS", "Chapter V", "Section 75"],
             "chunk_type": "section", "section_number": "75",
             "text": "Section 75. Sexual harassment.—A man committing physical contact and advances involving unwelcome and explicit sexual overtures; a demand or request for sexual favours; showing pornography against the will of a woman; or making sexually coloured remarks shall be punished with rigorous imprisonment which may extend to three years, or with fine, or with both. Showing pornography or sexually coloured remarks attract imprisonment up to one year.",
             "metadata": {"act_short": "BNS"}},
            {"hierarchy_path": ["BNS", "Chapter V", "Section 78"],
             "chunk_type": "section", "section_number": "78",
             "text": "Section 78. Stalking.—(1) Any man who follows a woman and contacts, or attempts to contact such woman to foster personal interaction repeatedly despite a clear indication of disinterest by such woman; or monitors the use by a woman of the internet, email or any other form of electronic communication, commits the offence of stalking. (2) Whoever commits the offence of stalking shall be punished on a first conviction with imprisonment of either description for a term which may extend to three years, and on second or subsequent conviction up to five years, and shall also be liable to fine.",
             "metadata": {"act_short": "BNS"}},
            {"hierarchy_path": ["BNS", "Chapter XVII", "Section 303"],
             "chunk_type": "section", "section_number": "303",
             "text": "Section 303. Theft.—(1) Whoever, intending to take dishonestly any movable property out of the possession of any person without that person's consent, moves that property in order to such taking, is said to commit theft. (2) Whoever commits theft shall be punished with imprisonment of either description for a term which may extend to three years, or with fine, or with both, and for a second or subsequent conviction with imprisonment which shall not be less than one year and may extend to five years.",
             "metadata": {"act_short": "BNS"}},
            {"hierarchy_path": ["BNS", "Chapter VI", "Section 115"],
             "chunk_type": "section", "section_number": "115",
             "text": "Section 115. Voluntarily causing hurt.—(1) Whoever does any act with the intention of thereby causing hurt to any person, or with the knowledge that he is likely thereby to cause hurt to any person, and does thereby cause hurt to any person, is said voluntarily to cause hurt. (2) Whoever, except in cases provided for in section 122, voluntarily causes hurt, shall be punished with imprisonment of either description for a term which may extend to one year, or with fine which may extend to ten thousand rupees, or with both.",
             "metadata": {"act_short": "BNS"}},
            {"hierarchy_path": ["BNS", "Chapter XVII", "Section 308"],
             "chunk_type": "section", "section_number": "308",
             "text": "Section 308. Extortion.—(1) Whoever intentionally puts any person in fear of any injury to that person or to any other, and thereby dishonestly induces the person so put in fear to deliver to any person any property, valuable security, or anything signed or sealed which may be converted into a valuable security, commits extortion. (2) Whoever commits extortion shall be punished with imprisonment of either description for a term which may extend to seven years, or with fine, or with both.",
             "metadata": {"act_short": "BNS"}},
            {"hierarchy_path": ["BNS", "Chapter XIV", "Section 270"],
             "chunk_type": "section", "section_number": "270",
             "text": "Section 270. Public nuisance.—A person is guilty of a public nuisance who does any act or is guilty of an illegal omission which causes any common injury, danger or annoyance to the public or to the people in general who dwell or occupy property in the vicinity, or which must necessarily cause injury, obstruction, danger or annoyance to persons who may have occasion to use any public right.",
             "metadata": {"act_short": "BNS"}},
            {"hierarchy_path": ["BNS", "Chapter XIV", "Section 292"],
             "chunk_type": "section", "section_number": "292",
             "text": "Section 292. Punishment for public nuisance.—Every person who commits a public nuisance, in any case for which no special punishment is provided in this Sanhita, shall be punished with fine which may extend to one thousand rupees. Continued nuisance after injunction may attract simple imprisonment up to six months or fine, or both.",
             "metadata": {"act_short": "BNS"}},
        ],
    },

    # ---- BNSS (Procedure) ----
    {
        "doc": {
            "source_type": "central_statute", "title": "Bharatiya Nagarik Suraksha Sanhita, 2023",
            "short_citation": "BNSS", "long_citation": "Bharatiya Nagarik Suraksha Sanhita, 2023",
            "effective_from": "2024-07-01", "status": "in_force",
        },
        "chunks": [
            {"hierarchy_path": ["BNSS", "Chapter XII", "Section 173"],
             "chunk_type": "section", "section_number": "173",
             "text": "Section 173. Information in cognizable cases.—(1) Every information relating to the commission of a cognizable offence, irrespective of the area where the offence is committed, may be given orally or by electronic communication to an officer in charge of a police station and if given orally, shall be reduced to writing by him. The substance shall be entered in a book in such form as the State Government may prescribe. (3) The officer in charge of a police station shall, on receipt of information of a cognizable offence, register the FIR. The informant is entitled to a copy of the FIR free of cost.",
             "metadata": {"act_short": "BNSS"}},
            {"hierarchy_path": ["BNSS", "Chapter XXXV", "Section 482"],
             "chunk_type": "section", "section_number": "482",
             "text": "Section 482. Direction for grant of bail to person apprehending arrest.—(1) When any person has reason to believe that he may be arrested on accusation of having committed a non-bailable offence, he may apply to the High Court or the Court of Session for a direction under this section that in the event of such arrest he shall be released on bail. The Court may impose conditions: that the person shall make himself available for interrogation, shall not directly or indirectly make any inducement, threat or promise to dissuade evidence, shall not leave India without permission, and other conditions as the Court may deem fit.",
             "metadata": {"act_short": "BNSS"}},
            {"hierarchy_path": ["BNSS", "Chapter V", "Section 35"],
             "chunk_type": "section", "section_number": "35",
             "text": "Section 35. When police may arrest without warrant.—Any police officer may without an order from a Magistrate and without a warrant arrest any person who commits, in the presence of a police officer, a cognizable offence; or against whom a reasonable complaint has been made, or credible information has been received, or a reasonable suspicion exists that he has committed a cognizable offence punishable with imprisonment for a term which may be less than seven years, subject to conditions that the police officer is satisfied that arrest is necessary to prevent further offences or proper investigation.",
             "metadata": {"act_short": "BNSS"}},
            {"hierarchy_path": ["BNSS", "Chapter XXXV", "Section 480"],
             "chunk_type": "section", "section_number": "480",
             "text": "Section 480. When bail may be taken in case of non-bailable offence.—(1) When any person accused of, or suspected of, the commission of any non-bailable offence is arrested or detained without warrant by an officer in charge of a police station, or appears or is brought before a Court other than the High Court or Court of Session, he may be released on bail, subject to the proviso that such person shall not be so released if there appear reasonable grounds for believing that he has been guilty of an offence punishable with death or imprisonment for life.",
             "metadata": {"act_short": "BNSS"}},
        ],
    },

    # ---- IT Act 2000 (cybercrime) ----
    {
        "doc": {
            "source_type": "central_statute", "title": "Information Technology Act, 2000",
            "short_citation": "IT Act", "long_citation": "Information Technology Act, 2000",
            "status": "in_force",
        },
        "chunks": [
            {"hierarchy_path": ["IT Act", "Chapter XI", "Section 66C"],
             "chunk_type": "section", "section_number": "66C",
             "text": "Section 66C. Punishment for identity theft.—Whoever, fraudulently or dishonestly makes use of the electronic signature, password or any other unique identification feature of any other person, shall be punished with imprisonment of either description for a term which may extend to three years and shall also be liable to fine which may extend to rupees one lakh.",
             "metadata": {"act_short": "IT Act"}},
            {"hierarchy_path": ["IT Act", "Chapter XI", "Section 66D"],
             "chunk_type": "section", "section_number": "66D",
             "text": "Section 66D. Punishment for cheating by personation by using computer resource.—Whoever, by means for any communication device or computer resource cheats by personation, shall be punished with imprisonment of either description for a term which may extend to three years and shall also be liable to fine which may extend to one lakh rupees.",
             "metadata": {"act_short": "IT Act"}},
            {"hierarchy_path": ["IT Act", "Chapter XI", "Section 67"],
             "chunk_type": "section", "section_number": "67",
             "text": "Section 67. Punishment for publishing or transmitting obscene material in electronic form.—Whoever publishes or transmits or causes to be published or transmitted in the electronic form, any material which is lascivious or appeals to the prurient interest, shall be punished on first conviction with imprisonment of either description for a term which may extend to three years and with fine which may extend to five lakh rupees, and on second or subsequent conviction up to five years and with fine up to ten lakh rupees.",
             "metadata": {"act_short": "IT Act"}},
        ],
    },

    # ---- Constitution: more articles ----
    {
        "doc": {
            "source_type": "constitution", "title": "Constitution of India",
            "short_citation": "Constitution",
            "long_citation": "Constitution of India",
            "status": "in_force",
        },
        "chunks": [
            {"hierarchy_path": ["Constitution", "Part III", "Article 19"],
             "chunk_type": "article", "section_number": "19",
             "text": "Article 19. Protection of certain rights regarding freedom of speech, etc.—(1) All citizens shall have the right—(a) to freedom of speech and expression; (b) to assemble peaceably and without arms; (c) to form associations or unions or co-operative societies; (d) to move freely throughout the territory of India; (e) to reside and settle in any part of the territory of India; (g) to practise any profession, or to carry on any occupation, trade or business. (2) Reasonable restrictions may be imposed in the interests of the sovereignty and integrity of India, the security of the State, friendly relations with foreign States, public order, decency or morality, contempt of court, defamation or incitement to an offence.",
             "metadata": {}},
            {"hierarchy_path": ["Constitution", "Part III", "Article 32"],
             "chunk_type": "article", "section_number": "32",
             "text": "Article 32. Remedies for enforcement of rights conferred by this Part.—(1) The right to move the Supreme Court by appropriate proceedings for the enforcement of the rights conferred by this Part is guaranteed. (2) The Supreme Court shall have power to issue directions or orders or writs, including writs in the nature of habeas corpus, mandamus, prohibition, quo warranto and certiorari, whichever may be appropriate, for the enforcement of any of the rights conferred by this Part.",
             "metadata": {}},
            {"hierarchy_path": ["Constitution", "Part III", "Article 226"],
             "chunk_type": "article", "section_number": "226",
             "text": "Article 226. Power of High Courts to issue certain writs.—Notwithstanding anything in article 32, every High Court shall have power, throughout the territories in relation to which it exercises jurisdiction, to issue to any person or authority, including in appropriate cases any Government, within those territories directions, orders or writs, including writs in the nature of habeas corpus, mandamus, prohibition, quo warranto and certiorari, or any of them, for the enforcement of any of the rights conferred by Part III and for any other purpose.",
             "metadata": {}},
        ],
    },

    # ---- Specific Relief Act 1963 ----
    {
        "doc": {
            "source_type": "central_statute", "title": "Specific Relief Act, 1963",
            "short_citation": "Specific Relief Act",
            "long_citation": "Specific Relief Act, 1963",
            "status": "in_force",
        },
        "chunks": [
            {"hierarchy_path": ["Specific Relief Act", "Section 10"],
             "chunk_type": "section", "section_number": "10",
             "text": "Section 10. Specific performance in respect of contracts.—The specific performance of a contract shall be enforced by the court subject to the provisions contained in sub-section (2) of section 11, section 14 and section 16. The court shall, while granting specific performance, take into account whether the contract is one in which compensation in money would be inadequate.",
             "metadata": {"act_short": "Specific Relief Act"}},
            {"hierarchy_path": ["Specific Relief Act", "Section 38"],
             "chunk_type": "section", "section_number": "38",
             "text": "Section 38. Perpetual injunction when granted.—(1) Subject to the other provisions contained in or referred to by this Chapter, a perpetual injunction may be granted to the plaintiff to prevent the breach of an obligation existing in his favour, whether expressly or by implication.",
             "metadata": {"act_short": "Specific Relief Act"}},
        ],
    },

    # ---- CPC (summary suit, recovery of money) ----
    {
        "doc": {
            "source_type": "central_statute", "title": "Code of Civil Procedure, 1908",
            "short_citation": "CPC",
            "long_citation": "Code of Civil Procedure, 1908",
            "status": "in_force",
        },
        "chunks": [
            {"hierarchy_path": ["CPC", "Order XXXVII", "Rule 1-2 (Summary Suit)"],
             "chunk_type": "section", "section_number": "37",
             "text": "Order XXXVII (Summary Procedure).—(1) Summary procedure applies to suits upon bills of exchange, hundies and promissory notes; suits in which the plaintiff seeks only to recover a debt or liquidated demand in money payable by the defendant arising on a written contract, or on an enactment where the sum sought to be recovered is a fixed sum of money, or on a guarantee. (2) Such suit shall be instituted by presenting a plaint which shall, in addition to the particulars required by Order VI Rule 4, contain a specific averment that the suit is filed under this Order and that no relief which does not fall within the ambit of this Order is claimed.",
             "metadata": {"act_short": "CPC"}},
        ],
    },

    # ---- Limitation Act ----
    {
        "doc": {
            "source_type": "central_statute", "title": "Limitation Act, 1963",
            "short_citation": "Limitation Act",
            "long_citation": "Limitation Act, 1963",
            "status": "in_force",
        },
        "chunks": [
            {"hierarchy_path": ["Limitation Act", "First Schedule", "Article 18 (Recovery of money)"],
             "chunk_type": "section", "section_number": "18",
             "text": "Article 18. For money payable for money lent.—Three years from when the loan is made (or from the date of any subsequent acknowledgment in writing under Section 18). For money payable for an account stated, three years from the date of the stated account.",
             "metadata": {"act_short": "Limitation Act"}},
            {"hierarchy_path": ["Limitation Act", "First Schedule", "Article 21"],
             "chunk_type": "section", "section_number": "21",
             "text": "Article 21. For money lent under an agreement that it shall be payable on demand.—Three years from the date of the loan.",
             "metadata": {"act_short": "Limitation Act"}},
        ],
    },

    # ---- Negotiable Instruments Act §138 limitation ----
    {
        "doc": {
            "source_type": "central_statute", "title": "Negotiable Instruments Act, 1881",
            "short_citation": "NI Act",
            "long_citation": "Negotiable Instruments Act, 1881",
            "status": "in_force",
        },
        "chunks": [
            {"hierarchy_path": ["NI Act", "Chapter XVII", "Section 142 (Cognizance of offences)"],
             "chunk_type": "section", "section_number": "142",
             "text": "Section 142. Cognizance of offences.—(1) Notwithstanding anything contained in the Code of Criminal Procedure, no court shall take cognizance of any offence punishable under section 138 except upon a complaint, in writing, made by the payee or, as the case may be, the holder in due course of the cheque; such complaint is made within one month of the date on which the cause-of-action arises under clause (c) of the proviso to section 138. The cause of action arises only when (a) the cheque is dishonoured, (b) statutory notice of demand is given within 30 days of dishonour, and (c) the drawer fails to pay within 15 days of receiving the notice.",
             "metadata": {"act_short": "NI Act"}},
        ],
    },

    # ---- Consumer Protection Act 2019: deficiency of service ----
    {
        "doc": {
            "source_type": "central_statute", "title": "Consumer Protection Act, 2019",
            "short_citation": "CPA 2019",
            "long_citation": "Consumer Protection Act, 2019",
            "status": "in_force",
        },
        "chunks": [
            {"hierarchy_path": ["CPA 2019", "Chapter IV", "Section 35"],
             "chunk_type": "section", "section_number": "35",
             "text": "Section 35. Manner in which complaint shall be made.—(1) A complaint, in relation to any goods sold or delivered or any service provided or agreed to be provided, may be filed with a District Commission by—(a) the consumer to whom such goods are sold or delivered or service is rendered or agreed to be rendered; (b) any recognised consumer association, whether the consumer to whom such goods or service was sold/rendered is a member or not; (c) one or more consumers having same interest; (d) the Central Government, the Central Authority, or the State Government. (2) Every complaint may be filed by electronic means.",
             "metadata": {"act_short": "CPA 2019"}},
        ],
    },

    # ---- POSH Act 2013 ----
    {
        "doc": {
            "source_type": "central_statute", "title": "Sexual Harassment of Women at Workplace (Prevention, Prohibition and Redressal) Act, 2013",
            "short_citation": "POSH Act",
            "long_citation": "Sexual Harassment of Women at Workplace (Prevention, Prohibition and Redressal) Act, 2013",
            "status": "in_force",
        },
        "chunks": [
            {"hierarchy_path": ["POSH Act", "Chapter II", "Section 4 (Internal Committee)"],
             "chunk_type": "section", "section_number": "4",
             "text": "Section 4. Constitution of Internal Committee.—(1) Every employer of a workplace shall, by an order in writing, constitute an Internal Committee. (2) The Internal Committee shall consist of a Presiding Officer who shall be a woman employed at a senior level; not less than two Members from amongst employees committed to the cause of women or who have had experience in social work; and one member from amongst non-governmental organisations or associations committed to the cause of women.",
             "metadata": {"act_short": "POSH Act"}},
        ],
    },

    # ---- Indian Contract Act extras ----
    {
        "doc": {
            "source_type": "central_statute", "title": "Indian Contract Act, 1872",
            "short_citation": "Contract Act",
            "long_citation": "Indian Contract Act, 1872",
            "status": "in_force",
        },
        "chunks": [
            {"hierarchy_path": ["Contract Act", "Chapter II", "Section 23"],
             "chunk_type": "section", "section_number": "23",
             "text": "Section 23. What considerations and objects are lawful, and what not.—The consideration or object of an agreement is lawful, unless—it is forbidden by law; or is of such a nature that, if permitted, it would defeat the provisions of any law; or is fraudulent; or involves or implies injury to the person or property of another; or the Court regards it as immoral, or opposed to public policy.",
             "metadata": {"act_short": "Contract Act"}},
        ],
    },

    # ---- CGST Act registration threshold ----
    {
        "doc": {
            "source_type": "central_statute", "title": "Central Goods and Services Tax Act, 2017",
            "short_citation": "CGST Act",
            "long_citation": "Central Goods and Services Tax Act, 2017",
            "status": "in_force",
        },
        "chunks": [
            {"hierarchy_path": ["CGST Act", "Chapter VI", "Section 22"],
             "chunk_type": "section", "section_number": "22",
             "text": "Section 22. Persons liable for registration.—(1) Every supplier shall be liable to be registered under this Act in the State or Union territory, other than special category States, from where he makes a taxable supply of goods or services or both, if his aggregate turnover in a financial year exceeds twenty lakh rupees: Provided that where such person makes taxable supplies of goods or services or both from any of the special category States, he shall be liable to be registered if his aggregate turnover in a financial year exceeds ten lakh rupees. The threshold for exclusive supply of goods (other than ice cream, pan masala, tobacco, fly ash) was raised to forty lakh rupees by Notification 10/2019-Central Tax.",
             "metadata": {"act_short": "CGST Act"}},
        ],
    },

    # ---- Maharashtra Rent Control (state law often asked about) ----
    {
        "doc": {
            "source_type": "state_statute", "title": "Maharashtra Rent Control Act, 1999",
            "jurisdiction": "MH",
            "short_citation": "MRCA-1999",
            "long_citation": "Maharashtra Rent Control Act, 1999",
            "status": "in_force",
        },
        "chunks": [
            {"hierarchy_path": ["MRCA 1999", "Chapter II", "Section 7 (Standard Rent)"],
             "chunk_type": "section", "section_number": "7",
             "text": "Section 7. Definition of standard rent.—Standard rent in relation to any premises means the rent at which the premises were let on the date of commencement of this Act, with such increases as are permitted by the Act. The Act caps annual rent increase at four per cent unless tenant agrees otherwise or the increase is for permitted improvements. A landlord cannot unilaterally raise rent without the procedure prescribed in section 11.",
             "metadata": {"state": "MH", "act_short": "MRCA-1999"}},
            {"hierarchy_path": ["MRCA 1999", "Chapter III", "Section 16 (Grounds for Eviction)"],
             "chunk_type": "section", "section_number": "16",
             "text": "Section 16. When tenant may be evicted.—No suit for recovery of possession shall be instituted against a tenant on any ground other than: (a) the tenant has been guilty of conduct which is a nuisance or annoyance; (b) the tenant has not paid the standard rent and permitted increases for fifteen days after notice; (c) the tenant has unlawfully sublet, assigned or transferred the premises; (d) the premises are reasonably and bona fide required by the landlord. Notice under section 106 of the Transfer of Property Act is mandatory.",
             "metadata": {"state": "MH", "act_short": "MRCA-1999"}},
        ],
    },
]
