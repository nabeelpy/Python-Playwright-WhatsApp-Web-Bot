from playwright.sync_api import sync_playwright
import time

processed_messages = set()

with sync_playwright() as p:

    browser = p.chromium.launch_persistent_context(
        user_data_dir="sessions",
        headless=False
    )

    # WhatsApp tab
    whatsapp = browser.new_page()
    whatsapp.goto("https://web.whatsapp.com")

    # Website tab
    portal = browser.new_page()
    portal.goto("https://my.stormfiber.com/index.php")

    input("Login to WhatsApp and website, then press ENTER...")

    print("Bot started...")

    while True:

        try:

            # Incoming messages
            messages = whatsapp.locator("div.message-in")

            count = messages.count()

            if count > 0:

                last_message = messages.nth(count - 1)

                text = last_message.inner_text()

                # Avoid duplicate processing
                if text not in processed_messages:

                    processed_messages.add(text)

                    print("New Message:", text)

                    ################################################
                    # WEBSITE SEARCH PART
                    ################################################

                    # Example search
                    # Replace these selectors later

                    # portal.fill("#search", text)
                    # portal.keyboard.press("Enter")
                    # time.sleep(2)
                    # result = portal.locator(".result").inner_text()

                    # Temporary fake response
                    result = f"Result found for: {text}"

                    ################################################
                    # SEND WHATSAPP REPLY
                    ################################################

                    box = whatsapp.locator(
                        '[contenteditable="true"]'
                    ).last

                    box.fill(result)

                    whatsapp.keyboard.press("Enter")

                    print("Reply Sent")

        except Exception as e:
            print("Error:", e)

        time.sleep(5)