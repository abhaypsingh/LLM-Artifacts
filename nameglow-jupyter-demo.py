# Copy the NameGlow class code from the previous cell (or import it if saved as a module)
# Then run this code to test the functionality

# Initialize the NameGlow system (without external API)
nameglow = NameGlow(use_api=False)

# Test with your own name
my_name = "Alexander"  # Replace with any name you want to test
content = nameglow.generate_daily_content(my_name)

# Display the content visually in the notebook
nameglow.display_content(content)

# Print the raw content for debugging
print("\nRaw content generated:")
print(json.dumps(content, indent=2))

# Test with multiple names to see different results
test_names = ["Maria", "David", "Sophia", "James"]
print("\nTesting with multiple names:")

for name in test_names:
    print(f"\n--- Results for {name} ---")
    content = nameglow.generate_daily_content(name)
    # Show just the highlights without the full visual display
    print(f"Anagram: {content['anagram'].capitalize()} → Virtue: {content['virtue']}")
    print("Nicknames:")
    for nick in content['nicknames']:
        print(f"  • {nick['nickname']}: {nick['meaning']}")
    print(f"Reflection prompt: {content['reflection_prompt']}")
