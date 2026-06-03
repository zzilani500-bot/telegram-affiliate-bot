import requests
import json
import time
import random
import logging
import os
from datetime import datetime

# ==================== CONFIGURATION ====================
BOT_TOKEN = "8866390249:AAF15MgldD6okO87A2gXQ7qsvLOmQkR4p7A"
CHANNEL_ID = "@shopfreeshop"  # Try @shopfree_shop if this doesn't work
GEMINI_API_KEY = "AIzaSyC6cSqjMa9aDyNL5AUYIWLZc4XptrFTnk8"
WISHLINK_URL = "https://wishlink.com/zilani"
POST_INTERVAL = 3600  # Post every 1 hour (in seconds)

# ==================== LOGGING ====================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

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

# Track posted products to avoid duplicates
posted_products = set()

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
        # Clean up the response - remove markdown code blocks if present
        text = text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()
        
        product = json.loads(text)
        logger.info(f"Generated product: {product['product_name']}")
        return product
        
    except Exception as e:
        logger.error(f"Gemini API error: {e}")
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
        
        # Add the affiliate link at the end
        caption += f"\n\n🛒 <b>Buy Now:</b> {WISHLINK_URL}\n"
        caption += f"\n📢 Join @shopfreeshop for daily deals!"
        
        return caption
        
    except Exception as e:
        logger.error(f"Gemini caption error: {e}")
        # Fallback caption
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


def find_product_image(search_term):
    """Try to find a product image URL using free sources"""
    # Using a placeholder approach - Telegram bot will send text post if no image
    # In production, you could use free image APIs or scrape product images
    return None


def send_telegram_message(caption, image_url=None):
    """Send message to Telegram channel"""
    
    if image_url:
        # Send photo with caption
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
        data = {
            "chat_id": CHANNEL_ID,
            "photo": image_url,
            "caption": caption,
            "parse_mode": "HTML"
        }
    else:
        # Send text message
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
            logger.info("✅ Message posted successfully!")
            return True
        else:
            logger.error(f"❌ Telegram error: {result.get('description', 'Unknown error')}")
            # Try alternate channel ID
            if CHANNEL_ID == "@shopfreeshop":
                logger.info("Trying alternate channel ID @shopfree_shop...")
                data["chat_id"] = "@shopfree_shop"
                response = requests.post(url, data=data, timeout=30)
                result = response.json()
                if result.get("ok"):
                    logger.info("✅ Message posted with alternate channel ID!")
                    return True
                else:
                    logger.error(f"❌ Alternate also failed: {result.get('description')}")
            return False
            
    except Exception as e:
        logger.error(f"Send message error: {e}")
        return False


def test_bot_connection():
    """Test if the bot can access the channel"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getMe"
    try:
        response = requests.get(url, timeout=10)
        result = response.json()
        if result.get("ok"):
            logger.info(f"✅ Bot connected: @{result['result']['username']}")
            return True
        else:
            logger.error(f"❌ Bot connection failed: {result}")
            return False
    except Exception as e:
        logger.error(f"Connection error: {e}")
        return False


def run_bot():
    """Main bot loop"""
    logger.info("=" * 50)
    logger.info("🚀 Starting Telegram Affiliate Bot")
    logger.info(f"📢 Channel: {CHANNEL_ID}")
    logger.info(f"⏰ Post interval: {POST_INTERVAL} seconds")
    logger.info(f"🔗 Affiliate link: {WISHLINK_URL}")
    logger.info("=" * 50)
    
    # Test connection
    if not test_bot_connection():
        logger.error("Failed to connect bot. Check your token.")
        return
    
    post_count = 0
    
    while True:
        try:
            logger.info(f"\n--- Generating post #{post_count + 1} ---")
            
            # Generate product using Gemini AI
            product = generate_product_with_gemini()
            
            if product is None:
                logger.warning("Failed to generate product. Retrying in 5 minutes...")
                time.sleep(300)
                continue
            
            # Check for duplicates
            product_key = product['product_name'].lower().strip()
            if product_key in posted_products:
                logger.info("Duplicate product, regenerating...")
                continue
            
            # Generate attractive caption using Gemini AI
            caption = generate_post_caption(product)
            
            # Try to find product image
            image_url = find_product_image(product.get('image_search_term', ''))
            
            # Send to Telegram
            success = send_telegram_message(caption, image_url)
            
            if success:
                posted_products.add(product_key)
                post_count += 1
                logger.info(f"Total posts sent: {post_count}")
            
            # Wait before next post
            # Add some randomness to seem more natural (±15 minutes)
            wait_time = POST_INTERVAL + random.randint(-900, 900)
            wait_time = max(600, wait_time)  # Minimum 10 minutes
            
            next_post_time = datetime.now().strftime("%H:%M:%S")
            logger.info(f"Next post in {wait_time//60} minutes...")
            time.sleep(wait_time)
            
        except KeyboardInterrupt:
            logger.info("\n🛑 Bot stopped by user.")
            break
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            time.sleep(60)


if __name__ == "__main__":
    run_bot()
