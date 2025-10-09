# 🤖 AI Hiring Evaluation System

A comprehensive multi-agent AI system for automated candidate evaluation using CrewAI framework. This system analyzes resumes and interview transcripts to provide detailed, objective candidate assessments.

## 🌟 Features

- **Multi-Agent Architecture**: Uses CrewAI framework with specialized agents for different evaluation aspects
- **Resume Analysis**: AI-powered extraction and analysis of candidate skills, experience, and qualifications
- **Interview Evaluation**: Comprehensive assessment of communication, problem-solving, and cultural fit
- **Automated Scoring**: Intelligent scoring across multiple criteria with detailed reasoning
- **Web Interface**: User-friendly frontend for uploading files and viewing results
- **RESTful API**: Complete API for integration with other systems
- **File Processing**: Support for PDF, DOCX, and TXT file formats
- **Comprehensive Testing**: Full test suite with unit and integration tests

## 🏗️ Architecture

### Multi-Agent System

The system uses three specialized AI agents working in sequence:

1. **Resume Analyzer Agent**: Extracts and analyzes resume content
   - Identifies skills, experience, education, and certifications
   - Assesses relevance to the target position
   - Identifies potential red flags or concerns

2. **Interview Evaluator Agent**: Evaluates interview performance
   - Analyzes communication skills and clarity
   - Assesses problem-solving approach and technical knowledge
   - Evaluates cultural fit and leadership potential

3. **Scoring Agent**: Provides final assessment and recommendation
   - Synthesizes information from resume and interview analysis
   - Generates detailed scoring across multiple criteria
   - Provides hiring recommendation with confidence levels

### Technology Stack

- **Backend**: FastAPI (Python)
- **AI Framework**: CrewAI with OpenAI GPT-4
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **File Processing**: PyPDF2, python-docx
- **Testing**: pytest, pytest-asyncio
- **Documentation**: FastAPI auto-generated docs

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenAI API key
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-hiring-evaluation
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env and add your OpenAI API key
   ```

5. **Run the application**
   ```bash
   python main.py
   ```

6. **Access the application**
   - Web Interface: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/api/health

## 📖 Usage

### Web Interface

1. **Create Candidate**: Fill in candidate information and position details
2. **Upload Files**: Upload resume (PDF/DOCX/TXT) and interview transcript
3. **Evaluate**: Click "Evaluate Candidate" to run the AI analysis
4. **View Results**: See detailed scoring, recommendations, and feedback

### API Usage

#### Create a Candidate
```bash
curl -X POST "http://localhost:8000/api/candidates" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "name=John Doe&email=john@example.com&position_applied=Software Engineer"
```

#### Upload Resume
```bash
curl -X POST "http://localhost:8000/api/candidates/{candidate_id}/resume" \
  -F "file=@resume.pdf"
```

#### Upload Interview Transcript
```bash
curl -X POST "http://localhost:8000/api/candidates/{candidate_id}/interview" \
  -F "file=@interview.pdf"
```

#### Evaluate Candidate
```bash
curl -X POST "http://localhost:8000/api/candidates/{candidate_id}/evaluate"
```

#### Get Evaluation Results
```bash
curl -X GET "http://localhost:8000/api/candidates/{candidate_id}/evaluation"
```

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest app/tests/test_agents.py

# Run with verbose output
pytest -v
```

### Test Categories

- **Unit Tests**: Individual component testing
- **Integration Tests**: API endpoint testing
- **Model Tests**: Data model validation
- **Agent Tests**: AI agent functionality

## 📊 Evaluation Criteria

The system evaluates candidates across five key dimensions:

1. **Technical Skills** (0-10): Programming languages, frameworks, tools
2. **Communication** (0-10): Verbal and written communication clarity
3. **Problem Solving** (0-10): Analytical thinking and solution approach
4. **Cultural Fit** (0-10): Alignment with company values and team dynamics
5. **Experience Relevance** (0-10): Applicability of past experience to the role

### Scoring Scale

- **9-10**: Exceptional
- **7-8**: Strong
- **5-6**: Average
- **3-4**: Below Average
- **0-2**: Poor

### Recommendations

- **Strong Hire**: Exceptional candidate with high confidence
- **Hire**: Good candidate with positive indicators
- **Maybe**: Mixed signals, requires additional evaluation
- **No Hire**: Significant concerns or poor fit
- **Strong No Hire**: Major red flags or poor performance

## 🔧 Configuration

### Environment Variables

```bash
OPENAI_API_KEY=your_openai_api_key_here
LANGCHAIN_API_KEY=your_langchain_api_key_here  # Optional
LANGCHAIN_TRACING_V2=true  # Optional, for debugging
LANGCHAIN_PROJECT=ai-hiring-evaluation  # Optional
```

### File Upload Limits

- **Maximum file size**: 10MB (configurable)
- **Supported formats**: PDF, DOCX, TXT
- **Processing timeout**: 30 seconds per file

## 🏢 Production Deployment

### Docker Deployment

1. **Create Dockerfile**
   ```dockerfile
   FROM python:3.9-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD ["python", "main.py"]
   ```

2. **Build and run**
   ```bash
   docker build -t ai-hiring-evaluation .
   docker run -p 8000:8000 -e OPENAI_API_KEY=your_key ai-hiring-evaluation
   ```

### Cloud Deployment

The application can be deployed to:
- **AWS**: Using ECS, Lambda, or EC2
- **Google Cloud**: Using Cloud Run or Compute Engine
- **Azure**: Using Container Instances or App Service
- **Heroku**: Direct deployment with Procfile

### Database Integration

For production use, replace the in-memory storage with:
- **PostgreSQL**: For relational data
- **MongoDB**: For document storage
- **Redis**: For caching and session management

## 📈 Performance Considerations

- **Concurrent Evaluations**: System supports multiple simultaneous evaluations
- **Caching**: Implement Redis caching for frequently accessed data
- **Rate Limiting**: Add rate limiting for API endpoints
- **Monitoring**: Implement logging and monitoring for production use

## 🔒 Security Considerations

- **API Authentication**: Implement JWT or OAuth2 authentication
- **File Validation**: Enhanced file type and content validation
- **Data Encryption**: Encrypt sensitive data at rest and in transit
- **Access Control**: Implement role-based access control
- **Audit Logging**: Log all evaluation activities

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the API documentation at `/docs`
- Review the test cases for usage examples

## 🔮 Future Enhancements

- **Multi-language Support**: Support for non-English resumes and interviews
- **Video Interview Analysis**: Integration with video interview platforms
- **Bias Detection**: AI-powered bias detection and mitigation
- **Integration APIs**: Connect with ATS and HR systems
- **Advanced Analytics**: Dashboard with evaluation trends and insights
- **Custom Evaluation Criteria**: Configurable evaluation criteria per organization

---

**Built with ❤️ using CrewAI and FastAPI**

