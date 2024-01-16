# from flask import Flask, request, jsonify
import re
import random

# app = Flask(__name__)

# Define patterns and responses related to the medical field
medical_patterns_and_responses = {
    r'hello|hi|hey': ['Hello!', 'Hi there!', 'Hey! How can I assist you with your medical questions?'],
    r'who are you': ['I am AI bot, here to help with Medical Issues'],
    r'how are you': ['I am just a computer program, but I am here to help with your medical inquiries.', 'I am functioning as usual. What can I do for you today?'],
    r'what is your name': ['I am a medical chatbot.', 'I don\'t have a name, but I can provide medical information and answer your health-related questions.'],
    r'bye|goodbye': ['Goodbye! If you have more questions in the future, feel free to return.', 'Take care!'],
    r'help': ['I can provide information on medical conditions, symptoms, treatments, and general health advice. Just ask your question.'],
    r'(.*) fever': ['Fever can be a symptom of various underlying conditions. It is important to consult a healthcare professional for a proper diagnosis and treatment.'],
    r'(.*) headache': ['Headaches can be caused by a variety of factors, including tension, dehydration, or underlying medical conditions. If your headache persists or worsens, consult a doctor.'],
    r'(.*) stomach pain': ['Stomach pain can have numerous causes, from indigestion to serious medical conditions. It is best to seek medical advice if you are experiencing stomach pain.'],
    r'(.*) cough': ['A cough can be due to various reasons, such as infections, allergies, or irritants. If you have a persistent cough, consult a healthcare provider for evaluation.'],
    r'(.*) cold': ['The common cold is a viral infection that can cause symptoms like a runny or stuffy nose, sore throat, and cough. Rest and hydration are typically recommended for recovery.'],
    r'(.*) COVID-19': ['COVID-19 is a contagious respiratory illness caused by the coronavirus SARS-CoV-2. If you suspect you have COVID-19 or have been exposed, follow public health guidelines and seek medical advice.'],
    r'(.*) diabetes': ['Diabetes is a chronic condition that affects blood sugar levels. Treatment may involve medication, lifestyle changes, and monitoring blood glucose levels. Consult a healthcare professional for guidance.'],
    r'(.*) heart disease': ['Heart disease is a broad term that includes various cardiovascular conditions. Prevention measures include a healthy diet, regular exercise, and avoiding risk factors like smoking.'],
    r'(.*) cancer': ['Cancer is a complex group of diseases characterized by the uncontrolled growth and spread of abnormal cells. Early detection and treatment are crucial.'],
    r'(.*) pregnancy': ['Pregnancy involves numerous changes in a woman\'s body. It is essential to receive prenatal care and follow medical advice during pregnancy for a healthy outcome.'],
    r'(.*) fever': ['Fever can be a symptom of various underlying conditions. It is important to consult a healthcare professional for a proper diagnosis and treatment.'],
    r'(.*) headache': ['Headaches can be caused by a variety of factors, including tension, dehydration, or underlying medical conditions. If your headache persists or worsens, consult a doctor.'],
    r'(.*) stomach pain': ['Stomach pain can have numerous causes, from indigestion to serious medical conditions. It\'s best to seek medical advice if you\'re experiencing stomach pain.'],
    r'(.*) cough': ['A cough can be due to various reasons, such as infections, allergies, or irritants. If you have a persistent cough, consult a healthcare provider for evaluation.'],
    r'(.*) cold': ['The common cold is a viral infection that can cause symptoms like a runny or stuffy nose, sore throat, and cough. Rest and hydration are typically recommended for recovery.'],
    r'(.*) COVID-19': ['COVID-19 is a contagious respiratory illness caused by the coronavirus SARS-CoV-2. If you suspect you have COVID-19 or have been exposed, follow public health guidelines and seek medical advice.'],
    r'(.*) diabetes': ['Diabetes is a chronic condition that affects blood sugar levels. Treatment may involve medication, lifestyle changes, and monitoring blood glucose levels. Consult a healthcare professional for guidance.'],
    r'(.*) heart disease': ['Heart disease is a broad term that includes various cardiovascular conditions. Prevention measures include a healthy diet, regular exercise, and avoiding risk factors like smoking.'],
    r'(.*) cancer': ['Cancer is a complex group of diseases characterized by the uncontrolled growth and spread of abnormal cells. Early detection and treatment are crucial.'],
    r'(.*) pregnancy': ['Pregnancy involves numerous changes in a woman\'s body. It\'s essential to receive prenatal care and follow medical advice during pregnancy for a healthy outcome.'],
    r'(.*) medication': ['Medications should be taken as prescribed by a healthcare provider. Always follow the recommended dosage and consult your doctor if you have questions or experience side effects.'],
    r'(.*) surgery': ['Surgery may be recommended for certain medical conditions. Discuss the risks, benefits, and alternatives with your surgeon before making a decision.'],
    r'(.*) mental health': ['Mental health is as important as physical health. If you or someone you know is struggling with mental health issues, consider seeking support from a mental health professional.'],
    r'(.*) vaccination': ['Vaccinations are essential for preventing infectious diseases. Consult your healthcare provider to ensure you are up to date with recommended vaccines.'],
    r'(.*) insurance': ['Health insurance can help cover medical expenses. It\'s important to understand your insurance plan and how to access healthcare services within your network.'],
    r'(.*) diet': ['A balanced diet plays a crucial role in maintaining good health. Consult a registered dietitian for personalized dietary advice.'],
    r'(.*) Ayurveda': ['Ayurveda is a traditional system of medicine that originated in India. It emphasizes balance in the body, mind, and spirit to maintain health and wellness. How can I assist you with Ayurveda-related questions?'],
    r'(.*) dosha': ['In Ayurveda, doshas are the three energies that govern our physical and mental well-being: Vata, Pitta, and Kapha. Each person has a unique dosha constitution.'],
    r'(.*) Ayurvedic remedies': ['Ayurveda offers a range of natural remedies, including herbs, diet, and lifestyle practices, to promote health and address imbalances.'],
    r'(.*) Panchakarma': ['Panchakarma is a detoxification and rejuvenation therapy in Ayurveda. It involves a series of treatments to remove toxins and restore balance in the body.'],
    r'(.*) Ayurvedic diet': ['Ayurvedic diet recommendations are based on your dosha constitution. It focuses on eating foods that balance your doshas for optimal health.'],
    r'(.*) Ayurvedic herbs': ['Ayurveda uses various herbs and botanicals for therapeutic purposes. Some common Ayurvedic herbs include turmeric, ashwagandha, and triphala.'],
    r'(.*) Ayurvedic lifestyle': ['Ayurvedic lifestyle practices include daily routines (dinacharya), yoga, meditation, and stress management to promote overall well-being.'],
    r'(.*) Ayurvedic treatment': ['Ayurvedic treatments are tailored to an individual\'s dosha constitution and health concerns. They may include herbal remedies, massages, and therapies.'],
    r'(.*) Ayurvedic practitioner': ['Consulting an Ayurvedic practitioner or Ayurvedic doctor (vaidya) can provide personalized guidance and treatment plans based on your Ayurvedic profile.'],
    r'(.*) Ministry of Ayush': ['The Ministry of Ayush is the Indian government ministry responsible for the development and promotion of Ayurveda, Yoga, Naturopathy, Unani, Siddha, and Homeopathy (AYUSH) systems of medicine. It plays a vital role in supporting and regulating these traditional healthcare practices.'],
    r'(.*) Ayush initiatives': ['The Ministry of Ayush initiates various programs and initiatives to promote and preserve traditional systems of medicine. These include research, education, and healthcare delivery.'],
    r'(.*) Ayush research': ['Ayush research focuses on scientific validation, standardization, and modernization of traditional medicine practices. It aims to bridge the gap between traditional knowledge and contemporary healthcare needs.'],
    r'(.*) Ayush education': ['The Ministry of Ayush supports Ayurvedic and other traditional medicine education through institutions and colleges. It also offers scholarships and training programs.'],
    r'(.*) Ayush regulations': ['Ayush systems of medicine are regulated by the Ministry of Ayush to ensure safety, quality, and efficacy. This includes the certification of Ayurvedic practitioners and the standardization of herbal products.'],
    r'(.*) Ayush promotion': ['The Ministry of Ayush promotes Ayurveda and traditional medicine both in India and globally. It participates in international collaborations and organizes events to raise awareness.'],
    r'(.*) AYUSH systems': ['The AYUSH systems include Ayurveda, Yoga, Naturopathy, Unani, Siddha, and Homeopathy. These systems have been practiced for centuries and offer holistic approaches to health and well-being.'],
    r'(.*) National Ayurveda Day': ['National Ayurveda Day is celebrated in India on Dhanteras (the first day of Diwali) to promote awareness and understanding of Ayurveda. It is an occasion to recognize the importance of traditional medicine.'],
    r'(.*) Ayush research institutes': ['The Ministry of Ayush supports various research institutes and centers dedicated to the study of traditional medicine systems. These institutes conduct research on Ayurveda, Yoga, and other AYUSH systems.'],
    r'(.*) Ayush wellness centers': ['Ayush wellness centers offer holistic healthcare services, including Ayurvedic treatments, Yoga, and Naturopathy. They aim to promote well-being and prevent illness.'],
    r'(.*) Ayush scholarships': ['The Ministry of Ayush provides scholarships to students pursuing courses in Ayurveda, Yoga, Naturopathy, Unani, Siddha, and Homeopathy. These scholarships support education in traditional medicine systems.'],
    r'(.*) Ayush healthcare delivery': ['Ayush systems of medicine are integrated into healthcare delivery in India. Many healthcare facilities offer Ayurvedic and other traditional treatments alongside modern medicine.'],
    r'(.*) Ayush international collaborations': ['The Ministry of Ayush collaborates with international organizations and countries to promote AYUSH systems globally. These collaborations include research, training, and cultural exchange programs.'],
    r'(.*) Ayush Startup Challenge': ['The Ayush Startup Challenge is an initiative by the Ministry of Ayush in collaboration with Startup India. It encourages startups to innovate and develop solutions in the field of traditional medicine and wellness.'],
    r'(.*) objectives of the challenge': ['The primary objectives of the Ayush Startup Challenge include fostering innovation in traditional medicine, promoting entrepreneurship in the Ayush sector, and supporting startups in the development of healthcare solutions.'],
    r'(.*) Ayush Startup winners': ['The challenge recognizes and rewards innovative startups in the Ayush sector. Winning startups may receive financial incentives, mentorship, and opportunities for further development and scaling.'],
    r'(.*) application process': ['Startups interested in participating in the Ayush Startup Challenge can typically apply through a designated platform or portal. The application process may involve submitting project proposals and meeting specific criteria.'],
    r'(.*) Ayush Startup benefits': ['Participating in the Ayush Startup Challenge can provide startups with access to valuable resources, visibility, networking opportunities, and potential funding to advance their projects.'],
    r'(.*) collaboration with Startup India': ['Startup India is a government initiative that promotes entrepreneurship and innovation. Collaborating with Startup India enhances the reach and impact of the Ayush Startup Challenge.'],
    r'(.*) Ayush Startup Challenge winners': ['Winners of the Ayush Startup Challenge are selected based on their innovative solutions and potential impact in the Ayush sector. They often receive recognition and support for further development.'],
    r'(.*) Ayush Startup Challenge eligibility': ['Eligibility criteria for the Ayush Startup Challenge may vary from one edition to another. Typically, startups with innovative ideas or products related to Ayurveda and traditional medicine are encouraged to apply.'],
    r'(.*) Ayush Startup Challenge timeline': ['The Ayush Startup Challenge usually follows a specific timeline, including announcement of the challenge, application period, evaluation, and announcement of winners. It is important to stay updated on official announcements for specific dates.'],
    r'(.*) Ayush Startup Challenge mentors': ['Mentorship is often a valuable aspect of the Ayush Startup Challenge. Selected startups may have the opportunity to receive guidance and mentorship from experts in the Ayush and entrepreneurship fields.'],
    r'(.*) Ayush Startup Challenge success stories': ['The Ayush Startup Challenge has seen success stories of startups that have gone on to make significant contributions to the Ayush sector. These stories inspire and showcase the potential for innovation in traditional medicine.'],
    r'(.*) Ayush Startup Challenge benefits': ['Participating in the Ayush Startup Challenge offers startups the opportunity to gain recognition, access funding, collaborate with experts, and contribute to the growth of traditional medicine and wellness solutions.'],
    r'(.*) Ayush Startup Challenge impact': ['The Ayush Startup Challenge aims to make a positive impact on the Ayush sector by fostering innovation, addressing healthcare challenges, and promoting the use of traditional medicine for holistic well-being.'],
    r'(.*) Ayush Startup Challenge partnerships': ['The challenge often collaborates with industry partners, academic institutions, and healthcare organizations to support and promote innovative startups in the Ayush field.'],
    r'(.*) Ayush Startup Challenge sectors': ['Startups participating in the Ayush Startup Challenge may focus on various sectors within traditional medicine, including Ayurveda, Yoga, Naturopathy, Unani, Siddha, Homeopathy, and more.'],
    r'(.*) Ayush Startup Challenge evaluation': ['Evaluation criteria for the Ayush Startup Challenge typically include innovation, feasibility, potential impact, scalability, and alignment with Ayush principles and goals.'],
    r'(.*) Ayush Startup Challenge future': ['The Ayush Startup Challenge continues to play a significant role in promoting entrepreneurship and innovation in traditional medicine. Future editions are expected to bring forth more innovative solutions in the Ayush sector.'],
    r'(.*) Ayush Startup Program': ['The Ayush Startup Program is designed to provide support and opportunities to new companies/startups in the Ayush sector. Here\'s how you can get help:'],
    r'(.*) eligibility for the program': ['To be eligible for the Ayush Startup Program, your company/startup typically needs to focus on Ayurveda, Yoga, Naturopathy, Unani, Siddha, Homeopathy, or related fields. Check the official guidelines for specific eligibility criteria.'],
    r'(.*) application process': ['To get help from the Ayush Startup Program, you should apply through the official application process. This usually involves submitting your business plan, project proposal, and other required documents.'],
    r'(.*) selection criteria': ['Startups are often selected based on the uniqueness of their ideas, potential impact on the Ayush sector, scalability, and alignment with Ayush principles and goals.'],
    r'(.*) support and benefits': ['Selected startups may receive various forms of support, including funding, mentorship, access to resources, collaboration opportunities, and recognition within the Ayush community.'],
    r'(.*) connecting with Ayush authorities': ['To learn more about the Ayush Startup Program and how your company/startup can get help, consider reaching out to Ayush authorities, attending program-related events, or visiting the official website for updates and contact information.'],
    r'(.*) success stories from the program': ['Many startups have benefited from the Ayush Startup Program and have gone on to make significant contributions to the Ayush sector. Learning from their success stories can provide insights for your own journey.'],
    r'(.*) Ayush Startup Program funding': ['One of the significant benefits of the Ayush Startup Program is the potential for funding support. Startups selected for the program may receive financial assistance to develop and scale their Ayush-related projects.'],
    r'(.*) mentorship and guidance': ['The Ayush Startup Program often offers mentorship and guidance from experts in the Ayush sector. This can include access to experienced professionals who can provide valuable insights and advice for startups.'],
    r'(.*) networking opportunities': ['Participating in the program can provide startups with networking opportunities within the Ayush community. This can lead to collaborations, partnerships, and exposure to potential investors or customers.'],
    r'(.*) resources and facilities': ['Some Ayush Startup Programs may offer access to research facilities, laboratories, or co-working spaces where startups can work on their projects and experiments.'],
    r'(.*) scaling and market access': ['Selected startups may receive support in scaling their products or services and gaining access to markets. This can be crucial for expanding the reach of Ayush solutions.'],
    r'(.*) program updates and deadlines': ['To stay informed about the Ayush Startup Program, it is essential to regularly check for program updates, application deadlines, and announcements on the official website or through program-related communications.'],
    r'(.*) reaching out to program coordinators': ['If you have specific questions or need assistance with your application, consider reaching out to the program coordinators or authorities. They can provide guidance and clarify any doubts you may have.'],
    r'.*': ['I am not qualified to provide a definitive medical diagnosis. If you have health concerns, consult a licensed healthcare professional for personalized advice.']
}

# Function to respond to user input
def respond(user_input):
    if user_input.lower() in ['exit', 'quit', 'goodbye']:
        return "Goodbye! If you have more questions in the future, feel free to return."
    for pattern, responses in medical_patterns_and_responses.items():
        if re.match(pattern, user_input, re.IGNORECASE):
            return random.choice(responses)
    return "I'm not sure how to respond to that. For specific information about getting help from the Ayush Startup Program, please visit the official program website or contact the relevant authorities."

# Main loop for user interaction
while True:
    user_input = input("You: ")
    response = respond(user_input)
    print("Ayush ChatBot:", response)
    if user_input.lower() in ['exit', 'quit', 'goodbye']:
        break

# @app.route('/chat', methods=['POST'])
# def chat():
#     user_input = request.json['user_input']
#     # Call your chatbot logic function with user_input and get the chatbot's response
#     chatbot_response = medical_patterns_and_responses(user_input)
#     return jsonify({'response': chatbot_response})

# if __name__ == '__main__':
#     app.run(debug=True)