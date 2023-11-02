import requests
from datetime import date
import json
import sys
import os
import argparse

def parse_input():
    parser=argparse.ArgumentParser(description='Create New Tasks in CVAT for rocas extracted images')
    parser.add_argument('-p','--path',type=str,metavar='',help='Path of directory containing all the directories of extracted images for each rosbag')
    parser.add_argument('-p_id','--project_id',type=str,metavar='',help='Project id in which tasks are to be created')
    parser.add_argument('-c','--camera',type=str,metavar='',help='Camera namespace: either jai_cam or realsenseD435')
    parser.add_argument('-s','--segment_size',type=str,metavar='',required=False,default='10',help='Number of images for one job')

    
    args=parser.parse_args()
    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(0)

    return args



class CvatApi():


    def __init__(self,cvat_url,username,password):

        self.cvat_url=cvat_url
        self.username=username
        self.password=password


    def crete_login(self):
        '''
        This method check the credentials and return the REST Token if the credentials are valid and authenticated
        '''
        login_data={
            "username": self.username,
            "password": self.password,
        }
        header={"Content-Type":"application/json"}

        self.login_response = requests.post(f"{self.cvat_url}/auth/login", json=login_data,headers=header)
        if self.login_response.status_code==200:
            print('Login Successful')
            self.api_key=self.login_response.json()['key']
        
        else:
            print('Login Unsuccessful')
            sys.exit(0)


    def get_project_details(self,project_id):

        '''
        Method returns details of a specific project with project_id
        '''
        
        header={'Authorization': f'Token {self.api_key}'}

        self.project_data=requests.get(f"{self.cvat_url}/projects/{project_id}", headers=header)

        if self.login_response.status_code==200:
            if self.project_data.status_code==200:
                print('Project available with id : {}'.format(project_id))
                print(self.project_data.json())

            else:
                print('Project not available with id : {}'.format(project_id))
        else:
            print("Login Unsuccessful")
            sys.exit(0)
        
        return self.project_data.json()


    def create_task(self,task_name,project_id,owner_id,segment_size):

        '''
        Method creates a new task in a database without any attached images and videos
        '''
        
        task_name=str(task_name)

        header={'Authorization': f'Token {self.api_key}'}

        task_data={
            "name": task_name,
            "project_id": int(project_id),
            "owner_id": int(owner_id),
            "mode": 'annotation',
            "segment_size":int(segment_size),
            "overlap":0,
            }
        
        if self.login_response.status_code==200:
            
            if self.project_data.status_code==200:

                self.new_task=requests.post("{}/tasks".format(self.cvat_url),headers=header,json=task_data)
                #self.new_task_id=self.new_task.json()['id']
                
                if self.new_task.status_code==201:
                    print('Successfully created task with task name : {}'.format(task_name))
                
                else:
                    print('Task creation failed')
            
            else:
                print('No such Project found for the given Id :{} '.format(project_id))
        
        else:
            print("Login Unsuccessful")
            sys.exit(0)
        
        return self.new_task.json()


    def get_task_details(self,task_id):

        header={'Authorization': f'Token {self.api_key}'}
        task_id=int(task_id)

        if self.login_response.status_code==200:

            task_details=requests.get("{}/tasks/{}".format(self.cvat_url,task_id),headers=header)
            
            if task_details.status_code==200:
                print('Task with task_id : {} is available \n'.format(task_id))
                print(task_details.json())
            
            else:
                print('Failed to fetch details of Task with id : {}'.format(task_id))
       
        else:
            print('Login Unsuccessful')
            sys.exit(0)


    def post_images(self,task_id,image_dir,cam_namespace):
        
        header={'Authorization': f'Token {self.api_key}'}
        upload_image_url="{}/tasks/{}/data".format(self.cvat_url,task_id)
        image_paths=[]
        #realsense_image_paths=[]
        count=0

        for root,dirs,files in os.walk(image_dir):
            
            for file in files:
                if count>=15:
                    break

                if cam_namespace=='jai_cam':

                    if file.endswith(".png"):
                        if cam_namespace in file:
                            jai_image_path=os.path.join(root,file)
                            image_paths.append(jai_image_path)
                            count+=1

                elif cam_namespace=='realsenseD435':            
                    
                    if file.endswith(".png"):    
                        if cam_namespace in file:
                            realsense_image_path=os.path.join(root,file)
                            image_paths.append(realsense_image_path)
                            count+=1
        
        images = {f'client_files[{i}]': open(f, 'rb') for i, f in enumerate(image_paths)}
        data={
            "image_quality":[70]
        }
        send_image=requests.post(upload_image_url,headers=header,files=images,auth=(self.username,self.password),data=data)
        
        if self.login_response.status_code==200:
            
            if send_image.status_code==202:
                print('Images uploaded successfully')
            
            else:
                print('Image upload failed {}'.format(send_image.status_code))
        
        else:
            print('Login Unsuccessful')
            sys.exit(0)


    def create_jobs(self,task_id,image_dir):
        header={'Authorization': f'Token {self.api_key}'}
        job_url="{}/tasks/{}/jobs".format(self.cvat_url,task_id)
        job_data={
            "stage": "annotation",
            "type": "annotation",
            "task_id": task_id,
            "assignee": 0
        }

        self.new_job=requests.post(job_url,headers=header,json=job_data,auth=(self.username,self.password))
        if self.new_job.status_code==201:
            print('Job created successfully')
        else:
            print('Job creation failed {}'.format(self.new_job.status_code))
        
        print(self.new_job.json())






if __name__=='__main__':

    argmuents=parse_input()

    today=date.today()

    
    cvat_api_obj=CvatApi('http://localhost:8080/api','admin','admin')

    cvat_api_obj.crete_login()
    project_data=cvat_api_obj.get_project_details(argmuents.project_id)
    if argmuents.camera=='jai_cam':
        jai_cam_task=cvat_api_obj.create_task('jai_cam_{}'.format(today),argmuents.project_id,project_data['owner']['id'],argmuents.segment_size)
        cvat_api_obj.post_images(jai_cam_task['id'],argmuents.path,argmuents.camera)

    elif argmuents.camera=='realsenseD435':
        realsense_cam_task=cvat_api_obj.create_task('realsenseD435_{}'.format(today),argmuents.project_id,project_data['owner']['id'],argmuents.segment_size)
        cvat_api_obj.post_images(realsense_cam_task['id'],argmuents.path,argmuents.camera)
