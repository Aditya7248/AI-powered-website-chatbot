from bs4 import BeautifulSoup
from openai import OpenAI
import logging
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv() # to load environment variables

# Configure logging
logging.basicConfig(level=logging.WARNING)  # Change logging level to WARNING
logging.getLogger('httpx').setLevel(logging.WARNING)  # Specifically silence httpx logs
logging.getLogger('selenium').setLevel(logging.WARNING)  # Silence selenium logs
logging.getLogger('WDM').setLevel(logging.WARNING)  # Silence WebDriver Manager logs

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_welcome():
    """Print welcome message with ASCII art"""
    welcome_text = """
    ╔══════════════════════════════════════════╗
    ║    🤖 Website Chatbot Assistant 🌐       ║
    ║    Chat with any website and learn more! ║
    ╚══════════════════════════════════════════╝
    """
    print(welcome_text)

def get_api_key():
    """Get API key from environment variable or user input"""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        api_key = input("Please enter your OpenAI API key: ").strip()
        if not api_key:
            raise ValueError("API key is required to run the chatbot")
    return api_key

def validate_url(url):
    """Validate if the provided URL is properly formatted"""
    try:
        result = urlparse(url)
        if not all([result.scheme, result.netloc]):
            return False
        if not result.scheme in ['http', 'https']:
            return False
        return True
    except:
        return False

# Selenium WebDriver Options
options = Options()
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-extensions")
options.add_argument("--disable-notifications")
options.add_argument("--disable-infobars")
options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")

def init_selenium():
    """Initialize Selenium WebDriver"""
    try:
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    except Exception as e:
        logging.error(f"Error initializing Selenium: {e}")
        raise

def extract_website_content(url):
    """Extract content from any website using Selenium"""
    print("Loading website content... ⏳")
    driver = init_selenium()
    try:
        driver.get(url)
        time.sleep(3)  # time for dynamic content to load
        
        # Scroll to load dynamic content with progress indicator
        print("Scanning website content... 🔍")
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        
        # removing unnecessary elements
        for tag in soup(['script', 'style', 'nav', 'footer', 'iframe', 'meta', 'link', 'noscript', 'header', 'aside']):
            tag.decompose()
        
        # extracting main content and headers
        main_content = soup.find('main') or soup.find('article') or soup.find('body')
        headers = [h.get_text(strip=True) for h in main_content.find_all(['h1', 'h2', 'h3'])]
        paragraphs = [p.get_text(strip=True) for p in main_content.find_all(['p', 'div']) if p.get_text(strip=True)]
        
        # Combine and format the content
        all_content = "\n".join(headers + paragraphs)
        cleaned_text = ' '.join(all_content.split())
        
        # Truncate if too long (to fit within API limits)
        return cleaned_text[:4000]
        
    except Exception as e:
        logging.error(f"Error extracting website content: {e}")
        return ""
    finally:
        driver.quit()

# chatbot prompting
def create_chatbot_context(website_content, url):
    """Create initial context for the chatbot"""
    domain = urlparse(url).netloc
    return f"""You are a helpful chatbot that has analyzed the content from {domain}. 
    Use this information to answer questions about the website and its content: {website_content}
    
    Focus on providing accurate information based on the website's content. If you're unsure about something
    or if the information isn't present in the extracted content, please say so. Engage in a natural, friendly, 
    and helpful conversation with the user. If asked about unrelated topics, politely redirect the conversation 
    to the website's content. Add personality with occasional emojis and light humor where appropriate.

    Remember to:
    1. Be concise but informative
    2. Use emojis sparingly but effectively
    3. Maintain a helpful and friendly tone
    4. Admit when information is not available
    5. Stay focused on the website content"""

def get_chatbot_response(client, conversation_history, user_input):
    """Get response from ChatGPT API"""
    try:
        messages = conversation_history + [
            {"role": "user", "content": user_input}
        ]
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=250,  # Increased for more detailed responses
            temperature=0.7,
            presence_penalty=0.6  # Encourage more concise responses

        )
        
        return response.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"Error getting chatbot response: {e}")
        return f"I apologize, but I'm having trouble processing your request. Error: {str(e)}"

def main():
    try:
        clear_screen()
        print_welcome()
        
        # Get API key
        api_key = get_api_key()
        
        # Initialize OpenAI client
        client = OpenAI(api_key=api_key)
        
        # Get website URL from user
        while True:
            url = input("\n📎 Enter website URL (or 'exit' to quit): ").strip()
            
            if url.lower() == 'exit':
                print("\n👋 Thank you for using Website Chatbot! Goodbye!")
                break
            
            if not validate_url(url):
                print("❌ Invalid URL format. Please enter a valid URL (e.g., https://www.example.com)")
                continue
            
            website_content = extract_website_content(url)
            
            if not website_content:
                print("❌ Could not extract website content. Please check the URL and try again.")
                continue
            
            # Initialize conversation history with system context
            conversation_history = [
                {"role": "system", "content": create_chatbot_context(website_content, url)}
            ]
            
            print(f"\n✨ Ready! Ask me anything about {url}")
            print("💡 Type 'new' for a different website or 'exit' to quit")
            
            while True:
                try:
                    user_input = input("\nYou: ").strip()
                    
                    if user_input.lower() == 'exit':
                        print("\n👋 Thank you for using Website Chatbot! Goodbye!")
                        return
                    
                    if user_input.lower() == 'new':
                        print("\n🔄 Switching to new website...")
                        break
                    
                    if not user_input:
                        continue
                    
                    # Get chatbot response
                    response = get_chatbot_response(client, conversation_history, user_input)
                    
                    # Update conversation history
                    conversation_history.append({"role": "user", "content": user_input})
                    conversation_history.append({"role": "assistant", "content": response})
                    
                    # Keeping conversation history manageable
                    if len(conversation_history) > 10:
                        conversation_history = [conversation_history[0]] + conversation_history[-8:]
                    
                    # Format and print response
                    print("\n🤖 Bot Response:")
                    print("━" * 50)  # Adding separator line
                    
                    # Clean up markdown formatting
                    cleaned_response = response.replace('**', '')  # To remove bold markdown
                    cleaned_response = cleaned_response.replace('*', '')   # To remove italic markdown
                    
                    # Split response into paragraphs and print with proper spacing
                    paragraphs = cleaned_response.split('\n')
                    for paragraph in paragraphs:
                        # proper indentation for numbered points
                        if paragraph.strip().startswith(str(tuple(range(1, 10)))):
                            print(f"  {paragraph.strip()}")
                        else:
                            print(paragraph.strip())
                    
                    print("─" * 50)  # Adding separator line                    
                except KeyboardInterrupt:
                    print("\n\n👋 Exiting chatbot...")
                    return
                except Exception as e:
                    print(f"\n❌ An error occurred: {str(e)}")
                    continue

    except Exception as e:
        print(f"❌ Fatal error: {str(e)}")

if __name__ == "__main__":
    main()