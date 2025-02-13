# AI Research Assistant 🧠

A modern web application that provides AI-powered research assistance, similar to Perplexity AI. Built with Python Flask and Google's Gemini API, this application offers intelligent answers by searching and analyzing web content in real-time.

![AI Research Assistant Screenshot](screenshot.png)

## ✨ Features

- 🔍 Real-time web search and content analysis
- 🤖 AI-powered comprehensive answers using Google's Gemini
- 🌐 Source attribution with clickable links
- 💡 Related questions suggestions
- 🎨 Modern dark theme UI
- 📱 Responsive design for all devices

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key ([Get it here](https://makersuite.google.com/app/apikey))

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-research-assistant.git
cd ai-research-assistant
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/MacOS
python3 -m venv venv
source venv/bin/activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root and add your Gemini API key:
```
GEMINI_API_KEY=your_api_key_here
```

### Running the Application

1. Start the Flask development server:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

## 🔧 Usage

1. Enter your question in the search box
2. Click "Search" or press Enter
3. The AI will:
   - Search relevant web content
   - Analyze the information
   - Provide a comprehensive answer
   - List sources used
   - Suggest related questions

## 🛠️ Technology Stack

- **Backend**: Python Flask
- **AI Model**: Google Gemini API
- **Frontend**: HTML, CSS, JavaScript
- **UI Framework**: Bootstrap 5
- **Icons**: Font Awesome
- **Web Scraping**: BeautifulSoup4

## 📝 Project Structure

```
ai-research-assistant/
├── app.py              # Main Flask application
├── templates/
│   └── index.html      # Main HTML template
├── requirements.txt    # Python dependencies
├── .env               # Environment variables
└── README.md          # Project documentation
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google Gemini API for providing the AI capabilities
- Flask framework for the web application structure
- Bootstrap for the responsive UI components
- Font Awesome for the beautiful icons
