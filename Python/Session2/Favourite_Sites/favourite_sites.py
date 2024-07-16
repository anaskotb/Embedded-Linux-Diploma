
import webbrowser

# Dictionary of favorite websites
favorite_sites = {
    'Google': 'www.google.com',
    'GitHub': 'www.github.com/anaskotb',
    'OpenAI': 'www.openai.com'
}

def Firefox(url):
    webbrowser.open(f"https://{url}")
