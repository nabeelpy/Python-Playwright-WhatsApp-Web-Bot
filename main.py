from playwright.sync_api import sync_playwright
import time
import re

processed = set()

with sync_playwright() as p:

    browser = p.chromium.launch_persistent_context(
        user_data_dir="sessions",
        headless=False
    )

    # WhatsApp
    whatsapp = browser.new_page()
    whatsapp.goto("https://web.whatsapp.com")

    # StormFiber
    portal = browser.new_page()
    portal.goto("https://my.stormfiber.com/index.php")

    input("Login WhatsApp + StormFiber then press ENTER...")

    print("Bot started...")
    last_refresh = time.time()

    while True:
        try:

            # -----------------------------------
            # KEEP STORMFIBER SESSION ALIVE
            # -----------------------------------
            if time.time() - last_refresh > 300:  # 5 minutes
                try:
                    portal.bring_to_front()

                    # simple harmless action (depends on portal)
                    portal.mouse.move(100, 100)
                    portal.keyboard.press("Shift")  # optional "activity"

                    print("Keep-alive triggered")

                except Exception as e:
                    print("Keep-alive error:", e)

                last_refresh = time.time()




            messages = whatsapp.locator("div.message-in")
            count = messages.count()

            if count > 0:

                last_msg = messages.nth(count - 1)
                text = last_msg.inner_text().strip()

                if text not in processed:
                    processed.add(text)

                    print("New WhatsApp Message:", text)

                    # -----------------------------
                    # STEP 1: Extract phone number
                    # -----------------------------
                    phone = re.sub(r"\D", "", text)  # keep digits only

                    # Remove starting 03
                    if phone.startswith("03"):
                        phone = phone[2:]

                    print("FINAL PHONE:", phone)

                    if len(phone) < 6:
                        reply = "Invalid number received. Please send correct mobile number."
                    else:

                        # -----------------------------
                        # STEP 2: Open StormFiber
                        # -----------------------------
                        portal.bring_to_front()
                        portal.locator("#customerMobileNo").clear()
                        portal.fill("#customerMobileNo", phone)

                        # optional debug
                        current_value = portal.locator("#customerMobileNo").input_value()
                        print("customerMobileNoSearched:", phone)
                        print("customerMobileNo:", current_value)

                        portal.click("#submit")

                        # -----------------------------
                        # STEP 3: Wait for result
                        # -----------------------------
                        try:
                            portal.wait_for_timeout(11000)

                            # CHANGE THIS SELECTOR after inspecting result area
                            # result = portal.locator("body").inner_text()
                            # result = portal.locator("#optical_power").inner_text()
                        # portal.wait_for_selector("#optical_power")

                            result = portal.locator("#optical_power").input_value()
                        except:
                            result = "No data found or request failed."

                        # -----------------------------
                        # STEP 4: Return message
                        # -----------------------------
                        reply = f"StormFiber Result:\n{result}"

                    # -----------------------------
                    # STEP 5: Send WhatsApp reply
                    # -----------------------------
                    whatsapp.bring_to_front()

                    box = whatsapp.locator('[contenteditable="true"]').last
                    box.fill(reply)

                    whatsapp.keyboard.press("Enter")

                    print("Reply sent")

        except Exception as e:
            print("Error:", e)

        time.sleep(3)