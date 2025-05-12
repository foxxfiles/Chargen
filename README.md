# chargercharacter

## Mission  
The mission of **chargercharacter** is to provide writers, game designers, and content creators with an agile way to generate fictional characters, combining offline data with AI services to deliver coherent and customizable results in fantasy, science-fiction, medieval, and modern settings :contentReference[oaicite:0]{index=0}.

## Vision  
To become the go-to tool for character creation in the game development and narrative community, evolving into an extensible platform that integrates new data sources, collaborative features, and advanced multimedia generation :contentReference[oaicite:1]{index=1}.

## Quick Start  
1. Install Python 3.7  
2. Clone the repository  
3. Configure `config.json`  
4. Run:
   ```bash
   python3 chargen.py

## config.json

{
  "api": {
    "grok-2-latest": {
      "api_base_url": "https://api.x.ai/v1",   // Base URL of the API
      "api_key": "YOUR_SECRET_TOKEN",           // Your access key
      "api_type": "openai",                     // API type (here: OpenAI)
      "model": "grok-2-latest",                 // Name of the model to invoke
      "is_reasoner": false                      // Enable reasoning mode? (true/false)
    }
  }
}
## Usage Guide  
**Description of the “Character Generator” Interface:**  
![Character Generator (located at /utils/img)](/utils/img)

At the top you will see two tabs:

1. **Generator** — where the main panel resides.  
2. **History** — records of previously generated characters.

Below the tabs:

- **Label “Mode:”** Options: **offline**, **AI**.  
- **Label “Gender:”** Options: **random**, **Male**, **Female**, **Neutral**.  
- **Label “Style:”** Options: **fantasy**.  
- On the right, a **Generate** button to start the process.

Generation volume options:

- **Generate detailed character**  
- **Generate multiple**

At the bottom there are three buttons:

- **Copy** — to copy the generated information to the clipboard.  
- **Save** — to export the character sheet to a file.  
- **Clear** — to clear the text area.

This interface is designed to let the user quickly configure generation parameters, view progress, and manage the output (copy, save, or clear), all within a dark theme accented in orange for titles and active controls.  
