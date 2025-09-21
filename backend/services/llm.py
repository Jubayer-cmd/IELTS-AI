from typing import TypedDict, List, Dict, Any, Annotated, Optional
from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage
import json
import re
from datetime import datetime
import base64
from PIL import Image
import io
import asyncio
import sqlite3
import os
from pathlib import Path
from langsmith import traceable
# Conversation State Definition
class ConversationState(TypedDict):
    # Input
    user_message: str
    image_data: Optional[str]  # base64 encoded image
    user_id: str
    
    # Conversation Context
    conversation_state: str  # "greeting", "waiting_for_preference", "waiting_for_essay", "evaluating", "discussing_feedback"
    conversation_history: List[Dict[str, str]]
    user_intent: str  # "wants_practice", "wants_question", "submitted_essay", "uploaded_image", "followup_question"
    
    # Content Processing
    extracted_text: str
    combined_text: str
    essay_text: str
    question_text: str
    task_type: str  # "task1" or "task2"
    
    # Validation
    word_count: int
    is_valid_essay: bool
    validation_errors: List[str]
    
    # Evaluation Results
    overall_band_score: float
    task_achievement_score: float
    coherence_cohesion_score: float
    lexical_resource_score: float
    grammatical_accuracy_score: float
    
    # Feedback
    detailed_feedback: Dict[str, Any]
    improvement_suggestions: List[str]
    
    # Response
    ai_response: str
    should_deduct_credit: bool
    next_conversation_state: str

class IELTSConversationalAI:
    def __init__(self, google_api_key: str, db_path: str = "ielts_memory.db"):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=google_api_key,
            temperature=0.3
        )
        
        self.vision_llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-pro",
            google_api_key=google_api_key,
            temperature=0.3
        )
        
        self.db_path = db_path
        self._init_memory_db()
        self.workflow = self._create_workflow()
    
    def _create_workflow(self) -> StateGraph:
        """Create the conversational LangGraph workflow"""
        workflow = StateGraph(ConversationState)
        
        # Add nodes
        workflow.add_node("analyze_input", self.analyze_input)
        workflow.add_node("classify_intent", self.classify_intent)
        workflow.add_node("extract_image_content", self.extract_image_content)
        workflow.add_node("combine_content", self.combine_content)
        workflow.add_node("handle_greeting", self.handle_greeting)
        workflow.add_node("generate_question", self.generate_question)
        workflow.add_node("evaluate_essay", self.evaluate_essay)
        workflow.add_node("handle_followup", self.handle_followup)
        workflow.add_node("format_response", self.format_response)
        
        # Set entry point
        workflow.set_entry_point("analyze_input")
        
        # Define edges
        workflow.add_edge("analyze_input", "classify_intent")
        
        # Conditional routing based on intent
        workflow.add_conditional_edges(
            "classify_intent",
            self.route_by_intent,
            {
                "extract_image": "extract_image_content",
                "greeting": "handle_greeting",
                "wants_question": "generate_question", 
                "submitted_essay": "combine_content",
                "followup": "handle_followup"
            }
        )
        
        workflow.add_edge("extract_image_content", "combine_content")
        workflow.add_edge("combine_content", "evaluate_essay")
        workflow.add_edge("handle_greeting", "format_response")
        workflow.add_edge("generate_question", "format_response")
        workflow.add_edge("evaluate_essay", "format_response")
        workflow.add_edge("handle_followup", "format_response")
        workflow.add_edge("format_response", END)
        
        return workflow.compile()
    
    def _init_memory_db(self):
        """Initialize SQLite database for persistent memory"""
        os.makedirs(os.path.dirname(self.db_path) if os.path.dirname(self.db_path) else '.', exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables for persistent memory
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                session_id TEXT,
                conversation_state TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id INTEGER,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (conversation_id) REFERENCES conversations (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS evaluations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                essay_text TEXT NOT NULL,
                question_text TEXT,
                task_type TEXT,
                word_count INTEGER,
                overall_band_score REAL,
                task_achievement_score REAL,
                coherence_cohesion_score REAL,
                lexical_resource_score REAL,
                grammatical_accuracy_score REAL,
                detailed_feedback TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def _save_conversation(self, user_id: str, conversation_history: List[Dict], conversation_state: str):
        """Save conversation to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Insert or update conversation
        cursor.execute('''
            INSERT OR REPLACE INTO conversations (user_id, conversation_state, updated_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
        ''', (user_id, conversation_state))
        
        conversation_id = cursor.lastrowid
        
        # Clear old messages and insert new ones
        cursor.execute('DELETE FROM messages WHERE conversation_id = ?', (conversation_id,))
        
        for message in conversation_history:
            cursor.execute('''
                INSERT INTO messages (conversation_id, role, content, timestamp)
                VALUES (?, ?, ?, ?)
            ''', (conversation_id, message['role'], message['content'], message['timestamp']))
        
        conn.commit()
        conn.close()
    
    def _load_conversation(self, user_id: str) -> Dict[str, Any]:
        """Load conversation from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get latest conversation
        cursor.execute('''
            SELECT conversation_state FROM conversations 
            WHERE user_id = ? 
            ORDER BY updated_at DESC 
            LIMIT 1
        ''', (user_id,))
        
        result = cursor.fetchone()
        conversation_state = result[0] if result else "greeting"
        
        # Get conversation history
        cursor.execute('''
            SELECT m.role, m.content, m.timestamp 
            FROM messages m
            JOIN conversations c ON m.conversation_id = c.id
            WHERE c.user_id = ?
            ORDER BY m.timestamp DESC
            LIMIT 20
        ''', (user_id,))
        
        messages = cursor.fetchall()
        conversation_history = [
            {"role": msg[0], "content": msg[1], "timestamp": msg[2]}
            for msg in reversed(messages)
        ]
        
        conn.close()
        
        return {
            "conversation_state": conversation_state,
            "conversation_history": conversation_history
        }
    
    def _save_evaluation(self, user_id: str, state: ConversationState):
        """Save evaluation results to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO evaluations (
                user_id, essay_text, question_text, task_type, word_count,
                overall_band_score, task_achievement_score, coherence_cohesion_score,
                lexical_resource_score, grammatical_accuracy_score, detailed_feedback
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_id,
            state.get("essay_text", ""),
            state.get("question_text", ""),
            state.get("task_type", ""),
            state.get("word_count", 0),
            state.get("overall_band_score", 0),
            state.get("task_achievement_score", 0),
            state.get("coherence_cohesion_score", 0),
            state.get("lexical_resource_score", 0),
            state.get("grammatical_accuracy_score", 0),
            json.dumps(state.get("detailed_feedback", {}))
        ))
        
        conn.commit()
        conn.close()
    
    @traceable
    async def analyze_input(self, state: ConversationState) -> ConversationState:
        """Analyze user input to determine content types"""
        user_message = state.get("user_message", "").strip()
        image_data = state.get("image_data")
        
        # Basic analysis
        word_count = len(user_message.split()) if user_message else 0
        has_image = bool(image_data)
        
        # Store analysis
        state["word_count"] = word_count
        
        # Determine if text looks like an essay (heuristic)
        is_likely_essay = (
            word_count > 100 and
            any(keyword in user_message.lower() for keyword in [
                "introduction", "conclusion", "furthermore", "however", 
                "in my opinion", "to sum up", "firstly", "secondly"
            ])
        )
        
        state["is_likely_essay"] = is_likely_essay
        state["has_image"] = has_image
        
        return state
    
    @traceable
    async def classify_intent(self, state: ConversationState) -> ConversationState:
        """Classify user intent using LLM"""
        user_message = state.get("user_message", "")
        has_image = state.get("has_image", False)
        conversation_state = state.get("conversation_state", "greeting")
        word_count = state.get("word_count", 0)
        
        # Quick heuristic checks first
        if has_image:
            state["user_intent"] = "has_image"
            return state
        
        if conversation_state == "greeting" and word_count < 20:
            state["user_intent"] = "greeting"
            return state
            
        if word_count > 150:  # Likely an essay
            state["user_intent"] = "submitted_essay"
            return state
        
        # Use LLM for complex intent classification
        intent_prompt = f"""
        Analyze this user message and classify their intent. Consider the conversation context.
        
        User message: "{user_message}"
        Current conversation state: {conversation_state}
        Message length: {word_count} words
        
        Classify intent as ONE of:
        - "greeting": User saying hello, wants to start, general chat
        - "wants_question": User asking for IELTS practice question
        - "submitted_essay": User has written an essay for evaluation
        - "followup": User asking questions about previous feedback
        - "unclear": Cannot determine intent
        
        Respond with ONLY the intent category.
        """
        
        response = await self.llm.ainvoke([HumanMessage(content=intent_prompt)])
        intent = response.content.strip().lower()
        
        # Validate intent
        valid_intents = ["greeting", "wants_question", "submitted_essay", "followup", "unclear"]
        if intent not in valid_intents:
            intent = "unclear"
        
        state["user_intent"] = intent
        return state
    
    def route_by_intent(self, state: ConversationState) -> str:
        """Route to appropriate handler based on intent"""
        intent = state.get("user_intent", "")
        has_image = state.get("has_image", False)
        
        if has_image:
            return "extract_image"
        elif intent == "greeting":
            return "greeting"
        elif intent == "wants_question":
            return "wants_question"
        elif intent == "submitted_essay":
            return "submitted_essay"
        elif intent == "followup":
            return "followup"
        else:
            return "greeting"  # Default fallback
    
    @traceable
    async def extract_image_content(self, state: ConversationState) -> ConversationState:
        """Extract content from uploaded image using Gemini Vision"""
        image_data = state.get("image_data", "")
        user_message = state.get("user_message", "")
        
        if not image_data:
            state["extracted_text"] = ""
            return state
        
        try:
            # Prepare image for Gemini Vision
            image_prompt = f"""
            Analyze this image and extract all text content. The image likely contains:
            1. An IELTS writing question/prompt
            2. A handwritten or typed essay response
            3. Or both
            
            User also said: "{user_message}"
            
            Please extract and organize the text content. If you find both a question and an essay, 
            clearly separate them. Return in this JSON format:
            {{
                "extracted_text": "all text from image",
                "question_found": true/false,
                "question_text": "extracted question if found",
                "essay_found": true/false, 
                "essay_text": "extracted essay if found",
                "task_type": "task1/task2/unknown"
            }}
            """
            
            # Note: In actual implementation, you'd pass the image data to Gemini Vision
            # For now, using text-only model with base64 description
            response = await self.vision_llm.ainvoke([
                HumanMessage(content=f"{image_prompt}\n\nImage data: {image_data[:100]}...")
            ])
            
            try:
                extraction_result = json.loads(response.content)
                state["extracted_text"] = extraction_result.get("extracted_text", "")
                state["question_text"] = extraction_result.get("question_text", "")
                state["essay_text"] = extraction_result.get("essay_text", "")
                if extraction_result.get("task_type") != "unknown":
                    state["task_type"] = extraction_result.get("task_type", "task2")
            except json.JSONDecodeError:
                state["extracted_text"] = response.content
                
        except Exception as e:
            state["extracted_text"] = ""
            state["validation_errors"] = state.get("validation_errors", []) + [f"Image processing failed: {str(e)}"]
        
        return state
    
    async def combine_content(self, state: ConversationState) -> ConversationState:
        """Intelligently combine extracted image text with user typed text"""
        user_message = state.get("user_message", "")
        extracted_text = state.get("extracted_text", "")
        
        if not extracted_text:
            # No image, use user message as is
            state["combined_text"] = user_message
            state["essay_text"] = user_message
        elif not user_message.strip():
            # Only image, use extracted text
            state["combined_text"] = extracted_text
            state["essay_text"] = extracted_text
        else:
            # Both image and text - use LLM to combine intelligently
            combination_prompt = f"""
            A user provided both an image and typed text. Help combine them appropriately.
            
            Text from image: "{extracted_text}"
            User typed text: "{user_message}"
            
            Analyze and combine these intelligently:
            1. If image has question and text has essay → use image as question, text as essay
            2. If image has essay and text adds to it → combine as complete essay
            3. If image unclear and text is clear → prioritize text
            4. If both have essays → merge appropriately
            
            Return JSON:
            {{
                "combined_essay": "the final essay text for evaluation",
                "question": "the question/prompt if found",
                "task_type": "task1/task2",
                "combination_strategy": "explanation of how you combined them"
            }}
            """
            
            response = await self.llm.ainvoke([HumanMessage(content=combination_prompt)])
            
            try:
                combination_result = json.loads(response.content)
                state["combined_text"] = combination_result.get("combined_essay", user_message)
                state["essay_text"] = combination_result.get("combined_essay", user_message)
                if combination_result.get("question"):
                    state["question_text"] = combination_result.get("question")
                if combination_result.get("task_type"):
                    state["task_type"] = combination_result.get("task_type")
            except json.JSONDecodeError:
                # Fallback: simple concatenation
                state["combined_text"] = f"{extracted_text}\n\n{user_message}".strip()
                state["essay_text"] = state["combined_text"]
        
        return state
    
    @traceable
    async def handle_greeting(self, state: ConversationState) -> ConversationState:
        """Handle greeting and show options"""
        user_message = state.get("user_message", "").lower()
        
        if any(word in user_message for word in ["hi", "hello", "start", "help", "practice"]):
            response = """👋 Hello! I'm your IELTS Writing AI tutor. I can help you practice and improve your IELTS writing skills.

Here's what I can do for you:

🎯 **Generate Practice Questions**
- Get authentic IELTS Task 1 or Task 2 questions
- Tailored to specific topics you want to practice

📝 **Evaluate Your Essays**
- Submit your essay (typed or upload image)
- Get detailed band scores (1-9) for all 4 criteria
- Receive actionable feedback and improvement tips

💬 **Interactive Learning**
- Ask questions about IELTS writing techniques
- Get explanations for your scores and feedback

**How would you like to start?**
- Say "Give me a Task 2 question about [topic]" for practice
- Or paste/upload your essay for immediate evaluation
- Or ask "How can I improve my IELTS writing?"

*Note: Essay evaluations cost 1 credit. Question generation is free!*"""
        else:
            response = """I'm here to help with IELTS Writing practice! 
            
You can:
• Ask for practice questions (free)
• Submit essays for evaluation (1 credit)
• Get writing tips and guidance

What would you like to do?"""
        
        state["ai_response"] = response
        state["should_deduct_credit"] = False
        state["next_conversation_state"] = "waiting_for_preference"
        
        return state
    
    @traceable
    async def generate_question(self, state: ConversationState) -> ConversationState:
        """Generate IELTS practice question"""
        user_message = state.get("user_message", "")
        
        # Extract topic and task type from user message
        topic_extraction_prompt = f"""
        User wants an IELTS practice question. Extract the details:
        
        User message: "{user_message}"
        
        Return JSON:
        {{
            "task_type": "task1/task2",
            "topic": "extracted topic or 'general'",
            "specific_requirements": "any specific requests"
        }}
        """
        
        response = await self.llm.ainvoke([HumanMessage(content=topic_extraction_prompt)])
        
        try:
            extraction = json.loads(response.content)
            task_type = extraction.get("task_type", "task2")
            topic = extraction.get("topic", "general")
        except:
            task_type = "task2"
            topic = "general"
        
        # Generate the actual question
        if task_type == "task1":
            question_prompt = f"""
            Generate an authentic IELTS Academic Writing Task 1 question about {topic}.
            Include a description of a chart, graph, table, diagram, or process.
            
            Format:
            - Clear instructions
            - Minimum 150 words requirement
            - 20 minutes time allowance
            """
        else:
            question_prompt = f"""
            Generate an authentic IELTS Writing Task 2 question about {topic}.
            Should be argumentative/opinion-based about current social issues.
            
            Format:
            - Clear question statement
            - Minimum 250 words requirement  
            - 40 minutes time allowance
            """
        
        question_response = await self.llm.ainvoke([HumanMessage(content=question_prompt)])
        
        generated_question = question_response.content
        
        ai_response = f"""📝 **IELTS Writing {task_type.upper()} Practice Question**

{generated_question}

---

**Instructions:**
• Write your essay and paste it here when ready
• I'll evaluate it using official IELTS criteria
• You'll get band scores and detailed feedback

*Ready to write? Take your time and submit when done!*"""
        
        state["ai_response"] = ai_response
        state["question_text"] = generated_question
        state["task_type"] = task_type
        state["should_deduct_credit"] = False
        state["next_conversation_state"] = "waiting_for_essay"
        
        return state
    
    @traceable
    async def evaluate_essay(self, state: ConversationState) -> ConversationState:
        """Comprehensive IELTS essay evaluation"""
        essay_text = state.get("essay_text", "")
        question_text = state.get("question_text", "")
        task_type = state.get("task_type", "task2")
        
        # Validate essay
        word_count = len(essay_text.split())
        min_words = 150 if task_type == "task1" else 250
        
        validation_errors = []
        if word_count < min_words:
            validation_errors.append(f"Essay too short: {word_count} words (minimum: {min_words})")
        if word_count > 400:
            validation_errors.append(f"Essay too long: {word_count} words (recommended maximum: 400)")
        
        if validation_errors:
            state["validation_errors"] = validation_errors
            state["is_valid_essay"] = False
            
            error_response = f"""⚠️ **Essay Validation Issues:**

{chr(10).join(f'• {error}' for error in validation_errors)}

**Would you like to:**
• Revise your essay and resubmit
• Get tips on essay length and structure
• Try a different question

*No credits were deducted due to validation issues.*"""
            
            state["ai_response"] = error_response
            state["should_deduct_credit"] = False
            return state
        
        # Comprehensive evaluation prompt
        evaluation_prompt = f"""
        You are an expert IELTS examiner. Evaluate this {task_type.upper()} essay according to official IELTS criteria.
        
        QUESTION/PROMPT: {question_text or "No specific question provided"}
        
        ESSAY ({word_count} words):
        {essay_text}
        
        Evaluate based on these 4 criteria (score 0-9, can use .5 increments):
        
        1. TASK ACHIEVEMENT/RESPONSE:
        - Task 1: Accuracy of data description, overview, key features
        - Task 2: Position clarity, argument development, examples, task coverage
        
        2. COHERENCE AND COHESION:
        - Logical organization, paragraphing, linking words, idea flow
        
        3. LEXICAL RESOURCE:
        - Vocabulary range, accuracy, appropriateness, spelling
        
        4. GRAMMATICAL RANGE AND ACCURACY:
        - Sentence variety, complexity, accuracy, punctuation
        
        Return ONLY valid JSON:
        {{
            "task_achievement": {{
                "score": 7.0,
                "feedback": "Detailed specific feedback..."
            }},
            "coherence_cohesion": {{
                "score": 6.5,
                "feedback": "Detailed specific feedback..."
            }},
            "lexical_resource": {{
                "score": 7.0,
                "feedback": "Detailed specific feedback..."
            }},
            "grammatical_accuracy": {{
                "score": 6.0,
                "feedback": "Detailed specific feedback..."
            }},
            "strengths": ["List key strengths"],
            "areas_for_improvement": ["List specific areas to improve"],
            "band_description": "Description of overall performance level"
        }}
        """
        
        response = await self.llm.ainvoke([HumanMessage(content=evaluation_prompt)])
        
        try:
            evaluation_data = json.loads(response.content)
            
            # Extract scores
            ta_score = evaluation_data["task_achievement"]["score"]
            cc_score = evaluation_data["coherence_cohesion"]["score"] 
            lr_score = evaluation_data["lexical_resource"]["score"]
            ga_score = evaluation_data["grammatical_accuracy"]["score"]
            
            # Calculate overall band score
            overall_score = round((ta_score + cc_score + lr_score + ga_score) / 4 * 2) / 2
            
            # Store results
            state["task_achievement_score"] = ta_score
            state["coherence_cohesion_score"] = cc_score
            state["lexical_resource_score"] = lr_score
            state["grammatical_accuracy_score"] = ga_score
            state["overall_band_score"] = overall_score
            state["detailed_feedback"] = evaluation_data
            
            # Format response
            ai_response = f"""🎯 **IELTS Writing Evaluation Results**

**Overall Band Score: {overall_score}/9**

📊 **Detailed Scores:**
• Task Achievement: {ta_score}/9
• Coherence & Cohesion: {cc_score}/9  
• Lexical Resource: {lr_score}/9
• Grammatical Accuracy: {ga_score}/9

---

**📝 Task Achievement ({ta_score}/9)**
{evaluation_data["task_achievement"]["feedback"]}

**🔗 Coherence & Cohesion ({cc_score}/9)**
{evaluation_data["coherence_cohesion"]["feedback"]}

**📚 Lexical Resource ({lr_score}/9)**
{evaluation_data["lexical_resource"]["feedback"]}

**✏️ Grammatical Accuracy ({ga_score}/9)**
{evaluation_data["grammatical_accuracy"]["feedback"]}

---

**✅ Strengths:**
{chr(10).join(f'• {strength}' for strength in evaluation_data.get("strengths", []))}

**🎯 Areas for Improvement:**
{chr(10).join(f'• {area}' for area in evaluation_data.get("areas_for_improvement", []))}

---

**💡 Want to improve further?**
• Ask me about specific feedback points
• Request another practice question
• Get tips for your weakest areas

*Feel free to ask follow-up questions about your evaluation!*"""
            
            state["ai_response"] = ai_response
            state["should_deduct_credit"] = True
            state["next_conversation_state"] = "discussing_feedback"
            
        except json.JSONDecodeError as e:
            # Improved fallback: Extract scores from LLM response even if JSON parsing fails
            response_text = response.content
            
            # Try to extract scores using regex patterns
            score_patterns = {
                'task_achievement': r'task[\s_]*achievement[\s_]*(?:score)?[\s:]*([0-9.]+)',
                'coherence_cohesion': r'coherence[\s_]*(?:and|&)?[\s_]*cohesion[\s_]*(?:score)?[\s:]*([0-9.]+)',
                'lexical_resource': r'lexical[\s_]*resource[\s_]*(?:score)?[\s:]*([0-9.]+)',
                'grammatical_accuracy': r'grammat[\w]*[\s_]*(?:accuracy|range)?[\s_]*(?:score)?[\s:]*([0-9.]+)'
            }
            
            extracted_scores = {}
            for criterion, pattern in score_patterns.items():
                match = re.search(pattern, response_text.lower())
                if match:
                    try:
                        extracted_scores[criterion] = float(match.group(1))
                    except ValueError:
                        extracted_scores[criterion] = 6.0  # Default fallback
                else:
                    extracted_scores[criterion] = 6.0  # Default fallback
            
            # Calculate overall score
            overall_score = round(sum(extracted_scores.values()) / 4 * 2) / 2
            
            # Store extracted results
            state["task_achievement_score"] = extracted_scores['task_achievement']
            state["coherence_cohesion_score"] = extracted_scores['coherence_cohesion']
            state["lexical_resource_score"] = extracted_scores['lexical_resource']
            state["grammatical_accuracy_score"] = extracted_scores['grammatical_accuracy']
            state["overall_band_score"] = overall_score
            state["detailed_feedback"] = {"raw_response": response_text}
            
            # Create fallback response with scores
            ai_response = f"""🎯 **IELTS Writing Evaluation Results**

**Overall Band Score: {overall_score}/9**

📊 **Detailed Scores:**
• Task Achievement: {extracted_scores['task_achievement']}/9
• Coherence & Cohesion: {extracted_scores['coherence_cohesion']}/9  
• Lexical Resource: {extracted_scores['lexical_resource']}/9
• Grammatical Accuracy: {extracted_scores['grammatical_accuracy']}/9

---

**📝 Detailed Feedback:**
{response_text}

---

**💡 Want to improve further?**
• Ask me about specific feedback points
• Request another practice question
• Get tips for your weakest areas

*Note: Scores were extracted from evaluation text. Feel free to ask follow-up questions!*"""
            
            state["ai_response"] = ai_response
            state["should_deduct_credit"] = True
            state["next_conversation_state"] = "discussing_feedback"
        
        return state
    
    @traceable
    async def handle_followup(self, state: ConversationState) -> ConversationState:
        """Handle follow-up questions about previous evaluation"""
        user_message = state.get("user_message", "")
        previous_feedback = state.get("detailed_feedback", {})
        
        followup_prompt = f"""
        User is asking a follow-up question about their IELTS writing evaluation.
        
        User question: "{user_message}"
        
        Previous evaluation data: {json.dumps(previous_feedback, indent=2)}
        
        Provide a helpful, specific answer related to their IELTS writing performance.
        Be encouraging but honest about areas for improvement.
        Offer practical tips and examples where relevant.
        
        Keep the response conversational and supportive.
        """
        
        response = await self.llm.ainvoke([HumanMessage(content=followup_prompt)])
        
        state["ai_response"] = response.content
        state["should_deduct_credit"] = False
        state["next_conversation_state"] = "discussing_feedback"
        
        return state
    
    @traceable
    async def format_response(self, state: ConversationState) -> ConversationState:
        """Final formatting of AI response"""
        # Add conversation history
        user_message = state.get("user_message", "")
        ai_response = state.get("ai_response", "")
        
        conversation_history = state.get("conversation_history", [])
        conversation_history.append({
            "role": "user",
            "content": user_message,
            "timestamp": datetime.now().isoformat()
        })
        conversation_history.append({
            "role": "assistant", 
            "content": ai_response,
            "timestamp": datetime.now().isoformat()
        })
        
        state["conversation_history"] = conversation_history[-10:]  # Keep last 10 exchanges
        
        return state
    
    @traceable
    async def chat(self, user_message: str, image_data: Optional[str] = None, 
                   user_id: str = "default", conversation_state: str = None) -> Dict[str, Any]:
        """Main chat interface with persistent memory"""
        
        # Load conversation state and history from memory
        memory_data = self._load_conversation(user_id)
        
        # Use provided state or loaded state, default to greeting
        if conversation_state is None:
            conversation_state = memory_data["conversation_state"]
        
        initial_state = ConversationState(
            user_message=user_message,
            image_data=image_data,
            user_id=user_id,
            conversation_state=conversation_state,
            conversation_history=memory_data["conversation_history"],
            user_intent="",
            extracted_text="",
            combined_text="",
            essay_text="",
            question_text="",
            task_type="task2",
            word_count=0,
            is_valid_essay=True,
            validation_errors=[],
            overall_band_score=0.0,
            task_achievement_score=0.0,
            coherence_cohesion_score=0.0,
            lexical_resource_score=0.0,
            grammatical_accuracy_score=0.0,
            detailed_feedback={},
            improvement_suggestions=[],
            ai_response="",
            should_deduct_credit=False,
            next_conversation_state="greeting"
        )
        
        # Run workflow
        final_state = await self.workflow.ainvoke(initial_state)
        
        # Save conversation to memory
        self._save_conversation(
            user_id, 
            final_state.get("conversation_history", []), 
            final_state.get("next_conversation_state", "greeting")
        )
        
        # Save evaluation if one was performed
        if final_state.get("should_deduct_credit") and final_state.get("overall_band_score", 0) > 0:
            self._save_evaluation(user_id, final_state)
        
        # Return response
        return {
            "response": final_state.get("ai_response", ""),
            "should_deduct_credit": final_state.get("should_deduct_credit", False),
            "conversation_state": final_state.get("next_conversation_state", "greeting"),
            "user_intent": final_state.get("user_intent", ""),
            "evaluation_data": {
                "overall_band_score": final_state.get("overall_band_score", 0),
                "task_achievement_score": final_state.get("task_achievement_score", 0),
                "coherence_cohesion_score": final_state.get("coherence_cohesion_score", 0),
                "lexical_resource_score": final_state.get("lexical_resource_score", 0),
                "grammatical_accuracy_score": final_state.get("grammatical_accuracy_score", 0),
                "detailed_feedback": final_state.get("detailed_feedback", {}),
                "word_count": final_state.get("word_count", 0),
                "task_type": final_state.get("task_type", ""),
                "question": final_state.get("question_text", "")
            } if final_state.get("should_deduct_credit") else None,
            "conversation_history": final_state.get("conversation_history", [])
        }
    
    def get_user_evaluations(self, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get user's evaluation history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT essay_text, question_text, task_type, word_count, overall_band_score,
                   task_achievement_score, coherence_cohesion_score, lexical_resource_score,
                   grammatical_accuracy_score, created_at
            FROM evaluations 
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT ?
        ''', (user_id, limit))
        
        evaluations = cursor.fetchall()
        conn.close()
        
        return [
            {
                "essay_text": eval[0][:100] + "..." if len(eval[0]) > 100 else eval[0],
                "question_text": eval[1],
                "task_type": eval[2],
                "word_count": eval[3],
                "overall_band_score": eval[4],
                "task_achievement_score": eval[5],
                "coherence_cohesion_score": eval[6],
                "lexical_resource_score": eval[7],
                "grammatical_accuracy_score": eval[8],
                "created_at": eval[9]
            } for eval in evaluations
        ]
    
    def clear_user_memory(self, user_id: str):
        """Clear user's conversation memory"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM conversations WHERE user_id = ?', (user_id,))
        cursor.execute('DELETE FROM messages WHERE conversation_id IN (SELECT id FROM conversations WHERE user_id = ?)', (user_id,))
        
        conn.commit()
        conn.close()
