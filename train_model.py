
import joblib
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

from sklearn.svm import LinearSVC

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.pipeline import FeatureUnion
# Training examples for each logic gate
data = {
    
    "AND": [
        "Output is high only when both inputs are high",
        "Both inputs must be one to get output one",
        "The output is true if A and B are true",
        "Both conditions must be satisfied",
        "Output is zero if any input is zero",
        "The result is one when A and B are one",
        "All inputs must be active",
        "Output is high when both switches are on",
        "The output is one only if both signals are one",
        "The circuit requires two active inputs",
        "Both sensors must detect a signal to activate the output",
        "The output becomes high if A and B are both high",
        "Two switches must be turned on simultaneously",
        "The output is low unless both inputs are high",
        "Both binary inputs need to be one",
        "The result is true only when both conditions hold",
        "The output activates when two requirements are met",
        "A security system activates if both sensors detect movement",
        "The light turns on only when both switches are closed",
        "Both signals must be present to produce a high output",
        "The output is one for input combination 11",
        "The output is zero for 00, 01 and 10",
        "The circuit performs logical conjunction",
        "A high output requires A and B to be high"
    ],

    
    "OR": [
        "Output is high when at least one input is high",
        "Either input can make the output one",
        "The output is true if A or B is true",
        "Output is zero only when both inputs are zero",
        "One or both inputs can be active",
        "Any input being one produces output one",
        "Output is high if either switch is on",
        "Only one active input is needed",
        "The result becomes one if at least one signal is one",
        "The output activates when any input is active",
        "Either A or B can produce a high output",
        "The circuit requires one or more active inputs",
        "A light turns on when either switch is pressed",
        "The output is high if one or both sensors detect movement",
        "At least one condition must be satisfied",
        "The output is zero when neither input is active",
        "One high input is sufficient for a high output",
        "The output is one for input combinations 01, 10 and 11",
        "The output is zero for input combination 00",
        "The circuit performs logical disjunction",
        "The output becomes active when A is one or B is one",
        "The result is true when any condition is true",
        "The output remains low only if both signals are low",
        "A warning activates if either sensor detects danger"
    ],

    
    "NOT": [
        "Output is the opposite of the input",
        "Invert the input signal",
        "Output is zero when input is one",
        "Output is one when input is zero",
        "The circuit reverses the input",
        "The output is the complement of A",
        "A single input is inverted",
        "Change high to low and low to high",
        "The output is always opposite to the input",
        "The circuit performs logical negation",
        "A high input produces a low output",
        "A low input produces a high output",
        "The input signal is complemented",
        "The output is the inverse of the input",
        "The circuit has one input and reverses its value",
        "When the input is true the output is false",
        "When the input is false the output is true",
        "The circuit converts binary one into binary zero",
        "The circuit converts binary zero into binary one",
        "The output becomes high when the input is low",
        "The output becomes low when the input is high",
        "A digital inverter changes the logic level",
        "The circuit produces the complement of a binary signal",
        "The output is the logical negation of the input"
    ],

    
    "NAND": [
        "Output is low only when both inputs are high",
        "The result is zero if A and B are one",
        "Output is the inverse of AND",
        "Both inputs high produce output low",
        "Output is high unless both inputs are high",
        "The AND result is inverted",
        "Output is one if any input is zero",
        "Only two high inputs produce zero",
        "The output is zero only for input combination 11",
        "The output is one for input combinations 00 01 and 10",
        "The circuit performs inverted logical conjunction",
        "The output becomes low when both switches are on",
        "A high output occurs when at least one input is low",
        "The result is false only if both conditions are true",
        "Both signals must be high to produce a low output",
        "The circuit combines AND operation with inversion",
        "The output is the complement of A AND B",
        "The output stays high except when both inputs are one",
        "When A and B are both true the output is false",
        "The output is high when either input is zero",
        "The gate produces zero only if both inputs are active",
        "A digital circuit gives low output when both sensors activate",
        "The result is one unless A and B are simultaneously one",
        "The output becomes zero when both binary inputs are high"
    ],

    
    "NOR": [
        "Output is high only when both inputs are low",
        "The result is one if A and B are zero",
        "Output is the inverse of OR",
        "Both inputs low produce output high",
        "Output is low if any input is high",
        "The OR result is inverted",
        "Neither input can be high for output one",
        "Only two low inputs produce one",
        "The output is one only for input combination 00",
        "The output is zero for input combinations 01 10 and 11",
        "The circuit performs inverted logical disjunction",
        "The output becomes high when both switches are off",
        "A high output occurs when neither input is active",
        "The result is true only if both conditions are false",
        "Both signals must be low to produce a high output",
        "The circuit combines OR operation with inversion",
        "The output is the complement of A OR B",
        "The output stays low whenever any input is one",
        "When A and B are both false the output is true",
        "The output is low when either input is one",
        "The gate produces one only if both inputs are inactive",
        "A digital circuit gives high output when neither sensor activates",
        "The result is zero unless A and B are simultaneously zero",
        "The output becomes one when both binary inputs are low"
    ],

    
    
    "XOR": [
        "Output is high when inputs are different",
        "Output is one if A and B are unequal",
        "Exactly one input must be high",
        "Different inputs produce output one",
        "Output is low when inputs are equal",
        "One input high and the other low gives one",
        "The result is true for unequal inputs",
        "Output is high when only one switch is on",
        "Output becomes one when A and B differ",
        "The two inputs must be different",
        "The output is one when inputs do not match",
        "Output is high for different binary inputs",
        "Only one of the two inputs should be one",
        "The result is high if the inputs are not equal",
        "Output is zero when both inputs are the same",
        "The output is true when exactly one input is true",
        "The gate detects inequality between two bits",
        "Output is high for input combinations 01 and 10",
        "The result is zero for input combinations 00 and 11",
        "The output is one when A differs from B",
        "The output is high if either A or B is high but not both",
        "The circuit performs exclusive logical OR",
        "The output activates when the input bits disagree",
        "The output is false when both switches have matching states"
    ],


    
    "XNOR": [
        "Output is high when inputs are equal",
        "Output is one if A and B are identical",
        "Both inputs must have the same value",
        "Equal inputs produce output one",
        "Output is low when inputs are different",
        "The result is true for matching inputs",
        "Both high or both low gives output one",
        "The output is one for identical signals",
        "Output becomes high when A and B match",
        "The two inputs must be equal",
        "The output is one when inputs are the same",
        "Output is high for identical binary inputs",
        "The result is high if the inputs are equal",
        "Output is zero when the inputs are unequal",
        "The output is true when both inputs agree",
        "The gate detects equality between two bits",
        "Output is high for input combinations 00 and 11",
        "The result is zero for input combinations 01 and 10",
        "The output is one when A equals B",
        "The output is high if both A and B are high or both are low",
        "The circuit performs exclusive NOR operation",
        "The output activates when the input bits agree",
        "The output is true when both switches have matching states",
        "The output is the complement of exclusive OR"
    ]

}


print("Training examples per gate:")
for gate, examples in data.items():
    print(gate, len(examples))

# Check dataset quality

from collections import defaultdict

sentence_labels = defaultdict(set)

for gate, examples in data.items():
    for sentence in examples:
        normalized = " ".join(sentence.lower().split())
        sentence_labels[normalized].add(gate)

conflicts = {
    sentence: gates
    for sentence, gates in sentence_labels.items()
    if len(gates) > 1
}

print("\n===== DATASET QUALITY CHECK =====")

print("Total examples:", sum(len(v) for v in data.values()))
print("Unique descriptions:", len(sentence_labels))
print("Conflicting descriptions:", len(conflicts))

for sentence, gates in conflicts.items():
    print("CONFLICT:", sentence, "->", sorted(gates))

# Prepare sentences and their correct gate labels
sentences = []
labels = []

for gate, examples in data.items():
    for sentence in examples:
        sentences.append(sentence)
        labels.append(gate)

# Split examples into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    sentences,
    labels,
    test_size=0.25,
    random_state=42,
    stratify=labels
)

# Check training and testing datasets

from collections import Counter

print("\n===== DATA SPLIT CHECK =====")

print("Total examples:", len(sentences))
print("Training examples:", len(X_train))
print("Testing examples:", len(X_test))

print("\nTraining examples per gate:")
print(dict(sorted(Counter(y_train).items())))

print("\nTesting examples per gate:")
print(dict(sorted(Counter(y_test).items())))

# Check whether identical sentences appear
# in both training and testing sets
train_set = {
    " ".join(sentence.lower().split())
    for sentence in X_train
}

test_set = {
    " ".join(sentence.lower().split())
    for sentence in X_test
}

overlap = train_set.intersection(test_set)

print("\nRepeated sentences across both sets:", len(overlap))

for sentence in sorted(overlap):
    print("Repeated:", sentence)

# Create the AI classification pipeline



# Improved AI model using character patterns


# STEP 32: Combine word and character features

model = Pipeline([
    ("features", FeatureUnion([
        ("word_features", TfidfVectorizer(
            analyzer="word",
            ngram_range=(1, 3),
            sublinear_tf=True
        )),
        ("character_features", TfidfVectorizer(
            analyzer="char_wb",
            ngram_range=(3, 5),
            sublinear_tf=True
        ))
    ])),
    ("classifier", LinearSVC(
        C=0.1,
        class_weight="balanced",
        max_iter=5000,
        random_state=42
    ))
])




# Train the AI
model.fit(X_train, y_train)

# Diagnose model performance

from sklearn.metrics import classification_report
from collections import Counter

print("\n===== MODEL DIAGNOSTICS =====")

# Check number of examples for each gate
print("\nTraining labels:")
print(Counter(y_train))

print("\nTesting labels:")
print(Counter(y_test))

# Check performance on training data
train_predictions = model.predict(X_train)

train_accuracy = accuracy_score(
    y_train,
    train_predictions
)

print(
    f"\nTraining Accuracy: {train_accuracy * 100:.2f}%"
)

# Check performance on unseen test data
test_predictions = model.predict(X_test)

test_accuracy = accuracy_score(
    y_test,
    test_predictions
)

print(
    f"Testing Accuracy: {test_accuracy * 100:.2f}%"
)

# Detailed performance for every gate
print("\nClassification Report:")

print(
    classification_report(
        y_test,
        test_predictions,
        zero_division=0
    )
)


# Test the AI
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)

print("AI Model Training Completed!")
print("Training examples:", len(X_train))
print("Testing examples:", len(X_test))
print(f"Test Accuracy: {accuracy * 100:.2f}%")

# Save the trained model
joblib.dump(model, "logic_gate_model.pkl")

print("Model saved as logic_gate_model.pkl")

print("\n--- Detailed Test Results ---")

for sentence, actual, predicted in zip(
    X_test, y_test, predictions
):
    print("\nSentence:", sentence)
    print("Correct Gate:", actual)
    print("AI Prediction:", predicted)

    if actual == predicted:
        print("Result: CORRECT")
    else:
        print("Result: WRONG")

# STEP 31: Analyze incorrect predictions

from sklearn.metrics import confusion_matrix
import pandas as pd

print("\n===== STEP 31: ERROR ANALYSIS =====")

# Predict all test descriptions
predictions = model.predict(X_test)

# Create confusion matrix
gate_names = [
    "AND", "OR", "NOT", "NAND",
    "NOR", "XOR", "XNOR"
]

cm = confusion_matrix(
    y_test,
    predictions,
    labels=gate_names
)

cm_table = pd.DataFrame(
    cm,
    index=gate_names,
    columns=gate_names
)

print("\nCONFUSION MATRIX")
print("Rows = Actual gates")
print("Columns = Predicted gates")
print(cm_table.to_string())

# Show incorrect predictions
print("\n===== INCORRECT PREDICTIONS =====")

wrong_count = 0

for sentence, actual, predicted in zip(
    X_test, y_test, predictions
):
    if actual != predicted:
        wrong_count += 1

        print(f"\nMistake {wrong_count}")
        print("Sentence:", sentence)
        print("Actual Gate:", actual)
        print("Predicted Gate:", predicted)

print("\nTotal incorrect predictions:", wrong_count)
print("Total test examples:", len(X_test))
