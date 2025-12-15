from playwright.async_api import async_playwright
import time
import asyncio

async def handle_consent(page):
    try:
        print("Checking for consent...")
        consent_button = page.get_by_role("button", name="Accetta tutto")
        if await consent_button.count() > 0:
            print("Clicking consent...")
            await consent_button.first.click()
            # Wait for navigation or just a bit for the overlay to disappear
            await page.wait_for_timeout(3000)
        else:
             consent_button_en = page.get_by_role("button", name="Accept all")
             if await consent_button_en.count() > 0:
                 print("Clicking consent (EN)...")
                 await consent_button_en.first.click()
                 await page.wait_for_timeout(3000)
    except Exception as e:
        print(f"Consent handling warning: {e}")

async def extract_results(page, limit=10, origin_address=None):
    # Extract results - Phase 1: Collection
    restaurants_to_scrape = []
    cards = await page.locator('div[role="feed"] > div > div[jsaction]').all()
    print(f"Found {len(cards)} potential cards. Limiting to {limit}.")
    
    # Limit to first N
    cards = cards[:limit]
        
    for card in cards:
        try:
            link = card.locator('a.hfpxzc')
            if await link.count() == 0:
                continue
                
            name = await link.get_attribute('aria-label')
            url = await link.get_attribute('href')
            
            # Rating from feed (still useful to capture here)
            rating = None
            star_rating = card.locator('span[role="img"][aria-label*="stars"]')
            if await star_rating.count() > 0:
               rating_text = await star_rating.get_attribute('aria-label')
               rating = rating_text.split(' ')[0]
            
            restaurants_to_scrape.append({
                "Name": name,
                "Rating": rating,
                "URL": url,
                # Placeholders for detail scraping
                "Address": None, 
                "Phone": None,
                "Website": None,
                "Charger Types": None,
                "Route Time": None,
                "Route Distance": None,
            })
            
        except Exception as e:
            print(f"Error parsing card: {e}")
            continue
    
    print(f"Collected {len(restaurants_to_scrape)} restaurants. Starting phase 2: Detail Scraping...")
    
    # Phase 2: Visit each URL for details
    results = []
    for i, r in enumerate(restaurants_to_scrape):
        print(f"[{i+1}/{len(restaurants_to_scrape)}] Scraping details for: {r['Name']}")
        try:
            await page.goto(r['URL'], timeout=60000)
            # Wait for detail logic
            try:
                # Wait for address button as a proxy for "loaded"
                await page.wait_for_selector('button[data-item-id="address"]', timeout=5000)
            except:
                # Maybe it doesn't have an address, or slow load. verify with h1
                await page.wait_for_selector('h1', timeout=5000)

            # Extract Details using known selectors
            
            # Address
            address_btn = page.locator('button[data-item-id="address"]')
            if await address_btn.count() > 0:
                 r["Address"] = (await address_btn.get_attribute("aria-label")).replace("Indirizzo: ", "").strip()
            
            # Phone
            phone_btn = page.locator('button[data-item-id^="phone:tel:"]')
            if await phone_btn.count() > 0:
                 r["Phone"] = (await phone_btn.get_attribute("aria-label")).replace("Telefono: ", "").strip()
                 
            # Website
            website_link = page.locator('a[data-item-id="authority"]')
            if await website_link.count() > 0:
                 aria = await website_link.get_attribute("aria-label") or ""
                 r["Website"] = aria.replace("Sito web: ", "").strip()

            # Charger Types Extraction
            # Logic: Scan text for "· ... kW" and take the line before it.
            r["Charger Types"] = None
            try:
                full_text = await page.locator('body').inner_text()
                lines = full_text.split('\n')
                connectors = []
                for k, line in enumerate(lines):
                    if '·' in line and 'kW' in line:
                        # Look back for non-empty line
                        j = k - 1
                        while j >= 0 and not lines[j].strip():
                            j -= 1
                        if j >= 0:
                            c_type = lines[j].strip()
                            power = line.strip().replace('·', '').strip()
                            if len(c_type) < 20: 
                                connectors.append(f"{c_type} ({power})")
                
                if connectors:
                    r["Charger Types"] = ", ".join(connectors)
            except Exception as e:
                 pass

            # Route Metrics Extraction
            try:
                print(f"  Getting directions...")
                
                # Click Directions
                directions_btn = page.locator('button[aria-label="Indicazioni"]')
                if await directions_btn.count() == 0:
                        directions_btn = page.locator('button[aria-label="Directions"]')
                
                if await directions_btn.count() > 0:
                    await directions_btn.first.click()
                    
                    # Wait for input (it usually appears even if "Your location" is default)
                    input_sel = 'div#directions-searchbox-0 input'
                    try:
                        # We always wait for the input to ensure the panel loaded
                        await page.wait_for_selector(input_sel, timeout=5000)
                        
                        # Only fill if we have a specific origin
                        if origin_address:
                            print(f"  Using origin: {origin_address}")
                            await page.locator(input_sel).fill(origin_address)
                            await page.keyboard.press("Enter")
                        else:
                            print("  Using default origin (Current Location)...")
                        
                        # Wait for result
                        # Time: div.Fk3sm
                        # Distance: div.ivN21e
                        await page.wait_for_selector('div.Fk3sm', timeout=10000)
                        
                        r["Route Time"] = await page.locator('div.Fk3sm').first.inner_text()
                        r["Route Distance"] = await page.locator('div.ivN21e').first.inner_text()
                        
                    except Exception as e:
                        print(f"  Routing failed (timeout/error): {e}")
                else:
                    print("  Directions button not found.")
                    
            except Exception as e:
                print(f"  Routing error: {e}")

            results.append(r)
            
        except Exception as e:
            print(f"Error scraping details for {r['Name']}: {e}")
            results.append(r) # Keep basic data even if detail fails
            
    return results

async def scrape_google_maps(search_query, origin_address):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        print(f"Navigating to Google Maps...")
        await page.goto("https://www.google.com/maps", timeout=60000)
        
        # Handle Consent
        await handle_consent(page)
        
        # Search
        print(f"Searching for '{search_query}'...")
        await page.wait_for_selector('input#searchboxinput', timeout=10000)
        await page.locator('input#searchboxinput').fill(search_query)
        await page.keyboard.press("Enter")
        
        # Wait for results to load
        print("Waiting for results...")
        await page.wait_for_selector('div[role="feed"]', timeout=30000)
        
        # Scroll to load more results
        feed_selector = 'div[role="feed"]'
        await page.hover(feed_selector)
        
        print("Scrolling to load more results...")
        for _ in range(5):  # Scroll a few times
            await page.mouse.wheel(0, 5000)
            await asyncio.sleep(2)
            
        # Use extracted function
        results = await extract_results(page, limit=10, origin_address=origin_address)
        
        print(f"Scraping complete.")
        await browser.close()
        return results

async def scrape_nearby(address, search_query):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        print(f"Navigating to Google Maps...")
        await page.goto("https://www.google.com/maps", timeout=60000)
        
        await handle_consent(page)
        
        # 1. Search for the address (Our Origin)
        print(f"Searching for target address: {address}...")
        await page.wait_for_selector('input#searchboxinput', timeout=10000)
        await page.locator('input#searchboxinput').fill(address)
        await page.keyboard.press("Enter")
        
        # Wait for address details...
        print("Waiting for address details...")
        try:
            # Wait for Nearby button
            await page.wait_for_selector('button[aria-label="Nelle vicinanze"]', timeout=15000)
        except:
            # Try English selector if timeout
            try:
                await page.wait_for_selector('button[aria-label="Nearby"]', timeout=5000)
            except:
                print("Could not find Nearby button. Address might be ambiguous.")
                pass
                
        # 2. Click Nearby
        nearby_btn = page.locator('button[aria-label="Nelle vicinanze"]')
        if await nearby_btn.count() == 0:
             nearby_btn = page.locator('button[aria-label="Nearby"]')
             
        if await nearby_btn.count() > 0:
            print("Clicking 'Nearby'...")
            await nearby_btn.first.click()
            
            # 3. Search for Query (e.g. Restaurants)
            print(f"Searching for nearby '{search_query}'...")
            await page.wait_for_selector('input#searchboxinput', timeout=5000)
            await page.locator('input#searchboxinput').fill(search_query)
            await page.keyboard.press("Enter")
            
            # 4. Extract Results
            print("Waiting for results...")
            await page.wait_for_selector('div[role="feed"]', timeout=30000)
            
            # Scroll to load more results
            feed_selector = 'div[role="feed"]'
            await page.hover(feed_selector)
            
            print("Scrolling to load more results...")
            for _ in range(5):  # Scroll a few times
                await page.mouse.wheel(0, 5000)
                await asyncio.sleep(2)
            
            # Use shared extraction logic
            results = await extract_results(page, limit=10, origin_address=address)
            
            await browser.close()
            return results
            
        else:
            print("Failed to start nearby search.")
            await browser.close()
            return []

