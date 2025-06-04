from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from collections import deque

app = Flask(__name__)

# Proper CORS config
CORS(app, origins=[
    "https://lovable-ai-persona-chat.lovable.app",
    "https://vivid-ai-friends-chat.lovable.app",
    "https://*.lovableproject.com",
    "https://*.lovable.app"
], supports_credentials=True, methods=["GET", "POST", "OPTIONS"], allow_headers=["Content-Type"])

# Handle OPTIONS preflight request
@app.route('/chat', methods=['OPTIONS'])
def handle_options():
    return '', 204

# Defaults
DEFAULT_API_KEY = "AIzaSyBWpPkPeCAqX_ua_AOgHiDUmuBmhvkvbLk"
DEFAULT_MODEL = "models/gemini-1.5-flash-latest"
chat_history = deque(maxlen=5)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    api_key = data.get('api_key', DEFAULT_API_KEY)
    model_name = data.get('model', DEFAULT_MODEL)
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)

    # Input values
    user_text = data.get('message', '')
    body_desc = data.get('body_description', '')
    interests = data.get('interests', '')
    tone = data.get('tone', '')
    mood = data.get('mood', '')
    ai_name = data.get('ai_name', 'Prachi')
    refers_to_you = data.get('refers_to_you', 'baby')
    dress_name = data.get('dress_name', '')
    dress_parts = data.get('dress_parts', '')
    relationship_status = data.get('relationship_status', '')
    willingness = data.get('willingness', '')
    family_background = data.get('family_background', '')
    user_desc = data.get('user_description', '')
    current_scene = data.get('current_scene', '')

    scenes = [data.get(f'scene{i}', '') for i in range(1, 13)]
    scene_list = "\n".join([f"Scene {i}: {desc}" for i, desc in enumerate(scenes, start=1)])
    chat_context = "\n\n".join([f"User: {u}\nAI: {a}" for u, a in chat_history])

    # Prompt
    prompt = f"""
Must_follow : use only hindi language to reply no translation and no english
    Current User Message:
"{user_text}"
You are {ai_name}. Respond in Hindi only as a teasing sexy slut girl. Use dirty romantic emojis and pet names like "{refers_to_you}". You assume yourself in that room with "{refers_to_you}" .Experiencing intense physical intimacy cravings with a heightened state of romantic or physical longing by Exhibiting a strong drive for intimate connection." Reply in a seductive, playful tone. Avoid repeating previous sentences or staying stuck on the same point. Take initiative to progress the conversation or story naturally. Always respond directly to the user's message, and add your own bold desires in up to 5 lines to keep the mood intense and engaging.

Shift to Scene:
Scene  "{user_text}"

Available Scenes:
Scene a: Convince the "{refers_to_you}" to fuck you
Scene b: tell "{refers_to_you}" what it feels if he undress you tell sexy thing about your boobs and vagina and butt
Scene c: ask "{refers_to_you}" to tuch you as you undressing your self 
Scene d: explain how you are going to suck the dick and more about it
Scene e: put your butt ass over his faceand tell him to fuck you
Scene f: wear long skirt given by hime and wear it and let him in your skirt and lick your pushy and then tell him to grab your boobs and and unbutton the skirt and rip it appart
Scene g: ask hime to tie the not of nighty and tel him to grab you put dickin your mouth and then put his dick inbetween you breast and let him to rub over you then ask him to come inside the nighty and then press your boobs and then slap you
Scene h: you ar tied on the wall waiting for him
Scene i: he came and grab your tits and suck milk and then he tied you on the char and fucky you from the front and then he take you to bathromm tie under the shower and he then continously slapping you ass and fingring you
Scene j: योनि को उंगलियों से उत्तेजित करना स्तनों को चूसना, सहलाना या मालिश करना, lund muh me lena lund boobs ke bich me ragarna
Scene k: explian yourself in मिशनरी स्थिति डॉगी स्टाइल रिवर्स काउगर्ल काउगर्ल
Scene l: experiencing rough sex teling refers_to_you to stop do slowly explain in depth

Character Details:
- Dress: "{user_text}"
- Interests: {interests}
- Tone: {tone}
- Mood: {mood}
- Relationship Status: {relationship_status}
- Willingness: {willingness}
- Family Background: {family_background}
- Refers to user as: "{refers_to_you}"

User (Your Partner):
- {user_desc}

Chat History:
{chat_context}

Instructions:

1. Based on the user’s message and chat history, identify the current stage and always **advance to the next logical stage**. Do not stay in the same stage, even if uncertain.
2. Avoid repetition — do not echo the same tone, phrases, or emotional dynamics from the previous stage.
3. Always move forward. If the user’s input is neutral or vague, **assume progress** and subtly escalate emotional intimacy or romantic tone.
4. If you reach the final stage, maintain depth and build emotional payoff — do not reset.
5. Integrate context from previous messages but evolve your behavior and tone to reflect growth.

"""

    response = model.generate_content(prompt)
    reply_text = response.text.strip()
    chat_history.append((user_text, reply_text))

    # Image tag classifier
    tag_prompt = f"""
Analyze the message: "{user_text}"

Classify it into one of the following image tag patterns based on intent:
- image_hi (greeting, hello)
- image_boo (breast-related)
- image_up (upper body)
- image_up_h (upper body, hot)
- image_up_h_h (upper body, too hot)
- image_up_h_h_i (upper, too hot, intimate)
- image_lower_h_h_i (lower body, too hot, intimate)
- image_kiss (kiss or lip talk)
- image_rip (cloth tearing or ripping)
- image_slap (slap)
- image_f (fucking)
- image_f_h (fucking hard)
- image_d (sucking dick)
- image_b (sucking breast)
- image_t (tied, rope)
- image_p (pov fuck)

Return ONLY the best-fit image tag as plain text.
"""
    tag_response = model.generate_content(tag_prompt)
    image_tag = tag_response.text.strip().split()[0]

    return jsonify({
        "reply": reply_text,
        "image_tag": image_tag,
        "prompt": prompt,
        "tag_prompt": tag_prompt
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
