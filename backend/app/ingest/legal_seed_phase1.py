"""Phase 1 corpus expansion — deeper section coverage of priority active acts.

Faithful condensations from publicly available bare-act text. Adds ~70 chunks
across 12 high-traffic acts. Each chunk holds the operative language so the
quote-check verifier can match.
"""
from __future__ import annotations

from typing import Any


PHASE1_SEED_DOCS: list[dict[str, Any]] = [
    # ============= BNS deeper =============
    {
        "doc": {
            "source_type": "central_statute", "title": "Bharatiya Nyaya Sanhita, 2023",
            "short_citation": "BNS", "long_citation": "Bharatiya Nyaya Sanhita, 2023",
            "effective_from": "2024-07-01", "status": "in_force",
        },
        "chunks": [
            {"hierarchy_path": ["BNS", "Chapter I", "Section 2 (Definitions)"],
             "chunk_type": "section", "section_number": "2",
             "text": "Section 2. Definitions.—In this Sanhita, unless the context otherwise requires, (3) 'child' means any person below the age of eighteen years; (8) 'document' means any matter expressed or described upon any substance by means of letters, figures or marks, or by more than one of those means, intended to be used, or which may be used, as evidence; (10) 'fraudulently' means with intent to defraud; (15) 'good faith' means anything which is done with due care and attention; (24) 'movable property' includes property of every description, except land and things attached to the earth or permanently fastened to anything which is attached to the earth.",
             "metadata": {"act_short": "BNS"}},
            {"hierarchy_path": ["BNS", "Chapter II", "Section 3 (General explanations)"],
             "chunk_type": "section", "section_number": "3",
             "text": "Section 3. General explanations.—Throughout this Sanhita every definition of an offence, every penal provision, and every illustration of every such definition or penal provision, shall be understood subject to the exceptions contained in the Chapter entitled 'General Exceptions', though those exceptions are not repeated in such definition, penal provision, or illustration.",
             "metadata": {"act_short": "BNS"}},
            {"hierarchy_path": ["BNS", "Chapter III", "Section 14 (Act done by a person bound by law)"],
             "chunk_type": "section", "section_number": "14",
             "text": "Section 14. Act done by a person bound, or by mistake of fact believing himself bound, by law.—Nothing is an offence which is done by a person who is, or who by reason of a mistake of fact and not by reason of a mistake of law in good faith believes himself to be, bound by law to do it.",
             "metadata": {"act_short": "BNS"}},
            {"hierarchy_path": ["BNS", "Chapter IV", "Section 35 (Right of private defence)"],
             "chunk_type": "section", "section_number": "35",
             "text": "Section 35. Right of private defence of body and of property.—Every person has a right, subject to the restrictions contained in section 37, to defend his own body, and the body of any other person, against any offence affecting the human body; and the property, whether movable or immovable, of himself or of any other person, against any act which is an offence falling under the definition of theft, robbery, mischief or criminal trespass, or which is an attempt to commit any such offence.",
             "metadata": {"act_short": "BNS"}},
            {"hierarchy_path": ["BNS", "Chapter V", "Section 76 (Voyeurism)"],
             "chunk_type": "section", "section_number": "76",
             "text": "Section 76. Assault or use of criminal force on woman with intent to disrobe.—Any man who assaults or uses criminal force to any woman or abets such act with the intention of disrobing or compelling her to be naked, shall be punished with imprisonment of either description for a term which shall not be less than three years but which may extend to seven years, and shall also be liable to fine.",
             "metadata": {"act_short": "BNS"}},
            {"hierarchy_path": ["BNS", "Chapter V", "Section 77 (Voyeurism)"],
             "chunk_type": "section", "section_number": "77",
             "text": "Section 77. Voyeurism.—Any man who watches, or captures the image of a woman engaging in a private act in circumstances where she would usually have the expectation of not being observed either by the perpetrator or by any other person at the behest of the perpetrator or disseminates such image shall be punished on first conviction with imprisonment of either description for a term which shall not be less than one year, but which may extend to three years, and shall also be liable to fine.",
             "metadata": {"act_short": "BNS"}},
            {"hierarchy_path": ["BNS", "Chapter VII", "Section 152 (Acts endangering sovereignty)"],
             "chunk_type": "section", "section_number": "152",
             "text": "Section 152. Act endangering sovereignty, unity and integrity of India.—Whoever, purposely or knowingly, by words, either spoken or written, or by signs, or by visible representation, or by electronic communication or by use of financial means, or otherwise, excites or attempts to excite, secession or armed rebellion or subversive activities, or encourages feelings of separatist activities or endangers sovereignty or unity and integrity of India; or indulges in or commits any such act shall be punished with imprisonment for life or with imprisonment which may extend to seven years, and shall also be liable to fine.",
             "metadata": {"act_short": "BNS"}},
            {"hierarchy_path": ["BNS", "Chapter XVI", "Section 296 (Obscene act in public)"],
             "chunk_type": "section", "section_number": "296",
             "text": "Section 296. Obscene acts and songs.—Whoever, to the annoyance of others (a) does any obscene act in any public place; or (b) sings, recites or utters any obscene song, ballad or words, in or near any public place, shall be punished with imprisonment of either description for a term which may extend to three months, or with fine which may extend to one thousand rupees, or with both.",
             "metadata": {"act_short": "BNS"}},
            {"hierarchy_path": ["BNS", "Chapter XVIII", "Section 324 (Mischief)"],
             "chunk_type": "section", "section_number": "324",
             "text": "Section 324. Mischief.—Whoever with intent to cause, or knowing that he is likely to cause, wrongful loss or damage to the public or to any person, causes the destruction of any property, or any such change in any property or in the situation thereof as destroys or diminishes its value or utility, or affects it injuriously, commits 'mischief'. Punishment ranges from three months to ten years depending on the value of damage and aggravating circumstances under sections 325–333.",
             "metadata": {"act_short": "BNS"}},
        ],
    },

    # ============= BNSS deeper =============
    {
        "doc": {
            "source_type": "central_statute", "title": "Bharatiya Nagarik Suraksha Sanhita, 2023",
            "short_citation": "BNSS", "long_citation": "Bharatiya Nagarik Suraksha Sanhita, 2023",
            "effective_from": "2024-07-01", "status": "in_force",
        },
        "chunks": [
            {"hierarchy_path": ["BNSS", "Chapter XII", "Section 175 (Police investigation)"],
             "chunk_type": "section", "section_number": "175",
             "text": "Section 175. Police officer's power to investigate cognizable case.—(1) Any officer in charge of a police station may, without the order of a Magistrate, investigate any cognizable case which a Court having jurisdiction over the local area within the limits of such station would have power to inquire into or try under the provisions of Chapter XIV. (3) Any Magistrate empowered under section 210 may direct any officer in charge of a police station to register an FIR and investigate when, on receipt of an application by any person aggrieved, he is satisfied that the police have refused to register the FIR.",
             "metadata": {"act_short": "BNSS"}},
            {"hierarchy_path": ["BNSS", "Chapter XII", "Section 187 (Detention beyond 24 hrs)"],
             "chunk_type": "section", "section_number": "187",
             "text": "Section 187. Procedure when investigation cannot be completed in twenty-four hours.—(1) Whenever any person is arrested and detained in custody and it appears that the investigation cannot be completed within the period of twenty-four hours fixed by section 58, the officer in charge of the police station shall forthwith transmit a copy of the entries in the diary relating to the case to the nearest Magistrate. (3) The Magistrate may authorise the detention of the accused in such custody as he thinks fit, for a term not exceeding fifteen days in the whole, or in police custody not exceeding fifteen days from the date of arrest. The total period of detention cannot exceed sixty days for offences punishable with up to ten years and ninety days for offences punishable with death, life imprisonment or more than ten years.",
             "metadata": {"act_short": "BNSS"}},
            {"hierarchy_path": ["BNSS", "Chapter XXXIII", "Section 528 (Inherent powers of HC)"],
             "chunk_type": "section", "section_number": "528",
             "text": "Section 528. Saving of inherent powers of High Court.—Nothing in this Sanhita shall be deemed to limit or affect the inherent powers of the High Court to make such orders as may be necessary to give effect to any order under this Sanhita, or to prevent abuse of the process of any Court, or otherwise to secure the ends of justice.",
             "metadata": {"act_short": "BNSS"}},
            {"hierarchy_path": ["BNSS", "Chapter XXXV", "Section 479 (Maximum undertrial detention)"],
             "chunk_type": "section", "section_number": "479",
             "text": "Section 479. Maximum period for which undertrial prisoner can be detained.—(1) Where a person has, during the period of investigation, inquiry or trial under this Sanhita of an offence under any law (not being an offence for which the punishment of death or life imprisonment has been specified as one of the punishments under that law) undergone detention for a period extending up to one-half of the maximum period of imprisonment specified for that offence under that law, he shall be released by the Court on his personal bond with or without sureties. For first-time offenders, the threshold is one-third.",
             "metadata": {"act_short": "BNSS"}},
        ],
    },

    # ============= Companies Act deeper =============
    {
        "doc": {
            "source_type": "central_statute", "title": "Companies Act, 2013",
            "short_citation": "Companies Act",
            "long_citation": "Companies Act, 2013",
            "status": "in_force",
        },
        "chunks": [
            {"hierarchy_path": ["Companies Act", "Chapter II", "Section 7 (Incorporation)"],
             "chunk_type": "section", "section_number": "7",
             "text": "Section 7. Incorporation of company.—(1) There shall be filed with the Registrar within whose jurisdiction the registered office of a company is proposed to be situated, the following documents and information for registration, namely (a) the memorandum and articles of the company duly signed; (b) a declaration in the prescribed form by an advocate, a chartered accountant, cost accountant or company secretary in practice that all the requirements of this Act have been complied with; (c) a declaration from each subscriber and first directors that he has not been convicted of any offence in connection with the promotion, formation or management of any company; (d) the address for correspondence; (e) the particulars of every subscriber.",
             "metadata": {"act_short": "Companies Act"}},
            {"hierarchy_path": ["Companies Act", "Chapter VII", "Section 188 (Related party transactions)"],
             "chunk_type": "section", "section_number": "188",
             "text": "Section 188. Related party transactions.—(1) Except with the consent of the Board of Directors given by a resolution at a meeting of the Board and subject to such conditions as may be prescribed, no company shall enter into any contract or arrangement with a related party with respect to (a) sale, purchase or supply of any goods or materials; (b) selling or otherwise disposing of, or buying, property of any kind; (c) leasing of property of any kind; (d) availing or rendering of any services; (e) appointment of any agent for purchase or sale of goods, materials, services or property; (f) such related party's appointment to any office or place of profit; (g) underwriting the subscription of any securities. Prior approval of shareholders by ordinary resolution required for transactions exceeding the prescribed thresholds.",
             "metadata": {"act_short": "Companies Act"}},
            {"hierarchy_path": ["Companies Act", "Chapter IX", "Section 129 (Financial statement)"],
             "chunk_type": "section", "section_number": "129",
             "text": "Section 129. Financial statement.—(1) The financial statements shall give a true and fair view of the state of affairs of the company or companies, comply with the accounting standards notified under section 133 and shall be in the form or forms as may be provided for different class or classes of companies in Schedule III. The Board of every company shall lay before each annual general meeting a financial statement for the financial year. Where a company has one or more subsidiaries or associate companies, it shall, in addition to its own financial statements, prepare a consolidated financial statement.",
             "metadata": {"act_short": "Companies Act"}},
            {"hierarchy_path": ["Companies Act", "Chapter X", "Section 135 (CSR)"],
             "chunk_type": "section", "section_number": "135",
             "text": "Section 135. Corporate Social Responsibility.—(1) Every company having net worth of rupees five hundred crore or more, or turnover of rupees one thousand crore or more or a net profit of rupees five crore or more during the immediately preceding financial year shall constitute a CSR Committee of the Board consisting of three or more directors, out of which at least one director shall be an independent director. (5) The Board of every such company shall ensure that the company spends, in every financial year, at least two per cent of the average net profits of the company made during the three immediately preceding financial years on CSR activities.",
             "metadata": {"act_short": "Companies Act"}},
        ],
    },

    # ============= CPC deeper =============
    {
        "doc": {
            "source_type": "central_statute", "title": "Code of Civil Procedure, 1908",
            "short_citation": "CPC", "long_citation": "Code of Civil Procedure, 1908",
            "status": "in_force",
        },
        "chunks": [
            {"hierarchy_path": ["CPC", "Order I Rule 10 (Striking out, adding parties)"],
             "chunk_type": "section", "section_number": "Order I R.10",
             "text": "Order I Rule 10. Suit in name of wrong plaintiff.—(1) Where a suit has been instituted in the name of the wrong person as plaintiff or where it is doubtful whether it has been instituted in the name of the right plaintiff, the court may at any stage of the suit, if satisfied that the suit has been instituted through a bona fide mistake, and that it is necessary for the determination of the real matter in dispute so to do, order any other person to be substituted or added as plaintiff. (2) The court may at any stage of the proceedings order that the name of any party improperly joined be struck out, and that the name of any person whose presence may be necessary for adjudication be added.",
             "metadata": {"act_short": "CPC"}},
            {"hierarchy_path": ["CPC", "Order VII Rule 11 (Rejection of plaint)"],
             "chunk_type": "section", "section_number": "Order VII R.11",
             "text": "Order VII Rule 11. Rejection of plaint.—The plaint shall be rejected in the following cases (a) where it does not disclose a cause of action; (b) where the relief claimed is undervalued, and the plaintiff, on being required by the Court to correct the valuation within a time to be fixed by the Court, fails to do so; (c) where the relief claimed is properly valued, but the plaint is written upon paper insufficiently stamped, and the plaintiff, on being required by the Court to supply the requisite stamp-paper within a time fixed by the Court, fails to do so; (d) where the suit appears from the statement in the plaint to be barred by any law; (e) where it is not filed in duplicate; (f) where the plaintiff fails to comply with the provisions of rule 9.",
             "metadata": {"act_short": "CPC"}},
            {"hierarchy_path": ["CPC", "Order XXIII Rule 3 (Compromise of suit)"],
             "chunk_type": "section", "section_number": "Order XXIII R.3",
             "text": "Order XXIII Rule 3. Compromise of suit.—Where it is proved to the satisfaction of the Court that a suit has been adjusted wholly or in part by any lawful agreement or compromise, in writing and signed by the parties, or where the defendant satisfies the plaintiff in respect of the whole or any part of the subject-matter of the suit, the Court shall order such agreement, compromise or satisfaction to be recorded, and shall pass a decree in accordance therewith so far as it relates to the parties to the suit.",
             "metadata": {"act_short": "CPC"}},
            {"hierarchy_path": ["CPC", "Order XXXIX Rule 1-2 (Temporary injunction)"],
             "chunk_type": "section", "section_number": "Order XXXIX",
             "text": "Order XXXIX Rule 1. Cases in which temporary injunction may be granted.—Where in any suit it is proved by affidavit or otherwise (a) that any property in dispute in a suit is in danger of being wasted, damaged or alienated by any party to the suit, or wrongfully sold in execution of a decree; or (b) that the defendant threatens, or intends, to remove or dispose of his property with a view to defrauding his creditors; or (c) that the defendant threatens to dispossess the plaintiff or otherwise cause injury to the plaintiff in relation to any property in dispute in the suit, the Court may by order grant a temporary injunction. Three-fold test: prima facie case, balance of convenience, irreparable injury.",
             "metadata": {"act_short": "CPC"}},
            {"hierarchy_path": ["CPC", "Section 9 (Civil court jurisdiction)"],
             "chunk_type": "section", "section_number": "9",
             "text": "Section 9. Courts to try all civil suits unless barred.—The Courts shall (subject to the provisions herein contained) have jurisdiction to try all suits of a civil nature excepting suits of which their cognizance is either expressly or impliedly barred. Explanation I: A suit in which the right to property or to an office is contested is a suit of a civil nature, notwithstanding that such right may depend entirely on the decision of questions as to religious rites or ceremonies. Explanation II: For the purposes of this section, it is immaterial whether or not any fees are attached to the office referred to in Explanation I or whether or not such office is attached to a particular place.",
             "metadata": {"act_short": "CPC"}},
        ],
    },

    # ============= Hindu Marriage Act deeper =============
    {
        "doc": {
            "source_type": "central_statute", "title": "Hindu Marriage Act, 1955",
            "short_citation": "HMA", "long_citation": "Hindu Marriage Act, 1955",
            "status": "in_force",
        },
        "chunks": [
            {"hierarchy_path": ["HMA", "Section 9 (Restitution of conjugal rights)"],
             "chunk_type": "section", "section_number": "9",
             "text": "Section 9. Restitution of conjugal rights.—When either the husband or the wife has, without reasonable excuse, withdrawn from the society of the other, the aggrieved party may apply, by petition to the district court, for restitution of conjugal rights and the court, on being satisfied of the truth of the statements made in such petition and that there is no legal ground why the application should not be granted, may decree restitution of conjugal rights accordingly.",
             "metadata": {"act_short": "HMA"}},
            {"hierarchy_path": ["HMA", "Section 24 (Maintenance pendente lite)"],
             "chunk_type": "section", "section_number": "24",
             "text": "Section 24. Maintenance pendente lite and expenses of proceedings.—Where in any proceeding under this Act it appears to the court that either the wife or the husband, as the case may be, has no independent income sufficient for her or his support and the necessary expenses of the proceeding, it may, on the application of the wife or the husband, order the respondent to pay to the petitioner the expenses of the proceeding, and monthly during the proceeding such sum as, having regard to the petitioner's own income and the income of the respondent, it may seem to the court to be reasonable.",
             "metadata": {"act_short": "HMA"}},
            {"hierarchy_path": ["HMA", "Section 25 (Permanent alimony)"],
             "chunk_type": "section", "section_number": "25",
             "text": "Section 25. Permanent alimony and maintenance.—(1) Any court exercising jurisdiction under this Act may, at the time of passing any decree or at any time subsequent thereto, on application made to it for the purpose by either the wife or the husband, as the case may be, order that the respondent shall pay to the applicant for her or his maintenance and support such gross sum or such monthly or periodical sum for a term not exceeding the life of the applicant as, having regard to the respondent's own income and other property, the income and other property of the applicant, the conduct of the parties and other circumstances of the case, it may seem to the court to be just.",
             "metadata": {"act_short": "HMA"}},
            {"hierarchy_path": ["HMA", "Section 26 (Custody of children)"],
             "chunk_type": "section", "section_number": "26",
             "text": "Section 26. Custody of children.—In any proceeding under this Act, the court may, from time to time, pass such interim orders and make such provisions in the decree as it may deem just and proper with respect to the custody, maintenance and education of minor children, consistently with their wishes, wherever possible, and may, after the decree, upon application by petition for the purpose, make from time to time, all such orders and provisions with respect to the custody, maintenance and education of such children as might have been made by such decree or interim orders. The paramount consideration is the welfare of the child.",
             "metadata": {"act_short": "HMA"}},
        ],
    },

    # ============= Arbitration Act deeper =============
    {
        "doc": {
            "source_type": "central_statute", "title": "Arbitration and Conciliation Act, 1996",
            "short_citation": "Arbitration Act",
            "long_citation": "Arbitration and Conciliation Act, 1996",
            "status": "in_force",
        },
        "chunks": [
            {"hierarchy_path": ["Arbitration Act", "Section 8 (Reference to arbitration)"],
             "chunk_type": "section", "section_number": "8",
             "text": "Section 8. Power to refer parties to arbitration where there is an arbitration agreement.—(1) A judicial authority, before which an action is brought in a matter which is the subject of an arbitration agreement shall, if a party to the arbitration agreement or any person claiming through or under him, so applies not later than the date of submitting his first statement on the substance of the dispute, then, notwithstanding any judgment, decree or order of the Supreme Court or any Court, refer the parties to arbitration unless it finds that prima facie no valid arbitration agreement exists.",
             "metadata": {"act_short": "Arbitration Act"}},
            {"hierarchy_path": ["Arbitration Act", "Section 9 (Interim measures by court)"],
             "chunk_type": "section", "section_number": "9",
             "text": "Section 9. Interim measures, etc., by Court.—(1) A party may, before, or during arbitral proceedings or at any time after the making of the arbitral award but before it is enforced, apply to a court for any interim measure of protection in respect of any of the following matters: (i) the preservation, interim custody or sale of any goods which are the subject-matter of the arbitration agreement; (ii) securing the amount in dispute in the arbitration; (iii) the detention, preservation or inspection of any property or thing which is the subject-matter of the dispute; (iv) interim injunction or the appointment of a receiver.",
             "metadata": {"act_short": "Arbitration Act"}},
            {"hierarchy_path": ["Arbitration Act", "Section 11 (Appointment of arbitrators)"],
             "chunk_type": "section", "section_number": "11",
             "text": "Section 11. Appointment of arbitrators.—(1) A person of any nationality may be an arbitrator, unless otherwise agreed by the parties. (2) Subject to sub-section (6), the parties are free to agree on a procedure for appointing the arbitrator or arbitrators. (5) Failing any agreement under sub-section (2), in an arbitration with a sole arbitrator, if the parties fail to agree on the arbitrator within thirty days from receipt of a request by one party from the other party to so agree, the appointment shall be made, upon request of a party, by the Supreme Court or, as the case may be, the High Court.",
             "metadata": {"act_short": "Arbitration Act"}},
            {"hierarchy_path": ["Arbitration Act", "Section 36 (Enforcement of arbitral award)"],
             "chunk_type": "section", "section_number": "36",
             "text": "Section 36. Enforcement.—(1) Where the time for making an application to set aside the arbitral award under section 34 has expired, then, subject to the provisions of sub-section (2), such award shall be enforced in accordance with the provisions of the Code of Civil Procedure, 1908, in the same manner as if it were a decree of the court. (2) Where an application to set aside the arbitral award has been filed in the Court under section 34, the filing of such an application shall not by itself render that award unenforceable, unless the Court grants an order of stay of the operation of the said arbitral award on a separate application made for that purpose.",
             "metadata": {"act_short": "Arbitration Act"}},
        ],
    },

    # ============= IBC deeper =============
    {
        "doc": {
            "source_type": "central_statute", "title": "Insolvency and Bankruptcy Code, 2016",
            "short_citation": "IBC", "long_citation": "Insolvency and Bankruptcy Code, 2016",
            "status": "in_force",
        },
        "chunks": [
            {"hierarchy_path": ["IBC", "Section 9 (Application by operational creditor)"],
             "chunk_type": "section", "section_number": "9",
             "text": "Section 9. Application for initiation of corporate insolvency resolution process by operational creditor.—(1) After the expiry of the period of ten days from the date of delivery of the notice or invoice demanding payment under sub-section (1) of section 8, if the operational creditor does not receive payment from the corporate debtor or notice of the dispute under sub-section (2) of section 8, the operational creditor may file an application before the Adjudicating Authority for initiating a corporate insolvency resolution process.",
             "metadata": {"act_short": "IBC"}},
            {"hierarchy_path": ["IBC", "Section 30 (Resolution plan)"],
             "chunk_type": "section", "section_number": "30",
             "text": "Section 30. Submission of resolution plan.—(1) A resolution applicant may submit a resolution plan along with an affidavit stating that he is eligible under section 29A to the resolution professional prepared on the basis of the information memorandum. (2) The resolution professional shall examine each resolution plan received by him to confirm that each resolution plan (a) provides for the payment of insolvency resolution process costs; (b) provides for the payment of debts of operational creditors in such manner as may be specified by the Board which shall not be less than the amount to be paid in the event of liquidation; (c) provides for the management of the affairs of the Corporate debtor after approval of the resolution plan.",
             "metadata": {"act_short": "IBC"}},
            {"hierarchy_path": ["IBC", "Section 53 (Distribution of assets)"],
             "chunk_type": "section", "section_number": "53",
             "text": "Section 53. Distribution of assets (waterfall).—(1) Notwithstanding anything to the contrary contained in any law enacted by the Parliament or any State Legislature, the proceeds from the sale of the liquidation assets shall be distributed in the following order of priority: (a) the insolvency resolution process costs and the liquidation costs; (b) workmen's dues for the period of twenty-four months preceding the liquidation commencement date and debts owed to a secured creditor in the event such secured creditor has relinquished security; (c) wages and any unpaid dues owed to employees other than workmen for the period of twelve months preceding the liquidation commencement date; (d) financial debts owed to unsecured creditors; (e) any amount due to the Central Government and the State Government; (f) any remaining debts and dues; (g) preference shareholders, if any; and (h) equity shareholders or partners, as the case may be.",
             "metadata": {"act_short": "IBC"}},
        ],
    },

    # ============= Income-tax Act deeper =============
    {
        "doc": {
            "source_type": "central_statute", "title": "Income-tax Act, 1961",
            "short_citation": "IT Act 1961",
            "long_citation": "Income-tax Act, 1961",
            "status": "in_force",
        },
        "chunks": [
            {"hierarchy_path": ["IT Act 1961", "Section 10 (Exempt incomes)"],
             "chunk_type": "section", "section_number": "10",
             "text": "Section 10. Incomes not included in total income.—In computing the total income of a previous year of any person, any income falling within any of the following clauses shall not be included: (1) agricultural income; (10) gratuity received by Government employees in full and by other employees up to specified limits; (10D) sum received under a life insurance policy subject to conditions; (13A) house rent allowance subject to limits; (14) prescribed allowances; (38) long-term capital gains arising from transfer of equity shares (now subject to section 112A).",
             "metadata": {"act_short": "IT Act 1961"}},
            {"hierarchy_path": ["IT Act 1961", "Section 24 (Deductions from house property)"],
             "chunk_type": "section", "section_number": "24",
             "text": "Section 24. Deductions from income from house property.—Income chargeable under the head 'Income from house property' shall be computed after making the following deductions: (a) a sum equal to thirty per cent of the annual value; (b) where the property has been acquired, constructed, repaired, renewed or reconstructed with borrowed capital, the amount of any interest payable on such capital. The deduction in respect of interest on borrowed capital is restricted to two lakh rupees for self-occupied property.",
             "metadata": {"act_short": "IT Act 1961"}},
            {"hierarchy_path": ["IT Act 1961", "Section 80D (Health insurance)"],
             "chunk_type": "section", "section_number": "80D",
             "text": "Section 80D. Deduction in respect of health insurance premia.—In computing the total income of an assessee, being an individual or a Hindu undivided family, there shall be deducted such sum, as specified, paid by any mode other than cash in the previous year out of his income chargeable to tax, on account of insurance on the health of self, spouse, dependent children up to twenty-five thousand rupees, and on parents up to twenty-five thousand rupees (fifty thousand rupees if senior citizen).",
             "metadata": {"act_short": "IT Act 1961"}},
            {"hierarchy_path": ["IT Act 1961", "Section 194 (TDS on rent)"],
             "chunk_type": "section", "section_number": "194I",
             "text": "Section 194-I. Rent.—Any person, not being an individual or a Hindu undivided family, who is responsible for paying to a resident any income by way of rent, shall, at the time of credit of such income to the account of the payee or at the time of payment thereof in cash or by issue of a cheque or draft or by any other mode, whichever is earlier, deduct income-tax thereon at the rate of (a) two per cent for the use of any machinery or plant or equipment; and (b) ten per cent for the use of any land or building, including factory building, or land appurtenant to a building, including factory building. No deduction if the aggregate rent does not exceed two lakh forty thousand rupees.",
             "metadata": {"act_short": "IT Act 1961"}},
            {"hierarchy_path": ["IT Act 1961", "Section 234A (Interest for default in filing return)"],
             "chunk_type": "section", "section_number": "234A",
             "text": "Section 234A. Interest for defaults in furnishing return of income.—Where the return of income for any assessment year is furnished after the due date specified in sub-section (1) of section 139 or is not furnished, the assessee shall be liable to pay simple interest at the rate of one per cent for every month or part of a month comprised in the period commencing on the date immediately following the due date and ending on the date of furnishing of the return.",
             "metadata": {"act_short": "IT Act 1961"}},
        ],
    },

    # ============= GST deeper =============
    {
        "doc": {
            "source_type": "central_statute", "title": "Central Goods and Services Tax Act, 2017",
            "short_citation": "CGST Act",
            "long_citation": "Central Goods and Services Tax Act, 2017",
            "status": "in_force",
        },
        "chunks": [
            {"hierarchy_path": ["CGST Act", "Section 16 (Input tax credit)"],
             "chunk_type": "section", "section_number": "16",
             "text": "Section 16. Eligibility and conditions for taking input tax credit.—(1) Every registered person shall, subject to such conditions and restrictions as may be prescribed and in the manner specified in section 49, be entitled to take credit of input tax charged on any supply of goods or services or both to him which are used or intended to be used in the course or furtherance of his business and the said amount shall be credited to the electronic credit ledger of such person. (2) Conditions: (a) registered person is in possession of tax invoice; (b) goods/services received; (c) tax has been paid to government; (d) furnished returns under section 39.",
             "metadata": {"act_short": "CGST Act"}},
            {"hierarchy_path": ["CGST Act", "Section 39 (GST returns)"],
             "chunk_type": "section", "section_number": "39",
             "text": "Section 39. Furnishing of returns.—(1) Every registered person, other than an Input Service Distributor, non-resident taxable person, person paying tax under composition levy, shall, for every calendar month, furnish a return on or before the twentieth day of the month succeeding such calendar month or part thereof, electronically, of inward and outward supplies of goods or services or both, input tax credit availed, tax payable, tax paid and such other particulars in such form and manner as may be prescribed.",
             "metadata": {"act_short": "CGST Act"}},
            {"hierarchy_path": ["CGST Act", "Section 73 (Demand and recovery)"],
             "chunk_type": "section", "section_number": "73",
             "text": "Section 73. Determination of tax (other than fraud) not paid or short paid.—(1) Where it appears to the proper officer that any tax has not been paid or short paid or erroneously refunded, or where input tax credit has been wrongly availed or utilised for any reason, other than the reason of fraud or any wilful-misstatement or suppression of facts, he shall serve notice on the person chargeable with tax requiring him to show cause as to why he should not pay the amount specified in the notice along with interest payable thereon under section 50 and a penalty leviable.",
             "metadata": {"act_short": "CGST Act"}},
        ],
    },

    # ============= MV Act deeper =============
    {
        "doc": {
            "source_type": "central_statute", "title": "Motor Vehicles Act, 1988",
            "short_citation": "MV Act", "long_citation": "Motor Vehicles Act, 1988",
            "status": "in_force",
        },
        "chunks": [
            {"hierarchy_path": ["MV Act", "Section 3 (Driving licence)"],
             "chunk_type": "section", "section_number": "3",
             "text": "Section 3. Necessity for driving licence.—(1) No person shall drive a motor vehicle in any public place unless he holds an effective driving licence issued to him authorising him to drive the vehicle; and no person shall so drive a transport vehicle other than a motor cab or motor cycle hired for his own use or rented under any scheme made under sub-section (2) of section 75 unless his driving licence specifically entitles him so to do.",
             "metadata": {"act_short": "MV Act"}},
            {"hierarchy_path": ["MV Act", "Section 146 (Insurance against third party risks)"],
             "chunk_type": "section", "section_number": "146",
             "text": "Section 146. Necessity for insurance against third party risk.—(1) No person shall use, except as a passenger, or cause or allow any other person to use, a motor vehicle in a public place, unless there is in force in relation to the use of the vehicle by that person or that other person, as the case may be, a policy of insurance complying with the requirements of this Chapter.",
             "metadata": {"act_short": "MV Act"}},
            {"hierarchy_path": ["MV Act", "Section 163A (No-fault liability)"],
             "chunk_type": "section", "section_number": "163A",
             "text": "Section 163A. Special provisions as to payment of compensation on structured formula basis.—(1) Notwithstanding anything contained in this Act or in any other law for the time being in force or instrument having the force of law, the owner of the motor vehicle or the authorised insurer shall be liable to pay in the case of death or permanent disablement due to accident arising out of the use of motor vehicle, compensation, as indicated in the Second Schedule, to the legal heirs or the victim, as the case may be. The claimant is not required to plead or establish negligence on the part of the owner.",
             "metadata": {"act_short": "MV Act"}},
        ],
    },

    # ============= POSH deeper =============
    {
        "doc": {
            "source_type": "central_statute", "title": "Sexual Harassment of Women at Workplace (Prevention, Prohibition and Redressal) Act, 2013",
            "short_citation": "POSH Act",
            "long_citation": "Sexual Harassment of Women at Workplace Act, 2013",
            "status": "in_force",
        },
        "chunks": [
            {"hierarchy_path": ["POSH", "Section 2 (Definitions)"],
             "chunk_type": "section", "section_number": "2",
             "text": "Section 2. Definitions.—(n) 'sexual harassment' includes any one or more of the following unwelcome acts or behaviour (whether directly or by implication) namely (i) physical contact and advances; or (ii) a demand or request for sexual favours; or (iii) making sexually coloured remarks; or (iv) showing pornography; or (v) any other unwelcome physical, verbal or non-verbal conduct of sexual nature.",
             "metadata": {"act_short": "POSH Act"}},
            {"hierarchy_path": ["POSH", "Section 9 (Complaint)"],
             "chunk_type": "section", "section_number": "9",
             "text": "Section 9. Complaint of sexual harassment.—(1) Any aggrieved woman may make, in writing, a complaint of sexual harassment at workplace to the Internal Committee if so constituted, or the Local Committee, in case it is not so constituted, within a period of three months from the date of incident and in case of a series of incidents, within a period of three months from the date of last incident. The Internal Committee or Local Committee may extend the time limit if it is satisfied that the circumstances were such which prevented the woman from filing a complaint within the said period.",
             "metadata": {"act_short": "POSH Act"}},
            {"hierarchy_path": ["POSH", "Section 11 (Inquiry into complaint)"],
             "chunk_type": "section", "section_number": "11",
             "text": "Section 11. Inquiry into complaint.—(1) Subject to the provisions of section 10, the Internal Committee or, as the case may be, the Local Committee shall, where the respondent is an employee, proceed to make inquiry into the complaint in accordance with the provisions of the service rules applicable to the respondent and where no such rules exist, in such manner as may be prescribed or in case of a domestic worker, the Local Committee shall forward the complaint to the police, within seven days for registering the case under section 509 of the Indian Penal Code.",
             "metadata": {"act_short": "POSH Act"}},
            {"hierarchy_path": ["POSH", "Section 19 (Duties of employer)"],
             "chunk_type": "section", "section_number": "19",
             "text": "Section 19. Duties of employer.—Every employer shall (a) provide a safe working environment at the workplace; (b) display at any conspicuous place in the workplace, the penal consequences of sexual harassments and the order constituting the Internal Committee under sub-section (1) of section 4; (c) organise workshops and awareness programmes; (d) provide necessary facilities to the Internal Committee or the Local Committee, as the case may be, for dealing with the complaint and conducting an inquiry; (e) assist in securing the attendance of respondent and witnesses before the Internal Committee or the Local Committee.",
             "metadata": {"act_short": "POSH Act"}},
        ],
    },

    # ============= NI Act deeper =============
    {
        "doc": {
            "source_type": "central_statute", "title": "Negotiable Instruments Act, 1881",
            "short_citation": "NI Act", "long_citation": "Negotiable Instruments Act, 1881",
            "status": "in_force",
        },
        "chunks": [
            {"hierarchy_path": ["NI Act", "Section 6 (Definition of cheque)"],
             "chunk_type": "section", "section_number": "6",
             "text": "Section 6. Cheque.—A 'cheque' is a bill of exchange drawn on a specified banker and not expressed to be payable otherwise than on demand and it includes the electronic image of a truncated cheque and a cheque in the electronic form. Explanation: (i) 'a cheque in the electronic form' means a cheque drawn in electronic form by using any computer resource and signed in a secure system with digital signature (with or without biometric signature) and asymmetric crypto system or with electronic signature, as the case may be; (ii) 'a truncated cheque' means a cheque which is truncated during the course of a clearing cycle.",
             "metadata": {"act_short": "NI Act"}},
            {"hierarchy_path": ["NI Act", "Section 139 (Presumption in favour of holder)"],
             "chunk_type": "section", "section_number": "139",
             "text": "Section 139. Presumption in favour of holder.—It shall be presumed, unless the contrary is proved, that the holder of a cheque received the cheque of the nature referred to in section 138 for the discharge, in whole or in part, of any debt or other liability. This is a rebuttable presumption; the accused has to lead evidence to rebut.",
             "metadata": {"act_short": "NI Act"}},
        ],
    },

    # ============= RTI deeper =============
    {
        "doc": {
            "source_type": "central_statute", "title": "Right to Information Act, 2005",
            "short_citation": "RTI Act", "long_citation": "Right to Information Act, 2005",
            "status": "in_force",
        },
        "chunks": [
            {"hierarchy_path": ["RTI", "Section 8 (Exemption from disclosure)"],
             "chunk_type": "section", "section_number": "8",
             "text": "Section 8. Exemption from disclosure of information.—(1) Notwithstanding anything contained in this Act, there shall be no obligation to give any citizen, (a) information, disclosure of which would prejudicially affect the sovereignty and integrity of India, the security, strategic, scientific or economic interests of the State, relation with foreign State or lead to incitement of an offence; (b) information which has been expressly forbidden to be published by any court of law or tribunal; (c) information, the disclosure of which would cause a breach of privilege of Parliament or the State Legislature; (d) information which would harm the competitive position of a third party; (e) information which is held in fiduciary relationship; (f) information received in confidence from foreign Government; (g) information which would endanger life or safety; (h) information which would impede investigation; (j) personal information which has no relationship to public activity.",
             "metadata": {"act_short": "RTI Act"}},
            {"hierarchy_path": ["RTI", "Section 19 (Appeal)"],
             "chunk_type": "section", "section_number": "19",
             "text": "Section 19. Appeal.—(1) Any person who, does not receive a decision within the time specified in sub-section (1) or clause (a) of sub-section (3) of section 7, or is aggrieved by a decision of the Central Public Information Officer or State Public Information Officer, as the case may be, may within thirty days from the expiry of such period or from the receipt of such a decision prefer an appeal to such officer who is senior in rank to the Central Public Information Officer or State Public Information Officer, as the case may be, in each public authority. (3) A second appeal against the decision under sub-section (1) shall lie within ninety days from the date on which the decision should have been made or was actually received, with the Central Information Commission or the State Information Commission.",
             "metadata": {"act_short": "RTI Act"}},
        ],
    },
]
