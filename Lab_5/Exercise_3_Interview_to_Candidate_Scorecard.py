from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
import os

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=os.environ["GROQ_API_KEY"]
)


# Step 1: Structured output schema
class InterviewQA(BaseModel):
    question: str = Field(
        description="The interview question asked"
    )
    answer: str = Field(
        description="The candidate's answer to the question"
    )


class InterviewData(BaseModel):
    question_answers: list[InterviewQA] = Field(
        description="List of interview question and answer pairs"
    )


parser_step1 = PydanticOutputParser(
    pydantic_object=InterviewData
)


# Step 1: PromptTemplate
interview_prompt = PromptTemplate.from_template(
    """
Extract all interview question and answer pairs from the
following interview transcript.

Interview Transcript:
{transcript_text}

{format_instructions}
"""
).partial(
    format_instructions=parser_step1.get_format_instructions()
)


# Step 2: Structured output schema
class SkillEvaluation(BaseModel):
    skill: str = Field(
        description="The skill being evaluated"
    )
    demonstrated: bool = Field(
        description="Whether the candidate demonstrated the skill"
    )
    evidence_or_gap: str = Field(
        description="Evidence supporting the evaluation or the identified gap"
    )


class SkillEvaluationData(BaseModel):
    evaluations: list[SkillEvaluation] = Field(
        description="Skill evaluations for all requested skills"
    )


parser_step2 = PydanticOutputParser(
    pydantic_object=SkillEvaluationData
)


# Step 2: ChatPromptTemplate
skill_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a technical interviewer evaluating skill evidence."
        ),
        (
            "user",
            """
Evaluate the candidate's evidence against these skills:

Skills to assess:
{skills_to_assess}

Interview question and answer data:
{question_answers}

For each skill, determine whether the candidate demonstrated it.
Use only evidence from the structured interview question and answer data.

{format_instructions}
"""
        )
    ]
).partial(
    format_instructions=parser_step2.get_format_instructions()
)


# Step 3: Structured output schema
class ScorecardRow(BaseModel):
    skill: str = Field(
        description="The skill being assessed"
    )
    demonstrated: bool = Field(
        description="Whether the candidate demonstrated the skill"
    )
    evidence_or_gap: str = Field(
        description="Evidence or gap supporting the evaluation"
    )


class CandidateScorecard(BaseModel):
    scorecard: list[ScorecardRow] = Field(
        description="Final candidate scorecard containing one row for each skill"
    )
    overall_recommendation: str = Field(
        description="Overall hiring recommendation based on the skill evaluations"
    )


parser_step3 = PydanticOutputParser(
    pydantic_object=CandidateScorecard
)


# Step 3: ChatPromptTemplate
scorecard_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a hiring panel coordinator."
        ),
        (
            "user",
            """
Create the final candidate scorecard from the structured
skill evaluations below.

Skill Evaluations:
{skill_evaluations}

Include:
- Each assessed skill
- Whether it was demonstrated
- Evidence or gap
- Overall recommendation

Base the recommendation only on the structured skill evaluations.

{format_instructions}
"""
        )
    ]
).partial(
    format_instructions=parser_step3.get_format_instructions()
)


# Take input from user
print("Enter interview transcript.")
print("Type END on a new line when finished:")

transcript_lines = []

while True:
    line = input()

    if line == "END":
        break

    transcript_lines.append(line)

transcript_text = "\n".join(transcript_lines)

skills_to_assess = input(
    "Enter skills to assess (comma separated): "
)


# Step 1
step1_input = interview_prompt.invoke({
    "transcript_text": transcript_text
})

step1_response = llm.invoke(step1_input)

interview_data = parser_step1.invoke(step1_response)


# Convert question-answer objects into text
question_answers_text = "\n".join(
    [
        f"Question: {item.question}\nAnswer: {item.answer}"
        for item in interview_data.question_answers
    ]
)


# Step 2
step2_input = skill_prompt.invoke({
    "skills_to_assess": skills_to_assess,
    "question_answers": question_answers_text
})

step2_response = llm.invoke(step2_input)

skill_evaluations = parser_step2.invoke(step2_response)


# Convert skill evaluations into text
skill_evaluations_text = "\n".join(
    [
        f"Skill: {item.skill}\n"
        f"Demonstrated: {item.demonstrated}\n"
        f"Evidence/Gap: {item.evidence_or_gap}"
        for item in skill_evaluations.evaluations
    ]
)


# Step 3
step3_input = scorecard_prompt.invoke({
    "skill_evaluations": skill_evaluations_text
})

step3_response = llm.invoke(step3_input)

candidate_scorecard = parser_step3.invoke(step3_response)


# Display results
print("\nStep 1 - Interview Question and Answer Data:")
print(interview_data)

print("\nStep 2 - Skill Evaluations:")
print(skill_evaluations)

print("\nStep 3 - Candidate Scorecard:")
print(candidate_scorecard)
