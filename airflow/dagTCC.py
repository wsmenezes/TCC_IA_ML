from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.dummy import DummyOperator
from airflow.operators.bash_operator import BashOperator
from airflow.utils.task_group import TaskGroup

path_dataset = "/home/william/TCC/datasets"
path_scripts = "/home/william/TCC/scripts"
path_deploy = "/home/william/TCC/deploy"
path_model_pkl = "/home/william/TCC/deploy/model.pkl"
path_model_h5 = "/home/william/TCC/deploy/model.h5"
path_nlp_score = "/home/william/TCC/deploy/score_compound.txt"

LAME4_dataset_raw = "/home/william/TCC/datasets/LAME4_historico.csv"
LAME4_dataset_done = "/home/william/TCC/datasets/LAME4_historico_DONE.csv"
LAME4_dataset_news = "/home/william/TCC/datasets/LAME4_noticias_D-10.txt"
VAREJO_dataset_news = "/home/william/TCC/datasets/VAREJO_noticias_D-10.txt"

default_args = {
   'owner': 'TCC',
   'depends_on_past': True,
   'start_date': datetime(2022, 1, 1),
   'retries': 0,
   }

with DAG(
   'dag-pipeline-TCC',
   schedule_interval=timedelta(hours=24),
   catchup=False,
   default_args=default_args
   ) as dag:

    start = DummyOperator(task_id="start")

    with TaskGroup("datasets", tooltip="datasets") as datasets:
        
        t1 = BashOperator(
            dag=dag,
            task_id='LAME4_datasets_download',
            bash_command="""
            cd {0}
            curl -o LAME4_historico.csv https://raw.githubusercontent.com/wsmenezes/TCC_IA_ML/main/LAME4_historico.csv
            curl -o LAME4_noticias_D-10.txt https://raw.githubusercontent.com/wsmenezes/TCC_IA_ML/main/LAME4_noticias_D-10.txt
            curl -o VAREJO_noticias_D-10.txt https://raw.githubusercontent.com/wsmenezes/TCC_IA_ML/main/VAREJO_noticias_D-10.txt
            """.format(path_dataset)
        )
        [t1]

    with TaskGroup("pre_processing", tooltip="pre_processing") as pre_processing:
        t2 = BashOperator(
            dag=dag,
            task_id='datasets_cleanup',
            bash_command="""
            cd {0}            
            /usr/local/miniconda3/bin/python pre_processing.py {1} {2}
            """.format(path_scripts, LAME4_dataset_raw, LAME4_dataset_done)
        )
        [t2]

    with TaskGroup("nlp", tooltip="nlp") as nlp:
        t3 = BashOperator(
            dag=dag,
            task_id='sentiment_analysis',
            bash_command="""
            cd {0}            
            /usr/local/miniconda3/bin/python sentiment_analysis.py {1} {2} {3}
            """.format(path_scripts, LAME4_dataset_news, VAREJO_dataset_news, path_nlp_score)
        )
        [t3]

#    with TaskGroup("model", tooltip="model") as model:
#        t4 = BashOperator(
#            dag=dag,
#            task_id='model_lnr',
#            bash_command="""
#            cd {0}
#            /usr/local/miniconda3/bin/python model_lnr.py {1} {2}
#            """.format(path_scripts, LAME4_dataset_done, path_model_pkl)
#        )
#        [t4]

    with TaskGroup("model", tooltip="model") as model:
        t4 = BashOperator(
            dag=dag,
            task_id='model_lstm',
            bash_command="""
            cd {0}
            /usr/local/miniconda3/envs/tf/bin/python model_lstm.py {1} {2}
            """.format(path_scripts, LAME4_dataset_done, path_model_h5)
        )
        [t4]    

    with TaskGroup("docker_build", tooltip="docker_build") as docker_build:
        t5 = BashOperator(
            dag=dag,
            task_id='API_deploy',
            bash_command="""
            cd {0}     
            docker rm $(docker stop $(docker ps | grep -i flask-tcc | cut -d ' ' -f 1))
            docker rmi -f $(docker images | grep -i flask-tcc | cut -d ' ' -f 10)
            docker build -t flask-tcc:latest .
            docker run -d -p 5001:5001 flask-tcc
            """.format(path_deploy)
        )
        [t5]    

    end = DummyOperator(task_id='end')
        
    start >> datasets >> pre_processing >> nlp >> model >> docker_build >> end
