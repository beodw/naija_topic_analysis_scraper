from utils import mark_yoruba_text
from selenium.webdriver import Keys
from utils import format_csv_comments
from selenium import webdriver
import time


options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)
options.add_argument("--auto-open-devtools-for-tabs")
# A TRICK TO BYPASS CLOUDFLARE CAPTCHAS. SOMETIMES NEEDS TO BE RERUN
driver.execute_script('''window.open("https://www.nairaland.com/login","_blank");''')  # open page in new tab
time.sleep(20)  # wait until page has loaded
driver.switch_to.window(window_name=driver.window_handles[0])  # switch to first tab
driver.close()  # close first tab
driver.switch_to.window(window_name=driver.window_handles[0])  # switch back to new tab
time.sleep(2)
driver.get("https://google.com")
time.sleep(2)
driver.get("https://www.nairaland.com/login")  # this should pass cloudflare captchas now
time.sleep(15)

# Find the username and password input fields and fill them out
username_input = driver.find_element('name', 'login')
password_input = driver.find_element('name', 'password')

username_input.send_keys('beodw')
password_input.send_keys('Password123')

# Submit the form
password_input.send_keys(Keys.RETURN)
time.sleep(5)

driver.get("https://www.nairaland.com/racism-tribalism")
print("Opened the page:" + driver.current_url)

time.sleep(5)
driver.get(f"https://www.nairaland.com/racism-tribalism")
topicElements = driver.find_elements("xpath", "//*[starts-with(@id, 'top')]/b/a")
hrefs = []
for element in topicElements:
    hrefs.append(element.get_attribute("href"))

time.sleep(3)
# get total number of pages
pages_count = driver.find_element("xpath", "/html/body/div[1]/p[3]/b[2]").text
print(f"Found {pages_count} pages")

i = 1
while i <= int(pages_count) - 1:
    driver.get(f"https://www.nairaland.com/racism-tribalism/{i}")
    topicElements = driver.find_elements("xpath", "//*[starts-with(@id, 'top')]/b/a")
    for element in topicElements:
        link = element.get_attribute("href")
        hrefs.append(link)

    i += 1

print(f"Found {len(hrefs)} links:" + str(hrefs))

# Initialize an empty set to store links
# ONE link was new so we will write it to the file. Let's check if it is already in the file
existing_links = set()
# Check if the file exists and read existing links into the set
try:
    with open("nairaland_processed.csv", "r") as f:
        existing_links.update(f.read().splitlines())
except FileNotFoundError:
    pass

for link in hrefs:
    # Check if link already exists in the set
    if link not in existing_links:
        print(f"Link {link} is new, writing to file")

        # Write the new link to the file and add it to the set
        driver.get(link)
        # Adjust sleep time to allow page to load
        time.sleep(4)

        try:
            title = driver.find_element("xpath", "/html/body/div[1]/table[2]/tbody/tr[1]/td/a[4]").text.replace('"', "'")
            post = driver.find_elements("xpath", "//*[starts-with(@id, 'pb')]")[0]

            # Find if post contains imgs
            imgs = post.find_elements("tag name", "img")
            image_srcs = [img.get_attribute("src") for img in imgs]

            # Get the post text
            post_text_raw = post.find_element("xpath", "div").text.replace('\n', ' ').replace('"', "'") + (
                f"Images: {image_srcs}" if image_srcs else "")

            post_text = mark_yoruba_text(post_text_raw).replace('\n', '').replace('"', "'")

            if "No Yoruba language found" not in post_text:
                boolean_flag = True
                post_text = f"%%{post_text}%%" + " " + post_text_raw
            else:
                boolean_flag = False
                post_text = post_text_raw


            comments_raw = driver.find_elements("xpath", "//*[starts-with(@id, 'pb')]/div")[1:6]

            comments_to_process = []
            for comment in comments_raw:
                comments_to_process.append(comment.text.replace('"', "'"))

            formatted_comments = [format_csv_comments(title, comment) for comment in comments_to_process]
            formatted_comments = ", ".join(formatted_comments).replace('"', "'").replace('\n', '').replace("\t", "")

            # Handle potential exceptions
            with open("nairaland_data.csv", "a") as f:
                f.write(f'{title}"{post_text}"{formatted_comments}"{boolean_flag}"')
                f.write("\n")
                print(f"Written data for {title} to file")
            with open("nairaland_processed.csv", "a") as f:  # Open in append mode within the loop
                f.write(link + "\n")

            existing_links.add(link)
        except Exception as e:
            print(f"Error processing link {link}: {e}")

    else:
        print(f"Link {link} already exists in file")

#
