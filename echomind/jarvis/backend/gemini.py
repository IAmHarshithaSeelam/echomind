import google.generativeai as genai

# Your API key from Google AIzaSyDpdPDJlG1pLgtBrf4EAqaiKf4NujBl6YA
genai.configure(api_key="AIzaSyD-KxurA5FWUpG5XaIcvSBtPgNbl2n13lE")

model = genai.GenerativeModel("gemini-1.5-flash")


# def get_gemini_response(prompt):
#     try:
#         response = model.generate_content(prompt)
#         return response.text
#     except Exception as e:
#         print("Gemini Error:", e)
#         return "Sorry, I couldn't fetch a response from Gemini."

# Example usage:
# if _name_ == "_main_":
#     user_input = input("Ask something: ")
#     print("Gemini says:", get_gemini_response(user_input))
def handle_gemini_response(query: str) -> str:
    try:
        response = model.generate_content(query)
        return response.text.strip()
    except Exception as e:
        return f"Gemini Error: {str(e)}"
# import google.generativeai as genai

# # Replace with your actual API key from Google AI Studio
# genai.configure(api_key="AIzaSyD-KxurA5FWUpG5XaIcvSBtPgNbl2n13lE")

# model = genai.GenerativeModel(model_name="gemini-pro")

# response = model.generate_content("What's the latest news in tech?")
# print(response.text)