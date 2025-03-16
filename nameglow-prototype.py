import random
import itertools
import requests
import json
from IPython.display import display, HTML
import pandas as pd
import matplotlib.pyplot as plt
from typing import List, Dict, Tuple, Optional

# If you have an API key for a language model (OpenAI, Anthropic, etc.)
# You can uncomment and use this section
# import openai
# openai.api_key = "your-api-key-here"
# or
# import anthropic
# client = anthropic.Client(api_key="your-anthropic-key-here")

class NameGlow:
    def __init__(self, use_api=False, api_type=None, api_key=None):
        """
        Initialize the NameGlow prototype
        
        Parameters:
        -----------
        use_api : bool
            Whether to use an external API for generating content
        api_type : str
            Type of API to use ('openai' or 'anthropic')
        api_key : str
            API key for the selected service
        """
        self.use_api = use_api
        self.api_type = api_type
        self.api_key = api_key
        
        # Predefined virtues for rule-based generation
        self.virtues = [
            "Kindness", "Courage", "Wisdom", "Patience", "Honesty", "Compassion",
            "Creativity", "Resilience", "Generosity", "Gratitude", "Humility",
            "Joy", "Serenity", "Mindfulness", "Balance", "Authenticity", "Wonder",
            "Empathy", "Integrity", "Determination", "Gentleness", "Presence"
        ]
        
        # Nickname patterns with associated meanings
        self.nickname_patterns = {
            "prefix_patterns": ["Sunny", "Starry", "Gentle", "Bright", "Noble", "Kind", "Wise", "Brave"],
            "suffix_patterns": ["heart", "soul", "mind", "spirit", "light", "smile", "spark"],
            "diminutives": ["ie", "y", "kins", "boo", "bean", "pop", "love"]
        }
        
        # Reflection prompts that subtly introduce no-self concepts
        self.reflection_prompts = [
            "How does today's anagram resonate with you in this moment?",
            "What part of you does this virtue illuminate today?",
            "If you embodied this virtue fully today, how might your experience change?",
            "Notice how this quality can feel both familiar and new at once.",
            "What happens when you imagine this quality as flowing through you rather than belonging to you?",
            "How might this virtue appear differently in different contexts of your life?",
            "If this quality were a guest visiting your home, how would you welcome it?",
            "What if this virtue isn't something you have, but something you participate in?",
            "How does this quality exist beyond the boundaries of what you call 'me'?",
            "What happens if you allow this virtue to be present without claiming it as yours?"
        ]
    
    def generate_anagrams(self, name: str, max_results: int = 5) -> List[str]:
        """
        Generate anagrams from a name, allowing minor letter modifications
        
        Parameters:
        -----------
        name : str
            The name to transform
        max_results : int
            Maximum number of anagrams to return
            
        Returns:
        --------
        List[str]
            List of anagram strings
        """
        # Convert to lowercase for processing
        name = name.lower().replace(" ", "")
        original_letters = list(name)
        
        # For demonstration, we'll implement a simple algorithm
        # that swaps, adds, or removes a single letter
        
        results = []
        
        # Try pure anagrams first
        for perm in itertools.permutations(name):
            anagram = ''.join(perm)
            if anagram != name and anagram not in results:
                results.append(anagram)
                if len(results) >= max_results:
                    return results
        
        # If we need more, try with letter modifications
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        
        # Try adding one letter
        for letter in alphabet:
            new_letters = original_letters + [letter]
            for perm in itertools.permutations(new_letters):
                anagram = ''.join(perm)
                if anagram != name and anagram not in results:
                    results.append(anagram)
                    if len(results) >= max_results:
                        return results
        
        # Try removing one letter if name is long enough
        if len(name) > 3:
            for i in range(len(original_letters)):
                new_letters = original_letters.copy()
                new_letters.pop(i)
                for perm in itertools.permutations(new_letters):
                    anagram = ''.join(perm)
                    if anagram not in results:
                        results.append(anagram)
                        if len(results) >= max_results:
                            return results
        
        return results[:max_results]
    
    def associate_virtue_with_anagram(self, anagram: str, name: str) -> str:
        """
        Associate a virtue with an anagram
        
        Parameters:
        -----------
        anagram : str
            The anagram to associate with a virtue
        name : str
            The original name
            
        Returns:
        --------
        str
            A virtue association
        """
        if self.use_api and self.api_key:
            return self._get_virtue_from_api(anagram, name)
        else:
            # Rule-based approach
            # Simple hash function to select a virtue
            hash_value = sum(ord(c) for c in anagram) % len(self.virtues)
            return self.virtues[hash_value]
    
    def _get_virtue_from_api(self, anagram: str, name: str) -> str:
        """Use AI API to get virtue associations"""
        try:
            if self.api_type == 'openai':
                # Using OpenAI
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[{
                        "role": "system", 
                        "content": "You are an expert in finding meaningful virtue associations in words."
                    },
                    {
                        "role": "user",
                        "content": f"Find a virtue or positive quality that could be associated with the word '{anagram}' which is derived from the name '{name}'. Respond with just the single virtue word."
                    }]
                )
                return response.choices[0].message.content.strip()
            
            elif self.api_type == 'anthropic':
                # Using Anthropic
                response = client.messages.create(
                    model="claude-3-opus-20240229",
                    max_tokens=10,
                    system="You are an expert in finding meaningful virtue associations in words.",
                    messages=[
                        {"role": "user", "content": f"Find a virtue or positive quality that could be associated with the word '{anagram}' which is derived from the name '{name}'. Respond with just the single virtue word."}
                    ]
                )
                return response.content[0].text.strip()
            
            else:
                return random.choice(self.virtues)
                
        except Exception as e:
            print(f"API error: {e}")
            return random.choice(self.virtues)
    
    def generate_nicknames(self, name: str, count: int = 3) -> List[Dict]:
        """
        Generate nicknames based on a name
        
        Parameters:
        -----------
        name : str
            The name to transform into nicknames
        count : int
            Number of nicknames to generate
            
        Returns:
        --------
        List[Dict]
            List of nickname dictionaries with name and meaning
        """
        if self.use_api and self.api_key:
            return self._get_nicknames_from_api(name, count)
        
        # Simple rule-based approach
        results = []
        name = name.lower()
        
        # First letter + diminutive
        for dim in self.nickname_patterns["diminutives"]:
            if len(results) < count:
                nickname = name[0] + dim
                meaning = f"Represents the essence of {name.capitalize()}'s spirit"
                results.append({"nickname": nickname.capitalize(), "meaning": meaning})
        
        # First syllable transformation
        if len(results) < count:
            if len(name) >= 3:
                syllable = name[:3]
                nickname = syllable + "ie"
                meaning = f"Captures the playful energy of {name.capitalize()}"
                results.append({"nickname": nickname.capitalize(), "meaning": meaning})
        
        # Prefix + part of name
        if len(results) < count:
            prefix = random.choice(self.nickname_patterns["prefix_patterns"])
            nickname = prefix + name[:3]
            meaning = f"Highlights the {prefix.lower()} nature within {name.capitalize()}"
            results.append({"nickname": nickname, "meaning": meaning})
        
        # Name + suffix
        if len(results) < count:
            suffix = random.choice(self.nickname_patterns["suffix_patterns"])
            nickname = name + suffix
            meaning = f"Celebrates the {suffix} that {name.capitalize()} brings to others"
            results.append({"nickname": nickname.capitalize(), "meaning": meaning})
        
        return results[:count]
    
    def _get_nicknames_from_api(self, name: str, count: int) -> List[Dict]:
        """Use AI API to generate nicknames"""
        results = []
        try:
            if self.api_type == 'openai':
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[{
                        "role": "system", 
                        "content": "You generate meaningful, positive nicknames based on people's names."
                    },
                    {
                        "role": "user",
                        "content": f"Generate {count} nicknames for someone named '{name}'. For each nickname, provide a short meaning that connects to a positive quality. Format as JSON array with 'nickname' and 'meaning' fields."
                    }]
                )
                results = json.loads(response.choices[0].message.content)
                
            elif self.api_type == 'anthropic':
                response = client.messages.create(
                    model="claude-3-opus-20240229",
                    max_tokens=250,
                    system="You generate meaningful, positive nicknames based on people's names.",
                    messages=[
                        {"role": "user", "content": f"Generate {count} nicknames for someone named '{name}'. For each nickname, provide a short meaning that connects to a positive quality. Format as JSON array with 'nickname' and 'meaning' fields."}
                    ]
                )
                results = json.loads(response.content[0].text)
                
        except Exception as e:
            print(f"API error: {e}")
            # Fall back to rule-based approach
            return self.generate_nicknames(name, count)
            
        return results
    
    def get_reflection_prompt(self) -> str:
        """Return a randomly selected reflection prompt"""
        return random.choice(self.reflection_prompts)
    
    def generate_daily_content(self, name: str) -> Dict:
        """
        Generate daily content for a user
        
        Parameters:
        -----------
        name : str
            The user's name
            
        Returns:
        --------
        Dict
            Dictionary with anagram, virtue, nicknames, and reflection prompt
        """
        # Get anagrams
        anagrams = self.generate_anagrams(name, max_results=3)
        
        # Select one anagram and associate virtue
        selected_anagram = anagrams[0] if anagrams else name[::-1]  # Fallback to reverse name
        virtue = self.associate_virtue_with_anagram(selected_anagram, name)
        
        # Generate nicknames
        nicknames = self.generate_nicknames(name, count=2)
        
        # Get reflection prompt
        reflection = self.get_reflection_prompt()
        
        return {
            "date": pd.Timestamp.now().strftime("%Y-%m-%d"),
            "name": name,
            "anagram": selected_anagram,
            "virtue": virtue,
            "nicknames": nicknames,
            "reflection_prompt": reflection,
            "alternative_anagrams": anagrams[1:] if len(anagrams) > 1 else []
        }
    
    def display_content(self, content: Dict):
        """
        Display the generated content in a visually appealing way in the notebook
        
        Parameters:
        -----------
        content : Dict
            The content to display
        """
        html = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; border-radius: 10px; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);">
            <h2 style="text-align: center; color: #4a6fa5;">NameGlow Daily Insight</h2>
            <p style="text-align: center; color: #666;">For {content['name']} on {content['date']}</p>
            
            <div style="background-color: white; border-radius: 8px; padding: 15px; margin: 15px 0; box-shadow: 0 2px 10px rgba(0,0,0,0.05);">
                <h3 style="color: #4a6fa5; margin-top: 0;">Your Anagram of the Day</h3>
                <p style="font-size: 28px; text-align: center; margin: 10px 0; color: #2c3e50;">{content['anagram'].capitalize()}</p>
                <p style="text-align: center; font-style: italic; color: #7f8c8d;">Embodying the virtue of <strong>{content['virtue']}</strong></p>
            </div>
            
            <div style="background-color: white; border-radius: 8px; padding: 15px; margin: 15px 0; box-shadow: 0 2px 10px rgba(0,0,0,0.05);">
                <h3 style="color: #4a6fa5; margin-top: 0;">Your Suggested Nicknames</h3>
                <ul style="list-style-type: none; padding: 0;">
        """
        
        for nickname in content['nicknames']:
            html += f"""
                    <li style="margin-bottom: 10px;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span style="font-size: 20px; color: #2c3e50;"><strong>{nickname['nickname']}</strong></span>
                            <span style="color: #7f8c8d; font-style: italic; font-size: 14px;">{nickname['meaning']}</span>
                        </div>
                    </li>
            """
        
        html += f"""
                </ul>
            </div>
            
            <div style="background-color: white; border-radius: 8px; padding: 15px; margin: 15px 0; box-shadow: 0 2px 10px rgba(0,0,0,0.05);">
                <h3 style="color: #4a6fa5; margin-top: 0;">Today's Reflection</h3>
                <p style="color: #34495e; font-style: italic; text-align: center;">{content['reflection_prompt']}</p>
            </div>
        </div>
        """
        
        display(HTML(html))
    
    def save_user_content(self, user_id: str, content: Dict, filepath: str = "nameglow_data.json"):
        """
        Save the generated content to a JSON file
        
        Parameters:
        -----------
        user_id : str
            Unique identifier for the user
        content : Dict
            The content to save
        filepath : str
            Path to the JSON file
        """
        try:
            # Load existing data if available
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                data = {"users": {}}
            
            # Initialize user if not exists
            if user_id not in data["users"]:
                data["users"][user_id] = {"history": []}
            
            # Add new content
            data["users"][user_id]["history"].append(content)
            
            # Save data
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
                
            print(f"Data saved successfully to {filepath}")
            
        except Exception as e:
            print(f"Error saving data: {e}")

# Create a demo function to show usage
def run_nameglow_demo():
    """Run a demonstration of the NameGlow prototype"""
    print("Welcome to the NameGlow Prototype!")
    print("----------------------------------")
    
    # Create instance (without API for demo)
    nameglow = NameGlow(use_api=False)
    
    # Get user name
    name = input("Enter a name to transform: ")
    
    # Generate and display content
    content = nameglow.generate_daily_content(name)
    nameglow.display_content(content)
    
    # Show alternative anagrams
    if content["alternative_anagrams"]:
        print("\nAlternative anagrams that could be used tomorrow:")
        for idx, anagram in enumerate(content["alternative_anagrams"], 1):
            virtue = nameglow.associate_virtue_with_anagram(anagram, name)
            print(f"{idx}. {anagram.capitalize()} - {virtue}")
    
    # Ask if user wants to save
    save = input("\nDo you want to save this result? (y/n): ")
    if save.lower() == 'y':
        user_id = name.lower().replace(" ", "_")
        nameglow.save_user_content(user_id, content)

# Test functionality with sample data
def test_functionality():
    """Test core functionality with sample names"""
    nameglow = NameGlow(use_api=False)
    
    test_names = ["Michael", "Sophia", "Robert", "Emma", "William"]
    results = []
    
    print("Testing NameGlow functionality with sample names:")
    print("------------------------------------------------")
    
    for name in test_names:
        content = nameglow.generate_daily_content(name)
        results.append({
            "name": name,
            "anagram": content["anagram"],
            "virtue": content["virtue"],
            "nickname_1": content["nicknames"][0]["nickname"],
            "nickname_2": content["nicknames"][1]["nickname"] if len(content["nicknames"]) > 1 else ""
        })
    
    # Display results as a table
    df = pd.DataFrame(results)
    print(df)
    
    # Return NameGlow instance for further testing
    return nameglow

# Example of how to use in a Jupyter notebook
if __name__ == "__main__":
    # For testing basic functionality
    nameglow = test_functionality()
    
    # Uncomment to run interactive demo
    # run_nameglow_demo()
    
    # Example of generating content for a specific name
    example_name = "Jennifer"
    content = nameglow.generate_daily_content(example_name)
    nameglow.display_content(content)
