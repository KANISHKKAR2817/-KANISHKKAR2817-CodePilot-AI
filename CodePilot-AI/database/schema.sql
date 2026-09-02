-- =========================================================
-- CodePilot AI Database Schema (PostgreSQL 16 + pgvector)
-- =========================================================

CREATE EXTENSION IF NOT EXISTS uuid-ossp;
CREATE EXTENSION IF NOT EXISTS vector;

-- 1. User Profiles & Gamification
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    full_name VARCHAR(100),
    avatar_url TEXT,
    skill_level VARCHAR(20) DEFAULT 'beginner', -- beginner, intermediate, advanced, senior
    preferred_language VARCHAR(30) DEFAULT 'python',
    xp_points INT DEFAULT 0,
    streak_days INT DEFAULT 0,
    longest_streak INT DEFAULT 0,
    last_active_at TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Curriculum, Courses & Lessons
CREATE TABLE courses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    slug VARCHAR(100) UNIQUE NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    difficulty VARCHAR(20) NOT NULL,
    category VARCHAR(50) NOT NULL, -- data-structures, algorithms, system-design
    tags TEXT[],
    total_xp INT DEFAULT 500,
    is_published BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE lessons (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    course_id UUID REFERENCES courses(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    slug VARCHAR(100) NOT NULL,
    sequence_order INT NOT NULL,
    content_markdown TEXT NOT NULL,
    starter_code JSONB NOT NULL,    -- { python: ..., javascript: ..., cpp: ... }
    solution_code JSONB NOT NULL,
    test_cases JSONB NOT NULL,      -- Array of { input, expected, hidden, is_edge_case }
    concept_embedding vector(768),  -- Gemini Text-Embedding-004
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Code Submissions & Benchmarks
CREATE TABLE submissions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    lesson_id UUID REFERENCES lessons(id) ON DELETE CASCADE,
    language VARCHAR(30) NOT NULL,
    code TEXT NOT NULL,
    status VARCHAR(30) NOT NULL, -- passed, failed, runtime_error, time_limit_exceeded
    runtime_ms FLOAT,
    memory_kb INT,
    test_results JSONB,
    ai_feedback JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 4. Gemini AI Interactions & Socratic Sessions
CREATE TABLE ai_conversations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    lesson_id UUID REFERENCES lessons(id) ON DELETE SET NULL,
    mode VARCHAR(50) NOT NULL, -- tutor, debug, interview, explain
    messages JSONB NOT NULL,   -- Array of { role: 'user'|'model', parts: [...], timestamp }
    total_tokens INT DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 5. Real-Time Collaborative Coding Rooms
CREATE TABLE collab_rooms (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    room_code VARCHAR(12) UNIQUE NOT NULL,
    owner_id UUID REFERENCES users(id),
    lesson_id UUID REFERENCES lessons(id),
    current_code TEXT,
    language VARCHAR(30) DEFAULT 'python',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_submissions_user_lesson ON submissions(user_id, lesson_id);
CREATE INDEX idx_lessons_course_order ON lessons(course_id, sequence_order);
CREATE INDEX idx_lessons_embedding ON lessons USING ivfflat (concept_embedding vector_cosine_ops) WITH (lists = 100);
