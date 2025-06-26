-- Sample Data Population Script for AI Model Platform Database
-- Created: June 25, 2025
-- Description: Populates the database with realistic test data for development and testing

-- Note: This script assumes the main database schema has been created
-- Run this after executing database_schema.sql

-- Begin transaction to ensure data consistency
BEGIN;

-- Insert sample users
INSERT INTO users (username, email, password_hash, first_name, last_name, date_of_birth, phone_number, country, city, bio, status, email_verified) VALUES
('john_doe', 'john.doe@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewkOTDjDQJD8b5nu', 'John', 'Doe', '1990-05-15', '+1-555-0101', 'USA', 'San Francisco', 'Software engineer interested in AI and machine learning applications.', 'active', TRUE),
('jane_smith', 'jane.smith@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewkOTDjDQJD8b5nu', 'Jane', 'Smith', '1988-11-22', '+44-20-7946-0958', 'UK', 'London', 'Data scientist working on natural language processing projects.', 'active', TRUE),
('bob_wilson', 'bob.wilson@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewkOTDjDQJD8b5nu', 'Bob', 'Wilson', '1992-03-08', '+1-416-555-0123', 'Canada', 'Toronto', 'Full-stack developer exploring AI integration in web applications.', 'active', TRUE),
('alice_johnson', 'alice.johnson@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewkOTDjDQJD8b5nu', 'Alice', 'Johnson', '1985-09-30', '+61-2-9374-4000', 'Australia', 'Sydney', 'Product manager focusing on AI-powered consumer applications.', 'active', TRUE),
('carlos_mendez', 'carlos.mendez@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewkOTDjDQJD8b5nu', 'Carlos', 'Mendez', '1991-07-12', '+34-91-123-4567', 'Spain', 'Madrid', 'Research scientist working on computer vision and image processing.', 'active', TRUE),
('test_user', 'test@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewkOTDjDQJD8b5nu', 'Test', 'User', '1995-01-01', NULL, 'USA', 'New York', 'Test account for development purposes.', 'pending_verification', FALSE);

-- Insert sample developers
INSERT INTO developers (username, email, password_hash, first_name, last_name, company_name, website_url, github_profile, linkedin_profile, phone_number, country, city, bio, expertise_areas, years_of_experience, status, email_verified, api_quota_limit) VALUES
('ai_innovator', 'sarah@aiinnovations.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewkOTDjDQJD8b5nu', 'Sarah', 'Chen', 'AI Innovations Inc', 'https://aiinnovations.com', 'sarahchen-ai', 'sarah-chen-ai', '+1-650-555-0199', 'USA', 'Palo Alto', 'AI researcher and entrepreneur specializing in natural language processing and conversational AI systems.', ARRAY['machine_learning', 'nlp', 'deep_learning', 'transformers'], 8, 'active', TRUE, 50000),
('ml_master', 'alex@mlstudio.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewkOTDjDQJD8b5nu', 'Alex', 'Rodriguez', 'ML Studio', 'https://mlstudio.com', 'alexmlstudio', 'alex-rodriguez-ml', '+1-415-555-0142', 'USA', 'San Francisco', 'Machine learning engineer with expertise in computer vision and generative models.', ARRAY['computer_vision', 'generative_ai', 'pytorch', 'tensorflow'], 6, 'active', TRUE, 30000),
('code_wizard', 'emma@codegenius.io', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewkOTDjDQJD8b5nu', 'Emma', 'Thompson', 'CodeGenius', 'https://codegenius.io', 'emmacodegenius', 'emma-thompson-dev', '+44-20-7946-0741', 'UK', 'Cambridge', 'Software architect specializing in AI-powered code generation and analysis tools.', ARRAY['code_generation', 'static_analysis', 'compilers', 'language_models'], 10, 'active', TRUE, 40000),
('data_sage', 'michael@datasolutions.de', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewkOTDjDQJD8b5nu', 'Michael', 'Weber', 'Data Solutions GmbH', 'https://datasolutions.de', 'michaelweber-data', 'michael-weber-data', '+49-30-12345678', 'Germany', 'Berlin', 'Data scientist and ML engineer focused on business intelligence and predictive analytics.', ARRAY['data_analysis', 'predictive_modeling', 'business_intelligence', 'statistics'], 7, 'active', TRUE, 25000),
('startup_dev', 'lisa@aiprototype.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewkOTDjDQJD8b5nu', 'Lisa', 'Park', 'AI Prototype Labs', NULL, 'lisapark-ai', NULL, '+82-2-1234-5678', 'South Korea', 'Seoul', 'Independent AI developer creating innovative prototypes and experimental models.', ARRAY['prototyping', 'research', 'experimental_ai'], 4, 'active', TRUE, 15000);

-- Get developer IDs for foreign key references (using known emails)
-- Note: In a real application, you'd typically get these IDs from the insert operations or use CTEs

-- Insert sample models
INSERT INTO models (developer_id, model_name, display_name, description, detailed_description, version, api_name, api_key, api_endpoint, category, tags, input_format, output_format, max_input_length, max_output_length, response_time_ms, accuracy_score, status, is_public, documentation_url, example_request, example_response, featured) VALUES
-- Sarah's models (AI Innovations)
((SELECT developer_id FROM developers WHERE email = 'sarah@aiinnovations.com'), 'smart-chat-v2', 'SmartChat Pro', 'Advanced conversational AI model for customer service and support', 'SmartChat Pro is a state-of-the-art conversational AI model trained on millions of customer service interactions. It provides intelligent, context-aware responses and can handle complex multi-turn conversations with high accuracy.', '2.1.0', 'smartchat_pro_v2', 'sk-ai_innovations_smartchat_abc123def456ghi789', 'https://api.aiinnovations.com/v2/smartchat', 'text_generation', ARRAY['conversational_ai', 'customer_service', 'chatbot', 'nlp'], 'text', 'text', 4000, 2000, 850, 0.94, 'active', TRUE, 'https://docs.aiinnovations.com/smartchat', '{"prompt": "Hello, I need help with my order", "context": "customer_service", "max_tokens": 150}', '{"response": "I''d be happy to help you with your order! Could you please provide me with your order number so I can look up the details for you?", "confidence": 0.96}', TRUE),

((SELECT developer_id FROM developers WHERE email = 'sarah@aiinnovations.com'), 'text-summarizer', 'Neural Summarizer', 'Intelligent text summarization for documents and articles', 'Neural Summarizer uses advanced transformer architecture to create concise, coherent summaries of long-form text. Perfect for research papers, news articles, and business documents.', '1.3.2', 'neural_summarizer_v1', 'sk-ai_innovations_summarizer_xyz789abc123def456', 'https://api.aiinnovations.com/v1/summarize', 'summarization', ARRAY['text_processing', 'summarization', 'document_analysis'], 'text', 'text', 10000, 500, 1200, 0.91, 'active', TRUE, 'https://docs.aiinnovations.com/summarizer', '{"text": "Long article text here...", "summary_length": "medium", "style": "bullet_points"}', '{"summary": "• Key point 1\\n• Key point 2\\n• Key point 3", "original_length": 2450, "summary_length": 180}', FALSE),

-- Alex's models (ML Studio)
((SELECT developer_id FROM developers WHERE email = 'alex@mlstudio.com'), 'vision-analyzer', 'ImageSense AI', 'Advanced image recognition and analysis system', 'ImageSense AI provides comprehensive image analysis including object detection, scene understanding, and content moderation. Built with cutting-edge computer vision models.', '3.0.1', 'imagesense_ai_v3', 'sk-mlstudio_imagesense_mno456pqr789stu012', 'https://api.mlstudio.com/v3/analyze', 'image_generation', ARRAY['computer_vision', 'object_detection', 'image_analysis', 'content_moderation'], 'image', 'json', 1, 1000, 2100, 0.96, 'active', TRUE, 'https://docs.mlstudio.com/imagesense', '{"image_url": "https://example.com/image.jpg", "analysis_types": ["objects", "scene", "text"]}', '{"objects": [{"name": "person", "confidence": 0.98}, {"name": "car", "confidence": 0.87}], "scene": "urban_street", "text_detected": "STOP"}', TRUE),

((SELECT developer_id FROM developers WHERE email = 'alex@mlstudio.com'), 'art-creator', 'DreamCanvas', 'AI-powered artistic image generation', 'DreamCanvas creates stunning, original artwork based on text descriptions. Uses advanced diffusion models to generate high-quality images in various artistic styles.', '2.5.0', 'dreamcanvas_v2', 'sk-mlstudio_dreamcanvas_vwx123yza456bcd789', 'https://api.mlstudio.com/v2/generate', 'image_generation', ARRAY['image_generation', 'art', 'creative_ai', 'diffusion_models'], 'text', 'image', 500, 1, 5500, 0.89, 'active', TRUE, 'https://docs.mlstudio.com/dreamcanvas', '{"prompt": "A serene mountain lake at sunset", "style": "impressionist", "resolution": "1024x1024"}', '{"image_url": "https://cdn.mlstudio.com/generated/abc123.jpg", "seed": 42, "generation_time": 5.2}', TRUE),

-- Emma's models (CodeGenius)
((SELECT developer_id FROM developers WHERE email = 'emma@codegenius.io'), 'code-assistant', 'DevMentor AI', 'Intelligent code generation and programming assistant', 'DevMentor AI helps developers write better code faster. It provides intelligent code completion, bug detection, and can generate entire functions based on natural language descriptions.', '4.2.1', 'devmentor_ai_v4', 'sk-codegenius_devmentor_efg789hij012klm345', 'https://api.codegenius.io/v4/assist', 'code_generation', ARRAY['code_generation', 'programming', 'software_development', 'debugging'], 'text', 'text', 3000, 1500, 1800, 0.92, 'active', TRUE, 'https://docs.codegenius.io/devmentor', '{"task": "create a function to sort array", "language": "python", "context": "data processing"}', '{"code": "def sort_array(arr, reverse=False):\\n    return sorted(arr, reverse=reverse)", "explanation": "This function sorts an array with optional reverse parameter"}', FALSE),

((SELECT developer_id FROM developers WHERE email = 'emma@codegenius.io'), 'bug-hunter', 'BugDetector Pro', 'Advanced static code analysis and bug detection', 'BugDetector Pro scans codebases to identify potential bugs, security vulnerabilities, and code quality issues. Supports multiple programming languages and frameworks.', '1.8.3', 'bugdetector_pro_v1', 'sk-codegenius_bugdetector_nop456qrs789tuv012', 'https://api.codegenius.io/v1/analyze', 'code_generation', ARRAY['static_analysis', 'bug_detection', 'security', 'code_quality'], 'text', 'json', 50000, 2000, 3200, 0.88, 'active', TRUE, 'https://docs.codegenius.io/bugdetector', '{"code": "function example() { var x; return x + 1; }", "language": "javascript"}', '{"issues": [{"type": "warning", "line": 1, "message": "Variable x used before initialization"}], "score": 7.5}', FALSE),

-- Michael's models (Data Solutions)
((SELECT developer_id FROM developers WHERE email = 'michael@datasolutions.de'), 'trend-predictor', 'MarketSeer', 'Business trend analysis and prediction engine', 'MarketSeer analyzes business data to identify trends, predict market movements, and provide actionable insights for strategic decision making.', '2.3.0', 'marketseer_v2', 'sk-datasolutions_marketseer_wxy123zab456cde789', 'https://api.datasolutions.de/v2/predict', 'data_analysis', ARRAY['business_intelligence', 'predictive_analytics', 'market_analysis', 'forecasting'], 'json', 'json', 5000, 1000, 2800, 0.87, 'active', TRUE, 'https://docs.datasolutions.de/marketseer', '{"data": {"sales": [100, 120, 95, 140]}, "prediction_horizon": 30}', '{"predicted_values": [145, 152, 148], "confidence_interval": [140, 160], "trend": "upward"}', FALSE),

-- Lisa's experimental model (AI Prototype Labs)
((SELECT developer_id FROM developers WHERE email = 'lisa@aiprototype.com'), 'multi-modal-ai', 'OmniSense Beta', 'Experimental multi-modal AI system', 'OmniSense is an experimental AI system that can process and understand multiple types of input including text, images, and audio. Currently in beta testing phase.', '0.8.0-beta', 'omnisense_beta', 'sk-aiprototype_omnisense_fgh890ijk123lmn456', 'https://api.aiprototype.com/beta/omnisense', 'other', ARRAY['multimodal', 'experimental', 'research', 'beta'], 'json', 'json', 2000, 800, 4500, 0.78, 'under_review', TRUE, 'https://docs.aiprototype.com/omnisense', '{"inputs": {"text": "Describe this", "image_url": "https://example.com/img.jpg"}}', '{"description": "A complex scene with multiple elements", "modality_confidence": {"text": 0.95, "image": 0.82}}', FALSE);

-- Insert sample user history (interactions)
INSERT INTO user_history (user_id, model_id, session_id, prompt, response, response_status, request_timestamp, response_timestamp, response_time_ms, input_tokens, output_tokens, cost_incurred, user_rating, user_feedback, ip_address, user_agent, api_version) VALUES
-- John Doe's interactions
((SELECT user_id FROM users WHERE username = 'john_doe'), (SELECT model_id FROM models WHERE api_name = 'smartchat_pro_v2'), 'sess_john_001', 'Hello, I need help setting up my API integration', 'Hi! I''d be happy to help you with your API integration. What specific aspect would you like assistance with? Are you looking for authentication setup, endpoint documentation, or help with a particular programming language?', 'success', CURRENT_TIMESTAMP - INTERVAL '2 hours', CURRENT_TIMESTAMP - INTERVAL '2 hours' + INTERVAL '0.85 seconds', 850, 15, 42, 0.021, 5, 'Excellent response, very helpful!', '192.168.1.100', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', 'v2'),

((SELECT user_id FROM users WHERE username = 'john_doe'), (SELECT model_id FROM models WHERE api_name = 'devmentor_ai_v4'), 'sess_john_002', 'Create a function to validate email addresses in Python', 'Here''s a Python function to validate email addresses:\n\n```python\nimport re\n\ndef validate_email(email):\n    pattern = r''^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$''\n    return re.match(pattern, email) is not None\n\n# Example usage:\nprint(validate_email("user@example.com"))  # True\nprint(validate_email("invalid.email"))     # False\n```\n\nThis function uses regex to check for a valid email format.', 'success', CURRENT_TIMESTAMP - INTERVAL '1 day', CURRENT_TIMESTAMP - INTERVAL '1 day' + INTERVAL '1.8 seconds', 1800, 12, 89, 0.045, 4, 'Good code example, works as expected.', '192.168.1.100', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', 'v4'),

-- Jane Smith's interactions
((SELECT user_id FROM users WHERE username = 'jane_smith'), (SELECT model_id FROM models WHERE api_name = 'neural_summarizer_v1'), 'sess_jane_001', 'Please summarize this research paper about machine learning advances in natural language processing...', '• Recent advances in transformer architectures have significantly improved NLP performance\n• Self-attention mechanisms enable better context understanding\n• Pre-trained language models show strong transfer learning capabilities\n• Multimodal approaches combining text and images show promising results\n• Efficiency improvements make large models more practical for deployment', 'success', CURRENT_TIMESTAMP - INTERVAL '3 hours', CURRENT_TIMESTAMP - INTERVAL '3 hours' + INTERVAL '1.2 seconds', 1200, 1847, 67, 0.092, 5, 'Perfect summary, captured all key points!', '203.0.113.45', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36', 'v1'),

((SELECT user_id FROM users WHERE username = 'jane_smith'), (SELECT model_id FROM models WHERE api_name = 'imagesense_ai_v3'), 'sess_jane_002', 'Analyze this conference room photo for accessibility features', '{"objects": [{"name": "wheelchair_ramp", "confidence": 0.94}, {"name": "adjustable_table", "confidence": 0.87}, {"name": "hearing_loop_sign", "confidence": 0.91}], "accessibility_score": 8.5, "recommendations": ["Add tactile indicators", "Ensure adequate lighting"]}', 'success', CURRENT_TIMESTAMP - INTERVAL '5 hours', CURRENT_TIMESTAMP - INTERVAL '5 hours' + INTERVAL '2.1 seconds', 2100, 8, 156, 0.078, 4, 'Very detailed analysis, helpful for compliance.', '203.0.113.45', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36', 'v3'),

-- Bob Wilson's interactions
((SELECT user_id FROM users WHERE username = 'bob_wilson'), (SELECT model_id FROM models WHERE api_name = 'dreamcanvas_v2'), 'sess_bob_001', 'Generate an image of a futuristic city skyline at night with neon lights', '{"image_url": "https://cdn.mlstudio.com/generated/futuristic_city_xyz789.jpg", "prompt_used": "futuristic city skyline at night with neon lights, cyberpunk style, high detail", "generation_time": 5.8, "style_applied": "cyberpunk", "resolution": "1024x1024"}', 'success', CURRENT_TIMESTAMP - INTERVAL '1 day', CURRENT_TIMESTAMP - INTERVAL '1 day' + INTERVAL '5.8 seconds', 5800, 18, 1, 0.145, 5, 'Amazing artwork! Exactly what I envisioned.', '198.51.100.23', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36', 'v2'),

-- Alice Johnson's interactions
((SELECT user_id FROM users WHERE username = 'alice_johnson'), (SELECT model_id FROM models WHERE api_name = 'marketseer_v2'), 'sess_alice_001', 'Analyze Q4 sales trends for tech products', '{"trend_analysis": {"direction": "upward", "strength": 0.78, "seasonality": "high_q4"}, "predicted_growth": 0.15, "key_factors": ["holiday_shopping", "product_launches", "supply_chain_recovery"], "confidence": 0.87, "recommendation": "Increase inventory for Q4 surge"}', 'success', CURRENT_TIMESTAMP - INTERVAL '6 hours', CURRENT_TIMESTAMP - INTERVAL '6 hours' + INTERVAL '2.8 seconds', 2800, 25, 198, 0.124, 4, 'Insightful analysis for business planning.', '172.16.0.45', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Edge/91.0', 'v2'),

-- Carlos Mendez's interactions
((SELECT user_id FROM users WHERE username = 'carlos_mendez'), (SELECT model_id FROM models WHERE api_name = 'bugdetector_pro_v1'), 'sess_carlos_001', 'Analyze this JavaScript code for potential security issues', '{"security_issues": [{"type": "XSS_vulnerability", "line": 15, "severity": "high", "description": "Unescaped user input in DOM manipulation"}, {"type": "SQL_injection_risk", "line": 28, "severity": "medium", "description": "String concatenation in database query"}], "overall_score": 6.2, "recommendations": ["Use parameterized queries", "Implement input sanitization"]}', 'success', CURRENT_TIMESTAMP - INTERVAL '4 hours', CURRENT_TIMESTAMP - INTERVAL '4 hours' + INTERVAL '3.2 seconds', 3200, 156, 245, 0.089, 5, 'Found critical issues I missed. Very thorough!', '10.0.0.67', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0', 'v1');

-- Insert sample model reviews
INSERT INTO model_reviews (model_id, user_id, rating, review_title, review_text, is_verified_user, helpful_votes, total_votes) VALUES
-- Reviews for SmartChat Pro
((SELECT model_id FROM models WHERE api_name = 'smartchat_pro_v2'), (SELECT user_id FROM users WHERE username = 'john_doe'), 5, 'Excellent for customer service', 'We''ve been using SmartChat Pro for our customer support for 3 months now. The responses are incredibly natural and it handles complex queries very well. Highly recommended!', TRUE, 12, 15),
((SELECT model_id FROM models WHERE api_name = 'smartchat_pro_v2'), (SELECT user_id FROM users WHERE username = 'jane_smith'), 4, 'Good but room for improvement', 'Overall solid performance. The AI understands context well, but sometimes gives overly verbose responses. Would benefit from more concise output options.', TRUE, 8, 10),
((SELECT model_id FROM models WHERE api_name = 'smartchat_pro_v2'), (SELECT user_id FROM users WHERE username = 'alice_johnson'), 5, 'Game-changer for our business', 'This has transformed our customer support operations. Response quality is consistently high and it integrates seamlessly with our existing systems.', FALSE, 15, 18),

-- Reviews for ImageSense AI
((SELECT model_id FROM models WHERE api_name = 'imagesense_ai_v3'), (SELECT user_id FROM users WHERE username = 'jane_smith'), 4, 'Very accurate image analysis', 'The object detection is impressive and the accuracy is very high. Great for content moderation tasks. API is well-documented and easy to use.', TRUE, 9, 11),
((SELECT model_id FROM models WHERE api_name = 'imagesense_ai_v3'), (SELECT user_id FROM users WHERE username = 'carlos_mendez'), 5, 'Perfect for computer vision projects', 'I''ve tested this against several other vision APIs and this one consistently delivers the best results. The response time is also excellent.', FALSE, 7, 8),

-- Reviews for DevMentor AI
((SELECT model_id FROM models WHERE api_name = 'devmentor_ai_v4'), (SELECT user_id FROM users WHERE username = 'john_doe'), 4, 'Helpful coding assistant', 'Great for generating boilerplate code and explaining complex algorithms. Sometimes the solutions could be more optimized, but overall very useful.', TRUE, 6, 9),
((SELECT model_id FROM models WHERE api_name = 'devmentor_ai_v4'), (SELECT user_id FROM users WHERE username = 'bob_wilson'), 5, 'Speeds up development significantly', 'This tool has become essential in my workflow. The code quality is high and it saves me hours of development time every week.', FALSE, 11, 12),

-- Reviews for DreamCanvas
((SELECT model_id FROM models WHERE api_name = 'dreamcanvas_v2'), (SELECT user_id FROM users WHERE username = 'bob_wilson'), 5, 'Stunning AI-generated art', 'The quality of generated images is absolutely incredible. Perfect for creative projects and marketing materials. Worth every penny!', TRUE, 14, 16),
((SELECT model_id FROM models WHERE api_name = 'dreamcanvas_v2'), (SELECT user_id FROM users WHERE username = 'alice_johnson'), 4, 'Great for concept art', 'We use this for rapid prototyping of visual concepts. The variety of styles available is impressive. Could use more control over specific details.', FALSE, 5, 7),

-- Reviews for MarketSeer
((SELECT model_id FROM models WHERE api_name = 'marketseer_v2'), (SELECT user_id FROM users WHERE username = 'alice_johnson'), 4, 'Solid business intelligence tool', 'The trend analysis is quite accurate and has helped us make better inventory decisions. The confidence scores are particularly useful.', TRUE, 8, 10),

-- Reviews for BugDetector Pro
((SELECT model_id FROM models WHERE api_name = 'bugdetector_pro_v1'), (SELECT user_id FROM users WHERE username = 'carlos_mendez'), 5, 'Caught bugs I missed', 'This tool found several critical security vulnerabilities in our codebase that our team had overlooked. Essential for any serious development project.', TRUE, 13, 14);

-- Insert sample API usage logs
INSERT INTO api_usage_logs (user_id, developer_id, model_id, api_key_used, request_method, request_path, response_status_code, request_size_bytes, response_size_bytes, processing_time_ms) VALUES
-- Recent API calls
((SELECT user_id FROM users WHERE username = 'john_doe'), (SELECT developer_id FROM developers WHERE username = 'ai_innovator'), (SELECT model_id FROM models WHERE api_name = 'smartchat_pro_v2'), 'sk-ai_innovations_smartchat_abc123def456ghi789', 'POST', '/v2/smartchat/generate', 200, 145, 687, 850),
((SELECT user_id FROM users WHERE username = 'jane_smith'), (SELECT developer_id FROM developers WHERE username = 'ai_innovator'), (SELECT model_id FROM models WHERE api_name = 'neural_summarizer_v1'), 'sk-ai_innovations_summarizer_xyz789abc123def456', 'POST', '/v1/summarize', 200, 8934, 456, 1200),
((SELECT user_id FROM users WHERE username = 'bob_wilson'), (SELECT developer_id FROM developers WHERE username = 'ml_master'), (SELECT model_id FROM models WHERE api_name = 'dreamcanvas_v2'), 'sk-mlstudio_dreamcanvas_vwx123yza456bcd789', 'POST', '/v2/generate', 200, 234, 1024000, 5800),
((SELECT user_id FROM users WHERE username = 'jane_smith'), (SELECT developer_id FROM developers WHERE username = 'ml_master'), (SELECT model_id FROM models WHERE api_name = 'imagesense_ai_v3'), 'sk-mlstudio_imagesense_mno456pqr789stu012', 'POST', '/v3/analyze', 200, 2048000, 890, 2100),
((SELECT user_id FROM users WHERE username = 'alice_johnson'), (SELECT developer_id FROM developers WHERE username = 'data_sage'), (SELECT model_id FROM models WHERE api_name = 'marketseer_v2'), 'sk-datasolutions_marketseer_wxy123zab456cde789', 'POST', '/v2/predict', 200, 1567, 1203, 2800),
((SELECT user_id FROM users WHERE username = 'carlos_mendez'), (SELECT developer_id FROM developers WHERE username = 'code_wizard'), (SELECT model_id FROM models WHERE api_name = 'bugdetector_pro_v1'), 'sk-codegenius_bugdetector_nop456qrs789tuv012', 'POST', '/v1/analyze', 200, 15678, 2345, 3200),
-- Some failed requests for realistic data
((SELECT user_id FROM users WHERE username = 'test_user'), (SELECT developer_id FROM developers WHERE username = 'startup_dev'), (SELECT model_id FROM models WHERE api_name = 'omnisense_beta'), 'sk-aiprototype_omnisense_fgh890ijk123lmn456', 'POST', '/beta/omnisense', 429, 567, 0, 100),
((SELECT user_id FROM users WHERE username = 'john_doe'), (SELECT developer_id FROM developers WHERE username = 'ai_innovator'), (SELECT model_id FROM models WHERE api_name = 'smartchat_pro_v2'), 'sk-ai_innovations_smartchat_invalid_key', 'POST', '/v2/smartchat/generate', 401, 123, 89, 50);

-- Update some timestamps to make data more realistic (spread over time)
UPDATE user_history SET 
    request_timestamp = CURRENT_TIMESTAMP - (RANDOM() * INTERVAL '30 days'),
    response_timestamp = request_timestamp + (response_time_ms * INTERVAL '1 millisecond')
WHERE history_id IN (SELECT history_id FROM user_history LIMIT 5);

UPDATE model_reviews SET 
    created_at = CURRENT_TIMESTAMP - (RANDOM() * INTERVAL '60 days'),
    updated_at = created_at
WHERE review_id IN (SELECT review_id FROM model_reviews LIMIT 8);

UPDATE api_usage_logs SET 
    created_at = CURRENT_TIMESTAMP - (RANDOM() * INTERVAL '7 days')
WHERE log_id IN (SELECT log_id FROM api_usage_logs);

-- Commit the transaction
COMMIT;

-- Display summary of inserted data
SELECT 'Sample data insertion completed!' AS status;

SELECT 
    'Users' AS table_name, 
    COUNT(*) AS records_inserted 
FROM users
UNION ALL
SELECT 
    'Developers' AS table_name, 
    COUNT(*) AS records_inserted 
FROM developers
UNION ALL
SELECT 
    'Models' AS table_name, 
    COUNT(*) AS records_inserted 
FROM models
UNION ALL
SELECT 
    'User History' AS table_name, 
    COUNT(*) AS records_inserted 
FROM user_history
UNION ALL
SELECT 
    'Model Reviews' AS table_name, 
    COUNT(*) AS records_inserted 
FROM model_reviews
UNION ALL
SELECT 
    'API Usage Logs' AS table_name, 
    COUNT(*) AS records_inserted 
FROM api_usage_logs;

-- Show some sample data to verify
SELECT 'Sample Users:' AS info;
SELECT username, first_name, last_name, country, status FROM users LIMIT 3;

SELECT 'Sample Models:' AS info;
SELECT display_name, category, status, featured FROM models LIMIT 3;

SELECT 'Sample Reviews:' AS info;
SELECT 
    m.display_name as model_name,
    u.username as reviewer,
    mr.rating,
    mr.review_title
FROM model_reviews mr
JOIN models m ON mr.model_id = m.model_id
JOIN users u ON mr.user_id = u.user_id
LIMIT 3;
