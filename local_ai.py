def ask_local_ai(prompt):
    url = "http://localhost:1234/v1/chat/completions"
    headers = {"Content-Type": "application/json"}
    data = {
        "model": "mistral",
        "messages": [
            {
                "role": "system",
                "content": "Siz Pioneers jamoasi tomonidan yaratilgan aqlli kripto yordamchisiz. Faqat o‘zbek tilida javob bering. Kripto, treyding, grafik, tahlil va narxlar bo‘yicha savollarga oddiy, aniq va ishonchli javob bering."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=data)
    result = response.json()
    if "choices" in result:
        return result['choices'][0]['message']['content']
    else:
        return "Javob topilmadi."
