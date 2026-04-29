"""Phase 2 corpus expansion — broader active-acts coverage.

Adds ~85 chunks across 14 acts that weren't (or were thinly) covered in
Phase 0/1. Faithful condensations of the operative bare-act language so the
verifier's quote-check can match real model citations.

Acts added or deepened in Phase 2:
- Transfer of Property Act, 1882         (sale, mortgage, lease, gift)
- Specific Relief Act, 1963              (specific performance, injunction)
- Limitation Act, 1963                   (key bars to suit/appeal)
- Consumer Protection Act, 2019          (definitions, jurisdiction, e-com)
- Information Technology Act, 2000       (66, 66A struck down, 67, 69, 79)
- Patents Act, 1970                      (patentability, infringement)
- Trade Marks Act, 1999                  (definitions, infringement, passing-off)
- Copyright Act, 1957                    (definitions, fair dealing, infringement)
- Bharatiya Sakshya Adhiniyam, 2023      (electronic evidence, presumptions)
- Constitution of India                  (Parts V, VI, X, XI, XIV — extra arts)
- POCSO Act, 2012                        (sexual offences against children)
- NDPS Act, 1985                         (commercial-quantity offences, bail)
- Foreign Exchange Management Act, 1999  (key offences, compounding)
- Prevention of Money Laundering Act 2002 (definitions, attachment, ECIR)
"""
from __future__ import annotations

from typing import Any


PHASE2_SEED_DOCS: list[dict[str, Any]] = [

    # ============= Transfer of Property Act, 1882 =============
    {
        "doc": {
            "source_type": "central_statute", "title": "Transfer of Property Act, 1882",
            "short_citation": "TP Act", "long_citation": "Transfer of Property Act, 1882",
            "status": "in_force",
            "source_url": "https://indiacode.nic.in/handle/123456789/2338",
        },
        "chunks": [
            {"hierarchy_path": ["TP Act", "Chapter II", "Section 5 (Transfer of property)"],
             "chunk_type": "section", "section_number": "5",
             "text": "Section 5. Transfer of property defined.—In the following sections 'transfer of property' means an act by which a living person conveys property, in present or in future, to one or more other living persons, or to himself, or to himself and one or more other living persons; and 'to transfer property' is to perform such act.",
             "metadata": {"act_short": "TP Act"}},
            {"hierarchy_path": ["TP Act", "Chapter II", "Section 6 (What may be transferred)"],
             "chunk_type": "section", "section_number": "6",
             "text": "Section 6. What may be transferred.—Property of any kind may be transferred, except as otherwise provided by this Act or by any other law for the time being in force.— (a) The chance of an heir-apparent succeeding to an estate, the chance of a relation obtaining a legacy on the death of a kinsman, or any other mere possibility of a like nature, cannot be transferred. (dd) A right to future maintenance, in whatsoever manner arising, secured or determined, cannot be transferred. (e) A mere right to sue cannot be transferred.",
             "metadata": {"act_short": "TP Act"}},
            {"hierarchy_path": ["TP Act", "Chapter III", "Section 54 (Sale)"],
             "chunk_type": "section", "section_number": "54",
             "text": "Section 54. 'Sale' defined.—'Sale' is a transfer of ownership in exchange for a price paid or promised or part-paid and part-promised. Sale how made.—Such transfer, in the case of tangible immoveable property of the value of one hundred rupees and upwards, or in the case of a reversion or other intangible thing, can be made only by a registered instrument. Contract for sale.—A contract for the sale of immoveable property is a contract that a sale of such property shall take place on terms settled between the parties. It does not, of itself, create any interest in or charge on such property.",
             "metadata": {"act_short": "TP Act"}},
            {"hierarchy_path": ["TP Act", "Chapter IV", "Section 58 (Mortgage)"],
             "chunk_type": "section", "section_number": "58",
             "text": "Section 58. 'Mortgage', 'mortgagor', 'mortgagee', 'mortgage-money' and 'mortgage-deed' defined.—(a) A mortgage is the transfer of an interest in specific immoveable property for the purpose of securing the payment of money advanced or to be advanced by way of loan, an existing or future debt, or the performance of an engagement which may give rise to a pecuniary liability. The transferor is called a mortgagor, the transferee a mortgagee; the principal money and interest of which payment is secured for the time being are called the mortgage-money, and the instrument (if any) by which the transfer is effected is called a mortgage-deed.",
             "metadata": {"act_short": "TP Act"}},
            {"hierarchy_path": ["TP Act", "Chapter V", "Section 105 (Lease)"],
             "chunk_type": "section", "section_number": "105",
             "text": "Section 105. Lease defined.—A lease of immoveable property is a transfer of a right to enjoy such property, made for a certain time, express or implied, or in perpetuity, in consideration of a price paid or promised, or of money, a share of crops, service or any other thing of value, to be rendered periodically or on specified occasions to the transferor by the transferee, who accepts the transfer on such terms.",
             "metadata": {"act_short": "TP Act"}},
            {"hierarchy_path": ["TP Act", "Chapter V", "Section 106 (Notice to quit)"],
             "chunk_type": "section", "section_number": "106",
             "text": "Section 106. Duration of certain leases in absence of written contract or local usage.—(1) In the absence of a contract or local law or usage to the contrary, a lease of immoveable property for agricultural or manufacturing purposes shall be deemed to be a lease from year to year, terminable, on the part of either lessor or lessee, by six months' notice; and a lease of immoveable property for any other purpose shall be deemed to be a lease from month to month, terminable, on the part of either lessor or lessee, by fifteen days' notice.",
             "metadata": {"act_short": "TP Act"}},
            {"hierarchy_path": ["TP Act", "Chapter VII", "Section 122 (Gift)"],
             "chunk_type": "section", "section_number": "122",
             "text": "Section 122. 'Gift' defined.—'Gift' is the transfer of certain existing moveable or immoveable property made voluntarily and without consideration, by one person, called the donor, to another, called the donee, and accepted by or on behalf of the donee. Acceptance when to be made.—Such acceptance must be made during the lifetime of the donor and while he is still capable of giving. If the donee dies before acceptance, the gift is void.",
             "metadata": {"act_short": "TP Act"}},
        ],
    },

    # ============= Specific Relief Act, 1963 =============
    {
        "doc": {
            "source_type": "central_statute", "title": "Specific Relief Act, 1963",
            "short_citation": "SR Act", "long_citation": "Specific Relief Act, 1963",
            "status": "in_force",
            "source_url": "https://indiacode.nic.in/handle/123456789/1593",
        },
        "chunks": [
            {"hierarchy_path": ["SR Act", "Chapter II", "Section 10 (Specific performance)"],
             "chunk_type": "section", "section_number": "10",
             "text": "Section 10. Specific performance in respect of contracts.—The specific performance of a contract shall be enforced by the court subject to the provisions contained in sub-section (2) of section 11, section 14 and section 16. (As substituted by the 2018 Amendment, specific performance is now the rule and damages the exception, where the contract is enforceable.)",
             "metadata": {"act_short": "SR Act"}},
            {"hierarchy_path": ["SR Act", "Chapter II", "Section 14 (Contracts not specifically enforceable)"],
             "chunk_type": "section", "section_number": "14",
             "text": "Section 14. Contracts not specifically enforceable.—The following contracts cannot be specifically enforced, namely:—(a) where a party to the contract has obtained substituted performance of contract in accordance with the provisions of section 20; (b) a contract, the performance of which involves the performance of a continuous duty which the court cannot supervise; (c) a contract which is so dependent on the personal qualifications of the parties that the court cannot enforce specific performance of its material terms; and (d) a contract which is in its nature determinable.",
             "metadata": {"act_short": "SR Act"}},
            {"hierarchy_path": ["SR Act", "Chapter VII", "Section 38 (Perpetual injunction)"],
             "chunk_type": "section", "section_number": "38",
             "text": "Section 38. Perpetual injunction when granted.—(1) Subject to the other provisions contained in or referred to by this Chapter, a perpetual injunction may be granted to the plaintiff to prevent the breach of an obligation existing in his favour, whether expressly or by implication. (3) When the defendant invades or threatens to invade the plaintiff's right to, or enjoyment of, property, the court may grant a perpetual injunction in cases where there is no standard for ascertaining the actual damage, or where compensation in money would not afford adequate relief, or where the injunction is necessary to prevent a multiplicity of judicial proceedings.",
             "metadata": {"act_short": "SR Act"}},
            {"hierarchy_path": ["SR Act", "Chapter VIII", "Section 41 (Injunction refused)"],
             "chunk_type": "section", "section_number": "41",
             "text": "Section 41. Injunction when refused.—An injunction cannot be granted—(a) to restrain any person from prosecuting a judicial proceeding pending at the institution of the suit in which the injunction is sought, unless such restraint is necessary to prevent a multiplicity of proceedings; (b) to restrain any person from instituting or prosecuting any proceeding in a court not subordinate to that from which the injunction is sought; (h) when equally efficacious relief can certainly be obtained by any other usual mode of proceeding except in case of breach of trust.",
             "metadata": {"act_short": "SR Act"}},
        ],
    },

    # ============= Limitation Act, 1963 =============
    {
        "doc": {
            "source_type": "central_statute", "title": "Limitation Act, 1963",
            "short_citation": "Limitation Act", "long_citation": "Limitation Act, 1963",
            "status": "in_force",
            "source_url": "https://indiacode.nic.in/handle/123456789/1565",
        },
        "chunks": [
            {"hierarchy_path": ["Limitation Act", "Part II", "Section 3 (Bar of limitation)"],
             "chunk_type": "section", "section_number": "3",
             "text": "Section 3. Bar of limitation.—(1) Subject to the provisions contained in sections 4 to 24 (inclusive), every suit instituted, appeal preferred, and application made after the prescribed period shall be dismissed although limitation has not been set up as a defence. Explanation: A suit is instituted, in ordinary cases, when the plaint is presented to the proper officer.",
             "metadata": {"act_short": "Limitation Act"}},
            {"hierarchy_path": ["Limitation Act", "Part III", "Section 5 (Extension of period)"],
             "chunk_type": "section", "section_number": "5",
             "text": "Section 5. Extension of prescribed period in certain cases.—Any appeal or any application, other than an application under any of the provisions of Order XXI of the Code of Civil Procedure, 1908, may be admitted after the prescribed period if the appellant or the applicant satisfies the court that he had sufficient cause for not preferring the appeal or making the application within such period.",
             "metadata": {"act_short": "Limitation Act"}},
            {"hierarchy_path": ["Limitation Act", "Schedule", "Article 113 (Residuary suit)"],
             "chunk_type": "section", "section_number": "Art 113",
             "text": "Article 113 of the Schedule.—Any suit for which no period of limitation is provided elsewhere in this Schedule: period of limitation is three years; time from which the period begins to run—when the right to sue accrues. (This is the residuary article applicable to suits not otherwise specified.)",
             "metadata": {"act_short": "Limitation Act"}},
        ],
    },

    # ============= Consumer Protection Act, 2019 =============
    {
        "doc": {
            "source_type": "central_statute", "title": "Consumer Protection Act, 2019",
            "short_citation": "CPA 2019", "long_citation": "Consumer Protection Act, 2019",
            "effective_from": "2020-07-20", "status": "in_force",
            "source_url": "https://indiacode.nic.in/handle/123456789/15256",
        },
        "chunks": [
            {"hierarchy_path": ["CPA 2019", "Chapter I", "Section 2(7) (Consumer)"],
             "chunk_type": "section", "section_number": "2(7)",
             "text": "Section 2(7). 'Consumer' means any person who—(i) buys any goods for a consideration which has been paid or promised or partly paid and partly promised; or (ii) hires or avails of any service for a consideration; and includes any user of such goods or any beneficiary of such services other than the person who buys/hires for consideration. Excludes a person who obtains such goods for resale or for any commercial purpose. Explanation.—'commercial purpose' does not include use by a person of goods bought and used by him exclusively for the purpose of earning his livelihood, by means of self-employment.",
             "metadata": {"act_short": "CPA 2019"}},
            {"hierarchy_path": ["CPA 2019", "Chapter IV", "Section 34 (District Commission jurisdiction)"],
             "chunk_type": "section", "section_number": "34",
             "text": "Section 34. Jurisdiction of District Commission.—(1) Subject to the other provisions of this Act, the District Commission shall have jurisdiction to entertain complaints where the value of the goods or services paid as consideration does not exceed fifty lakh rupees (₹50,00,000). (As amended by the Consumer Protection (Jurisdiction of District/State/National Commission) Rules, 2021, with effect from 30 December 2021.) (2) A complaint shall be instituted in the District Commission within the local limits of whose jurisdiction—(a) the opposite party resides or carries on business; or (d) the cause of action wholly or in part arises; or where the complainant resides or personally works for gain.",
             "metadata": {"act_short": "CPA 2019"}},
            {"hierarchy_path": ["CPA 2019", "Chapter VI", "Section 94 (E-commerce)"],
             "chunk_type": "section", "section_number": "94",
             "text": "Section 94. Measures to prevent unfair trade practices in e-commerce, direct selling.—For the purposes of preventing unfair trade practices in e-commerce, direct selling and also to protect the interest and rights of consumers, the Central Government may take such measures in the manner as may be prescribed. (Implemented through the Consumer Protection (E-Commerce) Rules, 2020, which mandate disclosure of seller details, country of origin, grievance officer, and prohibit manipulation of prices.)",
             "metadata": {"act_short": "CPA 2019"}},
        ],
    },

    # ============= Information Technology Act, 2000 =============
    {
        "doc": {
            "source_type": "central_statute", "title": "Information Technology Act, 2000",
            "short_citation": "IT Act", "long_citation": "Information Technology Act, 2000",
            "status": "in_force",
            "source_url": "https://indiacode.nic.in/handle/123456789/1999",
        },
        "chunks": [
            {"hierarchy_path": ["IT Act", "Chapter XI", "Section 66 (Computer-related offences)"],
             "chunk_type": "section", "section_number": "66",
             "text": "Section 66. Computer related offences.—If any person, dishonestly or fraudulently, does any act referred to in section 43, he shall be punishable with imprisonment for a term which may extend to three years or with fine which may extend to five lakh rupees or with both. (Section 43 covers unauthorised access, downloading, virus introduction, denial of service, etc.)",
             "metadata": {"act_short": "IT Act"}},
            {"hierarchy_path": ["IT Act", "Chapter XI", "Section 66A (Struck down — Shreya Singhal)"],
             "chunk_type": "section", "section_number": "66A",
             "text": "Section 66A.—STRUCK DOWN as unconstitutional in Shreya Singhal v. Union of India (2015) 5 SCC 1 (24 Mar 2015) for being violative of Article 19(1)(a) and not saved by Article 19(2). It penalised sending offensive messages through communication services, etc., and was held void in its entirety. Police continue to register cases under it occasionally; the Supreme Court has repeatedly directed that no such FIR can be registered.",
             "metadata": {"act_short": "IT Act", "treatment_status": "struck_down"}},
            {"hierarchy_path": ["IT Act", "Chapter XI", "Section 66E (Privacy)"],
             "chunk_type": "section", "section_number": "66E",
             "text": "Section 66E. Punishment for violation of privacy.—Whoever, intentionally or knowingly captures, publishes or transmits the image of a private area of any person without his or her consent, under circumstances violating the privacy of that person, shall be punished with imprisonment which may extend to three years or with fine not exceeding two lakh rupees, or with both.",
             "metadata": {"act_short": "IT Act"}},
            {"hierarchy_path": ["IT Act", "Chapter XI", "Section 67 (Obscene material)"],
             "chunk_type": "section", "section_number": "67",
             "text": "Section 67. Punishment for publishing or transmitting obscene material in electronic form.—Whoever publishes or transmits or causes to be published or transmitted in the electronic form, any material which is lascivious or appeals to the prurient interest or if its effect is such as to tend to deprave and corrupt persons who are likely, having regard to all relevant circumstances, to read, see or hear the matter contained or embodied in it, shall be punished on first conviction with imprisonment of either description for a term which may extend to three years and with fine which may extend to five lakh rupees and in the event of a second or subsequent conviction with imprisonment of either description for a term which may extend to five years and also with fine which may extend to ten lakh rupees.",
             "metadata": {"act_short": "IT Act"}},
            {"hierarchy_path": ["IT Act", "Chapter XII", "Section 79 (Intermediary safe harbour)"],
             "chunk_type": "section", "section_number": "79",
             "text": "Section 79. Exemption from liability of intermediary in certain cases.—(1) Notwithstanding anything contained in any law for the time being in force but subject to the provisions of sub-sections (2) and (3), an intermediary shall not be liable for any third party information, data, or communication link made available or hosted by him. (3) The provisions of sub-section (1) shall not apply if—(a) the intermediary has conspired or abetted or aided or induced…the unlawful act; (b) upon receiving actual knowledge, or on being notified by the appropriate Government or its agency that any information, data or communication link residing in or connected to a computer resource controlled by the intermediary is being used to commit the unlawful act, the intermediary fails to expeditiously remove or disable access to that material on that resource without vitiating the evidence in any manner.",
             "metadata": {"act_short": "IT Act"}},
        ],
    },

    # ============= Patents Act, 1970 =============
    {
        "doc": {
            "source_type": "central_statute", "title": "Patents Act, 1970",
            "short_citation": "Patents Act", "long_citation": "Patents Act, 1970",
            "status": "in_force",
            "source_url": "https://indiacode.nic.in/handle/123456789/1392",
        },
        "chunks": [
            {"hierarchy_path": ["Patents Act", "Chapter II", "Section 3 (What are not inventions)"],
             "chunk_type": "section", "section_number": "3",
             "text": "Section 3. What are not inventions.—The following are not inventions within the meaning of this Act,—(d) the mere discovery of a new form of a known substance which does not result in the enhancement of the known efficacy of that substance or the mere discovery of any new property or new use for a known substance or of the mere use of a known process, machine or apparatus unless such known process results in a new product or employs at least one new reactant; (k) a mathematical or business method or a computer programme per se or algorithms; (p) an invention which in effect, is traditional knowledge or which is an aggregation or duplication of known properties of traditionally known component or components.",
             "metadata": {"act_short": "Patents Act"}},
            {"hierarchy_path": ["Patents Act", "Chapter II", "Section 2(1)(j) (Invention)"],
             "chunk_type": "section", "section_number": "2(1)(j)",
             "text": "Section 2(1)(j). 'Invention' means a new product or process involving an inventive step and capable of industrial application. 'Inventive step' (sec 2(1)(ja)) means a feature of an invention that involves technical advance as compared to the existing knowledge or having economic significance or both and that makes the invention not obvious to a person skilled in the art.",
             "metadata": {"act_short": "Patents Act"}},
            {"hierarchy_path": ["Patents Act", "Chapter XI", "Section 48 (Rights of patentee)"],
             "chunk_type": "section", "section_number": "48",
             "text": "Section 48. Rights of patentees.—Subject to the other provisions contained in this Act and the conditions specified in section 47, a patent granted under this Act shall confer upon the patentee—(a) where the subject matter of the patent is a product, the exclusive right to prevent third parties, who do not have his consent, from the act of making, using, offering for sale, selling or importing for those purposes that product in India; (b) where the subject matter of the patent is a process, the exclusive right to prevent third parties from the act of using that process, and from the act of using, offering for sale, selling or importing for those purposes the product obtained directly by that process in India.",
             "metadata": {"act_short": "Patents Act"}},
            {"hierarchy_path": ["Patents Act", "Chapter XVI", "Section 84 (Compulsory licence)"],
             "chunk_type": "section", "section_number": "84",
             "text": "Section 84. Compulsory licences.—(1) At any time after the expiration of three years from the date of the grant of a patent, any person interested may make an application to the Controller for grant of compulsory licence on the patent on any of the following grounds, namely:—(a) that the reasonable requirements of the public with respect to the patented invention have not been satisfied; (b) that the patented invention is not available to the public at a reasonably affordable price; (c) that the patented invention is not worked in the territory of India.",
             "metadata": {"act_short": "Patents Act"}},
        ],
    },

    # ============= Trade Marks Act, 1999 =============
    {
        "doc": {
            "source_type": "central_statute", "title": "Trade Marks Act, 1999",
            "short_citation": "TM Act", "long_citation": "Trade Marks Act, 1999",
            "status": "in_force",
            "source_url": "https://indiacode.nic.in/handle/123456789/1993",
        },
        "chunks": [
            {"hierarchy_path": ["TM Act", "Chapter I", "Section 2(1)(zb) (Trade mark)"],
             "chunk_type": "section", "section_number": "2(1)(zb)",
             "text": "Section 2(1)(zb). 'Trade mark' means a mark capable of being represented graphically and which is capable of distinguishing the goods or services of one person from those of others and may include shape of goods, their packaging and combination of colours; and—(i) in relation to Chapter XII (other than section 107), a registered trade mark or a mark used in relation to goods or services for the purpose of indicating or so as to indicate a connection in the course of trade between the goods or services and some person having the right as proprietor to use the mark; and (ii) in relation to other provisions of this Act, a mark used or proposed to be used in relation to goods or services for the purpose of indicating or so to indicate a connection in the course of trade.",
             "metadata": {"act_short": "TM Act"}},
            {"hierarchy_path": ["TM Act", "Chapter IV", "Section 29 (Infringement)"],
             "chunk_type": "section", "section_number": "29",
             "text": "Section 29. Infringement of registered trade marks.—(1) A registered trade mark is infringed by a person who, not being a registered proprietor or a person using by way of permitted use, uses in the course of trade, a mark which is identical with, or deceptively similar to, the trade mark in relation to goods or services in respect of which the trade mark is registered and in such manner as to render the use of the mark likely to be taken as being used as a trade mark. (4) A registered trade mark is infringed by a person who…uses in the course of trade a mark which is identical with or similar to the registered trade mark; and is used in relation to goods or services which are not similar to those for which the trade mark is registered; and the registered trade mark has a reputation in India.",
             "metadata": {"act_short": "TM Act"}},
            {"hierarchy_path": ["TM Act", "Chapter IV", "Section 27 (Passing off)"],
             "chunk_type": "section", "section_number": "27",
             "text": "Section 27. No action for infringement of unregistered trade mark.—(1) No person shall be entitled to institute any proceeding to prevent, or to recover damages for, the infringement of an unregistered trade mark. (2) Nothing in this Act shall be deemed to affect rights of action against any person for passing off goods or services as the goods of another person or as services provided by another person, or the remedies in respect thereof.",
             "metadata": {"act_short": "TM Act"}},
        ],
    },

    # ============= Copyright Act, 1957 =============
    {
        "doc": {
            "source_type": "central_statute", "title": "Copyright Act, 1957",
            "short_citation": "Copyright Act", "long_citation": "Copyright Act, 1957",
            "status": "in_force",
            "source_url": "https://indiacode.nic.in/handle/123456789/1367",
        },
        "chunks": [
            {"hierarchy_path": ["Copyright Act", "Chapter III", "Section 13 (Works in which copyright subsists)"],
             "chunk_type": "section", "section_number": "13",
             "text": "Section 13. Works in which copyright subsists.—(1) Subject to the provisions of this section and the other provisions of this Act, copyright shall subsist throughout India in the following classes of works, that is to say,—(a) original literary, dramatic, musical and artistic works; (b) cinematograph films; and (c) sound recording.",
             "metadata": {"act_short": "Copyright Act"}},
            {"hierarchy_path": ["Copyright Act", "Chapter III", "Section 14 (Meaning of copyright)"],
             "chunk_type": "section", "section_number": "14",
             "text": "Section 14. Meaning of copyright.—For the purposes of this Act, 'copyright' means the exclusive right subject to the provisions of this Act, to do or authorise the doing of any of the following acts in respect of a work or any substantial part thereof, namely:—in the case of a literary, dramatic or musical work—(i) to reproduce the work in any material form including storing of it in any medium by electronic means; (ii) to issue copies of the work to the public; (iii) to perform the work in public, or communicate it to the public; (iv) to make any cinematograph film or sound recording in respect of the work; (v) to make any translation or adaptation of the work.",
             "metadata": {"act_short": "Copyright Act"}},
            {"hierarchy_path": ["Copyright Act", "Chapter XI", "Section 52 (Fair dealing)"],
             "chunk_type": "section", "section_number": "52",
             "text": "Section 52. Certain acts not to be infringement of copyright.—(1) The following acts shall not constitute an infringement of copyright, namely:—(a) a fair dealing with any work, not being a computer programme, for the purposes of—(i) private or personal use, including research; (ii) criticism or review, whether of that work or of any other work; (iii) the reporting of current events and current affairs, including the reporting of a lecture delivered in public.",
             "metadata": {"act_short": "Copyright Act"}},
            {"hierarchy_path": ["Copyright Act", "Chapter XII", "Section 63 (Offence)"],
             "chunk_type": "section", "section_number": "63",
             "text": "Section 63. Offence of infringement of copyright or other rights conferred by this Act.—Any person who knowingly infringes or abets the infringement of—(a) the copyright in a work, or (b) any other right conferred by this Act except the right conferred by section 53A, shall be punishable with imprisonment for a term which shall not be less than six months but which may extend to three years and with fine which shall not be less than fifty thousand rupees but which may extend to two lakh rupees.",
             "metadata": {"act_short": "Copyright Act"}},
        ],
    },

    # ============= Bharatiya Sakshya Adhiniyam, 2023 =============
    {
        "doc": {
            "source_type": "central_statute", "title": "Bharatiya Sakshya Adhiniyam, 2023",
            "short_citation": "BSA", "long_citation": "Bharatiya Sakshya Adhiniyam, 2023",
            "effective_from": "2024-07-01", "status": "in_force",
            "source_url": "https://indiacode.nic.in/handle/123456789/2024",
        },
        "chunks": [
            {"hierarchy_path": ["BSA", "Chapter I", "Section 2 (Definitions)"],
             "chunk_type": "section", "section_number": "2",
             "text": "Section 2. Definitions.—(d) 'document' means any matter expressed or described upon any substance by means of letters, figures or marks, or by more than one of those means, intended to be used, or which may be used, as evidence; and includes electronic and digital records. Illustration: An e-mail, a server log, a screenshot, a CCTV recording stored on a hard disk, a WhatsApp message and a database entry are all 'documents'.",
             "metadata": {"act_short": "BSA"}},
            {"hierarchy_path": ["BSA", "Chapter VI", "Section 63 (Electronic records admissibility)"],
             "chunk_type": "section", "section_number": "63",
             "text": "Section 63. Admissibility of electronic records.—(1) Notwithstanding anything contained in this Adhiniyam, any information contained in an electronic record which is printed on paper, stored, recorded or copied in optical or magnetic media or semiconductor memory, produced by a computer or any communication device or otherwise stored, recorded or copied in any electronic form, shall be deemed to be also a document, if the conditions mentioned in this section are satisfied. (4) Such certificate shall identify the electronic record, describe the manner in which it was produced, and give such particulars of any device involved in the production of that electronic record. (Successor to IPC §65B; certificate is mandatory per Anvar P.V. v. P.K. Basheer.)",
             "metadata": {"act_short": "BSA", "successor_of": "IEA §65B"}},
            {"hierarchy_path": ["BSA", "Chapter VII", "Section 105 (Burden of proof)"],
             "chunk_type": "section", "section_number": "105",
             "text": "Section 105. Burden of proof.—The burden of proof in a suit or proceeding lies on that person who would fail if no evidence at all were given on either side. The burden of proving any particular fact lies on that person who wishes the Court to believe in its existence, unless it is provided by any law that the proof of that fact shall lie on any particular person.",
             "metadata": {"act_short": "BSA"}},
        ],
    },

    # ============= Constitution — additional Parts =============
    {
        "doc": {
            "source_type": "constitution", "title": "Constitution of India",
            "short_citation": "Constitution",
            "long_citation": "Constitution of India, 1950",
            "status": "in_force",
            "source_url": "https://www.mea.gov.in/Images/pdf1/Part1.pdf",
        },
        "chunks": [
            {"hierarchy_path": ["Constitution", "Part V", "Article 51A (Fundamental duties)"],
             "chunk_type": "article", "section_number": "51A",
             "text": "Article 51A. Fundamental duties.—It shall be the duty of every citizen of India—(a) to abide by the Constitution and respect its ideals and institutions, the National Flag and the National Anthem; (e) to promote harmony and the spirit of common brotherhood amongst all the people of India transcending religious, linguistic and regional or sectional diversities; (g) to protect and improve the natural environment including forests, lakes, rivers and wild life, and to have compassion for living creatures; (k) who is a parent or guardian to provide opportunities for education to his child or, as the case may be, ward between the age of six and fourteen years.",
             "metadata": {"part": "IVA"}},
            {"hierarchy_path": ["Constitution", "Part V", "Article 72 (President's pardon)"],
             "chunk_type": "article", "section_number": "72",
             "text": "Article 72. Power of President to grant pardons, etc.—(1) The President shall have the power to grant pardons, reprieves, respites or remissions of punishment or to suspend, remit or commute the sentence of any person convicted of any offence—(a) in all cases where the punishment or sentence is by a Court Martial; (b) in all cases where the punishment or sentence is for an offence against any law relating to a matter to which the executive power of the Union extends; (c) in all cases where the sentence is a sentence of death.",
             "metadata": {"part": "V"}},
            {"hierarchy_path": ["Constitution", "Part VI", "Article 161 (Governor's pardon)"],
             "chunk_type": "article", "section_number": "161",
             "text": "Article 161. Power of Governor to grant pardons, etc., and to suspend, remit or commute sentences in certain cases.—The Governor of a State shall have the power to grant pardons, reprieves, respites or remissions of punishment or to suspend, remit or commute the sentence of any person convicted of any offence against any law relating to a matter to which the executive power of the State extends.",
             "metadata": {"part": "VI"}},
            {"hierarchy_path": ["Constitution", "Part XI", "Article 245 (Extent of laws)"],
             "chunk_type": "article", "section_number": "245",
             "text": "Article 245. Extent of laws made by Parliament and by the Legislatures of States.—(1) Subject to the provisions of this Constitution, Parliament may make laws for the whole or any part of the territory of India, and the Legislature of a State may make laws for the whole or any part of the State. (2) No law made by Parliament shall be deemed to be invalid on the ground that it would have extra-territorial operation.",
             "metadata": {"part": "XI"}},
            {"hierarchy_path": ["Constitution", "Part XI", "Article 246 (Subject-matter of laws)"],
             "chunk_type": "article", "section_number": "246",
             "text": "Article 246. Subject-matter of laws made by Parliament and by the Legislatures of States.—(1) Notwithstanding anything in clauses (2) and (3), Parliament has exclusive power to make laws with respect to any of the matters enumerated in List I in the Seventh Schedule (Union List). (2) Notwithstanding anything in clause (3), Parliament, and, subject to clause (1), the Legislature of any State also, have power to make laws with respect to any of the matters enumerated in List III in the Seventh Schedule (Concurrent List). (3) Subject to clauses (1) and (2), the Legislature of any State has exclusive power to make laws for such State or any part thereof with respect to any of the matters enumerated in List II in the Seventh Schedule (State List).",
             "metadata": {"part": "XI"}},
            {"hierarchy_path": ["Constitution", "Part XIV", "Article 311 (Civil servants)"],
             "chunk_type": "article", "section_number": "311",
             "text": "Article 311. Dismissal, removal or reduction in rank of persons employed in civil capacities under the Union or a State.—(1) No person who is a member of a civil service of the Union or an all-India service or a civil service of a State or holds a civil post under the Union or a State shall be dismissed or removed by an authority subordinate to that by which he was appointed. (2) No such person as aforesaid shall be dismissed or removed or reduced in rank except after an inquiry in which he has been informed of the charges against him and given a reasonable opportunity of being heard in respect of those charges.",
             "metadata": {"part": "XIV"}},
            {"hierarchy_path": ["Constitution", "Part III", "Article 32 (Right to constitutional remedies)"],
             "chunk_type": "article", "section_number": "32",
             "text": "Article 32. Remedies for enforcement of rights conferred by this Part.—(1) The right to move the Supreme Court by appropriate proceedings for the enforcement of the rights conferred by this Part is guaranteed. (2) The Supreme Court shall have power to issue directions or orders or writs, including writs in the nature of habeas corpus, mandamus, prohibition, quo warranto and certiorari, whichever may be appropriate, for the enforcement of any of the rights conferred by this Part. (Dr. Ambedkar called Article 32 the 'heart and soul' of the Constitution.)",
             "metadata": {"part": "III"}},
        ],
    },

    # ============= POCSO Act, 2012 =============
    {
        "doc": {
            "source_type": "central_statute", "title": "Protection of Children from Sexual Offences Act, 2012",
            "short_citation": "POCSO Act",
            "long_citation": "Protection of Children from Sexual Offences Act, 2012",
            "status": "in_force",
            "source_url": "https://indiacode.nic.in/handle/123456789/2079",
        },
        "chunks": [
            {"hierarchy_path": ["POCSO Act", "Chapter II", "Section 3 (Penetrative sexual assault)"],
             "chunk_type": "section", "section_number": "3",
             "text": "Section 3. Penetrative sexual assault.—A person is said to commit 'penetrative sexual assault' if—(a) he penetrates his penis, to any extent, into the vagina, mouth, urethra or anus of a child or makes the child to do so with him or any other person; or (b) he inserts, to any extent, any object or a part of the body, not being the penis, into the vagina, the urethra or anus of the child or makes the child to do so with him or any other person.",
             "metadata": {"act_short": "POCSO Act"}},
            {"hierarchy_path": ["POCSO Act", "Chapter II", "Section 4 (Punishment)"],
             "chunk_type": "section", "section_number": "4",
             "text": "Section 4. Punishment for penetrative sexual assault.—(1) Whoever commits penetrative sexual assault shall be punished with imprisonment of either description for a term which shall not be less than ten years but which may extend to imprisonment for life, and shall also be liable to fine. (2) Whoever commits penetrative sexual assault on a child below sixteen years of age shall be punished with imprisonment for a term which shall not be less than twenty years, but which may extend to imprisonment for life, which shall mean imprisonment for the remainder of natural life of that person, and shall also be liable to fine.",
             "metadata": {"act_short": "POCSO Act"}},
        ],
    },

    # ============= NDPS Act, 1985 =============
    {
        "doc": {
            "source_type": "central_statute", "title": "Narcotic Drugs and Psychotropic Substances Act, 1985",
            "short_citation": "NDPS Act",
            "long_citation": "Narcotic Drugs and Psychotropic Substances Act, 1985",
            "status": "in_force",
            "source_url": "https://indiacode.nic.in/handle/123456789/1791",
        },
        "chunks": [
            {"hierarchy_path": ["NDPS Act", "Chapter IV", "Section 20 (Cannabis offences)"],
             "chunk_type": "section", "section_number": "20",
             "text": "Section 20. Punishment for contravention in relation to cannabis plant and cannabis.—Whoever, in contravention of any provision of this Act or any rule or order made or condition of licence granted thereunder—(a) cultivates any cannabis plant; or (b) produces, manufactures, possesses, sells, purchases, transports, imports inter-State, exports inter-State or uses cannabis, shall be punishable—(ii) where such contravention relates to commercial quantity, with rigorous imprisonment for a term which shall not be less than ten years but which may extend to twenty years and shall also be liable to fine which shall not be less than one lakh rupees but which may extend to two lakh rupees.",
             "metadata": {"act_short": "NDPS Act"}},
            {"hierarchy_path": ["NDPS Act", "Chapter IV", "Section 37 (Bail)"],
             "chunk_type": "section", "section_number": "37",
             "text": "Section 37. Offences to be cognizable and non-bailable.—(1) Notwithstanding anything contained in the Code of Criminal Procedure, 1973—(b) no person accused of an offence punishable for offences under section 19 or section 24 or section 27A and also for offences involving commercial quantity shall be released on bail or on his own bond unless—(i) the Public Prosecutor has been given an opportunity to oppose the application for such release, and (ii) where the Public Prosecutor opposes the application, the court is satisfied that there are reasonable grounds for believing that he is not guilty of such offence and that he is not likely to commit any offence while on bail.",
             "metadata": {"act_short": "NDPS Act"}},
        ],
    },

    # ============= FEMA, 1999 =============
    {
        "doc": {
            "source_type": "central_statute", "title": "Foreign Exchange Management Act, 1999",
            "short_citation": "FEMA", "long_citation": "Foreign Exchange Management Act, 1999",
            "status": "in_force",
            "source_url": "https://indiacode.nic.in/handle/123456789/1973",
        },
        "chunks": [
            {"hierarchy_path": ["FEMA", "Chapter II", "Section 3 (Dealing in foreign exchange)"],
             "chunk_type": "section", "section_number": "3",
             "text": "Section 3. Dealing in foreign exchange, etc.—Save as otherwise provided in this Act, rules or regulations made thereunder, or with the general or special permission of the Reserve Bank, no person shall—(a) deal in or transfer any foreign exchange or foreign security to any person not being an authorised person; (b) make any payment to or for the credit of any person resident outside India in any manner; (c) receive otherwise through an authorised person, any payment by order or on behalf of any person resident outside India in any manner.",
             "metadata": {"act_short": "FEMA"}},
            {"hierarchy_path": ["FEMA", "Chapter IV", "Section 13 (Penalties)"],
             "chunk_type": "section", "section_number": "13",
             "text": "Section 13. Penalties.—(1) If any person contravenes any provision of this Act, or contravenes any rule, regulation, notification, direction or order issued in exercise of the powers under this Act, or contravenes any condition subject to which an authorisation is issued by the Reserve Bank, he shall, upon adjudication, be liable to a penalty up to thrice the sum involved in such contravention where such amount is quantifiable, or up to two lakh rupees where the amount is not quantifiable, and where such contravention is a continuing one, further penalty which may extend to five thousand rupees for every day after the first day during which the contravention continues.",
             "metadata": {"act_short": "FEMA"}},
        ],
    },

    # ============= PMLA, 2002 =============
    {
        "doc": {
            "source_type": "central_statute", "title": "Prevention of Money Laundering Act, 2002",
            "short_citation": "PMLA", "long_citation": "Prevention of Money Laundering Act, 2002",
            "status": "in_force",
            "source_url": "https://indiacode.nic.in/handle/123456789/2031",
        },
        "chunks": [
            {"hierarchy_path": ["PMLA", "Chapter II", "Section 3 (Offence of money-laundering)"],
             "chunk_type": "section", "section_number": "3",
             "text": "Section 3. Offence of money-laundering.—Whosoever directly or indirectly attempts to indulge or knowingly assists or knowingly is a party or is actually involved in any process or activity connected with the proceeds of crime including its concealment, possession, acquisition or use and projecting or claiming it as untainted property shall be guilty of offence of money-laundering. Explanation (inserted 2019): for the removal of doubts, it is hereby clarified that…the process or activity connected with proceeds of crime is a continuing activity and continues till such time a person is directly or indirectly enjoying the proceeds of crime.",
             "metadata": {"act_short": "PMLA"}},
            {"hierarchy_path": ["PMLA", "Chapter II", "Section 4 (Punishment)"],
             "chunk_type": "section", "section_number": "4",
             "text": "Section 4. Punishment for money-laundering.—Whoever commits the offence of money-laundering shall be punishable with rigorous imprisonment for a term which shall not be less than three years but which may extend to seven years and shall also be liable to fine. Provided that where the proceeds of crime involved in money-laundering relates to any offence specified under paragraph 2 of Part A of the Schedule (NDPS), the provisions of this section shall have effect as if for the words 'which may extend to seven years', the words 'which may extend to ten years' had been substituted.",
             "metadata": {"act_short": "PMLA"}},
            {"hierarchy_path": ["PMLA", "Chapter III", "Section 5 (Attachment of property)"],
             "chunk_type": "section", "section_number": "5",
             "text": "Section 5. Attachment of property involved in money-laundering.—(1) Where the Director or any other officer not below the rank of Deputy Director authorised by the Director, has reason to believe (the reason for such belief to be recorded in writing), on the basis of material in his possession, that—(a) any person is in possession of any proceeds of crime; and (b) such proceeds of crime are likely to be concealed, transferred or dealt with in any manner which may result in frustrating any proceedings relating to confiscation of such proceeds of crime under this Chapter, he may, by order in writing, provisionally attach such property for a period not exceeding one hundred and eighty days from the date of the order.",
             "metadata": {"act_short": "PMLA"}},
            {"hierarchy_path": ["PMLA", "Chapter VII", "Section 45 (Bail)"],
             "chunk_type": "section", "section_number": "45",
             "text": "Section 45. Offences to be cognizable and non-bailable.—(1) Notwithstanding anything contained in the Code of Criminal Procedure, 1973, no person accused of an offence under this Act shall be released on bail or on his own bond unless—(i) the Public Prosecutor has been given an opportunity to oppose the application for such release; and (ii) where the Public Prosecutor opposes the application, the court is satisfied that there are reasonable grounds for believing that he is not guilty of such offence and that he is not likely to commit any offence while on bail. (Twin conditions; struck down as applied to 'arrest' in Nikesh Tarachand Shah; later restored by amendment.)",
             "metadata": {"act_short": "PMLA"}},
        ],
    },
]
