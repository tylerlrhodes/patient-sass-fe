import unittest
import requests
import json

TEST_URL_BASE="http://localhost:8001"
TEST_URL_RECORD=TEST_URL_BASE + "/record"

class APITester(unittest.TestCase):
  def send_json(self, json):
    return requests.post(TEST_URL_RECORD, json=json)

  def send_get(self, params):
    return requests.get(TEST_URL_RECORD + params)

  def test_result_category(self):
    table = "ResultCategory"
    data = {"name" : "Foo", "score_range" : "1-5", "tenant_id": 1}
    req_o = {"operation" : "insert", "table" : table, "data" : data }
    rsp = self.send_json(req_o)
    self.assertTrue(rsp.status_code == 201, "Bad status response code: {}".format(rsp.status_code))
    rsp_o = rsp.json()
    id = rsp_o["id"]
    self.assertTrue(id == 1, "Got unrespected ID in response {}".format(rsp_o["id"]))
    rsp = self.send_json(req_o)
    self.assertTrue(rsp.status_code == 409, "Bad status response code: {}".format(rsp.status_code))
    rsp = self.send_get("/{}/{}".format(table, id))
    self.assertTrue(rsp.status_code == 200, "Bad status response code: {}".format(rsp.status_code))
    rsp_o = rsp.json()
    expect_rsp_o = data.copy()
    expect_rsp_o["id"] = id
    self.assertTrue(rsp_o == expect_rsp_o, "Got unexpected data: {}, expected {}".format(rsp_o, expect_rsp_o))
if __name__ == '__main__':
  unittest.main()
