# 🧠 Nucleus - AI-Powered Document Summarizer

Flask web application that allows users to upload documents (PDF or TXT) and generate summaries using AI.

## 📋 Features

- ✅ PDF and TXT file upload
- ✅ Three summary types: Short, Detailed, and Bullet Points
- ✅ Three AI options: Groq (Llama 3.3), Google Gemini, and OpenAI (ChatGPT)
- ✅ Clean and responsive interface
- ✅ Real-time processing
- ✅ Markdown formatting support in summaries

## 🚀 Installation

### 1. Clone the repository
```bash
git clone https://github.com/Chikwa-git/nucleus.git
cd nucleus
```

### 2. Create and activate the virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure API keys

Edit the `.env` file and add your API keys:
```env
GROQ_API_KEY=your_groq_key_here
GEMINI_API_KEY=your_gemini_key_here
OPENAI_API_KEY=your_openai_key_here
```

**Where to get the keys:**
- Groq: https://console.groq.com/keys
- Gemini: https://makersuite.google.com/app/apikey
- OpenAI: https://platform.openai.com/api-keys

### 5. Run the application

**Option 1: Using the run.sh script**
```bash
./run.sh
```

**Option 2: Manually**
```bash
source venv/bin/activate
python app.py
```

The application will be available at: http://localhost:5000

## 📖 How to Use

1. Open http://localhost:5000 in your browser
2. Select a PDF or TXT file
3. Choose the summary type
4. Select the AI provider (Groq, Gemini, or OpenAI)
5. Click "Generate Summary"
6. Wait for processing and view the result

## 📁 Project Structure

nucleus/
├── app.py                 # Main Flask logic
├── templates/
│   └── index.html        # User interface
├── static/               # Static files (auto-created)
├── uploads/              # Temporary upload folder (auto-created)
├── .env                  # API keys (do not commit!)
├── requirements.txt      # Python dependencies
└── README.md             # This file

## 🛠️ Tech Stack

- **Flask** - Python web framework
- **PyPDF2** - PDF text extraction
- **python-dotenv** - Environment variable management
- **requests** - HTTP calls to APIs
- **google-genai** - Google Gemini SDK
- **groq** - Groq SDK (Llama 3.3)
- **openai** - OpenAI SDK (ChatGPT)

## 🔒 Security

- Never commit the `.env` file with your API keys
- File size limit: 16MB
- Temporary files are deleted after processing
- Text limited to 15,000 characters to avoid API limits

## 📝 Notes

- Make sure at least one API key is configured
- PDFs with images may not have all text extracted
- Processing time varies depending on document size

## 🐛 Troubleshooting

**Error: "GROQ_API_KEY not configured"**
- Check if you added the key to the `.env` file

**Error extracting text from PDF**
- Make sure the PDF is not password-protected or corrupted

**Error connecting to API**
- Check your internet connection
- Confirm your API keys are valid
