"""
Local Ultra-Lightweight LLM & High-EQ Neural Brain.
Designed for sub-100MB quantized local models (e.g., SmolLM 135M GGUF)
with an integrated zero-latency emotional inference engine fallback.
"""

import os
import urllib.request
import sys

DEFAULT_MODEL_URL = "https://huggingface.co/HuggingFaceTB/SmolLM-135M-Instruct-GGUF/resolve/main/smollm-135m-instruct-q4_k_m.gguf"
MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")
MODEL_PATH = os.path.join(MODEL_DIR, "smollm-135m-instruct-q4_k_m.gguf")

class LocalConversationalBrain:
    def __init__(self, profile, emotional_engine, model_path=MODEL_PATH):
        self.profile = profile
        self.emotional_engine = emotional_engine
        self.model_path = model_path
        self.llm = None
        self._init_local_model()

    def _init_local_model(self):
        """Attempts to load GGUF model via llama_cpp if present."""
        if os.path.exists(self.model_path):
            try:
                from llama_cpp import Llama
                print(f"[+] Loading local 100MB LLM: {self.model_path}")
                self.llm = Llama(
                    model_path=self.model_path,
                    n_ctx=1024,
                    n_threads=4,
                    verbose=False
                )
                print("[+] Local LLM successfully initialized.")
            except ImportError:
                print("[*] llama-cpp-python not installed. Using high-speed local neural heuristic engine.")
            except Exception as e:
                print(f"[-] Could not load GGUF model: {e}")

    @staticmethod
    def download_small_model():
        """Downloads the ~92MB SmolLM-135M-Instruct-Q4_K_M model."""
        os.makedirs(MODEL_DIR, exist_ok=True)
        if os.path.exists(MODEL_PATH):
            print(f"[+] Local model already exists at {MODEL_PATH}")
            return True

        print(f"[*] Downloading ~92MB local model from Hugging Face...")
        print(f"[*] URL: {DEFAULT_MODEL_URL}")
        try:
            def _progress(count, block_size, total_size):
                percent = int(count * block_size * 100 / total_size)
                sys.stdout.write(f"\rDownloading model: {percent}%")
                sys.stdout.flush()

            urllib.request.urlretrieve(DEFAULT_MODEL_URL, MODEL_PATH, reporthook=_progress)
            print(f"\n[+] Download complete! Saved to {MODEL_PATH}")
            return True
        except Exception as e:
            print(f"\n[-] Download failed: {e}")
            return False

    def generate_reply(self, incoming_text, history=None):
        analysis = self.emotional_engine.analyze(incoming_text, history)
        state = analysis["emotional_state"]
        text_lower = incoming_text.lower()

        # 1. If Local GGUF is available, use neural generation
        if self.llm:
            try:
                prompt = f"""<|im_start|>system
{self.profile.get_system_prompt_context()}
Current emotional state of subject: {state}
Directive: {analysis['directive']}
Reply concisely in {self.profile.data.get('language_preference', 'Hinglish')}.<|im_end|>
<|im_start|>user
{incoming_text}<|im_end|>
<|im_start|>assistant
"""
                output = self.llm(prompt, max_tokens=60, stop=["<|im_end|>", "\n\n"])
                reply = output["choices"][0]["text"].strip()
                if reply:
                    return reply, analysis
            except Exception as e:
                print(f"[-] Local LLM inference fallback triggered: {e}")

        # 2. Ultra-Fast High-EQ Contextual Engine (Zero Latency Fallback)
        reply = self._generate_contextual_fallback(incoming_text, analysis)
        return reply, analysis

    def _generate_contextual_fallback(self, incoming_text, analysis):
        state = analysis["emotional_state"]
        text_lower = incoming_text.lower()

        # Exit & Later scheduling
        if analysis["is_closing"] or "baad me" in text_lower or "later" in text_lower:
            return "Theek hai, kis time free rahogi baat karne ke liye? Time bata dena.", analysis

        if analysis["is_boundary"]:
            return "Theek hai, main samajh sakta hu. Aap araam se apna kaam karo, take care.", analysis

        if state == "HURT_AND_DEFENSIVE":
            if "doubt" in text_lower or "viswas" in text_lower or "partner" in text_lower or "character" in text_lower:
                return "Doubt to nahi hai, but vishwas bhi nahi hai...", analysis
            return "Haan main samajh sakta hu, galti meri hi thi. Dil se sorry baba, ab gussa thanda kar do na!", analysis

        if state == "PLAYFUL_BANTER":
            if any(w in text_lower for w in ["tandav", "chhat", "2:30"]):
                return "Hahaha arre wo to purani baat ho gayi! Tum to purani baatein nikaal ke baith gayi haha.. Abhi to sudhar gaya hu na thoda!", analysis
            if any(w in text_lower for w in ["boring", "daat", "ladai"]):
                return "Hahaha ye to sabka daily routine hai! Mummy ki daat ke bina din thodi banta hai haha.. Kisse ladai kar li aaj fir?", analysis
            return "Kyu, apni behen ki yaad aane ke liye koi time thodi chahiye hota hai haha! Aur batao, kya chal raha hai?", analysis

        # Default natural sibling greeting/follow-up
        return "Bas aise hi puch raha tha, free ho kya? Kaisi ho?", analysis
