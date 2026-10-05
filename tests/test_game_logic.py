from logic_utils import check_guess, parse_guess

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    ## FIXED a test bug in this function (and the next two), the test was failing because 
    ## the check_guess function was not correctly handling the output case
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"

def test_parse_valid_number():
    ok, value, err = parse_guess("42")
    assert ok and value == 42 and err is None

def test_parse_strips_spaces():
    ok, value, _ = parse_guess("  7 ")
    assert ok and value == 7

def test_parse_empty_input():
    ok, value, _ = parse_guess("")
    assert not ok and value is None

def test_parse_not_a_number():
    ok, _, _ = parse_guess("abc")
    assert not ok

def test_parse_rejects_decimals():
    # "12.9" used to be silently truncated to 12
    ok, _, _ = parse_guess("12.9")
    assert not ok

def test_parse_rejects_out_of_range():
    ok, _, err = parse_guess("21", low=1, high=20)
    assert not ok and "between 1 and 20" in err
