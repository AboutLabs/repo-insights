# GitHub Repository Insight Generator

## Introduction

The GitHub Repository Insight Generator is a powerful tool that leverages AI to analyze GitHub repositories and provide valuable insights. This application uses OpenAI's GPT-3.5 Turbo model to generate in-depth analysis and feature recommendations based on repository metadata. The insights are stored and retrieved using Pinecone, a vector database, allowing for efficient similarity searches.

Key features of this project include:

1. Automated insight generation for GitHub repositories
2. Feature recommendations based on repository descriptions
3. Similarity search for previously generated insights
4. User-friendly interface built with Streamlit

This tool is perfect for developers, project managers, and anyone interested in gaining quick, AI-powered insights into GitHub projects.

## Installation

Follow these steps to set up the GitHub Repository Insight Generator on your local machine:

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Steps

1. Clone the repository

2. Create a virtual environment (optional but recommended):
```
conda create -n repo-insights python=3.11
conda activate repo-insights
```

3. Install the required packages:
```
pip install -r requirements.txt
```

4. Set up your API keys:
- Create a `.streamlit/secrets.toml` file in the project directory
- Add your API keys to the file:
  ```toml
  [api_keys]
  openai_api_key = "your_openai_api_key_here"
  pinecone_api_key = "your_pinecone_api_key_here"
  ```

5. Run the Streamlit app:
```toml
streamlit run app.py
```


6. Open your web browser and navigate to the URL provided by Streamlit (usually `http://localhost:8501`)

## Usage

1. Enter the GitHub repository URL, description, number of stars, and primary language in the sidebar.
2. Click the "Generate Insights" button to analyze the repository.
3. View the generated insights and feature recommendations.
4. Use the query input to search for similar insights from previously analyzed repositories.

## Contributing

Contributions to the GitHub Repository Insight Generator are welcome! Please feel free to submit pull requests, create issues, or suggest new features.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- OpenAI for providing the GPT-3.5 Turbo model
- Pinecone for vector storage and similarity search capabilities
- Streamlit for the user interface framework
