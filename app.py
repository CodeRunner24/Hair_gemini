import os
import gradio as gr
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import traceback
import socket

def find_free_port():
    """Find an available port"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port

# Global variables
client = None
hair_changer = None
hair_evaluator = None
current_original_image = None
current_new_image = None
current_language = "en"  # Default language

# Language configurations
LANGUAGES = {
    "en": {
        "title": "🎨 AI Hair Stylist",
        "subtitle": "Professional hair transformation system powered by Gemini 2.0 Flash",
        "description": "Transform your hair while preserving your face and analyze if it suits you!",
        "api_key_title": "🔑 **API Key Required**",
        "api_key_desc": """
        This app uses Google Gemini 2.0 Flash API. To get started:
        
        1. **Go to https://ai.google.dev/**
        2. **Click "Get API Key"**  
        3. Create a new API key
        4. Paste your API key below and click **"Start System"**
        
        ⚠️ **Note:** Your API key is stored securely and used only for AI processing.
        """,
        "api_key_placeholder": "Paste your API key starting with AIza...",
        "start_system": "🚀 Start System",
        "system_status": "📊 System Status",
        "waiting_api": "⏳ Waiting for API key...",
        "how_to_use": "🚀 **How to Use:**",
        "how_to_steps": """
        1. **Enter your API key above and start the system**
        2. **Upload your photo** (left side)
        3. **Type your hair change request in chat** 
        4. **AI will transform your hair and analyze if it suits you!**
        5. **New photo will automatically appear on the left!**
        """,
        "example_requests": "💡 **Quality Result Tips:**",
        "examples": """
        - "Honey blonde hair color" (specify exact tone)
        - "Natural brown long hair"  
        - "Modern short bob cut"
        - "Chocolate tone medium hair"
        - "Golden blonde wavy hair"
        
        **💎 Tip:** Specify exact color tones for more natural results!
        """,
        "upload_photo": "📸 Upload Photo",
        "upload_label": "Upload your photo here",
        "result_photo": "✨ Transformed Photo",
        "result_label": "Your new hair style will automatically appear here",
        "chat_title": "💬 AI Hair Stylist Chat",
        "message_placeholder": "e.g., 'honey blonde hair color' or 'short bob cut'",
        "send_button": "📤 Send",
        "clear_chat": "🗑️ Clear Chat",
        "features_title": "🎯 **Features:**",
        "features_list": """
        ✅ High resolution HD photo processing  
        ✅ Tonal analysis and skin-compatible color selection  
        ✅ Natural hair texture rendering  
        ✅ Automatic result display  
        ✅ Original photo preservation with hair-only editing  
        ✅ Suitability evaluation  
        ✅ Chat-based user experience  
        ✅ Professional AI analysis  
        ✅ Multi-language support (English/Turkish)  
        """,
        "tech_info": """
        **💻 Technology:** Gemini 2.0 Flash Image Generation API  
        **🏗️ Platform:** Hugging Face Spaces  
        **⚡ Powered by:** Google AI Studio
        """,
        "welcome_msg": """🎉 **Welcome!** 
                    
Your photo has been uploaded successfully! Now you can chat with me about your hair style.

💬 **You can ask:**
- "How would honey blonde hair look on me?"
- "Can you try a short bob cut?"
- "Would chocolate tone hair suit me?"
- "I want long wavy hair"

Which hair style are you curious about? 🎨""",
        "processing_msg": "🎯 Editing only your hair while preserving your face... \n⏳ Ultra-precise image editing process started...",
        "success_msg": "🎯 **YOUR FACE PRESERVED, HAIR EDITED!** ✨",
        "api_setup_success": "✅ AI System successfully set up! Gemini 2.0 Flash connection verified.",
        "api_setup_error": "❌ API Connection Error: {}\n\nPlease check your API key.",
        "enter_api_first": "Please enter your API key and start the system first.",
        "upload_photo_first": "Please upload a photo first.",
    },
    "tr": {
        "title": "🎨 AI Saç Stilisti",
        "subtitle": "Gemini 2.0 Flash ile güçlendirilmiş profesyonel saç değiştirme sistemi",
        "description": "Yüzünüzü koruyarak sadece saçınızı değiştirir ve yakışıp yakışmadığını analiz eder!",
        "api_key_title": "🔑 **API Key Gerekli**",
        "api_key_desc": """
        Bu uygulama Google Gemini 2.0 Flash API kullanır. Başlamak için:
        
        1. **https://ai.google.dev/** adresine gidin
        2. **"Get API Key"** butonuna tıklayın  
        3. Yeni bir API key oluşturun
        4. API key'i aşağıya yapıştırın ve **"Sistemi Başlat"** butonuna basın
        
        ⚠️ **Not:** API key'iniz güvenli şekilde saklanır ve sadece AI işlemler için kullanılır.
        """,
        "api_key_placeholder": "AIza... ile başlayan API key'inizi buraya yapıştırın",
        "start_system": "🚀 Sistemi Başlat",
        "system_status": "📊 Sistem Durumu",
        "waiting_api": "⏳ API key bekleniyor...",
        "how_to_use": "🚀 **Nasıl Kullanılır:**",
        "how_to_steps": """
        1. **Yukarıdan API key'inizi girin ve sistemi başlatın**
        2. **Fotoğrafınızı yükleyin** (sol taraftan)
        3. **Chat'e saç değişikliği isteğinizi yazın** 
        4. **AI hem saçınızı değiştirecek hem de yakışıp yakışmadığını değerlendirecek!**
        5. **Yeni fotoğraf otomatik olarak sol tarafta gözükecek!**
        """,
        "example_requests": "💡 **Kaliteli Sonuç İçin Örnek İstekler:**",
        "examples": """
        - "Bal sarısı saç rengi" (spesifik ton belirt)
        - "Doğal kahverengi uzun saç"  
        - "Modern kısa bob kesimi"
        - "Çikolata tonunda orta boy saç"
        - "Altın sarısı dalgalı saç"
        
        **💎 İpucu:** Spesifik renk tonları belirtirseniz daha doğal sonuç alırsınız!
        """,
        "upload_photo": "📸 Fotoğraf Yükleme",
        "upload_label": "Fotoğrafınızı buraya yükleyin",
        "result_photo": "✨ Değiştirilmiş Fotoğraf",
        "result_label": "Yeni saç stiliniz otomatik olarak burada görünecek",
        "chat_title": "💬 AI Saç Stilisti Chat",
        "message_placeholder": "Örn: 'bal sarısı saç rengi' veya 'kısa bob kesimi'",
        "send_button": "📤 Gönder",
        "clear_chat": "🗑️ Chat'i Temizle",
        "features_title": "🎯 **Özellikler:**",
        "features_list": """
        ✅ Yüksek çözünürlük HD fotoğraf işleme  
        ✅ Tonal analiz ve cilt uyumlu renk seçimi  
        ✅ Doğal saç dokusunda rendering  
        ✅ Otomatik sonuç gösterimi  
        ✅ Original fotoğrafı koruyarak sadece saç editlenmesi  
        ✅ Yakışıp yakışmadığını değerlendirme  
        ✅ Chat tabanlı kullanıcı deneyimi  
        ✅ Profesyonel AI analizi  
        ✅ Çok dil desteği (İngilizce/Türkçe)  
        """,
        "tech_info": """
        **💻 Teknoloji:** Gemini 2.0 Flash Image Generation API  
        **🏗️ Platform:** Hugging Face Spaces  
        **⚡ Güç:** Google AI Studio
        """,
        "welcome_msg": """🎉 **Hoş geldiniz!** 
                    
Fotoğrafınız başarıyla yüklendi! Şimdi benimle saç stiliniz hakkında konuşabilirsiniz.

💬 **Şunları sorabilirsiniz:**
- "Bal sarısı saç bende nasıl durur?"
- "Kısa bob kesimi dener misin?"
- "Çikolata tonunda saç yakışır mı?"
- "Uzun dalgalı saç istiyorum"

Hangi saç stilini merak ediyorsunuz? 🎨""",
        "processing_msg": "🎯 Yüzünüzü koruyarak sadece saçınızı editliyorum... \n⏳ Ultra hassas image editing işlemi başladı...",
        "success_msg": "🎯 **YÜZÜNÜZ KORUNARAK SAÇ EDİTLENDİ!** ✨",
        "api_setup_success": "✅ AI Sistemi başarıyla kuruldu! Gemini 2.0 Flash bağlantısı doğrulandı.",
        "api_setup_error": "❌ API Bağlantı Hatası: {}\n\nLütfen API key'inizi kontrol edin.",
        "enter_api_first": "Lütfen önce API key'inizi girin ve sistemi başlatın.",
        "upload_photo_first": "Lütfen önce bir fotoğraf yükleyin.",
    }
}

class HairChangeAgent:
    """Hair transformation agent"""
    
    def __init__(self, client):
        self.client = client
        
    def change_hair_style(self, original_image, hair_request, language="en"):
        """Transform user's hair in the photo"""
        
        # Ultra-protective image editing prompt
        prompt = f"""
        CRITICAL: This is an IMAGE EDITING task, NOT image generation!

        TASK: Edit ONLY the hair area in this existing photo. DO NOT create a new photo.

        EDIT REQUEST: {hair_request}

        🚨 ABSOLUTE PRESERVATION RULES - ZERO TOLERANCE:
        
        PRESERVE 100% UNCHANGED:
        ❌ FACE shape, features, bone structure
        ❌ EYES: color, shape, size, position, eyelashes, eyebrows  
        ❌ NOSE: shape, size, nostrils
        ❌ MOUTH: lips shape, size, color
        ❌ SKIN: tone, texture, blemishes, wrinkles
        ❌ FACIAL expression and emotion
        ❌ HEAD position and angle
        ❌ BODY posture and clothing
        ❌ BACKGROUND and lighting
        ❌ PHOTO quality and resolution

        ✅ EDIT ONLY: Hair area within the existing hairline

        HAIR EDITING APPROACH:
        1. IDENTIFY the current hair area boundaries
        2. WORK ONLY within those boundaries  
        3. CHANGE hair color/style while preserving:
           - Original hairline shape
           - Natural hair growth direction
           - Existing hair volume and texture
        
        FOR "{hair_request}":
        - Change hair color to complement skin undertone
        - Maintain natural hair appearance
        - Keep realistic hair texture and lighting
        - Preserve hair's interaction with face shadows

        RESULT MUST BE: Same person, same face, same photo, different hair only.

        REMEMBER: You are editing an existing image, not creating a new one!

        RESPONSE LANGUAGE: {"Turkish" if language == "tr" else "English"}

        Request: {hair_request}
        """
        
        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash-exp-image-generation",
                contents=[prompt, original_image],
                config=types.GenerateContentConfig(
                    response_modalities=['TEXT', 'IMAGE'],
                    temperature=0.05,
                    top_p=0.6,
                    top_k=10,
                )
            )
            
            result_text = ""
            result_image = None
            
            for part in response.candidates[0].content.parts:
                if part.text is not None:
                    result_text += part.text
                elif part.inline_data is not None:
                    result_image = Image.open(BytesIO(part.inline_data.data))
            
            return result_image, result_text
            
        except Exception as e:
            try:
                simple_prompt = f"""
                Edit this photo: Change hair to {hair_request}. 
                IMPORTANT: Keep face, body, background exactly the same. Only edit hair area.
                Response in {"Turkish" if language == "tr" else "English"}.
                """
                
                response = self.client.models.generate_content(
                    model="gemini-2.0-flash-exp-image-generation",
                    contents=[simple_prompt, original_image],
                    config=types.GenerateContentConfig(
                        response_modalities=['TEXT', 'IMAGE'],
                        temperature=0.01,
                        top_p=0.5,
                    )
                )
                
                result_text = "✅ Hair style changed using alternative method."
                if language == "tr":
                    result_text = "✅ Alternatif yöntemle saç stili değiştirildi."
                    
                result_image = None
                
                for part in response.candidates[0].content.parts:
                    if part.text is not None:
                        result_text += f"\n\n{part.text}"
                    elif part.inline_data is not None:
                        result_image = Image.open(BytesIO(part.inline_data.data))
                
                return result_image, result_text
                
            except Exception as e2:
                error_msg = f"❌ Hair transformation error (both methods): {str(e2)}\n\n💡 Tip: Try simpler requests (e.g., 'blonde hair', 'short hair')"
                if language == "tr":
                    error_msg = f"❌ Saç değiştirme hatası (her iki yöntemde): {str(e2)}\n\n💡 İpucu: Daha basit istekler deneyin (örn: 'sarı saç', 'kısa saç')"
                return None, error_msg

class HairEvaluationAgent:
    """Hair suitability evaluation agent"""
    
    def __init__(self, client):
        self.client = client
        
    def evaluate_hair_match(self, original_image, new_image, hair_change_request, language="en"):
        """Evaluate if the new hair style suits the person"""
        
        if language == "tr":
            prompt = f"""
            Bu iki fotoğrafı karşılaştır ve saç değişimini değerlendir:

            📸 FOTOĞRAFLAR:
            1. ORİJİNAL: Mevcut saç stili
            2. YENİ: "{hair_change_request}" editi uygulanmış

            🔍 DEĞERLENDİRME KRİTERLERİ:

            📐 **Yüz Uyumu** (1-10): Saç kişinin yüz şekline uygun mu?
            🎨 **Renk Uyumu** (1-10): Saç rengi cilt tonuna yakışıyor mu?  
            ✨ **Doğallık** (1-10): Gerçekçi ve doğal görünüyor mu?
            💫 **Genel Görünüm** (1-10): Kişiye yakışıklı mı?

            📊 **SONUÇ FORMATI:**

            🎯 **TOPLAM PUAN: X/40**

            📋 **PUANLAR:**
            • Yüz Uyumu: X/10
            • Renk Uyumu: X/10  
            • Doğallık: X/10
            • Genel Görünüm: X/10

            ✅ **GÜZEL OLAN:**
            • [Hangi yönleri başarılı]

            💡 **ÖNERİ:**
            • [Varsa iyileştirme önerisi]

            🎭 **SONUÇ:**
            [Bu saç kişiye yakışıyor mu? Kısa ve net değerlendirme]

            Samimi Türkçe ile yanıtla! 😊
            """
        else:
            prompt = f"""
            Compare these two photos and evaluate the hair change:

            📸 PHOTOS:
            1. ORIGINAL: Current hair style
            2. NEW: "{hair_change_request}" edit applied

            🔍 EVALUATION CRITERIA:

            📐 **Face Compatibility** (1-10): Does the hair suit the person's face shape?
            🎨 **Color Harmony** (1-10): Does the hair color match the skin tone?  
            ✨ **Naturalness** (1-10): Does it look realistic and natural?
            💫 **Overall Appearance** (1-10): Does it look good on the person?

            📊 **RESULT FORMAT:**

            🎯 **TOTAL SCORE: X/40**

            📋 **SCORES:**
            • Face Compatibility: X/10
            • Color Harmony: X/10  
            • Naturalness: X/10
            • Overall Appearance: X/10

            ✅ **WHAT WORKS WELL:**
            • [Which aspects are successful]

            💡 **SUGGESTION:**
            • [Any improvement suggestion if needed]

            🎭 **CONCLUSION:**
            [Does this hair suit this person? Brief and clear evaluation]

            Respond in friendly English! 😊
            """
        
        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash-exp",
                contents=[prompt, original_image, new_image],
                config=types.GenerateContentConfig(
                    response_modalities=['TEXT']
                )
            )
            
            return response.text
            
        except Exception as e:
            if language == "tr":
                return f"❌ Değerlendirme hatası: {str(e)}"
            else:
                return f"❌ Evaluation error: {str(e)}"

def setup_ai_system(api_key):
    """Set up AI system"""
    global client, hair_changer, hair_evaluator
    
    try:
        client = genai.Client(api_key=api_key)
        
        test_response = client.models.generate_content(
            model="gemini-2.0-flash-exp-image-generation",
            contents="Test message",
            config=types.GenerateContentConfig(response_modalities=['TEXT'])
        )
        
        hair_changer = HairChangeAgent(client)
        hair_evaluator = HairEvaluationAgent(client)
        
        return True, LANGUAGES[current_language]["api_setup_success"]
        
    except Exception as e:
        return False, LANGUAGES[current_language]["api_setup_error"].format(str(e))

def process_hair_change(image, message, history):
    """Main processing function"""
    global current_original_image, current_new_image
    
    if client is None:
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": LANGUAGES[current_language]["enter_api_first"]})
        return history, "", None
    
    if image is None:
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": LANGUAGES[current_language]["upload_photo_first"]})
        return history, "", None
    
    current_original_image = Image.fromarray(image)
    
    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": LANGUAGES[current_language]["processing_msg"]})
    
    try:
        new_image, change_text = hair_changer.change_hair_style(current_original_image, message, current_language)
        
        if new_image:
            current_new_image = new_image
            
            evaluation = hair_evaluator.evaluate_hair_match(
                current_original_image, current_new_image, message, current_language
            )
            
            full_response = f"""
{LANGUAGES[current_language]["success_msg"]}

{change_text}

---

{evaluation}
            """
            
            history[-1] = {"role": "assistant", "content": full_response}
            return history, "", current_new_image
            
        else:
            history[-1] = {"role": "assistant", "content": change_text}
            return history, "", None
            
    except Exception as e:
        error_msg = f"❌ Error occurred: {str(e)}\n\nDetail: {traceback.format_exc()}"
        history[-1] = {"role": "assistant", "content": error_msg}
        return history, "", None

def clear_chat():
    """Clear chat"""
    global current_original_image, current_new_image
    current_original_image = None
    current_new_image = None
    return [], None, ""

def handle_api_key(api_key):
    """Handle API key and set up system"""
    if not api_key or not api_key.strip():
        return "⚠️ Please enter your API key.", gr.update(interactive=False), gr.update(interactive=False), gr.update(interactive=False)
    
    success, message = setup_ai_system(api_key.strip())
    
    if success:
        return message, gr.update(interactive=True), gr.update(interactive=True), gr.update(interactive=True)
    else:
        return message, gr.update(interactive=False), gr.update(interactive=False), gr.update(interactive=False)

def switch_language(lang):
    """Switch interface language"""
    global current_language
    current_language = lang
    
    texts = LANGUAGES[lang]
    
    return (
        f'<div class="main-header"><h1>{texts["title"]}</h1><h3>{texts["subtitle"]}</h3><p>{texts["description"]}</p></div>',
        texts["api_key_title"] + "\n\n" + texts["api_key_desc"],
        texts["api_key_placeholder"],
        texts["start_system"],
        texts["system_status"],
        texts["waiting_api"],
        texts["how_to_use"] + "\n" + texts["how_to_steps"],
        texts["example_requests"] + "\n" + texts["examples"],
        texts["upload_photo"],
        texts["upload_label"],
        texts["result_photo"],
        texts["result_label"],
        texts["chat_title"],
        texts["message_placeholder"],
        texts["send_button"],
        texts["clear_chat"],
        texts["features_title"] + "\n" + texts["features_list"] + "\n\n" + texts["tech_info"]
    )

def on_image_upload(image):
    """Handle image upload"""
    if image is not None and client is not None:
        welcome_msg = [{"role": "assistant", "content": LANGUAGES[current_language]["welcome_msg"]}]
        return welcome_msg
    return []

# Create Gradio interface
with gr.Blocks(
    title="🎨 AI Hair Stylist - Hugging Face Spaces",
    theme=gr.themes.Soft(primary_hue="purple"),
    css="""
    .api-key-box {
        background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
    }
    .main-header {
        text-align: center;
        background: linear-gradient(45deg, #f093fb 0%, #f5576c 100%);
        padding: 30px;
        border-radius: 20px;
        margin-bottom: 30px;
        color: white;
    }
    .language-selector {
        text-align: center;
        margin-bottom: 20px;
    }
    """
) as demo:
    
    # Language Selector
    with gr.Row(elem_classes="language-selector"):
        gr.Markdown("### 🌍 **Language / Dil**")
        with gr.Row():
            en_btn = gr.Button("🇺🇸 English", variant="primary", size="sm")
            tr_btn = gr.Button("🇹🇷 Türkçe", variant="secondary", size="sm")
    
    # Header
    header_html = gr.HTML(f"""
    <div class="main-header">
        <h1>{LANGUAGES["en"]["title"]}</h1>
        <h3>{LANGUAGES["en"]["subtitle"]}</h3>
        <p>{LANGUAGES["en"]["description"]}</p>
    </div>
    """)
    
    # API Key Section
    with gr.Row():
        with gr.Column():
            gr.HTML('<div class="api-key-box">')
            api_key_section = gr.Markdown(LANGUAGES["en"]["api_key_title"] + "\n\n" + LANGUAGES["en"]["api_key_desc"])
            
            api_key_input = gr.Textbox(
                label="🔐 Gemini API Key",
                placeholder=LANGUAGES["en"]["api_key_placeholder"],
                type="password",
                lines=1
            )
            
            api_submit_btn = gr.Button(
                LANGUAGES["en"]["start_system"], 
                variant="primary",
                size="lg"
            )
            
            api_status = gr.Textbox(
                label=LANGUAGES["en"]["system_status"],
                value=LANGUAGES["en"]["waiting_api"],
                interactive=False,
                lines=2
            )
            gr.HTML('</div>')
    
    gr.Markdown("---")
    
    # Main App Section
    how_to_section = gr.Markdown(LANGUAGES["en"]["how_to_use"] + "\n" + LANGUAGES["en"]["how_to_steps"])
    example_section = gr.Markdown(LANGUAGES["en"]["example_requests"] + "\n" + LANGUAGES["en"]["examples"])
    
    with gr.Row():
        # Left side - Photo upload and result
        with gr.Column(scale=1):
            upload_title = gr.Markdown("### " + LANGUAGES["en"]["upload_photo"])
            
            image_input = gr.Image(
                label=LANGUAGES["en"]["upload_label"],
                type="numpy",
                height=300,
                interactive=False
            )
            
            result_title = gr.Markdown("### " + LANGUAGES["en"]["result_photo"])
            result_image = gr.Image(
                label=LANGUAGES["en"]["result_label"],
                height=300,
                interactive=False
            )
        
        # Right side - Chat interface
        with gr.Column(scale=2):
            chat_title = gr.Markdown("### " + LANGUAGES["en"]["chat_title"])
            
            chatbot = gr.Chatbot(
                height=400,
                show_label=False,
                type='messages'
            )
            
            with gr.Row():
                msg_input = gr.Textbox(
                    label="Your message",
                    placeholder=LANGUAGES["en"]["message_placeholder"],
                    lines=2,
                    scale=4,
                    interactive=False
                )
                send_btn = gr.Button(LANGUAGES["en"]["send_button"], variant="primary", scale=1, interactive=False)
            
            clear_btn = gr.Button(LANGUAGES["en"]["clear_chat"], variant="secondary", interactive=True)
    
    # Footer
    footer_section = gr.Markdown(LANGUAGES["en"]["features_title"] + "\n" + LANGUAGES["en"]["features_list"] + "\n\n" + LANGUAGES["en"]["tech_info"])
    
    # Event handlers
    def handle_message(image, message, history):
        if not message.strip():
            return history, "", None
        return process_hair_change(image, message, history)
    
    # Language switching
    en_btn.click(
        fn=lambda: switch_language("en"),
        outputs=[header_html, api_key_section, api_key_input, api_submit_btn, api_status, api_status, how_to_section, example_section, upload_title, image_input, result_title, result_image, chat_title, msg_input, send_btn, clear_btn, footer_section]
    )
    
    tr_btn.click(
        fn=lambda: switch_language("tr"),
        outputs=[header_html, api_key_section, api_key_input, api_submit_btn, api_status, api_status, how_to_section, example_section, upload_title, image_input, result_title, result_image, chat_title, msg_input, send_btn, clear_btn, footer_section]
    )
    
    # API Key handling
    api_submit_btn.click(
        fn=handle_api_key,
        inputs=[api_key_input],
        outputs=[api_status, image_input, msg_input, send_btn]
    )
    
    # Message sending
    send_btn.click(
        fn=handle_message,
        inputs=[image_input, msg_input, chatbot],
        outputs=[chatbot, msg_input, result_image]
    )
    
    msg_input.submit(
        fn=handle_message,
        inputs=[image_input, msg_input, chatbot],
        outputs=[chatbot, msg_input, result_image]
    )
    
    # Chat clearing
    clear_btn.click(
        fn=clear_chat,
        outputs=[chatbot, result_image, msg_input]
    )
    
    # Image upload handling
    image_input.change(
        fn=on_image_upload,
        inputs=image_input,
        outputs=chatbot
    )

if __name__ == "__main__":
    # Check if running on Hugging Face Spaces
    is_spaces = os.getenv("SPACE_ID") is not None
    
    if is_spaces:
        # Hugging Face Spaces - use default port
        print("🚀 Launching on Hugging Face Spaces...")
        demo.launch(
            share=False,
            server_name="0.0.0.0",
            server_port=7860,
            show_error=True
        )
    else:
        # Local development - find available port
        try:
            available_port = find_free_port()
            print(f"🚀 Launching locally on port {available_port}...")
            demo.launch(
                share=True,  # Enable sharing for local development
                server_name="0.0.0.0", 
                server_port=available_port,
                show_error=True,
                inbrowser=True  # Auto-open browser locally
            )
        except Exception as e:
            print(f"⚠️ Port {available_port} failed, trying automatic port selection...")
            demo.launch(
                share=True,
                server_name="0.0.0.0",
                server_port=None,  # Let Gradio choose
                show_error=True,
                inbrowser=True
            )