import os
import streamlit as st
# Define job roles and the skills expected for each
# Define job roles and the mandatory skills required for each
roles = {
    "Data Scientist": {
        "mandatory_skills": [
            "python", "machine learning", "data analysis",
            "pandas", "numpy"
        ],
        "skills": [
            "matplotlib", "scikit-learn", "tensorflow", "deep learning", 
            "sql", "data visualization"
        ]
    },
    "Web Developer": {
        "mandatory_skills": [
            "html", "css", "javascript", "react", "node.js"
        ],
        "skills": [
            "express", "mongodb", "sql", "frontend", "backend",
            "api", "web development"
        ]
    },
    "Software Engineer": {
        "mandatory_skills": [
            "java", "c++", "python", "algorithms", "data structures"
        ],
        "skills": [
            "system design", "software development", "oop", "git", "debugging"
        ]
    },
    "DevOps Engineer": {
        "mandatory_skills": [
            "linux", "docker", "kubernetes", "jenkins", "ci/cd"
        ],
        "skills": [
            "aws", "azure", "cloud", "monitoring", "infrastructure as code"
        ]
    },
    "Android Developer": {
        "mandatory_skills": [
            "java", "kotlin", "android studio", "firebase"
        ],
        "skills": [
            "android sdk", "rest api", "mobile development"
        ]
    }
}
