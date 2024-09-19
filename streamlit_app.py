import streamlit as st
import time
from openai import OpenAI
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings

# Initialize OpenAI Client using secrets
client = OpenAI(api_key=st.secrets["api_keys"]["openai_api_key"])

# Get Pinecone API key from secrets
pinecone_api_key = st.secrets["api_keys"]["pinecone_api_key"]

# Initialize Pinecone client
pc = Pinecone(api_key=pinecone_api_key)
index_name = "repo-insights"

# Check if the index already exists
if index_name not in pc.list_indexes().names():
    # Create a ServerlessSpec for the index
    spec = ServerlessSpec(cloud="aws", region="us-east-1")
    
    # Create the index with the spec
    pc.create_index(
        name=index_name,
        dimension=1536,
        metric="cosine",
        spec=spec
    )

    # Wait for the index to be ready
    while not pc.describe_index(index_name).status['ready']:
        time.sleep(1)
    
    print(f"Index '{index_name}' created successfully.")
else:
    print(f"Index '{index_name}' already exists.")

# Get the Pinecone index
index = pc.Index(index_name)

# Initialize OpenAI embeddings
embeddings = OpenAIEmbeddings(api_key=st.secrets["api_keys"]["openai_api_key"])

# Initialize Pinecone vector store
vectorstore = PineconeVectorStore(
    index=index,
    embedding=embeddings,
    text_key="text"
)

# Function to generate insights using OpenAI GPT-3.5 Turbo
def generate_insights(repo_data):
    prompt = f"""
    Analyze the following GitHub repository metadata and provide insights:

    Repository URL: {repo_data['repo_url']}
    Description: {repo_data['description']}
    Stars: {repo_data['stars']}
    Primary Language: {repo_data['language']}

    Please provide insights on the following aspects:
    1. Repository popularity and community interest
    2. Potential use cases based on the description
    3. Suggestions for improvement or growth
    4. Relevance to current trends in {repo_data['language']} development
    5. Feature recommendations: Suggest 3-5 features or enhancements that are popular in similar projects

    Insights:
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# Function to generate feature recommendations using OpenAI
def generate_feature_recommendations(description, language):
    prompt = f"""
    Based on the following GitHub repository description, suggest 3-5 features or enhancements that are popular in similar projects:

    Repository Description: {description}
    Primary Language: {language}

    Feature Recommendations:
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# Store insights in Pinecone
def store_insights(repo_data, insights):
    vectorstore.add_texts(
        texts=[insights],
        metadatas=[repo_data]
    )

# Query insights stored in Pinecone
def query_insights(query):
    results = vectorstore.similarity_search(query, k=1)
    return results[0].page_content if results else "No relevant insights found."

# Streamlit UI
def main():
    st.title('GitHub Repository Insight Generator')

    # Sidebar for user inputs
    st.sidebar.header('Repository Information')
    repo_url = st.sidebar.text_input('GitHub Repo URL', 'https://github.com/tensorflow/tensorflow')
    description = st.sidebar.text_area('Description', 'A machine learning library for Python')
    stars = st.sidebar.number_input('Number of Stars', min_value=0, value=10000)
    language = st.sidebar.selectbox('Primary Language', ['Python', 'JavaScript', 'Java', 'C++', 'Other'])

    # Main content area
    if st.sidebar.button('Generate Insights'):
        if repo_url and description:
            with st.spinner('Generating insights and recommendations...'):
                repo_data = {
                    "repo_url": repo_url,
                    "description": description,
                    "stars": stars,
                    "language": language
                }
                insights = generate_insights(repo_data)
                store_insights(repo_data, insights)
                feature_recommendations = generate_feature_recommendations(description, language)

            st.subheader('Generated Insights')
            st.write(insights)

            st.subheader('Feature Recommendations')
            st.write(feature_recommendations)

            st.subheader('Query Insights')
            query = st.text_input('Enter a query to search insights')
            if query:
                result = query_insights(query)
                st.write(result)
        else:
            st.error('Please enter all required fields.')

    # Display input data preview
    st.sidebar.subheader('Input Data Preview')
    st.sidebar.write(f'Repo URL: {repo_url}')
    st.sidebar.write(f'Description: {description}')
    st.sidebar.write(f'Stars: {stars}')
    st.sidebar.write(f'Language: {language}')

if __name__ == '__main__':
    main()