import xmltodict
import random
import datetime
from common.config import *
from common.time_report import TimeReport
from locust import FastHttpUser, constant, tag, task, events
from locust.runners import MasterRunner


class QueryService(FastHttpUser):
    constant(1)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.spatial_ope = None
        self.geo_oper = None
        self.get_feature_params = None
        query_request = f"?{token}&service=wfs&version=2.0.0&request=GetFeature&typeNames={featureType}&outputFormat" \
                        f"=json&count={numbers_of_req}&sortBy={by_date} "
        with self.client.get(query_request, catch_response=True, verify=False, name="GetFeaturePostOnStart") as resp:
            if 200 == resp.status_code:
                resp.success()
                get_params_req = resp.json()
                self.get_feature_params = get_params_req[feature_name]
            else:
                resp.failure("init GetFeature failed")

        query_request = f"?{token}&service=wfs&version={version}&request=GetCapabilities"
        with self.client.get(query_request, catch_response=True, verify=False,
                             name="GetCapabilitiesOnStart") as response:
            if 200 == response.status_code:
                response.success()
                get_params_req = xmltodict.parse(response.text)
                geo_ope = get_params_req['wfs:WFS_Capabilities']['fes:Filter_Capabilities']['fes:Spatial_Capabilities'][
                    'fes:SpatialOperators']['fes:SpatialOperator']
                spatial_ope = \
                    get_params_req['wfs:WFS_Capabilities']['fes:Filter_Capabilities']['fes:Spatial_Capabilities'][
                        'fes:GeometryOperands']['fes:GeometryOperand']
                self.geo_oper = [name['@name'] for name in geo_ope]
                self.spatial_ope = [name['@name'].replace("gml:", "") for name in spatial_ope]
            else:
                response.failure(str(response.status_code) + " Query has sent: " + query_request)

    @task(1)
    @tag('GetCapabilities')
    def test_get_capabilities(self):
        query_request = f"?{token}&service=wfs&version={version}&request=GetCapabilities"
        with self.client.get(query_request, catch_response=True, verify=False, name="GetCapabilities") as response:
            if 200 == response.status_code:
                response.success()
            else:
                response.failure(str(response.status_code) + " Query has sent: " + query_request)

    @task(1)
    @tag('DescribeFeatureTypeGet')
    def test_describe_feature_type_get(self):
        query_request = f"?{token}&service=wfs&version={version}&request=DescribeFeatureType&typeNames={featureType} "
        with self.client.get(query_request, catch_response=True, verify=False,
                             name="DescribeFeatureTypeGet") as response:
            if 200 == response.status_code:
                response.success()
            else:
                response.failure(str(response.status_code) + " Query has sent: " + query_request)

    @task(7)
    @tag('GeometryFieldGet')
    def test_get_feature_geometry(self):
        bbox_cor_list = [random.uniform(bbox_x[0], bbox_x[-1]),
                         random.uniform(bbox_x[0], bbox_x[-1]),
                         random.uniform(bbox_y[0], bbox_y[-1]),
                         random.uniform(bbox_y[0], bbox_y[-1])]
        query_request = f"?{token}&service=wfs&version={version}&request=GetFeature&typeNames={featureType}" \
                        f"&bbox={bbox_cor_list[0]},{bbox_cor_list[1]},{bbox_cor_list[2]},{bbox_cor_list[-1]}&" \
                        f"count={random.randrange(15)}"
        with self.client.get(query_request, catch_response=True, verify=False,
                             name="GeometryFieldGet/bbox") as response:
            if 200 == response.status_code:
                response.success()
            else:
                response.failure(str(response.status_code) + " Query has sent: " + query_request)

    @task(7)
    @tag('GeometryFieldPost')  # must filters: by polygon, by MultiPolygon, by Envelope &count=6&type=Point
    def test_post_feature_geometry(self):
        query_request = f"?{token}&service=wfs&version={version}&request=GetFeature&typeNames={featureType}&count={str(random.randint(1, 9))}" \
                        f"&type={str(self.choice_params())}"
        with self.client.post(query_request, catch_response=True, verify=False, name="GeometryFieldPost") as response:
            if 200 == response.status_code:
                response.success()
            else:
                response.failure(str(response.status_code) + " Query has sent: " + query_request)

    @task(7)
    @tag('Date')
    def test_get_feature_date(self):
        start_date = datetime.datetime(2021, 1, 1)
        end_date = datetime.datetime.now()
        time_between_dates = end_date - start_date
        days_between_dates = time_between_dates.days
        random_number_of_days = random.randrange(days_between_dates)
        random_date = start_date + datetime.timedelta(days=random_number_of_days)
        ran_date = "'" + random_date.strftime("%x") + "'"
        query_request = f"?{token}&service=wfs&version={version}&request=GetFeature&typeNames={featureType}&{by_date}={ran_date}"
        date_filter = random.choice(by_date_filter)
        if "count" in date_filter:
            query_request += date_filter + str(random.randint(1, 9))
        else:
            query_request += date_filter

        with self.client.post(query_request, catch_response=True, verify=False, name="Date") as response:
            if 200 == response.status_code:
                response.success()
            else:
                response.failure(str(response.status_code) + " Query has sent: " + query_request)

    @task(7)
    @tag('GetFeatureGrid')
    def test_get_feature_grid(self):
        geo_id = self.choice_geo_pack()
        query_request = f"?{token}&service=wfs&version={version}&request=GetFeature&typeNames={featureType}&featureId='{geo_id[gfid]}'"
        with self.client.post(query_request, catch_response=True, verify=False, name="GetFeatureGfid") as response:
            if 200 == response.status_code:

                response.success()
            else:
                response.failure(str(response.status_code) + " Query has sent: " + query_request)

    def choice_geo_pack(self):
        chose = random.choice(self.get_feature_params)
        return chose

    def choice_params(self):
        return random.choice(self.geo_oper)


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
