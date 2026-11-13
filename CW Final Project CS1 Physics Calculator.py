
from dataclasses import dataclass
from drafter import *


# =====================================
# 1. DATACLASSES
# =====================================

@dataclass
class Formula:
    name: str
    topic: str
    equation: str
    description: str


@dataclass
class Calculation:
    calculation_name: str
    formula: str
    inputs: str
    result: float
    units: str


@dataclass
class State:
    selected_category: str
    user_inputs: list
    current_result: float
    calculation_history: list
    error_message: str
    result_formula: str
    result_name: str
    result_units: str


# =====================================
# 2. PHYSICS FORMULAS
# =====================================

formulas = [

    Formula("Velocity", "Motion", "v = d / t",
            "Distance divided by time."),

    Formula("Acceleration", "Motion", "a = (vf - vi) / t",
            "Change in velocity divided by time."),

    Formula("Final Velocity", "Motion", "vf = vi + a * t",
            "Initial velocity plus acceleration times time."),

    Formula("Newton's Second Law", "Forces", "F = m * a",
            "Mass multiplied by acceleration."),

    Formula("Weight", "Forces", "Fg = m * g",
            "Mass multiplied by gravity."),

    Formula("Kinetic Energy", "Energy", "KE = 0.5 * m * v**2",
            "Energy of motion."),

    Formula("Potential Energy", "Energy", "PE = m * g * h",
            "Mass multiplied by gravity and height."),

    Formula("Work", "Energy", "W = F * d",
            "Force multiplied by displacement."),

    Formula("Power", "Energy", "P = W / t",
            "Work divided by time."),

    Formula("Momentum", "Momentum", "p = m * v",
            "Mass multiplied by velocity."),

    Formula("Impulse", "Momentum", "J = F * t",
            "Force multiplied by time.")
]


# =====================================
# 3. HOME PAGE
# =====================================

@route
def index(state: State) -> Page:

    return Page(state, [

        Header("PhysiCalc"),

        Header("Physics Made Easier!"),

        "Welcome to PhysiCalc!",

        "Use this website to find physics equations, "
        "enter your known values, and calculate answers.",

        "--------------------------------",

        Header("Choose a Physics Category"),

        Button("Motion and Kinematics", motion_page),

        Button("Forces", forces_page),

        Button("Energy", energy_page),

        Button("Momentum", momentum_page),

        "--------------------------------",

        Header("Other Features"),

        Button("Open Physics Calculator", calculator_page),

        Button("Formula Library", formula_library),

        Button("Calculation History", history_page),

        Button("About PhysiCalc", about_page),

        "Learn Physics. Find Equations. Solve Problems."
    ])


# =====================================
# 4. MOTION PAGE
# =====================================

@route
def motion_page(state: State) -> Page:

    state.selected_category = "Motion"

    return Page(state, [

        Header("Motion and Kinematics"),

        "Calculate velocity, acceleration, and final velocity.",

        Header("Available Formulas"),

        "Velocity: v = d / t",

        "Acceleration: a = (vf - vi) / t",

        "Final Velocity: vf = vi + a * t",

        "--------------------------------",

        Button("Start Calculating", calculator_page),

        Button("Home", index)
    ])


# =====================================
# 5. FORCES PAGE
# =====================================

@route
def forces_page(state: State) -> Page:

    state.selected_category = "Forces"

    return Page(state, [

        Header("Forces Calculator"),

        "Calculate force and weight using physics equations.",

        Header("Available Formulas"),

        "Newton's Second Law: F = m * a",

        "Weight: Fg = m * g",

        "Gravity on Earth is approximately 9.81 m/s^2.",

        "--------------------------------",

        Button("Start Calculating", calculator_page),

        Button("Home", index)
    ])


# =====================================
# 6. ENERGY PAGE
# =====================================

@route
def energy_page(state: State) -> Page:

    state.selected_category = "Energy"

    return Page(state, [

        Header("Energy Calculator"),

        "Calculate kinetic energy, potential energy, work, and power.",

        Header("Available Formulas"),

        "Kinetic Energy: KE = 0.5 * m * v^2",

        "Potential Energy: PE = m * g * h",

        "Work: W = F * d",

        "Power: P = W / t",

        "--------------------------------",

        Button("Start Calculating", calculator_page),

        Button("Home", index)
    ])


# Momentum page

@route
def momentum_page(state: State) -> Page:

    state.selected_category = "Momentum"

    return Page(state, [

        Header("Momentum Calculator"),

        "Calculate momentum and impulse.",

        Header("Available Formulas"),

        "Momentum: p = m * v",

        "Impulse: J = F * t",

        "--------------------------------",

        Button("Start Calculating", calculator_page),

        Button("Home", index)
    ])


# Calculator page

@route
def calculator_page(state: State) -> Page:

    return Page(state, [

        Header("Physics Calculator"),

        "Choose your physics category:",

        SelectBox(
            "category",
            ["Motion", "Forces", "Energy", "Momentum"],
            state.selected_category
        ),

        "Choose the calculation:",

        SelectBox(
            "calculation",
            [
                "Velocity",
                "Acceleration",
                "Final Velocity",
                "Newton's Second Law",
                "Weight",
                "Kinetic Energy",
                "Potential Energy",
                "Work",
                "Power",
                "Momentum",
                "Impulse"
            ],
            "Velocity"
        ),

        Header("Enter Your Known Values"),

        "First value:",

        TextBox("value1"),

        "Second value:",

        TextBox("value2"),

        "Third value (if needed):",

        TextBox("value3"),

        "Check this box to save your calculation:",

        CheckBox("save_history", True),

        Button("Calculate Answer", calculate_result),

        Button("Home", index)
    ])


# Calculation function

@route
def calculate_result(
    state: State,
    category: str,
    calculation: str,
    value1: str,
    value2: str,
    value3: str,
    save_history: bool
) -> Page:

    state.selected_category = category

    try:

        if value1.strip() == "" or value2.strip() == "":
            raise ValueError("Please enter your first two values.")

        first = float(value1)
        second = float(value2)

        if value3.strip() == "":
            third = None
        else:
            third = float(value3)

        answer = 0
        equation = ""
        units = ""

        # MOTION

        if category == "Motion":

            if calculation == "Velocity":

                if second == 0:
                    raise ValueError("Time cannot equal zero.")

                answer = first / second
                equation = "v = d / t"
                units = "m/s"

            elif calculation == "Acceleration":

                if third is None or third == 0:
                    raise ValueError("Enter a nonzero time.")

                answer = (second - first) / third
                equation = "a = (vf - vi) / t"
                units = "m/s^2"

            elif calculation == "Final Velocity":

                if third is None:
                    raise ValueError("Enter the time.")

                answer = first + second * third
                equation = "vf = vi + a * t"
                units = "m/s"

            else:
                raise ValueError("Invalid motion calculation.")

        # FORCES

        elif category == "Forces":

            if calculation == "Newton's Second Law":

                answer = first * second
                equation = "F = m * a"
                units = "N"

            elif calculation == "Weight":

                answer = first * second
                equation = "Fg = m * g"
                units = "N"

            else:
                raise ValueError("Invalid force calculation.")

        # ENERGY

        elif category == "Energy":

            if calculation == "Kinetic Energy":

                answer = 0.5 * first * second ** 2
                equation = "KE = 0.5 * m * v^2"
                units = "J"

            elif calculation == "Potential Energy":

                if third is None:
                    raise ValueError("Enter the height.")

                answer = first * second * third
                equation = "PE = m * g * h"
                units = "J"

            elif calculation == "Work":

                answer = first * second
                equation = "W = F * d"
                units = "J"

            elif calculation == "Power":

                if second == 0:
                    raise ValueError("Time cannot equal zero.")

                answer = first / second
                equation = "P = W / t"
                units = "W"

            else:
                raise ValueError("Invalid energy calculation.")

        # MOMENTUM

        elif category == "Momentum":

            if calculation == "Momentum":

                answer = first * second
                equation = "p = m * v"
                units = "kg m/s"

            elif calculation == "Impulse":

                answer = first * second
                equation = "J = F * t"
                units = "N s"

            else:
                raise ValueError("Invalid momentum calculation.")

        else:
            raise ValueError("Choose a valid category.")

        # SAVE RESULT

        state.current_result = answer
        state.result_formula = equation
        state.result_name = calculation
        state.result_units = units

        state.user_inputs = [first, second]

        if third is not None:
            state.user_inputs.append(third)

        state.error_message = ""

        if save_history:

            new_calculation = Calculation(
                calculation,
                equation,
                str(state.user_inputs),
                answer,
                units
            )

            state.calculation_history.append(new_calculation)

    except ValueError as error:

        state.error_message = str(error)

    return results_page(state)


# Reulsts

@route
def results_page(state: State) -> Page:

    if state.error_message != "":

        return Page(state, [

            Header("Calculation Error"),

            state.error_message,

            Button("Try Again", calculator_page),

            Button("Home", index)
        ])

    return Page(state, [

        Header("Calculation Results"),

        Header(state.result_name),

        "Formula Used:",

        state.result_formula,

        "Values Entered:",

        str(state.user_inputs),

        "Your Answer:",

        str(round(state.current_result, 4))
        + " " + state.result_units,

        "--------------------------------",

        Button("Calculate Again", calculator_page),

        Button("View History", history_page),

        Button("Home", index)
    ])


# Calculation history

@route
def history_page(state: State) -> Page:

    history_items = [

        Header("Calculation History"),

        "Review your previous calculations."
    ]

    if len(state.calculation_history) == 0:

        history_items.append(
            "You have not saved any calculations yet."
        )

    else:

        for calculation in state.calculation_history:

            history_items.append(
                Header(calculation.calculation_name)
            )

            history_items.append(
                "Formula: " + calculation.formula
            )

            history_items.append(
                "Inputs: " + calculation.inputs
            )

            history_items.append(
                "Answer: " + str(round(calculation.result, 4))
                + " " + calculation.units
            )

            history_items.append(
                "--------------------------------"
            )

    history_items.append(
        Button("Back to Calculator", calculator_page)
    )

    history_items.append(
        Button("Home", index)
    )

    return Page(state, history_items)


# Formulas

@route
def formula_library(state: State) -> Page:

    formula_items = [

        Header("Physics Formula Library"),

        "Browse the equations available on PhysiCalc."
    ]

    for formula in formulas:

        formula_items.append(
            Header(formula.topic + ": " + formula.name)
        )

        formula_items.append(
            "Equation: " + formula.equation
        )

        formula_items.append(
            formula.description
        )

        formula_items.append(
            "--------------------------------"
        )

    formula_items.append(
        Button("Home", index)
    )

    return Page(state, formula_items)


# ABout page

@route
def about_page(state: State) -> Page:

    return Page(state, [

        Header("About PhysiCalc"),

        "PhysiCalc is a physics calculator designed "
        "to help students solve common physics problems.",

        Header("How to Use the Website"),

        "1. Choose a physics category.",

        "2. Select a calculation.",

        "3. Enter the values you already know.",

        "4. Click Calculate Answer.",

        "5. View your equation and answer.",

        "--------------------------------",

        "The website includes Motion, Forces, Energy, "
        "and Momentum.",

        Button("Home", index)
    ])


# Website start

start_server(State(

    selected_category="Motion",

    user_inputs=[],

    current_result=0.0,

    calculation_history=[],

    error_message="",

    result_formula="",

    result_name="",

    result_units=""
))
