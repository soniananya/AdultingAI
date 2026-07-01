from io import BytesIO
from pypdf import PdfReader
from app.models.structured_output_models import *
from app.services.llm import llm


# =====================================================
# PDF TEXT EXTRACTION
# =====================================================

def extract_text_from_pdf(
    file_bytes: bytes
) -> str:

    reader = PdfReader(
        BytesIO(file_bytes)
    )

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text



#============================================================


def extract_salary_slip_fields(
    text: str
) -> SalarySlipFields:

    structured_llm = llm.with_structured_output(
        SalarySlipFields
    )

    prompt = f"""
    Extract the following fields from the salary slip.

        Rules:
        - Return only information explicitly present.
        - If a field is missing, return null.
        - Do not guess.

        Document:

        {text}
        """

    result = structured_llm.invoke(
        prompt
    )

    return result



#===================================================================


def extract_offer_letter_fields(
    text: str
) -> OfferLetterFields:

    structured_llm = llm.with_structured_output(
        OfferLetterFields
    )

    prompt = f"""
    Extract the following fields from the offer letter.

    Rules:
    - Return only information explicitly present.
    - If a field is missing, return null.
    - Do not guess.

    Document:

    {text}
    """

    result = structured_llm.invoke(
        prompt
    )

    return result

#=====================offer analysis node==========================


def analyze_offer_letter(fields:OfferLetterFields)->OfferAnalysis:

    structured_llm=llm.with_structured_output(
        OfferAnalysis
    )
    prompt=f"""
        You are an expert offer letter reviewer.

        Analyze this offer letter.

        Offer Details:

        Employer:
        {fields.employer}

        CTC:
        {fields.ctc}

        Joining Date:
        {fields.joining_date}

        Notice Period:
        {fields.notice_period}

        Remote Policy:
        {fields.remote_policy}

        Tasks:

        1. Identify genuine red flags.

        Examples:
        - Notice period above 90 days
        - Extremely high variable pay
        - Bond clauses
        - Ambiguous compensation
        - Unclear remote work policy

        2. Generate practical negotiation tips.

        3. Set requires_hitl=true if:
        - Any red flags are found
        - User should review before profile updates

        Return structured output.
        """

    result = structured_llm.invoke(
        prompt
    )

    return result

#jd node==========================================================
def extract_jd_fields(
    text: str
) -> JDFields:

    structured_llm = (
        llm.with_structured_output(
            JDFields
        )
    )

    prompt = f"""
Extract information from this job description.

Rules:
- Return only information present in the JD.
- Do not invent skills.
- Put mandatory requirements in required_skills.
- Put optional requirements in nice_to_have_skills.
- Detect hiring red flags.

Possible red flags:
- Unpaid trial work
- Extremely broad responsibilities
- Unrealistic experience requirements
- Ambiguous compensation
- Excessive working hours
- Fake "startup hustle culture" language

Job Description:

{text}
"""

    result = structured_llm.invoke(
        prompt
    )

    return result