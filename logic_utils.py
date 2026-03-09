
#FIX: Corrected guessing range for each dfficulty level.
def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 50
    if difficulty == "Hard":
        return 1, 100
    return 1, 100


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low". Both inputs may be
    ints or numeric strings (the latter introduced by a deliberate glitch).

    We attempt numeric comparison first to avoid lexicographic errors like
    "9" > "10".
    """
    # coerce to integers when possible
    try:
        g_val = int(guess)
        s_val = int(secret)
    except Exception:
        g_val = guess
        s_val = secret

    if g_val == s_val:
        return "Win", "🎉 Correct!"

    try:
        if g_val > s_val:
            return "Too High", "📉 Go LOWER!"
        else:
            return "Too Low", "📈 Go HIGHER!"
    except TypeError:
        # fallback to string-based logic
        g_str = str(guess)
        s_str = str(secret)
        if g_str == s_str:
            return "Win", "🎉 Correct!"
        if g_str > s_str:
            return "Too High", "📉 Go LOWER!"
        return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int, max_score: int = None):
    """Update score based on outcome.

    Score starts at a max value (passed in or implied) and drops by 5 for each
    incorrect guess. Wins do not change the score further. Score never goes below
    zero.

    The optional `max_score` argument is unused here but kept for compatibility
    if callers choose to compute initial value elsewhere.
    """
    if outcome == "Win":
        # retain current score on win
        return current_score

    # incorrect guess, deduct 5 points but don't go negative
    new_score = current_score - 5
    if new_score < 0:
        new_score = 0
    return new_score
