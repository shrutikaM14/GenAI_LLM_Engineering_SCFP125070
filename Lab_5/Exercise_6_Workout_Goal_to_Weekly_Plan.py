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
class WorkoutData(BaseModel):
    goal_type: str = Field(
        description="The main fitness goal such as weight loss, muscle gain, strength, endurance, or general fitness"
    )
    fitness_level: str = Field(
        description="The person's fitness level such as beginner, intermediate, or advanced"
    )
    days_available: int = Field(
        description="Number of days per week available for workouts"
    )
    equipment_access: str = Field(
        description="Equipment available to the person"
    )


parser_step1 = PydanticOutputParser(
    pydantic_object=WorkoutData
)


# Step 1: PromptTemplate
goal_prompt = PromptTemplate.from_template(
    """
Extract the fitness goal, fitness level, number of available workout
days, and equipment access from the following workout goal description.

Workout Goal Description:
{fitness_goal_text}

Number of days per week:
{days_per_week}

{format_instructions}
"""
).partial(
    format_instructions=parser_step1.get_format_instructions()
)


# Take input from user
fitness_goal_text = input(
    "Enter your workout goal description: "
)

days_per_week = int(
    input("Enter number of days per week available: ")
)


# Step 1
step1_input = goal_prompt.invoke({
    "fitness_goal_text": fitness_goal_text,
    "days_per_week": days_per_week
})

step1_response = llm.invoke(step1_input)

workout_data = parser_step1.invoke(step1_response)


# Step 2: Structured output schema
class WorkoutDay(BaseModel):
    day: str = Field(
        description="The day of the week or workout day number"
    )
    workout: str = Field(
        description="The planned workout for that day"
    )
    duration: str = Field(
        description="Approximate workout duration"
    )


class WeeklyPlan(BaseModel):
    plan: list[WorkoutDay] = Field(
        description="Day-by-day weekly workout plan"
    )


parser_step2 = PydanticOutputParser(
    pydantic_object=WeeklyPlan
)


# Step 2: ChatPromptTemplate
plan_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a certified personal trainer."
        ),
        (
            "user",
            """
Create a weekly workout plan using only the structured workout
requirements provided below.

Goal Type: {goal_type}
Fitness Level: {fitness_level}
Days Available: {days_available}
Equipment Access: {equipment_access}

Create one workout entry for each available workout day.

The plan should include:
- Day
- Workout
- Approximate duration

Do not use information outside the structured workout requirements.

{format_instructions}
"""
        )
    ]
).partial(
    format_instructions=parser_step2.get_format_instructions()
)


# Step 2
step2_input = plan_prompt.invoke({
    "goal_type": workout_data.goal_type,
    "fitness_level": workout_data.fitness_level,
    "days_available": workout_data.days_available,
    "equipment_access": workout_data.equipment_access
})

step2_response = llm.invoke(step2_input)

weekly_plan = parser_step2.invoke(step2_response)


# Display results
print("\nStep 1 - Structured Workout Data:")
print(workout_data)

print("\nStep 2 - Weekly Workout Plan:")
print(weekly_plan)