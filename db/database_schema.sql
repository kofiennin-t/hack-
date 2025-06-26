-- PostgreSQL Database Schema for AI Model Platform
-- Created: June 25, 2025
-- Description: Database schema for managing users, developers, AI models, and user interaction history

-- Enable UUID extension for generating unique identifiers
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create enum types for better data integrity
CREATE TYPE user_status AS ENUM ('active', 'inactive', 'suspended', 'pending_verification');
CREATE TYPE developer_status AS ENUM ('active', 'inactive', 'suspended', 'pending_approval');
CREATE TYPE model_category AS ENUM ('text_generation', 'image_generation', 'code_generation', 'data_analysis', 'translation', 'summarization', 'question_answering', 'other');
CREATE TYPE model_status AS ENUM ('active', 'inactive', 'under_review', 'deprecated');

-- Users table - containing user personal information
CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    date_of_birth DATE,
    phone_number VARCHAR(20),
    country VARCHAR(100),
    city VARCHAR(100),
    profile_picture_url TEXT,
    bio TEXT,
    status user_status DEFAULT 'pending_verification',
    email_verified BOOLEAN DEFAULT FALSE,
    email_verification_token VARCHAR(255),
    password_reset_token VARCHAR(255),
    password_reset_expires TIMESTAMP,
    last_login TIMESTAMP,
    login_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Developers table - containing developer personal info and model relationships
CREATE TABLE developers (
    developer_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    company_name VARCHAR(200),
    website_url TEXT,
    github_profile VARCHAR(100),
    linkedin_profile VARCHAR(100),
    phone_number VARCHAR(20),
    country VARCHAR(100),
    city VARCHAR(100),
    profile_picture_url TEXT,
    bio TEXT,
    expertise_areas TEXT[], -- Array of expertise areas
    years_of_experience INTEGER,
    status developer_status DEFAULT 'pending_approval',
    email_verified BOOLEAN DEFAULT FALSE,
    email_verification_token VARCHAR(255),
    password_reset_token VARCHAR(255),
    password_reset_expires TIMESTAMP,
    api_quota_limit INTEGER DEFAULT 10000, -- Monthly API call limit
    api_quota_used INTEGER DEFAULT 0,
    last_login TIMESTAMP,
    login_count INTEGER DEFAULT 0,
    total_models_created INTEGER DEFAULT 0, -- Calculated field, updated by triggers
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Models table - containing model information, API details, and categorization
CREATE TABLE models (
    model_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    developer_id UUID NOT NULL REFERENCES developers(developer_id) ON DELETE CASCADE,
    model_name VARCHAR(200) NOT NULL,
    display_name VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    detailed_description TEXT,
    version VARCHAR(20) DEFAULT '1.0.0',
    api_name VARCHAR(100) UNIQUE NOT NULL, -- Unique identifier for API calls
    api_key VARCHAR(255) UNIQUE NOT NULL, -- API key for accessing the model
    api_endpoint TEXT, -- Full API endpoint URL
    category model_category NOT NULL,
    --subcategory VARCHAR(100),
    tags TEXT[], -- Array of tags for better searchability
    input_format VARCHAR(50) DEFAULT 'text', -- text, json, image, etc.
    output_format VARCHAR(50) DEFAULT 'text', -- text, json, image, etc.
    max_input_length INTEGER,
    max_output_length INTEGER,
    response_time_ms INTEGER, -- Average response time in milliseconds
    accuracy_score DECIMAL(3,2), -- Accuracy score between 0.00 and 1.00
    status model_status DEFAULT 'under_review',
    is_public BOOLEAN DEFAULT TRUE, -- Whether model is publicly available
    documentation_url TEXT,
    example_request TEXT, -- JSON example of API request
    example_response TEXT, -- JSON example of API response
    total_requests INTEGER DEFAULT 0, -- Total API requests made
    total_users INTEGER DEFAULT 0, -- Total unique users who used this model
    average_rating DECIMAL(3,2) DEFAULT 0.00, -- Average user rating
    rating_count INTEGER DEFAULT 0,
    featured BOOLEAN DEFAULT FALSE, -- Whether model is featured
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deprecated_at TIMESTAMP, -- When model was deprecated
    
    -- Constraints
    CONSTRAINT valid_accuracy_score CHECK (accuracy_score >= 0.00 AND accuracy_score <= 1.00),
    CONSTRAINT valid_average_rating CHECK (average_rating >= 0.00 AND average_rating <= 5.00)
);

-- User History table - tracking user interactions and sessions
CREATE TABLE user_history (
    history_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    model_id UUID NOT NULL REFERENCES models(model_id) ON DELETE CASCADE,
    session_id VARCHAR(255) NOT NULL, -- Groups related interactions
    prompt TEXT NOT NULL, -- User's input/prompt
    response TEXT, -- Model's response
    response_status VARCHAR(20) DEFAULT 'pending', -- pending, success, error, timeout
    error_message TEXT, -- Error details if response failed
    request_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    response_timestamp TIMESTAMP,
    response_time_ms INTEGER, -- Actual response time for this request
    input_tokens INTEGER, -- Number of input tokens processed
    output_tokens INTEGER, -- Number of output tokens generated
    cost_incurred DECIMAL(10,4), -- Cost for this specific request
    user_rating INTEGER, -- User rating for this interaction (1-5)
    user_feedback TEXT, -- Optional user feedback
    ip_address INET, -- User's IP address
    user_agent TEXT, -- Browser/client information
    api_version VARCHAR(10), -- API version used
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    CONSTRAINT valid_user_rating CHECK (user_rating >= 1 AND user_rating <= 5),
    CONSTRAINT valid_response_status CHECK (response_status IN ('pending', 'success', 'error', 'timeout'))
);

-- Additional tables for enhanced functionality

-- Model ratings and reviews
CREATE TABLE model_reviews (
    review_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    model_id UUID NOT NULL REFERENCES models(model_id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    review_title VARCHAR(200),
    review_text TEXT,
    is_verified_user BOOLEAN DEFAULT FALSE, -- Whether user has actually used the model
    helpful_votes INTEGER DEFAULT 0,
    total_votes INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Prevent duplicate reviews from same user for same model
    UNIQUE(model_id, user_id)
);

-- API usage tracking for rate limiting and analytics
CREATE TABLE api_usage_logs (
    log_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(user_id) ON DELETE SET NULL,
    developer_id UUID REFERENCES developers(developer_id) ON DELETE SET NULL,
    model_id UUID NOT NULL REFERENCES models(model_id) ON DELETE CASCADE,
    api_key_used VARCHAR(255),
    request_method VARCHAR(10),
    request_path TEXT,
    response_status_code INTEGER,
    request_size_bytes INTEGER,
    response_size_bytes INTEGER,
    processing_time_ms INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Index for efficient querying
    INDEX idx_api_usage_logs_created_at (created_at),
    INDEX idx_api_usage_logs_model_id (model_id),
    INDEX idx_api_usage_logs_user_id (user_id)
);

-- Create indexes for better query performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_status ON users(status);
CREATE INDEX idx_users_created_at ON users(created_at);

CREATE INDEX idx_developers_email ON developers(email);
CREATE INDEX idx_developers_username ON developers(username);
CREATE INDEX idx_developers_status ON developers(status);
CREATE INDEX idx_developers_created_at ON developers(created_at);

CREATE INDEX idx_models_developer_id ON models(developer_id);
CREATE INDEX idx_models_api_name ON models(api_name);
CREATE INDEX idx_models_category ON models(category);
CREATE INDEX idx_models_status ON models(status);
CREATE INDEX idx_models_is_public ON models(is_public);
CREATE INDEX idx_models_featured ON models(featured);
CREATE INDEX idx_models_created_at ON models(created_at);

CREATE INDEX idx_user_history_user_id ON user_history(user_id);
CREATE INDEX idx_user_history_model_id ON user_history(model_id);
CREATE INDEX idx_user_history_session_id ON user_history(session_id);
CREATE INDEX idx_user_history_created_at ON user_history(created_at);

CREATE INDEX idx_model_reviews_model_id ON model_reviews(model_id);
CREATE INDEX idx_model_reviews_user_id ON model_reviews(user_id);
CREATE INDEX idx_model_reviews_rating ON model_reviews(rating);

-- Create functions and triggers for automatic updates

-- Function to update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply the update trigger to relevant tables
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_developers_updated_at BEFORE UPDATE ON developers
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_models_updated_at BEFORE UPDATE ON models
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_model_reviews_updated_at BEFORE UPDATE ON model_reviews
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Function to update developer's total models count
CREATE OR REPLACE FUNCTION update_developer_models_count()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        UPDATE developers 
        SET total_models_created = total_models_created + 1
        WHERE developer_id = NEW.developer_id;
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        UPDATE developers 
        SET total_models_created = total_models_created - 1
        WHERE developer_id = OLD.developer_id;
        RETURN OLD;
    END IF;
    RETURN NULL;
END;
$$ language 'plpgsql';

-- Apply the trigger to models table
CREATE TRIGGER update_developer_models_count_trigger
    AFTER INSERT OR DELETE ON models
    FOR EACH ROW EXECUTE FUNCTION update_developer_models_count();

-- Function to update model statistics when new history entry is added
CREATE OR REPLACE FUNCTION update_model_stats()
RETURNS TRIGGER AS $$
BEGIN
    -- Update total requests count
    UPDATE models 
    SET total_requests = total_requests + 1
    WHERE model_id = NEW.model_id;
    
    -- Update unique users count (approximate, could be optimized)
    UPDATE models 
    SET total_users = (
        SELECT COUNT(DISTINCT user_id) 
        FROM user_history 
        WHERE model_id = NEW.model_id
    )
    WHERE model_id = NEW.model_id;
    
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply the trigger to user_history table
CREATE TRIGGER update_model_stats_trigger
    AFTER INSERT ON user_history
    FOR EACH ROW EXECUTE FUNCTION update_model_stats();

-- Function to update model average rating when review is added/updated
CREATE OR REPLACE FUNCTION update_model_rating()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' OR TG_OP = 'UPDATE' THEN
        UPDATE models 
        SET 
            average_rating = (
                SELECT AVG(rating)::DECIMAL(3,2) 
                FROM model_reviews 
                WHERE model_id = NEW.model_id
            ),
            rating_count = (
                SELECT COUNT(*) 
                FROM model_reviews 
                WHERE model_id = NEW.model_id
            )
        WHERE model_id = NEW.model_id;
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        UPDATE models 
        SET 
            average_rating = COALESCE((
                SELECT AVG(rating)::DECIMAL(3,2) 
                FROM model_reviews 
                WHERE model_id = OLD.model_id
            ), 0.00),
            rating_count = (
                SELECT COUNT(*) 
                FROM model_reviews 
                WHERE model_id = OLD.model_id
            )
        WHERE model_id = OLD.model_id;
        RETURN OLD;
    END IF;
    RETURN NULL;
END;
$$ language 'plpgsql';

-- Apply the trigger to model_reviews table
CREATE TRIGGER update_model_rating_trigger
    AFTER INSERT OR UPDATE OR DELETE ON model_reviews
    FOR EACH ROW EXECUTE FUNCTION update_model_rating();

-- Create some useful views for common queries

-- View for public models with developer information
CREATE VIEW public_models_view AS
SELECT 
    m.model_id,
    m.model_name,
    m.display_name,
    m.description,
    m.api_name,
    m.category,
    m.tags,
    m.average_rating,
    m.rating_count,
    m.total_requests,
    m.total_users,
    m.featured,
    m.created_at,
    d.username as developer_username,
    d.company_name as developer_company,
    d.first_name || ' ' || d.last_name as developer_name
FROM models m
JOIN developers d ON m.developer_id = d.developer_id
WHERE m.status = 'active' AND m.is_public = TRUE AND d.status = 'active';

-- View for user activity summary
CREATE VIEW user_activity_summary AS
SELECT 
    u.user_id,
    u.username,
    u.first_name || ' ' || u.last_name as full_name,
    COUNT(uh.history_id) as total_interactions,
    COUNT(DISTINCT uh.model_id) as unique_models_used,
    COUNT(DISTINCT uh.session_id) as total_sessions,
    AVG(uh.user_rating) as average_rating_given,
    SUM(uh.cost_incurred) as total_cost_incurred,
    MAX(uh.created_at) as last_interaction_date
FROM users u
LEFT JOIN user_history uh ON u.user_id = uh.user_id
GROUP BY u.user_id, u.username, u.first_name, u.last_name;

-- View for developer dashboard statistics
CREATE VIEW developer_dashboard_stats AS
SELECT 
    d.developer_id,
    d.username,
    d.first_name || ' ' || d.last_name as full_name,
    d.total_models_created,
    COUNT(DISTINCT m.model_id) as active_models,
    SUM(m.total_requests) as total_api_requests,
    SUM(m.total_users) as total_unique_users,
    AVG(m.average_rating) as overall_average_rating,
    SUM(uh.cost_incurred) as total_revenue_generated
FROM developers d
LEFT JOIN models m ON d.developer_id = m.developer_id AND m.status = 'active'
LEFT JOIN user_history uh ON m.model_id = uh.model_id
GROUP BY d.developer_id, d.username, d.first_name, d.last_name, d.total_models_created;

-- Insert some sample data for testing (optional - remove in production)
/*
-- Sample users
INSERT INTO users (username, email, password_hash, first_name, last_name, country, city) VALUES
('john_doe', 'john.doe@example.com', '$2b$12$hash1', 'John', 'Doe', 'USA', 'San Francisco'),
('jane_smith', 'jane.smith@example.com', '$2b$12$hash2', 'Jane', 'Smith', 'UK', 'London'),
('bob_wilson', 'bob.wilson@example.com', '$2b$12$hash3', 'Bob', 'Wilson', 'Canada', 'Toronto');

-- Sample developers
INSERT INTO developers (username, email, password_hash, first_name, last_name, company_name, expertise_areas) VALUES
('ai_dev_alice', 'alice@aicompany.com', '$2b$12$devhash1', 'Alice', 'Johnson', 'AI Innovations Inc', ARRAY['machine_learning', 'nlp', 'computer_vision']),
('ml_expert_bob', 'bob@mlstudio.com', '$2b$12$devhash2', 'Bob', 'Chen', 'ML Studio', ARRAY['deep_learning', 'data_science', 'neural_networks']);

-- Sample models (you'll need to get actual developer_ids from the inserted developers)
-- This is just an example structure - you'd need to replace with actual UUIDs
*/

-- Comments and documentation
COMMENT ON TABLE users IS 'Stores end-user information for the AI model platform';
COMMENT ON TABLE developers IS 'Stores developer/creator information for those who build and deploy AI models';
COMMENT ON TABLE models IS 'Contains information about AI models including API details and metadata';
COMMENT ON TABLE user_history IS 'Tracks all user interactions with AI models including prompts and responses';
COMMENT ON TABLE model_reviews IS 'User reviews and ratings for AI models';
COMMENT ON TABLE api_usage_logs IS 'Detailed logs of API usage for analytics and monitoring';

-- Final message
SELECT 'Database schema created successfully! 🎉' AS status;
