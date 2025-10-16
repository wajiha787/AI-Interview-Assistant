# Quick Start Guide - AI Career Development Platform

## 🚀 Get Started in 5 Minutes

### Step 1: Installation (2 minutes)

```bash
# Clone the repository
git clone <repository-url>
cd AI-Hiring-Evaluation

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configuration (1 minute)

Create a `.env` file in the project root:

```bash
OPENAI_API_KEY=your_openai_api_key_here
```

Get your OpenAI API key from: https://platform.openai.com/api-keys

### Step 3: Run the Application (1 minute)

```bash
python start.py
```

Or:

```bash
python main.py
```

### Step 4: Access the Platform (1 minute)

Open your browser and go to:
```
http://localhost:8000
```

You'll see the beautiful career development interface!

---

## 📋 First Time User Guide

### Step 1: Create Your Profile

1. Click on **"👤 Profile"** tab (already selected)
2. Fill in:
   - Your full name
   - Email address
   - Profession (e.g., "Software Engineer", "Data Scientist")
   - Experience level (Junior/Mid-Level/Senior/Expert)
3. Click **"Create Profile"**

✅ You should see your profile displayed!

---

### Step 2: Analyze Your CV

1. Click on **"📄 CV Analysis"** tab
2. Click **"Choose File"** and select your CV (PDF, DOCX, or TXT)
3. Click **"Analyze CV"**
4. Wait 30-60 seconds for AI analysis

✅ You'll see:
- Your Career Readiness Score (0-100)
- Your Strengths
- Skill Gaps
- Missing Certifications
- Priority Improvements

---

### Step 3: Get Learning Recommendations

1. Click on **"📚 Learning Path"** tab
2. Select your available time for learning
3. Click **"Get Recommendations"**
4. Wait 30-60 seconds for AI recommendations

✅ You'll receive:
- Recommended Certifications (with costs in PKR)
- Online Courses
- Practice Projects
- Learning Path Timeline (3, 6, 12 months)

---

### Step 4: Practice Interview

1. Click on **"🎤 Interview Practice"** tab
2. Click **"Start New Interview Session"**
3. Wait for questions to generate
4. Answer each question in the text area
5. Click **"Submit Answer"** after each question
6. Continue until all questions are answered

✅ Questions are generated based on your profession!

---

### Step 5: Review Performance

After completing all questions:

✅ You'll see:
- Your Interview Score (0-100)
- Performance breakdown by category
- Weak topics identified
- **If score < 100%**: Personalized Practice Plan
- **If score = 100%**: Congratulations! Ready for next level!

---

### Step 6: Practice & Improve (if score < 100%)

1. Review your weak topics
2. Check the practice plan
3. Study recommended resources
4. Practice the identified areas
5. When ready, start a new round from Step 4

**Goal**: Achieve 100% score to move to next level!

---

### Step 7: Track Progress

1. Click on **"📊 Dashboard"** tab
2. Click **"Refresh Dashboard"**

✅ See your statistics:
- Total Interviews
- Average Score
- Completed Sessions

---

## 🎯 Tips for Best Results

### For CV Analysis
- ✅ Upload a detailed, up-to-date CV
- ✅ Include all relevant experience
- ✅ List all skills and certifications
- ✅ Use clear formatting

### For Interview Practice
- ✅ Answer thoughtfully and completely
- ✅ Explain your reasoning
- ✅ Give examples when possible
- ✅ Be honest in your answers
- ✅ Take your time

### For Improvement
- ✅ Follow the practice plan systematically
- ✅ Focus on understanding, not memorization
- ✅ Take breaks between rounds
- ✅ Track what you learn
- ✅ Practice regularly

---

## 🔧 Troubleshooting

### "Missing OPENAI_API_KEY"
```bash
# Make sure .env file exists with:
OPENAI_API_KEY=sk-...your-key...
```

### "Module not found" errors
```bash
# Reinstall dependencies:
pip install -r requirements.txt --force-reinstall
```

### "Connection refused"
```bash
# Check if port 8000 is already in use
# Try different port:
uvicorn app.api.main:app --port 8001
```

### CV Analysis takes too long
- Check your internet connection
- Verify OpenAI API key is valid
- Ensure CV file is not corrupted
- Try a smaller CV file

### Questions not generating
- Verify profile is created
- Check OpenAI API quota
- Refresh the page and try again

---

## 📊 Understanding Scores

### Career Readiness Score (0-100)
- **90-100**: Ready for senior positions
- **70-89**: Ready for mid-level positions  
- **50-69**: Ready for junior positions
- **30-49**: Significant gaps to fill
- **0-29**: Major preparation needed

### Interview Score (0-100)
- **100**: Perfect! Ready for next level
- **80-99**: Excellent, minor improvements
- **60-79**: Good, practice key areas
- **40-59**: Average, significant practice needed
- **0-39**: Needs extensive preparation

---

## 🎓 Example Session

**Example: Junior Software Engineer**

1. **Profile Created**:
   - Name: Sarah Khan
   - Profession: Software Engineer
   - Level: Junior

2. **CV Analysis Result**:
   - Readiness Score: 65/100
   - Gaps: System Design, Advanced Algorithms, Cloud Services
   - Strengths: Web Development, JavaScript, Problem Solving

3. **Recommendations Received**:
   - AWS Certified Solutions Architect (PKR 40,000)
   - System Design Course on Udemy (PKR 3,500)
   - LeetCode Premium (PKR 2,500/month)
   - Project: Build a scalable e-commerce API

4. **First Interview Round**:
   - 15 questions asked
   - Score: 68/100
   - Weak topics: System design patterns, Database optimization

5. **Practice Plan**:
   - 7-day plan provided
   - Daily study schedule
   - Specific topics to cover
   - Mock questions to practice

6. **Second Round** (after practice):
   - Score improved to 85/100
   - Weak topics reduced
   - New practice plan for remaining gaps

7. **Third Round**:
   - Score: 100/100 🎉
   - Ready for mid-level interviews!

---

## 🌐 API Testing (Optional)

### Test with cURL

```bash
# Health check
curl http://localhost:8000/api/health

# Create user
curl -X POST http://localhost:8000/api/users \
  -F "name=John Doe" \
  -F "email=john@example.com" \
  -F "profession=Data Scientist" \
  -F "experience_level=junior"

# View API documentation
# Open browser: http://localhost:8000/docs
```

---

## 📚 Additional Resources

- **Full Documentation**: See `README.md`
- **Workflow Details**: See `WORKFLOW_GUIDE.md`
- **Technical Details**: See `TRANSFORMATION_SUMMARY.md`
- **API Docs**: http://localhost:8000/docs

---

## 🆘 Need Help?

1. Check the troubleshooting section above
2. Review the full README.md
3. Check API documentation at /docs
4. Create an issue on GitHub
5. Check your OpenAI API quota

---

## ✅ Checklist

Before starting:
- [ ] Python 3.8+ installed
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] OpenAI API key set in .env
- [ ] Application running on port 8000

First session:
- [ ] Profile created
- [ ] CV uploaded and analyzed
- [ ] Recommendations viewed
- [ ] Interview session started
- [ ] All questions answered
- [ ] Performance reviewed
- [ ] Dashboard checked

---

## 🎯 Your Goal

**Achieve 100% interview score and advance to the next level!**

Each round helps you improve. Keep practicing until you master your field!

---

## 🚀 Ready to Transform Your Career?

Start now: http://localhost:8000

Good luck on your career development journey! 💪

---

**Last Updated**: October 2025  
**Version**: 2.0.0  
**Support**: Create an issue on GitHub for help

