# Divar Advertisement Scraper

## Description

Welcome to the **Divar Advertisement Scraper**, a powerful and user-friendly web application designed to streamline your search for advertisements on [Divar.ir](https://divar.ir), Iran's leading online marketplace. This tool allows you to effortlessly find relevant ads by entering a search query (e.g., "apartment for rent") and selecting a city, with results presented in a clean, bulleted list format. Powered by AI-driven query optimization and robust web scraping, this application is perfect for users seeking efficiency and developers exploring AI and web technologies.

## Why Use This Project?

- **Save Time**: Quickly find relevant advertisements without manually navigating Divar.ir.
- **AI-Enhanced Search**: Optimize search queries for more accurate and relevant results.
- **User-Friendly**: Enjoy a simple, intuitive web interface built with Streamlit.
- **Customizable**: Search across major Iranian cities with support for Persian and English names.
- **Developer-Friendly**: Open-source with clear setup instructions for contributions.

## Features

- **Intuitive Interface**: Built with [Streamlit](https://streamlit.io/), offering a simple way to input queries and select cities.
- **AI-Powered Query Optimization**: Uses [Ollama](https://ollama.com/) with the "qwen2.5:latest" model to refine search terms, preferably in Persian, for better results.
- **City Support**: Supports major Iranian cities with a predefined mapping of Persian (e.g., تهران) to English (e.g., Tehran) names for URL generation.
- **Efficient Web Scraping**: Utilizes [Selenium](https://www.selenium.dev/) to handle dynamic content and infinite scrolling on Divar.ir.
- **Clean Output**: Displays advertisements with title, description, and price in a neat, bulleted list.
- **Workflow Management**: Employs [LangGraph](https://langchain-ai.github.io/langgraph/) to structure the workflow, ensuring a systematic process from input to output.
- **Error Handling**: Includes robust error checking for AI model initialization, web scraping, and user inputs, with troubleshooting guidance.

## Technologies Used

| Technology       | Role                                                                 |
|------------------|----------------------------------------------------------------------|
| **Python**       | Primary programming language for the application.                     |
| **Streamlit**    | Creates the interactive web interface for user input and result display. |
| **Selenium**     | Handles web scraping and automates browser interactions.              |
| **BeautifulSoup**| Parses HTML content for extracting advertisement details.             |
| **Ollama**       | Runs local AI models for query optimization.                         |
| **LangChain**    | Manages prompts and AI interactions for structured processing.        |
| **LangGraph**    | Structures the application's workflow for efficient task management.  |

## Installation

Follow these steps to set up the Divar Advertisement Scraper on your local machine:

1. **Install Python**:
   - Ensure [Python 3.8 or higher](https://www.python.org/downloads/) is installed.

2. **Install Dependencies**:
   - Install required Python libraries using pip:
     ```bash
     pip install beautifulsoup4 selenium streamlit langchain-core langchain-ollama langgraph
     ```

3. **Install Chrome and Chrome WebDriver**:
   - Install [Google Chrome](https://www.google.com/chrome/).
   - Download the [ChromeDriver](https://chromedriver.chromium.org/downloads) matching your Chrome version.
   - Add ChromeDriver to your system's PATH or specify its location in the code.

4. **Set up Ollama**:
   - Install [Ollama](https://ollama.com/) via its official website or package manager.
   - Pull the required AI model:
     ```bash
     ollama pull qwen2.5
     ```
   - Start Ollama:
     ```bash
     ollama serve
     ```

5. **Clone the Repository**:
   - Clone the repository (replace `your_username` with the actual GitHub username):
     ```bash
     git clone https://github.com/armanjscript/divar-ad-scraper.git
     ```
   - Navigate to the project directory:
     ```bash
     cd divar-ad-scraper
     ```

6. **Run the Application**:
   - Launch the Streamlit app:
     ```bash
     streamlit run main.py
     ```

**Note**: Running AI models locally requires sufficient computational resources (e.g., 16GB RAM, capable CPU/GPU). Ensure a stable internet connection for initial setup and ChromeDriver compatibility.

## Usage

1. **Launch the Application**:
   - Run `streamlit run main.py` to open the app in your default web browser.

2. **Interact with the Interface**:
   - **Enter a Query**: Input a search term (e.g., "apartment for rent").
   - **Select a City**: Choose a city from the dropdown (e.g., تهران, مشهد).
   - **Search**: Click the "Search" button to initiate the process.

3. **View Results**:
   - The app displays the optimized query and a bulleted list of advertisements, including title, description, and price.
   - If no results are found, try rephrasing the query or selecting a different city.

The interface features:
- A text input for search queries.
- A dropdown for city selection.
- A search button to trigger the scraping process.
- A display area for results, formatted for clarity.

## Troubleshooting

| Issue                     | Solution                                                                 |
|---------------------------|--------------------------------------------------------------------------|
| **Ollama Not Running**    | Ensure Ollama is running (`ollama serve`) and the `qwen2.5` model is pulled. |
| **ChromeDriver Issues**   | Verify ChromeDriver matches your Chrome version; update Chrome if needed. |
| **No Results**            | Rephrase the query or select a different city; check internet connection. |

## Contributing

We welcome contributions to enhance the project! To contribute:
- Fork the repository.
- Create a new branch for your changes.
- Submit a pull request with a clear description.
- For bugs or feature requests, open an issue on GitHub.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For questions or feedback, contact [your_email@example.com] or open an issue on GitHub.