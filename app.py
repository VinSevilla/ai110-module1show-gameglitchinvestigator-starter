import random
import streamlit as st

#FIX: Added missing imports for game logic functions.
from logic_utils import get_range_for_difficulty, parse_guess, check_guess, update_score

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

#FIX: Corrected the attempt limit for each difficulty
attempt_limit_map = {
    "Easy": 8,
    "Normal": 6,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")


#FIX:Regenerate secret and reset game if difficulty changed
if "current_difficulty" not in st.session_state or st.session_state.current_difficulty != difficulty:
    st.session_state.secret = random.randint(low, high)
    st.session_state.current_difficulty = difficulty
    # reset game state as if starting new game
    st.session_state.attempts = 0
    st.session_state.score = attempt_limit * 5
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.last_hint = ""

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

#FIX: Correctly displays attempts left interface using Copilot Agent mode
if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = attempt_limit * 5  # max score = 5 points per attempt allowed

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "last_hint" not in st.session_state:
    st.session_state.last_hint = ""

if "history" not in st.session_state:
    st.session_state.history = []

st.subheader("Make a guess")

st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

#FIX: rearranged debug expander to fix submit delay. 
#FIX: added st.rerun() to allow debug interface to remain in same location.
with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    # Display history with 1-based indexing
    history_display = [f"Guess {i+1}: {guess}" for i, guess in enumerate(st.session_state.history)]
    st.write("History:", history_display)

#FIX: input and controls wrapped in a form so Enter key works
with st.form("guess_form"):
    raw_guess = st.text_input(
        "Enter your guess:",
        key=f"guess_input_{difficulty}"
    )
    submit = st.form_submit_button("Submit Guess 🚀")

# new_game and show_hint remain outside form to trigger independently
col1, col2 = st.columns(2)
with col1:
    new_game = st.button("New Game 🔁")
with col2:
    show_hint = st.checkbox("Show hint", value=True)

# Display last hint if show_hint is enabled and there's an active game
if show_hint and st.session_state.status == "playing" and st.session_state.last_hint:
    st.warning(st.session_state.last_hint)

#FIX: added additional components to reset for new game
#FIX: secret is now generated on new game and when difficulty changes, instead of only on new game.
if new_game:
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    st.session_state.score = attempt_limit * 5
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.last_hint = ""
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.error(err)
    else:
        st.session_state.attempts += 1
        st.session_state.history.append(guess_int)

        if st.session_state.attempts % 2 == 0:
            secret = str(st.session_state.secret)
        else:
            secret = st.session_state.secret

        outcome, message = check_guess(guess_int, secret)

        st.session_state.last_hint = message

        if show_hint:
            st.warning(message)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )
            else:
                st.rerun()

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
