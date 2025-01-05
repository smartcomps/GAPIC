BACKGROUND_SVG = """
    <div style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: -1;">
        <svg width="100" height="100" viewBox="0 0 100 100" style="position: absolute; top: 10%; left: 10%; animation: float1 20s infinite ease-in-out;">
            <polygon points="50,0 100,100 0,100" fill="#1a73e8" style="opacity: 0.1;"/>
        </svg>
        <svg width="80" height="80" viewBox="0 0 100 100" style="position: absolute; top: 60%; left: 80%; animation: float2 25s infinite ease-in-out;">
            <polygon points="50,0 100,100 0,100" fill="#4285f4" style="opacity: 0.1;"/>
        </svg>
        <svg width="120" height="120" viewBox="0 0 100 100" style="position: absolute; top: 80%; left: 20%; animation: float3 22s infinite ease-in-out;">
            <polygon points="50,0 100,100 0,100" fill="#0f4fb8" style="opacity: 0.1;"/>
        </svg>
        <svg width="90" height="90" viewBox="0 0 100 100" style="position: absolute; top: 30%; left: 60%; animation: float4 28s infinite ease-in-out;">
            <polygon points="50,0 100,100 0,100" fill="#1a73e8" style="opacity: 0.1;"/>
        </svg>
        <svg width="110" height="110" viewBox="0 0 100 100" style="position: absolute; top: 70%; left: 40%; animation: float5 24s infinite ease-in-out;">
            <polygon points="50,0 100,100 0,100" fill="#4285f4" style="opacity: 0.1;"/>
        </svg>
    </div>
"""

CSS = """
    <style>
    @keyframes float1 {
        0%, 100% { transform: translate(0, 0) rotate(0deg); }
        50% { transform: translate(100px, -100px) rotate(180deg); }
    }
    @keyframes float2 {
        0%, 100% { transform: translate(0, 0) rotate(0deg); }
        50% { transform: translate(-100px, 100px) rotate(-180deg); }
    }
    @keyframes float3 {
        0%, 100% { transform: translate(0, 0) rotate(0deg); }
        50% { transform: translate(80px, -80px) rotate(120deg); }
    }
    @keyframes float4 {
        0%, 100% { transform: translate(0, 0) rotate(0deg); }
        50% { transform: translate(-80px, 80px) rotate(-120deg); }
    }
    @keyframes float5 {
        0%, 100% { transform: translate(0, 0) rotate(0deg); }
        50% { transform: translate(120px, -120px) rotate(240deg); }
    }
    
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
    .topic-box:hover {
        transform: scale(1.02);
        box-shadow: 0px 6px 16px rgba(0, 0, 0, 0.15);
    }
    .topic-preview {
        color: white;
        padding: 8px;
        border-radius: 8px;
        overflow: hidden;
        text-overflow: ellipsis;
        display: -webkit-box;
        -webkit-line-clamp: 4;
        -webkit-box-orient: vertical;
        white-space: normal;
        background: rgba(255, 255, 255, 0.2);
        flex-grow: 1;
        font-size: 0.9em;
    }
    .topic-box h3 {
        font-size: 1em;
        margin-bottom: 10px;
    }
    .view-full-button {
        background-color: #1a73e8;
        color: white;
        padding: 6px 10px;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        text-align: center;
        margin-top: 8px;
        width: 100%;
        font-size: 0.9em;
    }
    .view-full-button:hover {
        background-color: #0f4fb8;
    }
    .fixed-bottom {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        padding: 20px;
        box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
        z-index: 1000;
    }
    .content-padding {
        padding-bottom: 100px;
        position: relative;
        z-index: 1;
    }
    </style>
"""
