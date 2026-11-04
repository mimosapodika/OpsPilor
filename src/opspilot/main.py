from opspilot.classifier import classify_ticket

test_descriptions = [
    "My laptop keyboard is not working",
    "I received a suspicious password reset email",
    "The software application is running slowly",
    "Entire office internet is unavailable"
]

for description in test_descriptions:
    result = classify_ticket(description)

    print("\nDescription:", description)
    print("Classification:", result)