FROM public.ecr.aws/lambda/python:3.8

COPY src/ ./src/
COPY requirements.txt .
RUN pip install --target ./ -r ./requirements.txt
RUN chmod 777 /tmp
RUN yum -y install ipa-gothic-fonts ipa-pgothic-fonts

CMD ["src/summary_tweet.lambda_handler"] 