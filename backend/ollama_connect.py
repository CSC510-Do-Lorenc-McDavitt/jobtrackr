from flask import request, jsonify
from langchain_ollama import ChatOllama
from files import get_pdf_info
llm = ChatOllama(
    model="llama3.2",
    temperature=0,
)

system_prompt_cv_short = """
You are a helpful assistant that writes a cover letter from a resume and a job description.
Only respond with the cover letter and nothing else.
"""

system_prompt_cv_long = """
You are a helpful assistant that writes a cover letter from a resume and a job description.
You have also been provided with a few example cover letters.
Only respond with the cover letter and nothing else.

ANALYSIS REQUIREMENTS:
1. Use the top 3-5 skills from the job description
2. Include references to any matched experiences with qualities the job is looking for
3. Note any unique and strong candidate qualities
4. Reference the company's values if they match with the candidate

COVER LETTER GUIDELINES:
- Start with a compelling hook to grab the hiring manager's attention
- Ensure to focus on specific achievements that are relevant and quantifiable
- Show that you understand the company and their challenges
- Use a professional tone with genuine enthusiasm
- The length should be between 250 and 350 words
- Avoid generic phrases
- Address any potential hiring concerns (career changes, gap years, etc.)

STRUCTURE:
1. Opening Paragraph:
   - Reference something about the company
   - State position and why you are interested
   - Include compelling hook to engage the hiring manager

2. Body Paragraphs (2-3):
   - Match your top relevant achievements to job description
   - State relevant measurable outcomes
   - Demonstrate an openness to learn and grow
   - Show how you fit into the company culture

3. Closing Paragraph:
   - Restate why the job is a good fit
   - Express genuine enthusiasm for next steps in the hiring process
   - End with a call to action

TONE AND STYLE:
- Professional but approachable
- Confident and humble
- Enthusiastic without being desperate
- Matching company values with personal values

FORMAT:
Dear Hiring Manager,

[Cover Letter Content]

Sincerely,
[Your Name]
"""

entry_level_example_cv = """
Dear Hiring Manager,

I am writing to express my strong interest in the Entry Level Software Engineer 
position at Re/codeRealm. As a recent graduate with a degree in Computer Science 
and a passion for coding, I am excited about the opportunity to contribute to your 
innovative team and make a meaningful impact in the software development industry.

During my academic journey, I have gained a solid foundation in programming languages 
such as Java, C++, and Python. Through various projects and internships, I have developed 
a strong understanding of software development principles and best practices. I am 
particularly drawn to Re/codeRealm's commitment to cutting-edge technologies and its 
reputation for pushing boundaries in the industry. The prospect of working alongside 
talented professionals who share my passion for innovation is truly exhilarating.

What sets me apart as a candidate is my ability to think critically and solve complex 
problems. I thrive in fast-paced environments and enjoy collaborating with cross-functional 
teams to deliver high-quality software solutions. My experience working on a team project 
to develop a mobile application showcased my ability to adapt to changing requirements 
and deliver results under tight deadlines. I am confident that my strong analytical 
skills, attention to detail, and dedication to continuous learning make me a great 
fit for Re/codeRealm.

In addition to my technical skills, I possess excellent communication and interpersonal 
skills, which I believe are essential for effective collaboration and teamwork. I am a 
proactive and motivated individual who is always eager to learn and grow. I am confident 
that my passion for software engineering and my drive to excel will enable me to contribute 
to Re/codeRealm's success.

Thank you for considering my application. I am excited about the opportunity to further 
discuss how my skills and qualifications align with Re/codeRealm's vision. I have attached 
my resume for your review. I look forward to the possibility of joining your team and 
contributing to the development of innovative software solutions.

Sincerely,

Billie Horton
"""

experienced_example_cv = """
Dear Hiring Manager,

I am writing to express my strong interest in the Experienced Software Engineer 
position at FluxDesigns. With my extensive background in software development and 
a passion for creating innovative solutions, I am confident that I would be a 
valuable asset to your team.

Having worked in the software engineering field for over 8 years, I have gained 
a deep understanding of the industry and have honed my skills in various programming 
languages and technologies. My experience includes developing scalable web applications, 
implementing efficient algorithms, and collaborating with cross-functional teams to 
deliver high-quality software solutions.

What excites me most about the opportunity at FluxDesigns is the chance to work on 
cutting-edge projects that push the boundaries of technology. Your company's 
commitment to innovation aligns perfectly with my own drive to constantly learn 
and stay ahead of the curve. I am particularly drawn to FluxDesigns' emphasis on 
creating user-centric experiences and leveraging emerging technologies to solve 
complex problems.

In my previous role as a Senior Software Engineer at XYZ Corporation, I successfully 
led a team in developing a groundbreaking mobile application that received industry 
recognition for its seamless user interface and robust functionality. I believe 
that my strong problem-solving skills, attention to detail, and ability to 
collaborate effectively make me an ideal candidate for this position.

I am impressed by FluxDesigns' reputation for fostering a collaborative and 
inclusive work environment. Your commitment to employee growth and development, 
as well as your dedication to creating a positive impact on society through 
technology, resonates deeply with my own values. I am confident that my skills 
and experience would contribute to the continued success of your team.

Thank you for considering my application. I am excited about the opportunity 
to contribute to FluxDesigns and would welcome the chance to discuss how my 
qualifications align with your needs in more detail. I have attached my resume 
for your review. Please feel free to contact me at your convenience.

Sincerely,

Gabriel Turner
"""

junior_example_cv = """
Dear Hiring Manager,

I am writing to express my strong interest in the Junior Software Engineer 
position at Instagraph. As a highly motivated and skilled software engineer, 
I am excited about the opportunity to contribute to your team and make a 
meaningful impact on the development of innovative software solutions.

With a Bachelor's degree in Computer Science and hands-on experience in 
software development, I am confident in my ability to excel in this role. 
Throughout my academic and professional journey, I have gained a solid 
foundation in programming languages such as Java, C++, and Python, as 
well as a strong understanding of software development methodologies 
and best practices.

What truly excites me about the Junior Software Engineer position at 
Instagraph is the company's commitment to pushing the boundaries of 
technology and delivering cutting-edge solutions to clients. I am particularly 
drawn to Instagraph's focus on creating user-friendly and visually stunning 
software applications. This aligns perfectly with my passion for creating 
intuitive and impactful user experiences.

During my previous internship at a software development firm, I had the 
opportunity to work on a team responsible for developing a mobile 
application that received rave reviews for its sleek design and 
seamless functionality. I was actively involved in the entire software 
development lifecycle, from gathering requirements to testing and deployment. 
This experience not only honed my technical skills but also taught me the 
importance of effective collaboration and communication within a team.

I believe my strong problem-solving abilities, attention to detail, and 
dedication to delivering high-quality software make me an ideal fit for 
the Junior Software Engineer position at Instagraph. I am confident that 
my passion for software development and my ability to quickly adapt to new 
technologies will enable me to contribute to the success of your team.

Thank you for considering my application. I am eager to discuss how my 
skills and experiences align with Instagraph's needs in more detail. I 
look forward to the opportunity to contribute to your team and help drive 
the future of software development at Instagraph.

Sincerely,

Tracey Clayton
"""

def generate_cv(Files):
    """
    Generates a cover letter from a resume and a job description.
    ```
    Request:
    {
        resume: string,  
        job_desc: string
    }
    Response:
    {
        status: boolean
        data: message (Success / Error message as per status)
        
    }
    ```
    """
    try:
        if request:
            req = request.get_json()
            resume = get_pdf_info(req["file"], Files, req["email"])
            job_desc = req["job_desc"]
            context = req["context"] if req["context"] and len(req["context"]) > 0 else ""

            messages = [
                ("system",system_prompt_cv_short,),
                ("human", "Resume: " + resume),
                ("human", "Additional Requests and Context: " + context),
                ("human", "Job Description: " + job_desc),
            ]
            msg = llm.invoke(messages)
            response = msg.content
            return jsonify({'message': "Cover Letter Generated Successfully", 'letter': response}), 200

    except Exception as e:
        return jsonify({'error': "Something went wrong"}), 400
    
def resume_suggest(Files):
    """
    Reviews a resume and provides suggestions to tailor it for a job description.
    ```
    Request:
    {
        resume: string,  
        job_desc: string
    }
    Response:
    {
        status: boolean
        data: message (Success / Error message as per status)
        
    }
    ```
    """
    try:
        if request:
            req = request.get_json()
            resume = get_pdf_info(req["file"], Files, req["email"])
            job_desc = req["job_desc"]
            
            messages = [
                (
                    "system",
                    "You are a helpful assistant that provides resume suggestions to tailor a resume to the job description.",
                ),
                ("human", "Resume: " + resume),
                ("human", "Job Description: " + job_desc),
            ]
            msg = llm.invoke(messages)
            response = msg.content
            return jsonify({'message': "Successfully Created Resume Suggestions", 'suggestions': response}), 200

    except Exception as e:
        return jsonify({'error': "Something went wrong"}), 400
