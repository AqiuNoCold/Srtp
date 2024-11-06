

## Introduction

In the age of rapid technological advancement, information has become widely accessible through the internet. Various media outlets cover diverse topics, from local events to international conflicts. However, this abundance of information has led to significant challenges: **information overload** and **information bubbles**.

1. **Information Overload**: With the sheer volume of content generated daily, users struggle to filter valuable information from irrelevant noise. This often leads to missing important news or being overwhelmed by redundant data.
  
2. **Information Bubbles**: Users tend to consume content that aligns with their own views, leading to an "echo chamber" effect. This narrows their perspective and limits exposure to differing viewpoints, which can impact their understanding of complex issues.

To address these issues, the "News Wide-Angle Lens" system was developed with three main objectives:

1. **Reduce Information Overload**: Utilizing deep learning models such as CNN and Transformer, the system categorizes and filters news, enabling users to quickly access high-relevance information.
2. **Provide Diverse Perspectives**: By gathering reports from multiple sources on the same event, the system presents varied views, helping users understand the breadth of opinions and biases in media coverage.
3. **Analyze Media Bias**: The system evaluates different media outlets, revealing reporting styles, preferences, and tendencies to assist users in understanding potential biases.

## Theoretical Framework and Techniques

This section covers the primary theories and technical frameworks underpinning the project, including data acquisition, large language models, multimodal feature representation, and the Django framework.

#### 1. Data Acquisition Model
Efficient data acquisition and processing are crucial for news analysis. This project employs the **Scrapy framework** for web scraping, which enables simultaneous data requests to gather news information from diverse sources rapidly. Scrapy’s modular structure facilitates easy component integration and future updates.

To meet project requirements, adjustments were made to the Scrapy framework. These include modifications to the middleware, adding **Selenium** for handling dynamic web content and integrating a proxy pool to improve data collection success rates.

#### 2. Large Language Models (LLMs)
The project leverages recent advances in **large language models (LLMs)**, particularly **BERT** and **Transformer architectures**. BERT, which Google initially introduced, is a pre-trained language model that has shown significant improvements in tasks like sentiment analysis and text classification in NLP. The project utilizes the Chinese-Base-BERT model, optimized for Chinese language processing, to analyze the sentiment and categorization of news articles effectively.

#### 3. Multimodal Feature Representation
Multimodal representation captures both textual and visual content, enhancing the system's ability to process and display news more interactively. 

- **Text Features**: Using language models, the project converts text into vector embeddings, representing the semantic nuances and enabling better text classification and sentiment analysis.
- **Image Features**: **Vision Transformer (ViT)**, based on Transformer architecture, processes images to capture global dependencies and complements textual analysis by adding visual relevance.
- **CLIP Model**: To integrate images with text, **CLIP (Contrastive Language-Image Pretraining)** is used, aligning text and images within the same vector space. CLIP enables image-text matching, enhancing the clarity and engagement of the news content displayed.

#### 4. Django Framework
The **Django framework** underpins the system's structure, supporting the efficient organization of data processing, user authentication, and data visualization. Django’s model-template-view (MVT) architecture provides scalability and maintainability, ensuring that the system remains accessible to users through a web interface without additional installations.

This theoretical foundation supports the project’s overall objective to provide users with a comprehensive, efficient, and interactive news analysis platform.
