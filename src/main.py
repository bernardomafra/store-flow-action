from driver.chrome import Chrome

browser = Chrome(headless=False)
browser.open("https://google.com.br")
