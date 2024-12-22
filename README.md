# Image Storage Gallery with Vector Search
An image gallery to allow searching images by content and photo compositional techniques. 
Demo: https://img-cap-851de0d0f814.herokuapp.com/

How to Run
1. Clone repo: git clone https://github.com/HDWilliams/imgcap.git
2. Optional for VS Code: Set up python virtual env ( https://code.visualstudio.com/docs/python/environments )
3. Install Dependencies: python -m pip install -r requirements.txt
4. Add credentials to .env_CLONED file and change name to .env
   - OpenAi API key
   - AWS Key (For Rekognize and S3)
   - MEMCACHE CLOUD Key (Work in progress)
5. Run locally with: python -m flask run


# About ImgCap
ImgCap gallery as a project was meant to be a primarily backend focused effort to explore using machine learning and LLM APIs to create a user facing full stack application with unique functionality. As a photographer I wanted to explore and learn about the specifics of how images are stored and searched for content. I also wanted to allow users to search images based on emotion and photographic compositional techniques. 
- 'rule of thirds'
- 'centered'
- 'pattern'
- 'leading lines'
- 'symmetry'
- 'framing'

For me as a photographer emotion/mood and technique are important ways I search for inspiration for my photos.

# Highlights, Challenges and Learnings
- Image Storage
    - selecting an image storage network that would allow for scalability and also low upfront cost, while still being able to handle large highquality image files
    - added client side compression to reduce latency, but tuned amount of compression to allow for high quality AI image tagging and quality image display for users
    - Selected AWS in concert with Rekognize to reduce latency of passing image data between services
- Image Tagging
    - Original concept for project was to use Open Ai api for all image tagging -> resulted in high latency
    - instead a combination of AWS rekognize and OpenAi api were selected. Rekognize allows for consistent and quality detection of people/objects/animals etc.
    - the Open AI api provides interpretation of photo mood and can decipher use of 1 or more photographic techniques
    - OpenAi api can download image directly from S3 after upload via link, reduces load on server to pass image directly to OpenAi Api
- Vectorizing and Searching Tags for Images
    - Once tags were obtained they had to be vectorized
    - Multiple methods were explored including 1. creating embedding microservice with fasttext 2. running word2vec on server to tokenize tags 3. 3rd party services
    - Ultimately the OpenAI embedding service was chosen due to low cost and ability to recognize any potential input (unlike work2vec)
-  Database
    - Designed schema for storing image meta data and tags, tags must be individually searchable and relevant images can be derived from tags
        - decided to create table for tag and table for image metadata
        - used union table to allow searching in both directions
    - while both NoSQL and SQL was explored ultimately SQL was chosed for the project due to structured nature of data
    - SQL Lite was used for local dev and then migrated to heroku PostgreSQL for production
    - PostgreSQL also allowed the use of pgvector to easily make vectorized tags searchable, to power image search also had free tier to reduce upfront cost
    - a separate redis service is being used for WIP rate limiting feature
- Prompt Engineering
    - created initial prompt to get model provide tags for images based on emotion/mood and compositional techniques
    - iterated on prompt using AI to reduce character count and cost of each query
- Front End
    - while the primary focus was backend functionality, creating a clean, organized mobile first design was paramount
    - given limited resources for project image uploading/deleting can take time, an elegant way to disable user interaction during these operations was using overlays

