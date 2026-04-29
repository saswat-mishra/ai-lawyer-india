"""Constitution of India — Parts III (Fundamental Rights) and IV (Directive
Principles), the most-cited sections in everyday legal practice. Sourced
faithfully from legislative.gov.in / India Code.
"""
from __future__ import annotations

from typing import Any

CONSTITUTION_DOC = {
    "source_type": "constitution", "title": "Constitution of India",
    "short_citation": "Constitution",
    "long_citation": "Constitution of India",
    "status": "in_force",
    "source_url": "https://legislative.gov.in/constitution-of-india/",
}


def _art(num: str, title: str, text: str) -> dict[str, Any]:
    return {
        "hierarchy_path": ["Constitution", "Part III/IV", f"Article {num}"],
        "chunk_type": "article",
        "section_number": num,
        "text": text,
        "metadata": {},
    }


CONSTITUTION_CHUNKS: list[dict[str, Any]] = [
    # ---- Part III (Fundamental Rights), Articles 12–35 ----
    _art("12", "Definition of State",
         "Article 12. Definition.—In this Part, unless the context otherwise requires, "
         "'the State' includes the Government and Parliament of India and the Government "
         "and the Legislature of each of the States and all local or other authorities "
         "within the territory of India or under the control of the Government of India."),
    _art("13", "Laws inconsistent with or in derogation of fundamental rights",
         "Article 13. Laws inconsistent with or in derogation of the fundamental rights.—"
         "(1) All laws in force in the territory of India immediately before the "
         "commencement of this Constitution, in so far as they are inconsistent with the "
         "provisions of this Part, shall, to the extent of such inconsistency, be void. "
         "(2) The State shall not make any law which takes away or abridges the rights "
         "conferred by this Part and any law made in contravention of this clause shall, "
         "to the extent of the contravention, be void. (3) 'law' includes any Ordinance, "
         "order, bye-law, rule, regulation, notification, custom or usage having in the "
         "territory of India the force of law."),
    _art("15", "Prohibition of discrimination",
         "Article 15. Prohibition of discrimination on grounds of religion, race, caste, "
         "sex or place of birth.—(1) The State shall not discriminate against any citizen "
         "on grounds only of religion, race, caste, sex, place of birth or any of them. "
         "(2) No citizen shall, on grounds only of religion, race, caste, sex, place of "
         "birth or any of them, be subject to any disability, liability, restriction or "
         "condition with regard to (a) access to shops, public restaurants, hotels and "
         "places of public entertainment; or (b) the use of wells, tanks, bathing ghats, "
         "roads and places of public resort maintained wholly or partly out of State funds. "
         "(3) Special provision for women and children. (4) Special provision for SCs/STs "
         "and socially and educationally backward classes. (5) EWS reservations as inserted "
         "by the 103rd Amendment, 2019."),
    _art("16", "Equality of opportunity in public employment",
         "Article 16. Equality of opportunity in matters of public employment.—(1) There "
         "shall be equality of opportunity for all citizens in matters relating to "
         "employment or appointment to any office under the State. (2) No citizen shall, "
         "on grounds only of religion, race, caste, sex, descent, place of birth, "
         "residence or any of them, be ineligible for, or discriminated against in respect "
         "of, any employment or office under the State. (4) Reservations for backward "
         "classes; (4A) reservation in promotion for SCs/STs; (6) up-to-10% reservation "
         "for economically weaker sections."),
    _art("17", "Abolition of untouchability",
         "Article 17. Abolition of Untouchability.—'Untouchability' is abolished and its "
         "practice in any form is forbidden. The enforcement of any disability arising "
         "out of 'Untouchability' shall be an offence punishable in accordance with law."),
    _art("18", "Abolition of titles",
         "Article 18. Abolition of titles.—(1) No title, not being a military or academic "
         "distinction, shall be conferred by the State. (2) No citizen of India shall "
         "accept any title from any foreign State."),
    _art("20", "Protection in respect of conviction for offences",
         "Article 20. Protection in respect of conviction for offences.—(1) No person "
         "shall be convicted of any offence except for violation of a law in force at the "
         "time of the commission of the act charged as an offence, nor be subjected to a "
         "penalty greater than that which might have been inflicted under the law in force "
         "at the time of the commission of the offence. (2) No person shall be prosecuted "
         "and punished for the same offence more than once. (3) No person accused of any "
         "offence shall be compelled to be a witness against himself."),
    _art("22", "Protection against arrest and detention",
         "Article 22. Protection against arrest and detention in certain cases.—(1) No "
         "person who is arrested shall be detained in custody without being informed, as "
         "soon as may be, of the grounds for such arrest nor shall he be denied the right "
         "to consult, and to be defended by, a legal practitioner of his choice. (2) Every "
         "person who is arrested and detained in custody shall be produced before the "
         "nearest magistrate within a period of twenty-four hours of such arrest excluding "
         "the time necessary for the journey from the place of arrest to the court of the "
         "magistrate and no such person shall be detained in custody beyond the said "
         "period without the authority of a magistrate."),
    _art("23", "Prohibition of traffic in human beings and forced labour",
         "Article 23. Prohibition of traffic in human beings and forced labour.—(1) "
         "Traffic in human beings and begar and other similar forms of forced labour are "
         "prohibited and any contravention of this provision shall be an offence "
         "punishable in accordance with law."),
    _art("24", "Prohibition of employment of children in factories",
         "Article 24. Prohibition of employment of children in factories, etc.—No child "
         "below the age of fourteen years shall be employed to work in any factory or mine "
         "or engaged in any other hazardous employment."),
    _art("25", "Freedom of conscience and religion",
         "Article 25. Freedom of conscience and free profession, practice and propagation "
         "of religion.—(1) Subject to public order, morality and health and to the other "
         "provisions of this Part, all persons are equally entitled to freedom of "
         "conscience and the right freely to profess, practise and propagate religion."),
    _art("26", "Freedom to manage religious affairs",
         "Article 26. Freedom to manage religious affairs.—Subject to public order, "
         "morality and health, every religious denomination or any section thereof shall "
         "have the right (a) to establish and maintain institutions for religious and "
         "charitable purposes; (b) to manage its own affairs in matters of religion; "
         "(c) to own and acquire movable and immovable property; and (d) to administer "
         "such property in accordance with law."),
    _art("28", "Freedom from religious instruction in educational institutions",
         "Article 28. Freedom as to attendance at religious instruction or religious "
         "worship in certain educational institutions.—(1) No religious instruction shall "
         "be provided in any educational institution wholly maintained out of State funds."),
    _art("29", "Protection of interests of minorities",
         "Article 29. Protection of interests of minorities.—(1) Any section of the "
         "citizens residing in the territory of India or any part thereof having a "
         "distinct language, script or culture of its own shall have the right to "
         "conserve the same. (2) No citizen shall be denied admission into any educational "
         "institution maintained by the State or receiving aid out of State funds on "
         "grounds only of religion, race, caste, language or any of them."),
    _art("30", "Right of minorities to establish educational institutions",
         "Article 30. Right of minorities to establish and administer educational "
         "institutions.—(1) All minorities, whether based on religion or language, shall "
         "have the right to establish and administer educational institutions of their "
         "choice."),

    # ---- Part IV (Directive Principles), Articles 36–51 (most-cited) ----
    _art("39", "Certain principles of policy",
         "Article 39. Certain principles of policy to be followed by the State.—The State "
         "shall, in particular, direct its policy towards securing—(a) that the citizens, "
         "men and women equally, have the right to an adequate means of livelihood; "
         "(b) that the ownership and control of the material resources of the community "
         "are so distributed as best to subserve the common good; (c) that the operation "
         "of the economic system does not result in the concentration of wealth and means "
         "of production to the common detriment; (d) that there is equal pay for equal "
         "work for both men and women; (e) that the health and strength of workers are "
         "not abused; (f) that children are given opportunities and facilities to develop "
         "in a healthy manner."),
    _art("39A", "Equal justice and free legal aid",
         "Article 39A. Equal justice and free legal aid.—The State shall secure that the "
         "operation of the legal system promotes justice, on a basis of equal opportunity, "
         "and shall, in particular, provide free legal aid, by suitable legislation or "
         "schemes or in any other way, to ensure that opportunities for securing justice "
         "are not denied to any citizen by reason of economic or other disabilities."),
    _art("41", "Right to work, education and public assistance",
         "Article 41. Right to work, to education and to public assistance in certain "
         "cases.—The State shall, within the limits of its economic capacity and "
         "development, make effective provision for securing the right to work, to "
         "education and to public assistance in cases of unemployment, old age, sickness "
         "and disablement, and in other cases of undeserved want."),
    _art("44", "Uniform civil code",
         "Article 44. Uniform civil code for the citizens.—The State shall endeavour to "
         "secure for the citizens a uniform civil code throughout the territory of India."),
    _art("45", "Provision for early childhood care and education",
         "Article 45. Provision for early childhood care and education to children below "
         "the age of six years.—The State shall endeavour to provide early childhood care "
         "and education for all children until they complete the age of six years."),
    _art("46", "Promotion of educational and economic interests of SCs/STs",
         "Article 46. Promotion of educational and economic interests of Scheduled Castes, "
         "Scheduled Tribes and other weaker sections.—The State shall promote with special "
         "care the educational and economic interests of the weaker sections of the people, "
         "and, in particular, of the Scheduled Castes and the Scheduled Tribes, and shall "
         "protect them from social injustice and all forms of exploitation."),
    _art("48", "Organisation of agriculture and animal husbandry",
         "Article 48. Organisation of agriculture and animal husbandry.—The State shall "
         "endeavour to organise agriculture and animal husbandry on modern and scientific "
         "lines and shall, in particular, take steps for preserving and improving the "
         "breeds, and prohibiting the slaughter, of cows and calves and other milch and "
         "draught cattle."),
    _art("48A", "Protection and improvement of environment",
         "Article 48A. Protection and improvement of environment and safeguarding of "
         "forests and wild life.—The State shall endeavour to protect and improve the "
         "environment and to safeguard the forests and wild life of the country."),
    _art("50", "Separation of judiciary from executive",
         "Article 50. Separation of judiciary from executive.—The State shall take steps "
         "to separate the judiciary from the executive in the public services of the State."),
    _art("51", "Promotion of international peace and security",
         "Article 51. Promotion of international peace and security.—The State shall "
         "endeavour to (a) promote international peace and security; (b) maintain just "
         "and honourable relations between nations; (c) foster respect for international "
         "law and treaty obligations in the dealings of organised peoples with one another; "
         "and (d) encourage settlement of international disputes by arbitration."),

    # ---- Part IVA (Fundamental Duties) ----
    _art("51A", "Fundamental duties",
         "Article 51A. Fundamental duties.—It shall be the duty of every citizen of India "
         "(a) to abide by the Constitution and respect its ideals and institutions, the "
         "National Flag and the National Anthem; (b) to cherish and follow the noble ideals "
         "which inspired our national struggle for freedom; (c) to uphold and protect the "
         "sovereignty, unity and integrity of India; (d) to defend the country and render "
         "national service when called upon to do so; (e) to promote harmony and the "
         "spirit of common brotherhood amongst all the people of India; (f) to value and "
         "preserve the rich heritage of our composite culture; (g) to protect and improve "
         "the natural environment; (h) to develop the scientific temper, humanism and the "
         "spirit of inquiry and reform; (i) to safeguard public property and to abjure "
         "violence; (j) to strive towards excellence in all spheres of individual and "
         "collective activity; (k) duty of parents to provide opportunities for education "
         "of children between 6 and 14 years."),
]


CONSTITUTION_SEED = {"doc": CONSTITUTION_DOC, "chunks": CONSTITUTION_CHUNKS}
