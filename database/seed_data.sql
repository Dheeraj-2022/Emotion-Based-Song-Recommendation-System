-- Insert sample users
INSERT INTO users (username, email, password) VALUES
('demo_user', 'demo@example.com', '$2b$12$LQppY3L3X5E6QX5X5X5X5X'),
('test_user', 'test@example.com', '$2b$12$LQppY3L3X5E6QX5X5X5X5X');

-- Insert sample emotions
INSERT INTO emotions (user_id, emotion, confidence, language, singer) VALUES
(1, 'happy', 85, 'English', 'Ed Sheeran'),
(1, 'sad', 72, 'Hindi', 'Arijit Singh'),
(1, 'neutral', 90, 'Spanish', 'Shakira'),
(2, 'happy', 88, 'English', 'Taylor Swift'),
(2, 'angry', 65, 'Rock', 'Metallica');

-- Insert user preferences
INSERT INTO user_preferences (user_id, favorite_language, favorite_singer, favorite_genre) VALUES
(1, 'English', 'Ed Sheeran', 'Pop'),
(2, 'Hindi', 'Arijit Singh', 'Romantic');
