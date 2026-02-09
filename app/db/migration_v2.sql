-- Migration to add missing columns to job_seeker_profiles table
-- Run this in your Supabase SQL Editor

ALTER TABLE job_seeker_profiles ADD COLUMN IF NOT EXISTS summary TEXT;
ALTER TABLE job_seeker_profiles ADD COLUMN IF NOT EXISTS projects TEXT;
ALTER TABLE job_seeker_profiles ADD COLUMN IF NOT EXISTS github_url TEXT;
ALTER TABLE job_seeker_profiles ADD COLUMN IF NOT EXISTS linkedin_url TEXT;

-- Verify columns (optional)
-- SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'job_seeker_profiles';
