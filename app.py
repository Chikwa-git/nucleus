import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import PyPDF2
import requests
from dotenv import load_dotenv
from google import genai
from openai import OpenAI

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'

# Create uploads folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# API Keys
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Configure Gemini
gemini_client = None
if GEMINI_API_KEY:
    gemini_client = genai.Client(api_key=GEMINI_API_KEY)

# Configure OpenAI
openai_client = None
if OPENAI_API_KEY:
    openai_client = OpenAI(api_key=OPENAI_API_KEY)

ALLOWED_EXTENSIONS = {'pdf', 'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(file_path):
    """Extract text from PDF file"""
    text = ""
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text()
    except Exception as e:
        raise Exception(f"Error reading PDF: {str(e)}")
    return text

def extract_text_from_txt(file_path):
    """Extract text from TXT file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
    except Exception as e:
        raise Exception(f"Error reading TXT: {str(e)}")
    return text

def get_summary_prompt(text, summary_type):
    """Generate prompt based on summary type"""
    prompts = {
        'short': f"Faça um resumo curto e conciso do seguinte texto em até 3 parágrafos:\n\n{text}",
        'detailed': f"Faça um resumo detalhado e completo do seguinte texto, mantendo os pontos principais e informações importantes:\n\n{text}",
        'bullets': f"Faça um resumo do seguinte texto em formato de bullet points, destacando os pontos principais:\n\n{text}"
    }
    return prompts.get(summary_type, prompts['short'])

def summarize_with_groq(text, summary_type):
    """Summarize text using Groq API (Llama)"""
    if not GROQ_API_KEY:
        raise Exception("GROQ_API_KEY not configured")
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    prompt = get_summary_prompt(text, summary_type)
    
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": "Você é um assistente especializado em criar resumos de documentos."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 2000
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error calling Groq API: {str(e)}")

def summarize_with_gemini(text, summary_type):
    """Summarize text using Gemini API"""
    if not gemini_client:
        raise Exception("GEMINI_API_KEY not configured")
    
    try:
        prompt = get_summary_prompt(text, summary_type)
        
        response = gemini_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config={
                'system_instruction': "Você é um assistente especializado em criar resumos de documentos.",
                'temperature': 0.7,
                'max_output_tokens': 2000
            }
        )
        
        return response.text
    except Exception as e:
        raise Exception(f"Error calling Gemini API: {str(e)}")

def summarize_with_openai(text, summary_type):
    """Summarize text using OpenAI API (ChatGPT)"""
    if not OPENAI_API_KEY:
        raise Exception("OPENAI_API_KEY not configured")
    
    try:
        prompt = get_summary_prompt(text, summary_type)
        
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Você é um assistente especializado em criar resumos de documentos."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        return response.choices[0].message.content
    except Exception as e:
        raise Exception(f"Error calling OpenAI API: {str(e)}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    try:
        # Check if file was uploaded
        if 'document' not in request.files:
            return jsonify({'error': 'Nenhum arquivo enviado'}), 400
        
        file = request.files['document']
        if file.filename == '':
            return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Tipo de arquivo não permitido. Use PDF ou TXT'}), 400
        
        # Get parameters
        summary_type = request.form.get('summary_type', 'short')
        ai_provider = request.form.get('ai_provider', 'groq')
        
        # Save file temporarily
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Extract text based on file type
        file_extension = filename.rsplit('.', 1)[1].lower()
        if file_extension == 'pdf':
            text = extract_text_from_pdf(file_path)
        else:
            text = extract_text_from_txt(file_path)
        
        # Remove temporary file
        os.remove(file_path)
        
        if not text.strip():
            return jsonify({'error': 'Não foi possível extrair texto do documento'}), 400
        
        # Limit text size (to avoid API limits)
        max_chars = 15000
        if len(text) > max_chars:
            text = text[:max_chars] + "..."
        
        # Generate summary using selected AI
        if ai_provider == 'groq':
            summary = summarize_with_groq(text, summary_type)
        elif ai_provider == 'gemini':
            summary = summarize_with_gemini(text, summary_type)
        elif ai_provider == 'openai':
            summary = summarize_with_openai(text, summary_type)
        else:
            return jsonify({'error': 'Provedor de IA inválido'}), 400
        
        return jsonify({
            'success': True,
            'summary': summary,
            'ai_provider': ai_provider,
            'summary_type': summary_type
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

# Made with Bob
