# 📡 NewsGram – Intelligent News Aggregator

NewsGram is an AI-powered news extraction and summarization tool that fetches real-time news by using Google Serper API, and generated structured output by LLMs (like ChatGPT) or LangChain agents.

## Workflow of NewsGram
![image](https://github.com/user-attachments/assets/6946476a-8dee-43ea-acb7-37fe5035d8ee)



## Features

- Real-time news extraction from top Canadian sources.
- Summarization of news articles using AI.
- Intelligent querying using LLMs or LangChain agents.
- User-friendly web interface for searching and viewing news.

## Installation

### Prerequisites

- Python 3.10 or higher

### Manual Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/newsgram.git
   cd newsgram
   ```

2. Install dependencies using UV:

   ```bash
   pip install uv
   uv sync
   ```

3. Run the application:

   First run the API...
   ```bash
   uv run main.py
   ```

   Second, open `index.html` with a live server. You can use extensions like Live Server in VSCode or any other tool that provides live reloading.

## Usage

- Access the web interface at `http://localhost:8000`.
- Use the search bar to find news articles by keywords.
- View summarized news articles and explore intelligent querying options.

## Configuration

- Environment variables can be set in the `.env` file to configure API keys and other settings. Ensure that this file is not included in version control to protect sensitive information.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License.

## Acknowledgments
- Powered by FastAPI & LLMs

