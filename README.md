# Crop Care AI

## Overview
Crop Care AI is an innovative solution designed to assist farmers in identifying and managing crop diseases. Currently focusing on banana crops, this project aims to expand support for additional crops in the near future.

## Features
- **Disease Identification**: Utilizes Convolutional Neural Networks (CNN) for accurate disease detection in banana crops.
- **AI Assistance**: Integrates OLLMA for accessing Llama 3 via Langchain, providing farmers with AI-driven insights and recommendations.
- **Retrieval-Augmented Generation (RAG)**: Enhances the model’s ability to provide contextual and relevant information to farmers.
- **User-Friendly Interface**: Built with React and Tailwind for a seamless user experience.

## Technology Stack
- **Backend**: Flask
- **Frontend**: React, Tailwind CSS
- **Deep Learning Framework**: TensorFlow
- **Vector Database**: ChromaDB
- **Machine Learning**: CNN for disease identification

## Getting Started

### Prerequisites
- Python 3.x
- Node.js
- TensorFlow
- Flask

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/crop-care-ai.git
   ```

2. Navigate to the backend directory and install the required packages:
   ```bash
   cd crop-care-ai
   pip install -r requirements.txt
   ```

3. Navigate to the frontend directory and install the dependencies:
   ```bash
   cd ../frontend
   npm install
   ```

### Usage

1. Start the Flask backend:
   ```bash
   cd crop-care-ai
   python app.py
   ```

2. Start the React frontend:
   ```bash
   cd ../frontend
   npm start
   ```

3. Open your browser and navigate to `http://localhost:3000` to access the application.

## Future Enhancements
- Expand support for additional crops beyond bananas.
- Improve disease detection accuracy and expand the training dataset.
- Implement more advanced features using AI to provide actionable insights to farmers.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
