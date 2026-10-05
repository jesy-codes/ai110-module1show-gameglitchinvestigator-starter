# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?
- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

It wasn't easy to understand the goal of inputting a guess number at first. 
Then when I chose a number between 1-100, it kept saying go lower, even after inputting "1".
There is a clear bug after inputting the lowest number possible and the app still saying to go lower. The second thing was that after you win, and then click on "New game", although it looks like it's a new game it doesn't make any further assessment on the numbers guessed. 
Finally, the app was also showing the secret number (the winning number) in the debug info, not sure if this was on purpose. 


**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error | Suspected Code Location |
|-------|-------------------|-----------------|------------------------|-------------------------|
| 1|Assuming the secret number is 13, expected behavior is the app saying to go higher |The app says go lower | | `app.py` `check_guess()` lines 37-40: the hint messages are swapped (`guess > secret` returns "Go HIGHER", `else` returns "Go LOWER") |
|15 |Assuming the secret number is 13, expected behavior is the app saying to go lower | The app says go higher| | `app.py` `check_guess()` lines 37-40 (same swapped messages) |
|1,2,3,4 |Developer Debug Info should show 1,2,3,4 | Developer Debug Info shows 1,2,3| Developer Debug Info is always missing the last input tried | `app.py` lines 114-119 vs. 147-156: the debug expander is drawn *before* the submit handler appends the guess to `history`, so it always shows the previous run's state (Attempts, Score and "Attempts left" on line 111 are also one step behind) |
| click on new game after winning | being able to input more numbers | new numbers are ignored and the app continues saying "You already won. Start a new game to play again"| | `app.py` lines 134-138: the New Game handler never resets `st.session_state.status` back to `"playing"`, so lines 140-145 call `st.stop()`; it also doesn't clear `history` or `score` |
| 9, then 9 again (secret is 15) | The same guess always gets the same hint (9 < 15 → too low) | The hint changes between the two guesses ("Go LOWER", then "Go HIGHER"). On even attempts the secret is compared as text, so "9" > "15" counts as too high. Only shows up when the guess and secret have a different number of digits (2-9 or 100 vs. 15) | No error shown: the `TypeError: '>' not supported between instances of 'int' and 'str'` is caught silently by `except TypeError` | `app.py` lines 158-161 convert the secret to `str` on even attempts, so `guess > secret` on line 37 raises a `TypeError` and `check_guess()` falls into the text comparison at lines 41-47 |
| Click New Game while on Easy (range 1-20) | New secret is between 1 and 20 | New secret can be anything from 1 to 100 | | `app.py` line 136: `random.randint(1, 100)` ignores `low`/`high` for the chosen difficulty |
| Switch difficulty from Normal to Easy mid-game | A new secret inside the Easy range (1-20) | The old secret (e.g. 75) is kept, so it can be outside the range shown in the sidebar | | `app.py` lines 92-93: the secret is only created once and never regenerated when the difficulty changes |
| Select Hard difficulty | Hard has a larger range than Normal | Hard range is 1-50, smaller (easier) than Normal's 1-100 | | `app.py` `get_range_for_difficulty()` line 10 |
| Select Easy or Hard difficulty | Instructions show that difficulty's range | Message always says "Guess a number between 1 and 100" | | `app.py` line 110: range is hardcoded instead of using `low` and `high` |
| Start a fresh game on Normal (8 attempts) | "Attempts left: 8" and 8 guesses allowed | Shows "Attempts left: 7" and the game ends after 7 guesses; after New Game the count is different again | | `app.py` line 96 starts `attempts` at 1, but line 135 resets it to 0 |
| A wrong guess that is too high, on an even attempt | Score goes down for a wrong guess | Score goes **up** by 5 | | `app.py` `update_score()` lines 57-60; win points on line 52 also use `attempt_number + 1`, an extra off-by-one penalty |
| "abc" or an empty submit | Show an error without using up an attempt | Error is shown, but an attempt is used and "abc" is added to history | | `app.py` lines 148 and 152-153: `attempts` is incremented and history appended before checking `ok` |
| 500, -3, or 12.9 | Reject values outside the range / non-whole numbers | All accepted; 12.9 is silently truncated to 12 | | `app.py` `parse_guess()` lines 21-29: no range check, and `int(float(raw))` truncates decimals |
| Open "Developer Debug Info" | Secret stays hidden from the player | Secret number is displayed | | `app.py` line 115 (fine for debugging, but should be removed/hidden for real play) |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
Claude Code
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
Claude Code helped me figure out the TypeError fallback in the function check_guess(), and I couldn't figure out what input would fall into that line, but then it identified that lines at app.py:158-161 deliberately turned the secret into text on even attempts.
- Also, the AI helped me identify a bug in the test logic. The test was comparing the whole output, instead of just the first output of Too High or Too Low. We fixed this, so the test worked appropriately.

- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.
I asked Claude code to help me build the function for `parse_guess()` in `logic_utils.py` but when I tested it, it had a TypeError, because the low, and high parameters in parse_guess didn't have a value designated. 
---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
I tested the Streamlit app. I also ran the pytest tests. 
For the bug of an even attempt being turned into a string, I actually had AI help me figure out what I had to do for having that error. Basically, I had to input twice the same number to get a different answer. Then I just quickly changed the bug in the app.py file, lines 158-161.
- Describe at least one test you ran (manual or using pytest)
  and what it showed you about your code.
Tested 41 twice with a secret of 43. In the first attempt, I saw the hint was to go higher. Which is right. The second attempt, I was trying to see if the initial bug that converted int to strings, was fixed. And yes, once I inputted 41, it was fixed. 
- Did AI help you design or understand any tests? How?
Yes. It helped me figure out how we would get into the even attempt bug of turning an input from integer to string. 
---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
Rerun is when the app runs app.py again every time a user interacts with it.
Session refers to each user visit to the app. The information of this visit, such as the secret number to guess and the number of attempts, is stored in the session's data. So every time we interact with the app (as the code reruns), those variables are kept in the session, so the secret number stays the same and we can effectively find it.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
Building tests and refactoring functions.
- What is one thing you would do differently next time you work with AI on a coding task?
Ask to explain the structure of the app, and then, being more proactive in refactoring the functions. 
- In one or two sentences, describe how this project changed the way you think about AI generated code.
I'm pretty amazed by how well it can catch the logic between functions and files. We still need to be proactive in initiating the items that need attention, prioritizing the fixes from P0 to P3 and giving more instructions on how to refactor the functionality. 