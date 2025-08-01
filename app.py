import streamlit as st
import random

st.set_page_config(page_title="Guess the Word!", page_icon="🤔")
st.title("🤔 Guess the Word!")
#game instruction
with st.expander("How to Play"):
    st.info(
        """
        - A secret word has been chosen, and you have 10 attempts to guess it.
        - **Guess a single letter:** Enter one letter to see if it's in the word.
        - **Guess the full word:** If you think you know the answer, type the full word to win instantly!
        - A wrong guess (either a letter or the full word) will cost you one attempt.
        """
    )
# Initialize the game state from the word bank
if 'word' not in st.session_state:
    word_bank = [
        'adventure', 'avocado', 'backpack', 'balloon', 'bicycle', 'boulevard',
        'brilliant', 'broccoli', 'butterfly', 'camera', 'carnival', 'castle',
        'cathedral', 'celebrate', 'champion', 'cheetah', 'chocolate', 'clumsy',
        'computer', 'courageous', 'crocodile', 'curious', 'diamond', 'discover',
        'dolphin', 'dream', 'elephant', 'enormous', 'explore', 'fantastic',
        'festival', 'friendly', 'galaxy', 'generous', 'giraffe', 'guitar',
        'happiness', 'harbor', 'harmony', 'hilarious', 'hurricane', 'imagine',
        'important', 'journey', 'juggle', 'kaleidoscope', 'keyboard', 'kitchen',
        'library', 'liberty', 'magnificent', 'marshmallow', 'meadow', 'memory',
        'microwave', 'mountain', 'mysterious', 'navigate', 'nostalgia',
        'observatory', 'organize', 'oxygen', 'pancake', 'paradox', 'peacock',
        'penguin', 'pineapple', 'pizza', 'puzzle', 'question', 'quasar',
        'rainbow', 'remember', 'rhythm', 'spectacular', 'spaghetti', 'sphinx',
        'squirrel', 'stadium', 'strawberry', 'sunflower', 'telescope',
        'treasure', 'umbrella', 'unique', 'vacation', 'vibrant', 'village',
        'volcano', 'waffle', 'waterfall', 'weather', 'whisper', 'wizard',
        'xylophone', 'yesterday', 'yogurt', 'zebra', 'zombie', 'zodiac'
    ]
    st.session_state.word = random.choice(word_bank)
    st.session_state.guessed_letters = []
    st.session_state.attempts = 10
    st.session_state.game_over = False

# --- Display game UI ---
display_word = " ".join([letter if letter in st.session_state.guessed_letters else "_" for letter in st.session_state.word])
st.header(display_word)
st.write(f"Attempts remaining: {st.session_state.attempts}")

# --- Game Logic ---
if not st.session_state.game_over:
    guess = st.text_input("Guess a letter or the full word:", key="guess_input").lower()

    if st.button("Guess", key="guess_button"):
        if guess and guess.isalpha():
            if len(guess) > 1:
                if guess == st.session_state.word:
                    # If correct, reveal all letters to trigger the win condition
                    st.session_state.guessed_letters = list(st.session_state.word)
                else:
                    st.session_state.attempts -= 1
                    st.error("That's not the right word! You lose an attempt.")
            
            elif len(guess) == 1:
                if guess in st.session_state.guessed_letters:
                    st.warning(f"You already guessed '{guess}'. Try another letter.")
                elif guess in st.session_state.word:
                    st.session_state.guessed_letters.append(guess)
                    st.success("Great guess!")
                else:
                    st.session_state.guessed_letters.append(guess)
                    st.session_state.attempts -= 1
                    st.error("Wrong guess!")
            
            # Check for win/loss (now applies to both guess types)
            if all(letter in st.session_state.guessed_letters for letter in st.session_state.word):
                st.session_state.game_over = True
            elif st.session_state.attempts == 0:
                st.session_state.game_over = True
            
            st.rerun() # Rerun to update the display
        else:
            st.warning("Please enter a valid guess (letters only).")

# --- Game Over Logic ---
if st.session_state.game_over:
    if st.session_state.attempts > 0:
        st.success(f"🎉 Congratulations! You guessed the word: **{st.session_state.word}**")
    else:
        st.error(f"😔 Game Over! The word was: **{st.session_state.word}**")
    
    if st.button("Play Again"):
        # A simple way to reset the game is to clear the specific state keys
        st.session_state.pop('word')
        st.session_state.pop('guessed_letters')
        st.session_state.pop('attempts')
        st.session_state.pop('game_over')
        st.rerun()
