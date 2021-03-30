data = {
  "status": "ok",
  "text": [
    [
      "etter"
    ],
    [
      "x* ae"
    ],
    [
      "| Insert Format Tools Add-ons Help Last edit was seconds ago"
    ],
    [
      "100%"
    ],
    [
      "Normal text"
    ],
    [
      "1"
    ],
    [
      "Tahoma, > 4 + BIUA #"
    ],
    [
      "1 2 a 4 5 6 es"
    ],
    [
      "It’s Fundraiser Time!"
    ],
    [
      "Dear 1B Parents,"
    ],
    [
      "My name is Elizabeth Evans (Eva's Mommy) and I will be your Sally Foster",
      "Fundraiser rep for 2020."
    ],
    [
      "Just a few important reminders and some news about this critical",
      "Madeleine Fundraiser:"
    ],
    [
      "4",
      "2"
    ],
    [
      "3."
    ],
    [
      "No"
    ],
    [
      "The sale has officially started, so please begin approaching friends and family.",
      "When you're finished with sales, return your form and money to Ms. James ASAP,",
      "even if it's before the due date."
    ],
    [
      "The final day to turn in your forms is September 25."
    ],
    [
      ". Internet, Internet, Internet! Encourage your customers to place Internet orders"
    ],
    [
      "and have their merchandise delivered directly to them — avoiding the form",
      "entirely!"
    ],
    [
      ". 50% of what you raise goes toward your $200 PSA Commitment, so go all out and"
    ],
    [
      "get the bulk of your commitment done now!"
    ],
    [
      ". Remember, no cash!",
      ". NEW: Sally Foster has provided a new form to cut down on errors and to ensure"
    ],
    [
      "customers get exactly what they want. Take a moment to get familiar with the",
      "new form, and contact me if you have any questions.",
      "You may need additional forms—there’s not as much room on this one. If",
      "so, they will be available at the office, or I can e-mail you a PDF."
    ],
    [
      " "
    ],
    [
      "I am here to help if you have any questions or need any assistance. Good",
      "luck and happy selling!"
    ]
  ]
}

results = str()
for val_array in data["text"]:
    for val in val_array:
        if len(val.strip()) != 0:
            #print(val)
            results = results + " " +  val

print(results)