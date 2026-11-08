
import re



def detect_gate_by_rules(description):
    text = description.lower().strip()
    text = " ".join(text.split())

    # Priority rules for common two-input descriptions

    # NOR: output LOW when at least one input is HIGH
    if (
        "at least one" in text
        and "high" in text
        and "low" in text
        and text.find("low") < text.find("at least one")
    ):
        return "NOR"

    # NAND: output HIGH when at least one input is LOW
    if (
        "at least one" in text
        and "low" in text
        and "high" in text
        and text.find("high") < text.find("at least one")
    ):
        return "NAND"

    # NOR: output HIGH only when both inputs are LOW
    if (
        "both" in text
        and "low" in text
        and "high" in text
        and "only" in text
        and text.find("high") < text.find("both")
    ):
        return "NOR"

    # XNOR: two matching inputs produce HIGH
    if (
        any(word in text for word in [
            "match", "equal", "identical", "same"
        ])
        and any(word in text for word in [
            "two", "both", "inputs", "values"
        ])
        and any(word in text for word in [
            "high", "true", "one", "1"
        ])
    ):
        return "XNOR"

    # NAND: output FALSE only when both inputs are active
    if (
        ("false" in text or "low" in text or "zero" in text)
        and "both" in text
        and any(word in text for word in [
            "enabled", "active", "high"
        ])
        and any(word in text for word in [
            "only", "exclusively"
        ])
    ):
        return "NAND"

    # OR: at least one HIGH input activates the output
    if (
        "at least one" in text
        and "low" not in text
    ):
        return "OR"

    # XNOR: two inputs match and output is HIGH
    if (
        any(word in text for word in [
            "match", "equal", "identical", "same"
        ])
        and any(word in text for word in [
            "two", "both", "inputs", "values"
        ])
        and any(word in text for word in [
            "high", "true", "one", "1"
        ])
    ):
        return "XNOR"

    # NAND: output is false only when both inputs are active
    if (
        ("false" in text or "low" in text or "zero" in text)
        and ("both" in text)
        and (
            "enabled" in text
            or "active" in text
            or "high" in text
            or "on" in text.split()
        )
        and (
            "only" in text
            or "exclusively" in text
        )
    ):
        return "NAND"

    # Recognize common OR gate descriptions
    if "at least one" in text:
        return "OR"


    def matches(*patterns):
        return any(
            re.search(pattern, text)
            for pattern in patterns
        )

    # Explicit gate names and operations
    explicit_patterns = [
        ("XNOR", r"\bxnor\b|\bexclusive nor\b"),
        ("XOR", r"\bxor\b|\bexclusive or\b"),
        ("NAND", r"\bnand\b|\binverse of and\b"),
        ("NOR", r"\bnor\b|\binverse of or\b"),
        ("NOT", r"\bnot gate\b|\binverter\b"),
        ("AND", r"\band gate\b|\blogical conjunction\b"),
        ("OR", r"\bor gate\b|\blogical disjunction\b"),
    ]

    for gate, pattern in explicit_patterns:
        if matches(pattern):
            return gate

    # Negated compound operations
    if matches(
        r"\bcomplement of a and b\b",
        r"\band result is inverted\b",
        r"\binverted logical conjunction\b",
    ):
        return "NAND"

    if matches(
        r"\bcomplement of a or b\b",
        r"\bor result is inverted\b",
        r"\binverted logical disjunction\b",
    ):
        return "NOR"

    # STEP 39: Handle output polarity first

    # Recognize descriptions involving matching inputs
    matching_inputs = matches(
        r"\binputs? (are |is )?(equal|identical|the same)\b",
        r"\binputs? (match|agree)\b",
        r"\binputs? do not differ\b",
        r"\binputs? (are |is )?matching\b",
        r"\binputs? match\b"
    )

    # Recognize descriptions involving different inputs
    different_inputs = matches(
        r"\binputs? (are |is )?(different|unequal)\b",
        r"\binputs? (differ|disagree)\b",
        r"\binputs? do not match\b",
        r"\binputs? (are |is )?not equal\b"
    )

    low_output = matches(
        r"\boutput is low\b",
        r"\boutput is zero\b",
        r"\boutput is false\b"
    )

    high_output = matches(
        r"\boutput is high\b",
        r"\boutput is one\b",
        r"\boutput is true\b"
    )

    if matching_inputs and low_output:
        return "XOR"

    if matching_inputs and high_output:
        return "XNOR"

    if different_inputs and low_output:
        return "XNOR"

    if different_inputs and high_output:
        return "XOR"

    # XOR: output high for unequal inputs
    # or low for equal inputs
    if matches(
        r"\b(inputs?|signals?|bits?) (are |is )?(different|unequal)\b",
        r"\binputs? (do not match|disagree|differ)\b",
        r"\binputs? (are |is )?not equal\b",
        r"\bexactly one input\b",
        r"\bonly one of the two inputs\b",
        r"\blow when inputs are equal\b",
        r"\bzero when (both )?inputs are (the same|equal)\b",
        r"\bhigh when inputs are not equal\b",
    ):
        return "XOR"

    # XNOR: output high for equal inputs
    # or low for unequal inputs
    if matches(
        r"\binputs? (are |is )?(equal|identical|the same)\b",
        r"\binputs? (match|agree)\b",
        r"\bboth high or both low\b",
        r"\bone if a and b are identical\b",
        r"\blow when inputs are different\b",
        r"\bzero when inputs are unequal\b",
    ):
        return "XNOR"

    # NAND
    if matches(
        r"\blow only when both inputs are high\b",
        r"\bzero only when both inputs are high\b",
        r"\bhigh unless both inputs are high\b",
        r"\bzero when both inputs are high\b",
        r"\blow when both (switches|inputs) are on\b",
    ):
        return "NAND"

    # NOR
    if matches(
        r"\bhigh only when both inputs are low\b",
        r"\bone only when both inputs are low\b",
        r"\blow if any input is high\b",
        r"\bone if a and b are zero\b",
        r"\bboth inputs are zero\b",
        r"\bboth conditions are false\b",
    ):
        return "NOR"

    # AND
    if matches(
        r"\bhigh only when both inputs are high\b",
        r"\bboth inputs must be (high|one)\b",
        r"\bboth conditions must be satisfied\b",
        r"\bhigh when both inputs are high\b",
        r"\bboth inputs are high\b",
    ):
        return "AND"

    # OR
    if matches(
        r"\bat least one input is high\b",
        r"\beither input\b",
        r"\bone or both inputs\b",
        r"\bany input being one\b",
        r"\bany condition is true\b",
        r"\bat least one condition must be satisfied\b",
    ):
        return "OR"

    # NOT: single-input inversion
    if matches(
        r"\bopposite of the input\b",
        r"\binvert the input\b",
        r"\bsingle input is inverted\b",
        r"\breverses the input\b",
        r"\bcomplement of a\b$",
    ):
        return "NOT"

    # No matching rule: use ML fallback later
    
    # STEP 40: Additional natural-language patterns

    # AND
    if matches(
        r"\blamp glows only if two buttons are pressed\b",
        r"\bboth switches must be closed\b",
        r"\boutput is high when both switches are on\b"
    ):
        return "AND"

    # OR
    if matches(
        r"\balarm rings if any sensor\b",
        r"\bone active signal is enough\b"
    ):
        return "OR"

    # NOT
    if matches(
        r"\bsingle bit changes from 0 to 1 or 1 to 0\b"
    ):
        return "NOT"

    # NAND
    if matches(
        r"\boutput is false when both conditions are true\b",
        r"\bresult is 0 only for binary combination 11\b"
    ):
        return "NAND"

    # NOR
    if matches(
        r"\boutput is true only if neither signal is active\b",
        r"\bresult is 1 only for binary combination 00\b"
    ):
        return "NOR"

    # XOR
    if matches(
        r"\bhigh when exactly one switch is pressed\b",
        r"\bdifferent binary values make the output true\b"
    ):
        return "XOR"

    # XNOR
    if matches(
        r"\bmatching input bits produce a true output\b",
        r"\boutput is high for 00 and 11\b"
    ):
        return "XNOR"

    return None


# STEP 42: Detect clearly unsupported descriptions

def detect_unsupported_description(description):
    text = " ".join(description.lower().split())

    unsupported_patterns = [
        "majority of three",
        "majority of 3",
        "three input majority",
        "three-input majority",
        "at least two of three",
        "at least 2 of 3",
        "half adder",
        "full adder",
        "multiplexer",
        "demultiplexer",
        "flip flop",
        "flip-flop",
        "decoder",
        "encoder",
        "counter",
        "shift register"
    ]

    for phrase in unsupported_patterns:
        if phrase in text:
            return True

    return False

