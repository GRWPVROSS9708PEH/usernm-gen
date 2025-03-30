import streamlit as st
import random
import string
import time # For uniqueness generation timeout

# --- Word Lists ---

DEFAULT_ADJECTIVES = [
    "Quick", "Lazy", "Sleepy", "Nosy", "Hungry", "Clever", "Brave", "Shy",
    "Silent", "Happy", "Grumpy", "Lucky", "Eager", "Gentle", "Proud", "Silly",
    "Witty", "Zany", "Fuzzy", "Smooth", "Shiny", "Vast", "Tiny", "Icy", "Cozy",
    "Wild", "Calm", "Dark", "Bright", "Golden", "Rusty", "Hidden", "Ancient",
    "Spectral", "Cosmic", "Digital", "Quantum", "Arctic", "Urban", "Mystic"
]

DEFAULT_NOUNS = [
    "Fox", "Dog", "Cat", "Panda", "Tiger", "Lion", "Wolf", "Bear", "Rabbit",
    "Snake", "Eagle", "Shark", "Whale", "Squid", "Robot", "Ghost", "Ninja",
    "Wizard", "River", "Mountain", "Forest", "Desert", "Ocean", "Planet", "Star",
    "Comet", "Shadow", "Cipher", "Riddle", "Key", "Stone", "Echo", "Byte",
    "Nebula", "Droid", "Portal", "Dragon", "Elf", "Oracle", "Nomad", "Glacier"
]

# --- Themed Word Lists ---
THEMES = {
    "Default": (DEFAULT_ADJECTIVES, DEFAULT_NOUNS),
    "Fantasy": (
        ["Ancient", "Mystic", "Shadow", "Fell", "Noble", "Brave", "Grim", "Silent", "Golden", "Forgotten", "Whispering", "Iron", "Elven", "Dwarven"],
        ["Dragon", "Knight", "Castle", "Sword", "Spell", "Scroll", "Rune", "Goblin", "Orc", "Elf", "Dwarf", "Wizard", "Sorcerer", "Throne", "Quest", "Gate"]
    ),
    "Sci-Fi": (
        ["Cosmic", "Quantum", "Digital", "Astro", "Robotic", "Cyber", "Laser", "Plasma", "Future", "Android", "Stellar", "Void", "Hyper", "Galactic"],
        ["Nebula", "Droid", "Starship", "Planet", "Comet", "Wormhole", "Blaster", "Forcefield", "Data", "Pilot", "Explorer", "Alien", "Cyborg", "Station", "Core"]
    ),
    "Nature": (
        ["Silent", "Wild", "Green", "Ancient", "Whispering", "Sunlit", "Misty", "Stone", "River", "Forest", "Mountain", "Arctic", "Desert", "Coastal", "Verdant"],
        ["Wolf", "Eagle", "River", "Stone", "Peak", "Forest", "Grove", "Creek", "Flower", "Leaf", "Tree", "Root", "Moss", "Fauna", "Flora", "Canyon"]
    )
}


# --- Helper Function ---

def apply_case(username, case_choice):
    """Applies the chosen capitalization to the username."""
    if case_choice == 'lowercase':
        return username.lower()
    elif case_choice == 'UPPERCASE':
        return username.upper()
    elif case_choice == 'TitleCase':
        # Special handling for title case with separators to ensure each part is capitalized
        parts = []
        current_part = ""
        # Include common separators in the split logic
        for char in username:
            if char in ['_', '-', '.']:
                if current_part:
                    parts.append(current_part.capitalize())
                parts.append(char)
                current_part = ""
            else:
                current_part += char
        if current_part:
             parts.append(current_part.capitalize())
        return "".join(parts)
    else: # Default: No change (should match one of the above)
        return username

# --- Generation Functions ---

def generate_adj_noun(adj_list, noun_list, separator=''):
    """Generates an Adjective + Noun username."""
    adj = random.choice(adj_list)
    noun = random.choice(noun_list)
    return f"{adj}{separator}{noun}"

def generate_adj_noun_num(adj_list, noun_list, separator=''):
    """Generates an Adjective + Noun + Number username."""
    base = generate_adj_noun(adj_list, noun_list, separator=separator)
    number = random.randint(1, 999) # Adjust range if desired
    # Consistent separator use (optional)
    # return f"{base}{separator}{number}" if separator else f"{base}{number}"
    return f"{base}{number}" # Simpler: just append number

def generate_random_chars(length=8, use_lower=True, use_upper=True, use_digits=True, use_symbols=False):
    """Generates a username with random characters from selected pools."""
    characters = ""
    if use_lower:
        characters += string.ascii_lowercase
    if use_upper:
        characters += string.ascii_uppercase
    if use_digits:
        characters += string.digits
    if use_symbols:
        characters += string.punctuation # Be careful with symbols in usernames!

    if not characters: # Fallback if user selects nothing
        characters = string.ascii_lowercase + string.digits

    username = ''.join(random.choice(characters) for _ in range(length))
    return username

# --- Streamlit App UI ---

st.set_page_config(page_title="Username Generator", page_icon="👤", layout="wide")

st.title("👤 Anonymous Username Generator")
st.caption("Generate unique and random usernames to help protect your identity online.")

# --- Sidebar Controls ---
st.sidebar.header("⚙️ Generation Options")

gen_method = st.sidebar.radio(
    "Generation Method:",
    ("Adjective + Noun", "Adjective + Noun + Number", "Random Characters"),
    key="gen_method"
)

num_usernames = st.sidebar.number_input(
    "Number of Usernames:",
    min_value=1,
    max_value=100, # Set a reasonable max
    value=10,
    step=1,
    key="num_usernames"
)

separator_options = ['none', '_', '-', '.']
separator_choice = st.sidebar.selectbox(
    "Separator:",
    separator_options,
    index=0, # Default to 'none'
    key="separator",
    # Disable separator for random chars as it doesn't make sense there
    disabled=(gen_method == "Random Characters")
)
separator = separator_choice if separator_choice != 'none' else ''

case_options = ['lowercase', 'UPPERCASE', 'TitleCase', 'Original'] # Added Original
case_choice = st.sidebar.selectbox(
    "Capitalization:",
    case_options,
    index=2, # Default to TitleCase
    key="case"
)

# --- Method-Specific Options ---
char_length = 8 # Default
use_lower, use_upper, use_digits, use_symbols = (True, True, True, False) # Defaults for random

if gen_method == "Random Characters":
    st.sidebar.subheader("Random Character Options")
    char_length = st.sidebar.slider(
        "Username Length:",
        min_value=4,
        max_value=24,
        value=10,
        key="char_length"
    )
    use_lower = st.sidebar.checkbox("Include Lowercase (a-z)", value=True, key="use_lower")
    use_upper = st.sidebar.checkbox("Include Uppercase (A-Z)", value=True, key="use_upper")
    use_digits = st.sidebar.checkbox("Include Numbers (0-9)", value=True, key="use_digits")
    use_symbols = st.sidebar.checkbox("Include Symbols (!@#...)", value=False, key="use_symbols")
    # Warn about symbols
    if use_symbols:
        st.sidebar.warning("Symbols might not be allowed in all usernames!")
    # Ensure at least one character set is selected
    if not any([use_lower, use_upper, use_digits, use_symbols]):
        st.sidebar.error("Please select at least one character type.")
        # Force lowercase if nothing selected to avoid errors
        use_lower = True

elif gen_method in ["Adjective + Noun", "Adjective + Noun + Number"]:
    st.sidebar.subheader("Word List Theme")
    theme_choice = st.sidebar.selectbox(
        "Select Theme:",
        options=list(THEMES.keys()),
        index=0, # Default theme
        key="theme"
    )
    selected_adjectives, selected_nouns = THEMES[theme_choice]


# --- Generate Button ---
st.sidebar.markdown("---") # Separator line
generate_button = st.sidebar.button("✨ Generate Usernames", key="generate")

# --- Main Area Display ---
if generate_button:
    st.header("✅ Generated Usernames:")

    # Prevent generation if random chars has no types selected
    if gen_method == "Random Characters" and not any([use_lower, use_upper, use_digits, use_symbols]):
         st.error("Cannot generate random characters: No character types selected in sidebar.")
    else:
        generated_set = set()
        usernames_list = []
        max_attempts = num_usernames * 15 # Allow reasonable attempts to find unique names
        attempts = 0

        with st.spinner(f"Generating {num_usernames} unique usernames..."):
            start_time = time.time()
            while len(generated_set) < num_usernames and attempts < max_attempts:
                attempts += 1
                username_base = ""
                current_case = case_choice # Use selected case by default

                if gen_method == "Adjective + Noun":
                    username_base = generate_adj_noun(selected_adjectives, selected_nouns, separator)
                elif gen_method == "Adjective + Noun + Number":
                    username_base = generate_adj_noun_num(selected_adjectives, selected_nouns, separator)
                elif gen_method == "Random Characters":
                    username_base = generate_random_chars(char_length, use_lower, use_upper, use_digits, use_symbols)
                    # Apply case *after* generation for random chars if not 'Original'
                    if case_choice != 'Original':
                         final_username = apply_case(username_base, case_choice)
                    else:
                         final_username = username_base # Keep original mix for random

                # Apply case for word-based methods (unless 'Original')
                if gen_method != "Random Characters":
                    if case_choice != 'Original':
                        final_username = apply_case(username_base, case_choice)
                    else:
                        final_username = username_base # Keep original TitleCase from lists

                # Add to set if unique
                if final_username not in generated_set:
                    generated_set.add(final_username)
                    usernames_list.append(final_username)

                # Timeout protection
                if time.time() - start_time > 10: # 10 second timeout
                     st.warning("Timeout trying to generate unique names. Returning what was found.")
                     break


        if len(usernames_list) < num_usernames:
            st.warning(f"Could only generate {len(usernames_list)} unique usernames with the current settings after {attempts} attempts. Try different options or longer length.")

        if usernames_list:
            # Display as a numbered list
            st.markdown("---")
            cols = st.columns(2) # Display in two columns for better space usage
            half = (len(usernames_list) + 1) // 2
            with cols[0]:
                for i, name in enumerate(usernames_list[:half], 1):
                    st.write(f"{i}. `{name}`")
            with cols[1]:
                for i, name in enumerate(usernames_list[half:], half + 1):
                    st.write(f"{i}. `{name}`")
            st.markdown("---")


            # Prepare for download and copy
            usernames_text = "\n".join(usernames_list)

            # Display in a code block for easy copying
            st.subheader("📋 Copy List:")
            st.code(usernames_text, language="") # Use empty language for plain text look

            # Download button
            st.download_button(
                label="💾 Download List (.txt)",
                data=usernames_text,
                file_name=f"generated_usernames_{time.strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )
        else:
            st.error("No usernames were generated. Check your settings (especially for Random Characters).")

else:
    # Show placeholder or instructions if button not pressed
    st.info("Configure your desired username options in the sidebar and click 'Generate Usernames'.")
