#Image Downloader app
For start using this application need:  
1. clone from git: git clone "address".  
2. cd test_proj/
3. Change .env file for yourself:  
1.Auth settings  
2.Frequency mode of Cron job  
3.launch mode (need change in docker-compose line 22 RUN_API replace to RUN_TESTS for running as server or run tests)
4. docker-compose up --build  
5. Use API Client like Postman for use API:
6. default address of Search Endpoint it is http://0.0.0.0:5000/search/
7. You can use query params for find photos by tags => http://0.0.0.0:5000/search/?tags=<tags>
or by author http://0.0.0.0:5000/search/?author=<author> or by author and by tags http://0.0.0.0:5000/search/?tags=<tags>&author=<author>

