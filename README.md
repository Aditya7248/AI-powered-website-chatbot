# AI-powered-website-chatbot

🚀 **Now you can scrape any website and chat with it to understand its content!** Dive into the website's details, ask questions, and get instant insights—all in a friendly and conversational manner. 🌐🤖

---

## **Features**

- **Website Content Extraction**: 
  - Seamlessly handles dynamic content loading with Selenium and BeautifulSoup.
  - Extracts headers, paragraphs, and main content intelligently.

- **Interactive Chat Interface**:
  - Chat with the extracted website content using OpenAI GPT-3.5.
  - Enjoy natural, friendly conversations with a touch of humour and emojis. 😄

- **Error Handling**:
  - Validates URLs to avoid any mishaps.
  - Gracefully manages API errors and extraction failures.
  - Provides clear and helpful prompts for invalid inputs.

- **Navigation Commands**:
  - `new`: Switch to a new website effortlessly.
  - `exit`: End the chatbot session whenever you want.

---

## **Installation**

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/website-chatbot.git
   cd website-chatbot
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up OpenAI API Key**:
   - Create a `.env` file in the root directory.
   - Add your OpenAI API key:
     ```
     OPENAI_API_KEY=your_api_key_here
     ```

---

## **Usage**

1. **Run the Script**:
   ```bash
   python website_chatbot.py
   ```

2. **Interact with the Chatbot**:
   - Enter a valid website URL (e.g., `https://example.com`).
   - Ask questions like: *"What is this website about?"* or *"What are its main headings?"*
   - Switch websites easily by typing `new`.
   - Exit the chatbot anytime with `exit`.

🎉 **Pro Tip:** Get creative with your questions! The chatbot is here to help you dig deep into website content.

---

## **Example Interaction**

**Sample Commands:**
- URL: `https://example.com`
- Question: *"What is this website about?"*
- Question: *"Can you summarise its content for me?"*

### **Demo Video**:
[![Demo Video](demo_thumbnail.png)](https://youtu.be/demo-video-link)

### **Screenshots**:
![Chatbot Interface](screenshot1.png)
![Extracted Content](screenshot2.png)

---

## **License**

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## **Contributions**

Contributions are welcome! Feel free to open issues or submit pull requests.

---

## **Acknowledgements**

- [OpenAI](https://platform.openai.com/)
- [Selenium](https://www.selenium.dev/)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
- [Dotenv](https://pypi.org/project/python-dotenv/)

---

For questions or support, contact:
**Aditya Tiwari**
- [LinkedIn](https://www.linkedin.com/in/aditya-tiwari-24b4b924a/)
- Email: tiwariaditya2707@gmail.com
