-- Create database
CREATE DATABASE emotion_music_db;

-- Connect to database
\c emotion_music_db;

-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

-- Emotions table
CREATE TABLE emotions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    emotion VARCHAR(50) NOT NULL,
    confidence INTEGER DEFAULT 0,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    language VARCHAR(50),
    singer VARCHAR(100),
    recommendations TEXT
);

-- User preferences table
CREATE TABLE user_preferences (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    favorite_language VARCHAR(50),
    favorite_singer VARCHAR(100),
    favorite_genre VARCHAR(50),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Emotion history analytics table
CREATE TABLE emotion_analytics (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    emotion_counts JSON,
    total_detections INTEGER DEFAULT 0,
    UNIQUE (user_id, date)
);

-- Session table for tracking user sessions
CREATE TABLE user_sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    token VARCHAR(500) NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_emotions_user_timestamp ON emotions(user_id, timestamp DESC);
CREATE INDEX idx_emotions_emotion ON emotions(emotion);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_token ON user_sessions(token);
CREATE INDEX idx_expires ON user_sessions(expires_at);

-- Stored procedure for analytics
CREATE OR REPLACE FUNCTION update_emotion_analytics()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO emotion_analytics (user_id, date, emotion_counts, total_detections)
    VALUES (
        NEW.user_id,
        DATE(NEW.timestamp),
        json_build_object(NEW.emotion, 1),
        1
    )
    ON CONFLICT (user_id, date) DO UPDATE
    SET 
        emotion_counts = 
            CASE 
                WHEN emotion_analytics.emotion_counts ? NEW.emotion THEN
                    jsonb_set(
                        emotion_analytics.emotion_counts::jsonb,
                        ARRAY[NEW.emotion],
                        to_jsonb((emotion_analytics.emotion_counts->NEW.emotion)::int + 1)
                    )::json
                ELSE
                    (emotion_analytics.emotion_counts::jsonb || 
                     json_build_object(NEW.emotion, 1)::jsonb)::json
            END,
        total_detections = emotion_analytics.total_detections + 1;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger
CREATE TRIGGER emotion_analytics_trigger
AFTER INSERT ON emotions
FOR EACH ROW
EXECUTE FUNCTION update_emotion_analytics();

-- View
CREATE VIEW user_emotion_summary AS
SELECT 
    u.id as user_id,
    u.username,
    COUNT(e.id) as total_emotions,
    MAX(e.timestamp) as last_detection,
    (
        SELECT emotion 
        FROM emotions 
        WHERE user_id = u.id 
        GROUP BY emotion 
        ORDER BY COUNT(*) DESC 
        LIMIT 1
    ) as most_common_emotion
FROM users u
LEFT JOIN emotions e ON u.id = e.user_id
GROUP BY u.id, u.username;

-- Cleanup function
CREATE OR REPLACE FUNCTION cleanup_expired_sessions()
RETURNS void AS $$
BEGIN
    DELETE FROM user_sessions WHERE expires_at < NOW();
END;
$$ LANGUAGE plpgsql;
