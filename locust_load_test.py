from locust import HttpUser, task, between
import json


messages = [{"role": "user", "content": "What's an astronomical unit?"}]

class MyUser(HttpUser):
    host = "http://0.0.0.0:8080"
    wait_time = between(1, 3)

    @task
    def call_completion(self):
        headers = {'Accept': 'application/json',
                   'Authorization': 'Bearer sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
                   'Content-Type': 'application/json'}

        # try:
        #     response = self.client.chat.completions.create(
        #         model="gpt-4",
        #         messages=messages,
        #     )
        #     response_length = response.usage.total_tokens
        # except Exception as e:
        #     exception = e
        #     response_time = int((time.time() - start_time) * 1000)
        #     events.request.fire(
        #         request_type="client",
        #         name="Inference test",
        #         response_time=response_time,
        #         response_length=response_length,
        #         exception=exception,
        #         response=response)
            
        res = self.client.post("/v1/chat/completions", 
                               headers=headers, 
                               data=json.dumps({"messages": messages, 
                                                "model": "gpt-4",
                                                "max_tokens": 512,
                                                "temperature": 0}))

        