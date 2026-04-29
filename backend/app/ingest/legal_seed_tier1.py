"""Tier-1 seed: high-priority hand-curated sections.

Each chunk is condensed faithfully from publicly available bare-act text on
indiacode.nic.in, legislative.gov.in, or the relevant ministry's site.
We keep operative language so quote-checks succeed, but trim sub-clauses
not needed for general guidance.

Adding more is mechanical — append entries; re-run scripts/build_corpus.py.
"""
from __future__ import annotations

from typing import Any


TIER1_SEED_DOCS: list[dict[str, Any]] = [

    # ============= BSA =============
    {
        "doc": {
            "source_type": "central_statute", "title": "Bharatiya Sakshya Adhiniyam, 2023",
            "short_citation": "BSA", "long_citation": "Bharatiya Sakshya Adhiniyam, 2023",
            "effective_from": "2024-07-01", "status": "in_force",
        },
        "chunks": [
            {"hierarchy_path": ["BSA", "Section 63 (Electronic records)"],
             "chunk_type": "section", "section_number": "63",
             "text": "Section 63. Admissibility of electronic records.—Notwithstanding anything contained in this Adhiniyam, any information contained in an electronic record which is printed on paper, stored, recorded or copied in optical or magnetic media or semiconductor memory which is produced by a computer or any communication device or otherwise shall be deemed to be also a document, if conditions as to (a) regular use, (b) ordinary course of activities, (c) proper functioning of the computer, and (d) accuracy of the reproduction are satisfied. A certificate identifying the electronic record and describing the manner of its production must accompany it.",
             "metadata": {"act_short": "BSA"}},
            {"hierarchy_path": ["BSA", "Section 23 (Confessions)"],
             "chunk_type": "section", "section_number": "23",
             "text": "Section 23. Confession to police officer.—(1) No confession made to a police officer shall be proved as against a person accused of any offence. (2) No confession made by any person whilst he is in the custody of a police officer, unless it be made in the immediate presence of a Magistrate, shall be proved as against such person. However, when any fact is deposed to as discovered in consequence of information received from a person accused of an offence, in the custody of a police officer, so much of such information, whether it amounts to a confession or not, as relates distinctly to the fact thereby discovered, may be proved.",
             "metadata": {"act_short": "BSA"}},
        ],
    },

    # ============= Companies Act, 2013 =============
    {
        "doc": {
            "source_type": "central_statute", "title": "Companies Act, 2013",
            "short_citation": "Companies Act",
            "long_citation": "Companies Act, 2013",
            "status": "in_force",
        },
        "chunks": [
            {"hierarchy_path": ["Companies Act", "Chapter II", "Section 2(20) Definition"],
             "chunk_type": "section", "section_number": "2(20)",
             "text": "Section 2(20). 'Company' means a company incorporated under this Act or under any previous company law. The Act recognises (a) Private company (limited or unlimited), (b) Public company, (c) One-Person Company (OPC), (d) Section 8 (non-profit) company, and (e) Producer company.",
             "metadata": {"act_short": "Companies Act"}},
            {"hierarchy_path": ["Companies Act", "Chapter VII", "Section 149 Board composition"],
             "chunk_type": "section", "section_number": "149",
             "text": "Section 149. Company to have Board of Directors.—(1) Every company shall have a Board consisting of individuals as directors. Minimum: three for public, two for private, one for OPC. Maximum fifteen, extendable by special resolution. (4) Every listed public company shall have at least one-third independent directors. (1A) Every prescribed class of company shall have at least one woman director.",
             "metadata": {"act_short": "Companies Act"}},
            {"hierarchy_path": ["Companies Act", "Chapter X", "Section 166 Director duties"],
             "chunk_type": "section", "section_number": "166",
             "text": "Section 166. Duties of directors.—(1) A director shall act in accordance with the articles of the company. (2) A director shall act in good faith in order to promote the objects of the company for the benefit of its members as a whole, and in the best interests of the company, its employees, the shareholders, the community and the protection of the environment. (3) A director shall exercise his duties with due and reasonable care, skill and diligence. (4) A director shall not involve in a situation in which he may have a direct or indirect interest that conflicts with the interest of the company. (5) A director shall not achieve undue gain or advantage. (6) A director shall not assign his office.",
             "metadata": {"act_short": "Companies Act"}},
        ],
    },

    # ============= Hindu Marriage Act, 1955 =============
    {
        "doc": {
            "source_type": "central_statute", "title": "Hindu Marriage Act, 1955",
            "short_citation": "HMA",
            "long_citation": "Hindu Marriage Act, 1955",
            "status": "in_force",
        },
        "chunks": [
            {"hierarchy_path": ["HMA", "Section 5 Conditions for valid marriage"],
             "chunk_type": "section", "section_number": "5",
             "text": "Section 5. Conditions for a Hindu marriage.—A marriage may be solemnized between any two Hindus, if the following conditions are fulfilled: (i) neither party has a spouse living at the time of the marriage; (ii) at the time of the marriage, neither party is incapable of giving valid consent due to unsoundness of mind or has been suffering from mental disorder of such a kind or to such an extent as to be unfit for marriage and the procreation of children; (iii) the bridegroom has completed the age of twenty-one years and the bride the age of eighteen years at the time of the marriage; (iv) the parties are not within the degrees of prohibited relationship unless the custom or usage governing each of them permits.",
             "metadata": {"act_short": "HMA"}},
            {"hierarchy_path": ["HMA", "Section 13 Divorce"],
             "chunk_type": "section", "section_number": "13",
             "text": "Section 13. Divorce.—(1) Any marriage may, on a petition presented by either the husband or the wife, be dissolved by a decree of divorce on the ground that the other party (i) has had voluntary sexual intercourse with any person other than his or her spouse; (ia) has treated the petitioner with cruelty; (ib) has deserted the petitioner for a continuous period of not less than two years; (ii) has ceased to be a Hindu by conversion; (iii) has been incurably of unsound mind; (iv) has been suffering from a virulent and incurable form of leprosy; (v) has been suffering from venereal disease in a communicable form; (vi) has renounced the world; (vii) has not been heard of as alive for seven years.",
             "metadata": {"act_short": "HMA"}},
            {"hierarchy_path": ["HMA", "Section 13B Mutual consent"],
             "chunk_type": "section", "section_number": "13B",
             "text": "Section 13B. Divorce by mutual consent.—(1) A petition for dissolution of marriage by a decree of divorce may be presented to the district court by both the parties to a marriage on the ground that they have been living separately for a period of one year or more, that they have not been able to live together and that they have mutually agreed that the marriage should be dissolved. (2) On the motion of both the parties made not earlier than six months and not later than eighteen months after the date of presentation of the petition, the court shall pass a decree of divorce. The Supreme Court has held the six-month cooling-off period is waivable in appropriate cases (Amardeep Singh v. Harveen Kaur, 2017).",
             "metadata": {"act_short": "HMA"}},
        ],
    },

    # ============= Domestic Violence Act, 2005 =============
    {
        "doc": {
            "source_type": "central_statute", "title": "Protection of Women from Domestic Violence Act, 2005",
            "short_citation": "PWDV Act",
            "long_citation": "Protection of Women from Domestic Violence Act, 2005",
            "status": "in_force",
        },
        "chunks": [
            {"hierarchy_path": ["PWDV", "Section 3 Definition of domestic violence"],
             "chunk_type": "section", "section_number": "3",
             "text": "Section 3. Definition of domestic violence.—For the purposes of this Act, any act, omission or commission or conduct of the respondent shall constitute domestic violence in case it (a) harms or injures or endangers the health, safety, life, limb or well-being, whether mental or physical, of the aggrieved person or tends to do so and includes causing physical abuse, sexual abuse, verbal and emotional abuse and economic abuse; (b) harasses, harms, injures or endangers the aggrieved person with a view to coerce her or any other person related to her to meet any unlawful demand for any dowry or other property; (c) has the effect of threatening the aggrieved person or any person related to her by any conduct mentioned in clause (a) or clause (b); or (d) otherwise injures or causes harm, whether physical or mental, to the aggrieved person.",
             "metadata": {"act_short": "PWDV Act"}},
            {"hierarchy_path": ["PWDV", "Section 12 Application to Magistrate"],
             "chunk_type": "section", "section_number": "12",
             "text": "Section 12. Application to Magistrate.—(1) An aggrieved person or a Protection Officer or any other person on behalf of the aggrieved person may present an application to the Magistrate seeking one or more reliefs under this Act. The Magistrate shall, before passing any order on such application, take into consideration any domestic incident report received from the Protection Officer or the service provider. (5) The Magistrate shall endeavour to dispose of every application made under sub-section (1) within a period of sixty days from the date of its first hearing.",
             "metadata": {"act_short": "PWDV Act"}},
        ],
    },

    # ============= RTI Act 2005 =============
    {
        "doc": {
            "source_type": "central_statute", "title": "Right to Information Act, 2005",
            "short_citation": "RTI Act",
            "long_citation": "Right to Information Act, 2005",
            "status": "in_force",
        },
        "chunks": [
            {"hierarchy_path": ["RTI Act", "Section 6 Request for information"],
             "chunk_type": "section", "section_number": "6",
             "text": "Section 6. Request for obtaining information.—(1) A person who desires to obtain any information under this Act, shall make a request in writing or through electronic means in English or Hindi or in the official language of the area in which the application is being made, accompanying such fee as may be prescribed, to (a) the Central Public Information Officer or State Public Information Officer; (b) the Central Assistant Public Information Officer or State Assistant PIO. (2) An applicant making request for information shall not be required to give any reason for requesting the information or any other personal details except those that may be necessary for contacting him.",
             "metadata": {"act_short": "RTI Act"}},
            {"hierarchy_path": ["RTI Act", "Section 7 Time limit"],
             "chunk_type": "section", "section_number": "7",
             "text": "Section 7. Disposal of request.—(1) Subject to the proviso to sub-section (2) of section 5 or the proviso to sub-section (3) of section 6, the Central Public Information Officer or State Public Information Officer, as the case may be, on receipt of a request shall, as expeditiously as possible, and in any case within thirty days of the receipt of the request, either provide the information on payment of such fee as may be prescribed or reject the request. Where the information sought concerns the life or liberty of a person, the same shall be provided within forty-eight hours.",
             "metadata": {"act_short": "RTI Act"}},
        ],
    },

    # ============= RERA 2016 =============
    {
        "doc": {
            "source_type": "central_statute", "title": "Real Estate (Regulation and Development) Act, 2016",
            "short_citation": "RERA",
            "long_citation": "Real Estate (Regulation and Development) Act, 2016",
            "status": "in_force",
        },
        "chunks": [
            {"hierarchy_path": ["RERA", "Section 3 Project registration"],
             "chunk_type": "section", "section_number": "3",
             "text": "Section 3. Prior registration of real estate project with Real Estate Regulatory Authority.—(1) No promoter shall advertise, market, book, sell or offer for sale, or invite persons to purchase in any manner any plot, apartment or building, as the case may be, in any real estate project or part of it, in any planning area, without registering the real estate project with the Real Estate Regulatory Authority established under this Act. Provided that projects with land area not exceeding five hundred square metres or eight apartments inclusive of all phases need not be registered.",
             "metadata": {"act_short": "RERA"}},
            {"hierarchy_path": ["RERA", "Section 18 Refund / compensation"],
             "chunk_type": "section", "section_number": "18",
             "text": "Section 18. Return of amount and compensation.—(1) If the promoter fails to complete or is unable to give possession of an apartment, plot or building (a) in accordance with the terms of the agreement for sale or, as the case may be, duly completed by the date specified therein; or (b) due to discontinuance of his business as a developer on account of suspension or revocation of the registration under this Act or for any other reason, he shall be liable on demand to the allottees, in case the allottee wishes to withdraw from the project, without prejudice to any other remedy available, to return the amount received by him in respect of that apartment, plot, building, as the case may be, with interest at such rate as may be prescribed and also compensation. Where an allottee does not intend to withdraw, he shall be paid interest for every month of delay, till handing over of the possession.",
             "metadata": {"act_short": "RERA"}},
        ],
    },

    # ============= Arbitration & Conciliation Act, 1996 =============
    {
        "doc": {
            "source_type": "central_statute", "title": "Arbitration and Conciliation Act, 1996",
            "short_citation": "Arbitration Act",
            "long_citation": "Arbitration and Conciliation Act, 1996",
            "status": "in_force",
        },
        "chunks": [
            {"hierarchy_path": ["Arbitration Act", "Section 7 Arbitration agreement"],
             "chunk_type": "section", "section_number": "7",
             "text": "Section 7. Arbitration agreement.—(1) 'Arbitration agreement' means an agreement by the parties to submit to arbitration all or certain disputes which have arisen or which may arise between them in respect of a defined legal relationship, whether contractual or not. (2) An arbitration agreement may be in the form of an arbitration clause in a contract or in the form of a separate agreement. (3) An arbitration agreement shall be in writing.",
             "metadata": {"act_short": "Arbitration Act"}},
            {"hierarchy_path": ["Arbitration Act", "Section 34 Setting aside an award"],
             "chunk_type": "section", "section_number": "34",
             "text": "Section 34. Application for setting aside arbitral awards.—(1) Recourse to a Court against an arbitral award may be made only by an application for setting aside such award in accordance with sub-sections (2) and (3). (2) An award may be set aside only if (a) a party was under some incapacity; (b) the arbitration agreement is not valid; (c) the party was not given proper notice; (d) the award deals with disputes outside the submission to arbitration; (e) the composition of the tribunal was not in accordance with the agreement; (f) the subject-matter is not capable of settlement by arbitration; or (g) the award is in conflict with the public policy of India. (3) An application must be made within three months from the date on which the party making the application has received the award.",
             "metadata": {"act_short": "Arbitration Act"}},
        ],
    },

    # ============= IBC, 2016 =============
    {
        "doc": {
            "source_type": "central_statute", "title": "Insolvency and Bankruptcy Code, 2016",
            "short_citation": "IBC",
            "long_citation": "Insolvency and Bankruptcy Code, 2016",
            "status": "in_force",
        },
        "chunks": [
            {"hierarchy_path": ["IBC", "Section 7 Initiation by financial creditor"],
             "chunk_type": "section", "section_number": "7",
             "text": "Section 7. Initiation of corporate insolvency resolution process by financial creditor.—(1) A financial creditor either by itself or jointly with other financial creditors may file an application for initiating corporate insolvency resolution process against a corporate debtor before the Adjudicating Authority when a default has occurred. (2) The application shall be made in such form and manner and with such fee as may be prescribed. (3) The financial creditor shall, along with the application, furnish (a) record of the default; (b) name of the resolution professional proposed; (c) any other information.",
             "metadata": {"act_short": "IBC"}},
            {"hierarchy_path": ["IBC", "Section 14 Moratorium"],
             "chunk_type": "section", "section_number": "14",
             "text": "Section 14. Moratorium.—(1) Subject to provisions of sub-sections (2) and (3), on the insolvency commencement date, the Adjudicating Authority shall by order declare moratorium for prohibiting all of the following, namely (a) the institution of suits or continuation of pending suits or proceedings against the corporate debtor including execution of any judgment, decree or order; (b) transferring, encumbering, alienating or disposing of by the corporate debtor any of its assets; (c) any action to foreclose, recover or enforce any security interest; (d) the recovery of any property by an owner or lessor where such property is occupied by or in the possession of the corporate debtor.",
             "metadata": {"act_short": "IBC"}},
        ],
    },

    # ============= Income Tax Act, 1961 =============
    {
        "doc": {
            "source_type": "central_statute", "title": "Income-tax Act, 1961",
            "short_citation": "IT Act 1961",
            "long_citation": "Income-tax Act, 1961",
            "status": "in_force",
        },
        "chunks": [
            {"hierarchy_path": ["IT Act 1961", "Section 80C Deductions"],
             "chunk_type": "section", "section_number": "80C",
             "text": "Section 80C. Deduction in respect of life insurance premia, deferred annuity, contributions to provident fund, subscription to certain equity shares or debentures, etc.—In computing the total income of an assessee, being an individual or a Hindu undivided family, there shall be deducted, in accordance with and subject to the provisions of this section, the whole of the amount paid or deposited in the previous year, as does not exceed one hundred and fifty thousand rupees, in respect of specified investments and payments including life insurance premium, EPF, PPF, ELSS mutual funds, principal repayment of housing loan, tuition fees and other prescribed instruments.",
             "metadata": {"act_short": "IT Act 1961"}},
            {"hierarchy_path": ["IT Act 1961", "Section 139 Return filing"],
             "chunk_type": "section", "section_number": "139",
             "text": "Section 139. Return of income.—(1) Every person, being a company or a firm; or being a person other than a company or a firm, if his total income or the total income of any other person in respect of which he is assessable under this Act, during the previous year exceeded the maximum amount which is not chargeable to income-tax, shall, on or before the due date, furnish a return of his income or the income of such other person during the previous year, in the prescribed form and verified in the prescribed manner.",
             "metadata": {"act_short": "IT Act 1961"}},
        ],
    },

    # ============= Motor Vehicles Act =============
    {
        "doc": {
            "source_type": "central_statute", "title": "Motor Vehicles Act, 1988",
            "short_citation": "MV Act",
            "long_citation": "Motor Vehicles Act, 1988",
            "status": "in_force",
        },
        "chunks": [
            {"hierarchy_path": ["MV Act", "Section 166 Compensation claims"],
             "chunk_type": "section", "section_number": "166",
             "text": "Section 166. Application for compensation.—(1) An application for compensation arising out of an accident of the nature specified in sub-section (1) of section 165 may be made (a) by the person who has sustained the injury; or (b) by the owner of the property; or (c) where death has resulted from the accident, by all or any of the legal representatives of the deceased; or (d) by any agent duly authorised. The Claims Tribunal must enquire and pass an award on the principles of negligence and just compensation.",
             "metadata": {"act_short": "MV Act"}},
            {"hierarchy_path": ["MV Act", "Section 185 Drunken driving"],
             "chunk_type": "section", "section_number": "185",
             "text": "Section 185. Driving by a drunken person or by a person under the influence of drugs.—Whoever, while driving, or attempting to drive, a motor vehicle, has, in his blood, alcohol exceeding 30 mg per 100 ml of blood detected in a test by a breath analyser, or any other drugs to such an extent as to be incapable of exercising proper control over the vehicle, shall be punishable for the first offence with imprisonment for a term which may extend to six months, or with fine of ten thousand rupees, or with both; and for second or subsequent offence with imprisonment up to two years, or with fine of fifteen thousand rupees, or with both.",
             "metadata": {"act_short": "MV Act"}},
        ],
    },

    # ============= Trademark Act =============
    {
        "doc": {
            "source_type": "central_statute", "title": "Trade Marks Act, 1999",
            "short_citation": "TM Act",
            "long_citation": "Trade Marks Act, 1999",
            "status": "in_force",
        },
        "chunks": [
            {"hierarchy_path": ["TM Act", "Section 29 Infringement"],
             "chunk_type": "section", "section_number": "29",
             "text": "Section 29. Infringement of registered trade marks.—(1) A registered trade mark is infringed by a person who, not being a registered proprietor or a person using by way of permitted use, uses in the course of trade, a mark which is identical with, or deceptively similar to, the trade mark in relation to goods or services in respect of which the trade mark is registered and in such manner as to render the use of the mark likely to be taken as being used as a trade mark.",
             "metadata": {"act_short": "TM Act"}},
        ],
    },

    # ============= Copyright Act =============
    {
        "doc": {
            "source_type": "central_statute", "title": "Copyright Act, 1957",
            "short_citation": "Copyright Act",
            "long_citation": "Copyright Act, 1957",
            "status": "in_force",
        },
        "chunks": [
            {"hierarchy_path": ["Copyright Act", "Section 14 Meaning of copyright"],
             "chunk_type": "section", "section_number": "14",
             "text": "Section 14. Meaning of copyright.—For the purposes of this Act, 'copyright' means the exclusive right subject to the provisions of this Act, to do or authorise the doing of any of the following acts in respect of a work or any substantial part thereof, namely (a) in the case of a literary, dramatic or musical work, not being a computer programme: to reproduce the work; to issue copies; to perform; to make any cinematograph film or sound recording; to make any translation or adaptation; (b) in the case of a computer programme, to do any of the acts specified in clause (a) and to sell or give on commercial rental any copy of the computer programme.",
             "metadata": {"act_short": "Copyright Act"}},
            {"hierarchy_path": ["Copyright Act", "Section 52 Fair use"],
             "chunk_type": "section", "section_number": "52",
             "text": "Section 52. Certain acts not to be infringement of copyright.—(1) The following acts shall not constitute an infringement of copyright, namely (a) a fair dealing with any work, not being a computer programme, for the purposes of (i) private or personal use, including research; (ii) criticism or review, whether of that work or of any other work; (iii) the reporting of current events and current affairs, including the reporting of a lecture delivered in public.",
             "metadata": {"act_short": "Copyright Act"}},
        ],
    },

    # ============= DPDP Act 2023 =============
    {
        "doc": {
            "source_type": "central_statute", "title": "Digital Personal Data Protection Act, 2023",
            "short_citation": "DPDP Act",
            "long_citation": "Digital Personal Data Protection Act, 2023",
            "status": "in_force",
        },
        "chunks": [
            {"hierarchy_path": ["DPDP", "Section 6 Consent"],
             "chunk_type": "section", "section_number": "6",
             "text": "Section 6. Consent.—(1) The consent given by the Data Principal to the Data Fiduciary shall be free, specific, informed, unconditional and unambiguous with a clear affirmative action, and shall signify an agreement to the processing of her personal data for the specified purpose and be limited to such personal data as is necessary for such specified purpose. (2) Any infringement of any provision of this Act shall render any agreement, term or condition pertaining to the consent invalid. (4) The Data Principal shall have the right to withdraw consent at any time.",
             "metadata": {"act_short": "DPDP Act"}},
            {"hierarchy_path": ["DPDP", "Section 11 Right to access"],
             "chunk_type": "section", "section_number": "11",
             "text": "Section 11. Right to access information about personal data.—(1) The Data Principal shall have the right to obtain from the Data Fiduciary to whom she has previously given consent for the processing of personal data, on a request made in such manner as may be prescribed (a) a summary of personal data being processed; (b) the identities of all other Data Fiduciaries with whom the personal data has been shared; (c) any other information related to the personal data and its processing.",
             "metadata": {"act_short": "DPDP Act"}},
        ],
    },

    # ============= Advocates Act =============
    {
        "doc": {
            "source_type": "central_statute", "title": "Advocates Act, 1961",
            "short_citation": "Advocates Act",
            "long_citation": "Advocates Act, 1961",
            "status": "in_force",
        },
        "chunks": [
            {"hierarchy_path": ["Advocates Act", "Section 30 Right of advocate to practise"],
             "chunk_type": "section", "section_number": "30",
             "text": "Section 30. Right of advocates to practise.—Subject to the provisions of this Act, every advocate whose name is entered in the State roll shall be entitled as of right to practise throughout the territories to which this Act extends (i) in all courts including the Supreme Court; (ii) before any tribunal or person legally authorised to take evidence; (iii) before any other authority or person before whom such advocate is by or under any law for the time being in force entitled to practise.",
             "metadata": {"act_short": "Advocates Act"}},
        ],
    },

    # ============= NDPS Act =============
    {
        "doc": {
            "source_type": "central_statute", "title": "Narcotic Drugs and Psychotropic Substances Act, 1985",
            "short_citation": "NDPS Act",
            "long_citation": "Narcotic Drugs and Psychotropic Substances Act, 1985",
            "status": "in_force",
        },
        "chunks": [
            {"hierarchy_path": ["NDPS Act", "Section 20 Cannabis"],
             "chunk_type": "section", "section_number": "20",
             "text": "Section 20. Punishment for contravention in relation to cannabis plant and cannabis.—Whoever, in contravention of any provision of this Act or any rule or order made or condition of licence granted thereunder (a) cultivates any cannabis plant; or (b) produces, manufactures, possesses, sells, purchases, transports, imports inter-State, exports inter-State or uses cannabis, shall be punishable: (i) where the contravention involves small quantity, with rigorous imprisonment up to one year, or fine up to ten thousand rupees, or both; (ii) where the contravention involves quantity lesser than commercial quantity but greater than small quantity, with rigorous imprisonment up to ten years, and fine up to one lakh rupees; (iii) where the contravention involves commercial quantity, with rigorous imprisonment for not less than ten years and not more than twenty years, and fine of one lakh to two lakh rupees.",
             "metadata": {"act_short": "NDPS Act"}},
        ],
    },

    # ============= Indian Stamp Act =============
    {
        "doc": {
            "source_type": "central_statute", "title": "Indian Stamp Act, 1899",
            "short_citation": "Stamp Act",
            "long_citation": "Indian Stamp Act, 1899",
            "status": "in_force",
        },
        "chunks": [
            {"hierarchy_path": ["Stamp Act", "Section 17 Time of stamping"],
             "chunk_type": "section", "section_number": "17",
             "text": "Section 17. Instruments executed in India.—All instruments chargeable with duty and executed by any person in India shall be stamped before or at the time of execution. Insufficient stamping does not by itself invalidate the contract; however, an unstamped or insufficiently stamped instrument is inadmissible in evidence (Section 35) until the deficiency and penalty are paid.",
             "metadata": {"act_short": "Stamp Act"}},
        ],
    },

    # ============= Registration Act =============
    {
        "doc": {
            "source_type": "central_statute", "title": "Registration Act, 1908",
            "short_citation": "Registration Act",
            "long_citation": "Registration Act, 1908",
            "status": "in_force",
        },
        "chunks": [
            {"hierarchy_path": ["Registration Act", "Section 17 Mandatory registration"],
             "chunk_type": "section", "section_number": "17",
             "text": "Section 17. Documents of which registration is compulsory.—(1) The following documents shall be registered, namely (a) instruments of gift of immovable property; (b) other non-testamentary instruments which purport or operate to create, declare, assign, limit or extinguish, whether in present or in future, any right, title or interest, whether vested or contingent, of the value of one hundred rupees and upwards, to or in immovable property; (c) non-testamentary instruments which acknowledge the receipt or payment of any consideration on account of the creation, declaration, assignment, limitation or extinction of any such right, title or interest; (d) leases of immovable property from year to year, or for any term exceeding one year, or reserving a yearly rent.",
             "metadata": {"act_short": "Registration Act"}},
        ],
    },

    # ============= Indian Succession Act 1925 =============
    {
        "doc": {
            "source_type": "central_statute", "title": "Indian Succession Act, 1925",
            "short_citation": "Indian Succession Act",
            "long_citation": "Indian Succession Act, 1925",
            "status": "in_force",
        },
        "chunks": [
            {"hierarchy_path": ["Indian Succession Act", "Section 63 Execution of unprivileged Wills"],
             "chunk_type": "section", "section_number": "63",
             "text": "Section 63. Execution of unprivileged Wills.—Every testator, not being a soldier employed in an expedition or engaged in actual warfare, or an airman so employed or engaged, or a mariner at sea, shall execute his Will according to the following rules: (a) The testator shall sign or shall affix his mark to the Will, or it shall be signed by some other person in his presence and by his direction. (b) The signature or mark of the testator, or the signature of the person signing for him, shall be so placed that it shall appear that it was intended thereby to give effect to the writing as a Will. (c) The Will shall be attested by two or more witnesses, each of whom has seen the testator sign or affix his mark to the Will or has seen some other person sign the Will, in the presence and by the direction of the testator.",
             "metadata": {"act_short": "Indian Succession Act"}},
        ],
    },

    # ============= Hindu Succession Act =============
    {
        "doc": {
            "source_type": "central_statute", "title": "Hindu Succession Act, 1956",
            "short_citation": "HSA",
            "long_citation": "Hindu Succession Act, 1956",
            "status": "in_force",
        },
        "chunks": [
            {"hierarchy_path": ["HSA", "Section 6 Coparcenary property"],
             "chunk_type": "section", "section_number": "6",
             "text": "Section 6. Devolution of interest in coparcenary property.—On and from the commencement of the Hindu Succession (Amendment) Act, 2005, in a Joint Hindu family governed by the Mitakshara law, the daughter of a coparcener shall, by birth become a coparcener in her own right in the same manner as the son; have the same rights in the coparcenary property as she would have had if she had been a son; and be subject to the same liabilities in respect of the said coparcenary property as that of a son. (Confirmed retrospectively in Vineeta Sharma v. Rakesh Sharma, 2020.)",
             "metadata": {"act_short": "HSA"}},
        ],
    },

    # ============= Industrial Disputes Act =============
    {
        "doc": {
            "source_type": "central_statute", "title": "Industrial Disputes Act, 1947",
            "short_citation": "ID Act",
            "long_citation": "Industrial Disputes Act, 1947",
            "status": "in_force",
        },
        "chunks": [
            {"hierarchy_path": ["ID Act", "Section 25F Retrenchment"],
             "chunk_type": "section", "section_number": "25F",
             "text": "Section 25F. Conditions precedent to retrenchment of workmen.—No workman employed in any industry who has been in continuous service for not less than one year under an employer shall be retrenched by that employer until (a) the workman has been given one month's notice in writing indicating the reasons for retrenchment and the period of notice has expired, or the workman has been paid in lieu of such notice, wages for the period of the notice; (b) the workman has been paid, at the time of retrenchment, compensation which shall be equivalent to fifteen days' average pay for every completed year of continuous service or any part thereof in excess of six months; and (c) notice in the prescribed manner is served on the appropriate Government.",
             "metadata": {"act_short": "ID Act"}},
        ],
    },

    # ============= Payment of Gratuity Act =============
    {
        "doc": {
            "source_type": "central_statute", "title": "Payment of Gratuity Act, 1972",
            "short_citation": "Gratuity Act",
            "long_citation": "Payment of Gratuity Act, 1972",
            "status": "in_force",
        },
        "chunks": [
            {"hierarchy_path": ["Gratuity Act", "Section 4 Payment of gratuity"],
             "chunk_type": "section", "section_number": "4",
             "text": "Section 4. Payment of gratuity.—(1) Gratuity shall be payable to an employee on the termination of his employment after he has rendered continuous service for not less than five years (a) on his superannuation; (b) on his retirement or resignation; (c) on his death or disablement due to accident or disease (the five-year condition does not apply on death/disablement). (2) For every completed year of service or part thereof in excess of six months, the employer shall pay gratuity to an employee at the rate of fifteen days' wages based on the rate of wages last drawn. The maximum payable amount is twenty lakh rupees (post-2018 amendment).",
             "metadata": {"act_short": "Gratuity Act"}},
        ],
    },

    # ============= Maternity Benefit Act =============
    {
        "doc": {
            "source_type": "central_statute", "title": "Maternity Benefit Act, 1961",
            "short_citation": "Maternity Benefit Act",
            "long_citation": "Maternity Benefit Act, 1961",
            "status": "in_force",
        },
        "chunks": [
            {"hierarchy_path": ["Maternity Benefit Act", "Section 5 Right to payment of maternity benefit"],
             "chunk_type": "section", "section_number": "5",
             "text": "Section 5. Right to payment of maternity benefit.—(1) Subject to the provisions of this Act, every woman shall be entitled to, and her employer shall be liable for, the payment of maternity benefit at the rate of the average daily wage for the period of her actual absence, that is to say, the period immediately preceding the day of her delivery, the actual day of her delivery and any period immediately following that day. (3) The maximum period for which any woman shall be entitled to maternity benefit shall be twenty-six weeks of which not more than eight shall precede the date of her expected delivery (twelve weeks for a third or subsequent child, who has two or more surviving children).",
             "metadata": {"act_short": "Maternity Benefit Act"}},
        ],
    },

    # ============= Prevention of Money Laundering =============
    {
        "doc": {
            "source_type": "central_statute", "title": "Prevention of Money Laundering Act, 2002",
            "short_citation": "PMLA",
            "long_citation": "Prevention of Money Laundering Act, 2002",
            "status": "in_force",
        },
        "chunks": [
            {"hierarchy_path": ["PMLA", "Section 3 Offence of money-laundering"],
             "chunk_type": "section", "section_number": "3",
             "text": "Section 3. Offence of money-laundering.—Whosoever directly or indirectly attempts to indulge or knowingly assists or knowingly is a party or is actually involved in any process or activity connected with the proceeds of crime including its concealment, possession, acquisition or use and projecting or claiming it as untainted property shall be guilty of offence of money-laundering. The offence is cognizable and non-bailable.",
             "metadata": {"act_short": "PMLA"}},
        ],
    },

    # ============= Prevention of Corruption Act =============
    {
        "doc": {
            "source_type": "central_statute", "title": "Prevention of Corruption Act, 1988",
            "short_citation": "PC Act",
            "long_citation": "Prevention of Corruption Act, 1988",
            "status": "in_force",
        },
        "chunks": [
            {"hierarchy_path": ["PC Act", "Section 7 Public servant taking gratification"],
             "chunk_type": "section", "section_number": "7",
             "text": "Section 7. Offence relating to public servant being bribed.—Any public servant who (a) obtains or accepts or attempts to obtain from any person, an undue advantage, with the intention to perform or cause performance of public duty improperly or dishonestly or to forbear or cause forbearance to perform such duty either by himself or by another public servant; (b) obtains or accepts or attempts to obtain, an undue advantage from any person as a reward for the improper or dishonest performance of a public duty; shall be punishable with imprisonment for a term which shall not be less than three years but which may extend to seven years and shall also be liable to fine.",
             "metadata": {"act_short": "PC Act"}},
        ],
    },
]
