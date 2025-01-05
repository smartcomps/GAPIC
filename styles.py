BACKGROUND_STYLE = """
    <style>
    @keyframes float1 {
        0%, 100% { transform: translate(0, 0) rotate(0deg); }
        50% { transform: translate(100px, -100px) rotate(180deg); }
    }
    /* ... rest of your animations ... */
    
    .stApp {
        background-color: white;
        color: #333333;
    }
    .topic-box {
        border-radius: 12px;
        margin-bottom: 20px;
        padding: 15px;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
        color: white;
        height: 200px;
        display: flex;
        flex-direction: column;
    }
    /* ... rest of your styles ... */
    </style>
"""
