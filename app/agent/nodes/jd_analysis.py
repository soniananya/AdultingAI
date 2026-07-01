"""
JD Analysis Workflow

Nodes=

1. extract_jd_node- Extract structured information from a JD
2. analyse_resume_node- Compare resume against JD requirements
3. tailor_resume_node- Generate a role-specific tailored resume
4. build_prep_list_node- Generate interview preparation checklist

Graph Flow:
extract_jd
    ↓
analyse_resume
    ↓
tailor_resume
    ↓
build_prep_list

Outputs are stored as artifacts:
- Tailored Resume
- Interview Prep Checklist
"""


from app.services.extractor import (
    extract_jd_fields
)


def extract_jd_node(
    state
):

    jd_text = (
        state["messages"][-1].content
    )

    jd_requirements = (
        extract_jd_fields(
            jd_text
        )
    )

    return {

        "jd_text":
            jd_text,

        "jd_requirements":
            jd_requirements
    }



#=========================resume analysis====================
from app.services.storage import (
    download_file
)

from app.services.extractor import (
    extract_text_from_pdf
)

from app.services.llm import llm
from pydantic import BaseModel


class ResumeAnalysis(BaseModel):

    skill_gaps: list[str]
    keyword_mismatches: list[str]



def analyse_resume_node(
    state
):

    resume_url = (
        state["life_state"]
        .resume_url
    )

    pdf_bytes = (
        download_file(
            resume_url
        )
    )

    resume_text = (
        extract_text_from_pdf(
            pdf_bytes
        )
    )

    structured_llm = (
        llm.with_structured_output(
            ResumeAnalysis
        )
    )

    result = (
        structured_llm.invoke(
            f"""
Job Requirements:

{state["jd_requirements"]}

Resume:

{resume_text}

Identify:

1. Missing skills

2. Important keywords
   absent from resume
"""
        )
    )

    return {

        "resume_text":
            resume_text,

        "skill_gaps":
            result.skill_gaps,

        "keyword_mismatches":
            result.keyword_mismatches
    }




def tailor_resume_node(
    state
):

    prompt = f"""
You are a resume coach.

Job Requirements:

{state["jd_requirements"]}

Current Resume:

{state["resume_text"]}

Skill Gaps:

{state["skill_gaps"]}

Rewrite the resume.

Requirements:

- Improve keyword matching
- Emphasize relevant projects
- Keep truthful
- Output markdown
"""

    tailored_resume = (
        llm.invoke(
            prompt
        ).content
    )

    return {

        "tailored_resume":
            tailored_resume
    }



#===============prep list=======================
from pydantic import BaseModel


class PrepList(BaseModel):

    topics: list[str]

    likely_questions: list[str]

    resources: list[str]

def build_prep_list_node(
    state
):

    structured_llm = (
        llm.with_structured_output(
            PrepList
        )
    )

    result = (
        structured_llm.invoke(
            f"""
Job Requirements:

{state["jd_requirements"]}

Skill Gaps:

{state["skill_gaps"]}

Generate:

1. Topics to study

2. Likely interview questions

3. Resources to review
"""
        )
    )

    return {

        "prep_list":
            result.model_dump()
    }