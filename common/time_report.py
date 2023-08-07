import datetime
import json
from common.config import custom_path, low_time, med_time
import threading



class TimeReport:

    def __init__(self, file_name):
        print("Init")
        self.name = file_name
        self.low = 0
        self.med = 0
        self.high = 0
        self.lock = threading.Lock()


    def med_increase(self):
        with self.lock:
            self.med += 1

    def high_increase(self):
        with self.lock:
            self.high += 1

    def low_increase(self):
        with self.lock:
            self.low += 1

    def present(self):
        return f"LOW: {self.low}, MID: {self.med}, High: {self.high}"

    def write_rps_percent_results(self):
        """
        this function writes the percent result of the request per second ranges to JSON that located in the given path
        :param percente_value_by_range:
        :param custom_path: a path that provided by user
        :return:
        """
        json_obj = json.dumps(self.time_calculate())
        file_name = self.generate_unique_filename(file_base_name="percent_results")
        with open(f"{custom_path}/{file_name}", "w") as f:
            f.write(json_obj)

    def generate_unique_filename(self, file_base_name):
        """
        this function generate unique name for runs results
        :return:
        """
        now = datetime.datetime.now()
        formatted_date = now.strftime("%Y-%m-%d")
        formatted_time = now.strftime("%H-%M-%S")
        filename = f"{self.name}_{formatted_date}_{formatted_time}.json"
        return filename

    def times_count(self, time):
        if time <= low_time:
            self.low_increase()
        elif time <= med_time:
            self.med_increase()
        else:
            self.high_increase()

    def time_calculate(self):
        total = self.low + self.high + self.med
        if total is not 0:
            return {"Low": self.low / total, "Med": self.med / total, "High": self.high / total, "Total": total}
        else:
            return {'message':"Can't divide by Zero "}

    def reset_count(self):
        self.low = 0
        self.med = 0
        self.high = 0
        self.lock = threading.Lock()
        return self


"""
--- Read me --
To use this utils in locust follow the next steps : 
1. Add this file to your Projects
2 . add in your config file the custom_path= path in your system to local storage , low_time- minimum time until zero  , med_time - the meddile time 
3. Add to your locust the next code :

obj_time = TimeReport(__name__)


@events.request.add_listener
def my_request_handler(request_type, name, response_time, response_length, response,
                       context, exception, start_time, url, **kwargs):
    obj_time.times_count(response_time)


@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    obj_time.reset_count()
    if not isinstance(environment.runner, MasterRunner):
        print("Beginning test setup ")
    else:
        print("Started test from Master node")


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    if not isinstance(environment.runner, MasterRunner):
        print("Cleaning up test data" + obj_time.present())
        obj_time.write_rps_percent_results()
    else:
        print("Stopped test from Master node")


"""
