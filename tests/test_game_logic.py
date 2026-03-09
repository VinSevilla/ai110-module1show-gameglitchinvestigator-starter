from logic_utils import check_guess, update_score, parse_guess

#FIX: Added tests for check_guess and update_score functions to ensure game logic is correct.
def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"


def test_guess_with_string_secret():
    # glitch case: secret stored as string, numeric comparison should still work
    outcome, message = check_guess(9, "10")
    assert outcome == "Too Low"
    outcome, message = check_guess(11, "10")
    assert outcome == "Too High"


def test_update_score_incorrect():
    # score decreases by 5 on wrong guesses, floor at 0
    assert update_score(100, "Too High", 1) == 95
    assert update_score(5, "Too Low", 2) == 0


def test_update_score_win():
    # score remains unchanged on win
    assert update_score(50, "Win", 3) == 50


def test_update_score_drops_on_wrong():
    # start at 25, wrong guess reduces by 5
    assert update_score(25, "Too High", 1) == 20
    assert update_score(20, "Too Low", 2) == 15
    # never negative
    assert update_score(0, "Too Low", 3) == 0


def test_update_score_win_unchanged():
    # win should not change the score
    assert update_score(30, "Win", 1) == 30


def test_parse_guess_valid():
    # valid integer inputs
    ok, value, err = parse_guess("42")
    assert ok == True
    assert value == 42
    assert err is None

    # valid float input (should be converted to int)
    ok, value, err = parse_guess("42.0")
    assert ok == True
    assert value == 42
    assert err is None


def test_parse_guess_invalid():
    # empty string
    ok, value, err = parse_guess("")
    assert ok == False
    assert value is None
    assert err == "Enter a guess."

    # None input
    ok, value, err = parse_guess(None)
    assert ok == False
    assert value is None
    assert err == "Enter a guess."

    # non-numeric string
    ok, value, err = parse_guess("abc")
    assert ok == False
    assert value is None
    assert err == "That is not a number."
