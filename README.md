#Image Downloader app
For start using this application need:  
1. clone from git: git clone https://github.com/antl31/image_downloader.git 
2. cd image_downloader/
3. Change .env file for yourself:  
1.Auth settings  for external api
2.Frequency mode of Cron job  (Cron format)
3.launch mode (need change in docker-compose line 22  
 default parameter: RUN_API for running as server  
 if you want run test replace RUN_API to RUN_TESTS)
4. docker-compose up --build  
5. Use API Client like Postman for use API:
6. default address of Search Endpoint it is http://0.0.0.0:5000/search/
7. You can use query params for find photos by tags => http://0.0.0.0:5000/search/?tags=<tags>
or by author http://0.0.0.0:5000/search/?author=<author> or by author and by tags http://0.0.0.0:5000/search/?tags=<tags>&author=<author>
8. Ctrl + C for stopping server

