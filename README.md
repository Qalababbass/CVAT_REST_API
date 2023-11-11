# CVAT_REST_API

Using CVAT REST API to login in CVAT server using credentials. Create projects,extract project details. Create tasks in a project using the project id. Upload images to task using the task id.

## Usage:

1. Provide the server address and login credentials [here](https://github.com/Qalababbass/CVAT_REST_API/blob/0d5408a84501456bb3a529454125ad38cee7d07b/create_cvat_tasks.py#L221) .
2. The script takes four inputs
   + **--path** Path of directory containing all the directories of extracted images for each rosbag
   + **--project_id** The script assumes that project is already created manually, so it takes the project_id as input
   + **--camera** Camera namepsace
   + **--segment_size** This integer value is number of images to be allocated for one single job in cvat task

## Provided Functions:

1. [crete_login](https://github.com/Qalababbass/CVAT_REST_API/blob/b45f6e634965c81fe007b50401ab8022f418d708/create_cvat_tasks.py#L35) This method check the credentials and return the REST Token if the credentials are valid and authenticated
2. [get_project_details](https://github.com/Qalababbass/CVAT_REST_API/blob/b45f6e634965c81fe007b50401ab8022f418d708/create_cvat_tasks.py#L55C9-L55C28) Method returns details of a specific project with project_id
3. [create_task](https://github.com/Qalababbass/CVAT_REST_API/blob/b45f6e634965c81fe007b50401ab8022f418d708/create_cvat_tasks.py#L79C9-L79C20) Method creates a new task in a database without any attached images and videos
4. [get_task_details](https://github.com/Qalababbass/CVAT_REST_API/blob/b45f6e634965c81fe007b50401ab8022f418d708/create_cvat_tasks.py#L121C9-L121C25) Method returns details of a specific task with task_id
5. [post_images](https://github.com/Qalababbass/CVAT_REST_API/blob/b45f6e634965c81fe007b50401ab8022f418d708/create_cvat_tasks.py#L142C9-L142C20) Method post the images from the **--path** provided for images directories. It was set to only get first 15 images depending on **--camera** namepsace
