import requests
import json
import random
import time

# ==================== CONFIGURATION ====================
BOT_TOKEN = "8866390249:AAF15MgldD6okO87A2gXQ7qsvLOmQkR4p7A"
CHANNEL_ID = "@shopfreeshop"
GEMINI_API_KEY = "AIzaSyC6cSqjMa9aDyNL5AUYIWLZc4XptrFTnk8"
WISHLINK_URL = "https://wishlink.com/zilani"

# ==================== PRODUCT CATEGORIES ====================
CATEGORIES = [
    "smartphones under 15000",
    "wireless earbuds under 2000",
    "smartwatches under 3000",
    "laptop deals under 40000",
    "women's kurta sets under 500",
    "men's sneakers under 1500",
    "skincare products under 500",
    "home decor items under 1000",
    "kitchen appliances under 2000",
    "fitness accessories under 1000",
    "power banks under 1000",
    "bluetooth speakers under 2000",
    "backpacks under 800",
    "sunglasses under 500",
    "books bestsellers under 300",
    "gaming accessories under 2000",
    "women's handbags under 1000",
    "men's watches under 2000",
    "bedsheets and pillows under 800",
    "protein supplements under 1500",
    "kids toys under 500",
    "camera accessories under 1500",
    "tablet deals under 15000",
    "hair styling tools under 1000",
    "water bottles and lunch boxes under 500"
]


def generate_product_with_gemini():
    """Use Gemini AI to generate a trending product recommendation"""
    category = random.choice(CATEGORIES)

    prompt = f"""You are an affiliate marketing expert for Indian e-commerce. Generate ONE trending product deal for the category: "{category}"

Return ONLY a valid JSON object (no markdown, no code blocks) with these fields:
{{
    "product_name": "exact product name",
    "brand": "brand name",
    "original_price": "original MRP in INR (number only)",
    "deal_price": "discounted price in INR (number only)",
    "discount_percent": "discount percentage (number only)",
    "description": "2-3 line catchy description highlighting key features",
    "platform": "Amazon/Flipkart/Myntra/Ajio/Nykaa",
    "category": "category name",
    "rating": "rating out of 5",
    "image_search_term": "search term to find product image"
}}

Make it realistic with actual trending products available in India right now. Use real brand names and realistic prices."""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.9,
            "maxOutputTokens": 1000
        }
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        result = response.json()

        text = result['candidates'][0]['content']['parts'][0]['text']
        text = text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()

        product = json.loads(text)
        print(f"Generated product: {product['product_name']}")
        return product

    except Exception as e:
        print(f"Gemini API error: {e}")
        return None


def generate_post_caption(product):
    """Use Gemini AI to generate an attractive Telegram post caption"""

    prompt = f"""Create an attractive Telegram channel post for this product deal. Use emojis, make it eye-catching and create urgency.

Product: {product['product_name']}
Brand: {product['brand']}
Original Price: ₹{product['original_price']}
Deal Price: ₹{product['deal_price']}
Discount: {product['discount_percent']}% OFF
Description: {product['description']}
Platform: {product['platform']}
Rating: {product['rating']}/5

Rules:
- Use HTML formatting (use <b> for bold, <i> for italic)
- Include emojis for visual appeal
- Create urgency (limited time, stocks running out, etc.)
- Keep it under 200 words
- End with a clear call-to-action
- Do NOT include any link - I will add it separately
- Make it look like a professional deal channel post
- Add relevant hashtags at the end

Return ONLY the post text, nothing else."""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.8,
            "maxOutputTokens": 500
        }
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        result = response.json()

        caption = result['candidates'][0]['content']['parts'][0]['text'].strip()
        caption += f"\n\n🛒 <b>Buy Now:</b> {WISHLINK_URL}\n"
        caption += f"\n📢 Join @shopfreeshop for daily deals!"
        return caption

    except Exception as e:
        print(f"Gemini caption error: {e}")
        caption = f"""🔥 <b>DEAL ALERT!</b> 🔥

🏷️ <b>{product['product_name']}</b>

💰 MRP: <s>₹{product['original_price']}</s>
✅ Deal Price: <b>₹{product['deal_price']}</b>
🎉 {product['discount_percent']}% OFF!

📦 Platform: {product['platform']}
⭐ Rating: {product['rating']}/5

{product['description']}

⚡ Limited time offer - Grab it before it's gone!

🛒 <b>Buy Now:</b> {WISHLINK_URL}

📢 Join @shopfreeshop for daily deals!

#deals #offers #shopping #india"""
        return caption


def send_telegram_message(caption):
    """Send message to Telegram channel"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHANNEL_ID,
        "text": caption,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }

    try:
        response = requests.post(url, data=data, timeout=30)
        result = response.json()

        if result.get("ok"):
            print("✅ Message posted successfully!")
            return True
        else:
            print(f"❌ Telegram error: {result.get('description', 'Unknown error')}")
            # Try alternate channel ID
            data["chat_id"] = "@shopfree_shop"
            response = requests.post(url, data=data, timeout=30)
            result = response.json()
            if result.get("ok"):
                print("✅ Message posted with alternate channel ID!")
                return True
            else:
                print(f"❌ Alternate also failed: {result.get('description')}")
            return False

    except Exception as e:
        print(f"Send message error: {e}")
        return False


def main():
    """Generate and post one deal"""
    print("🚀 Generating deal post...")

    # Try up to 3 times
    for attempt in range(3):
        product = generate_product_with_gemini()
        if product:
            break
        print(f"Attempt {attempt + 1} failed, retrying in 5s...")
        time.sleep(5)

    if not product:
        print("❌ Failed to generate product after 3 attempts")
        return

    caption = generate_post_caption(product)
    success = send_telegram_message(caption)

    if success:
        print("🎉 Deal posted to channel!")
    else:
        print("❌ Failed to post deal")


if __name__ == "__main__":
    main()
