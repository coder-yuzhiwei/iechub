from abc import ABC
from typing import Dict, Text, Any, List, Union, Optional
import json
from rasa_sdk import Tracker, Action
from rasa_sdk.events import UserUtteranceReverted, Restarted, SlotSet, SessionStarted, ActionExecuted, EventType
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk import FormValidationAction
from rasa_sdk.types import DomainDict
import re
#from actions.db_connect import conn
from actions import ChatApis
from actions.WeatherApis import get_weather_by_day
#　from actions.sparql import conn
from actions.cossimiliry import similar
from actions.sparql_search import conn
from requests import (
    ConnectionError,
    HTTPError,
    TooManyRedirects,
    Timeout
)

class ActionDefaultFallback(Action):
    """Executes the fallback action and goes back to the previous state
    of the dialogue"""

    def name(self):
        return 'action_default_fallback'

    def run(self, dispatcher, tracker, domain):

        # 访问图灵机器人API(闲聊)
        text = tracker.latest_message.get('text')
        message = ChatApis.get_response(text)
        print(message)
        if message is not None:
            dispatcher.utter_message(message)
        else:
            dispatcher.utter_template('utter_default', tracker, silent_fail=True)
        return []


class JobForm(FormValidationAction):

    def name(self) -> Text:
        """Unique identifier of the form"""
        return 'validate_jobsearch_form'

    async def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: "Tracker",
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        """Define what the form has to do
            after all required slots are filled"""
        job = tracker.get_slot('job')
        company = tracker.get_slot('company')
        welfare = tracker.get_slot('welfare')
        salary = tracker.get_slot('salary')
        address = tracker.get_slot('address')
        if job is None:
            dispatcher.utter_message("没听懂您要查找什么工作岗位，试试说：我想找个软件工程师的工作")
            return []
        data,id = conn(job, company, address, salary, welfare)
        len1 = len(data)
        if len1 == 0:
            s1 ,s2, max1, max2 = similar(job)
            if max1 >= 0.3 and max2 >=0.3:
                dispatcher.utter_message("抱歉，没有找到符合要求的岗位,您可以试试查找{}或{}的工作".format(s1,s2))
            elif max2<0.3 and max1>=0.3:
                dispatcher.utter_message("抱歉，没有找到符合要求的岗位,您可以试试查找{}的工作".format(s1))
            else:
                dispatcher.utter_message("抱歉，没有找到符合要求的岗位呢")
            return []
        if len1 > 2:
            data = "共为您找到{}条{}相关信息，请通过微信公众号查看".format(len1, job)
            dispatcher.utter_message(data, id)
        else:
            # data = data.to_json(orient='index', force_ascii=False)
            for i in data.values():
                txt = eval(i)
                dispatcher.utter_message("为您找到{}的{}工作，月薪为{}".format(txt['employee_unitName'], txt['employee_quar'], txt['employee_salary']),id)
        return []


class ActionSessionStart(Action):
    def name(self) -> Text:
        return "action_session_start"

    @staticmethod
    def fetch_slots(tracker: Tracker) -> List[EventType]:
        """Collect slots that contain the user's name and phone number."""

        slots = []
        for key in ("job", "company", "address"):
            value = tracker.get_slot(key)
            if value is not None:
                slots.append(SlotSet(key=key, value=value))
        return slots

    async def run(
      self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        # the session should begin with a `session_started` event
        events = [SessionStarted()]

        # any slots that should be carried over should come after the
        # `session_started` event
        events.extend(self.fetch_slots(tracker))

        # an `action_listen` should be added at the end as a user message follows
        events.append(ActionExecuted("action_listen"))
        return events

class companyaskForm(FormValidationAction):

    def name(self) -> Text:
        """Unique identifier of the form"""
        return 'validate_companyask_form'

    async def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: "Tracker",
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        """Define what the form has to do
            after all required slots are filled"""
        job = tracker.get_slot('job')
        welfare = tracker.get_slot('welfare')
        salary = tracker.get_slot('salary')
        address = tracker.get_slot('address')
        company = tracker.get_slot('company')
        if company is not None:
            dispatcher.utter_message("没听懂您在问什么，试试说哪些公司招聘软件工程师")
            return []
        data,id = conn(job, None, address, salary, welfare)
        len1 = len(data)
        dataa = ""
        for i in data.values():
            txt = eval(i)
            dataa = dataa +" "+ txt['employee_unitName']
        dispatcher.utter_message("为您找到相关的公司，公司有{}，详情请查看微信公众号".format(dataa), id)
        return []

class welfareaskForm(FormValidationAction):

    def name(self) -> Text:
        """Unique identifier of the form"""
        return 'validate_welfareask_form'

    async def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: "Tracker",
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        """Define what the form has to do
            after all required slots are filled"""
        job = tracker.get_slot('job')
        welfare = tracker.get_slot('welfare')
        salary = tracker.get_slot('salary')
        address = tracker.get_slot('address')
        company = tracker.get_slot('company')
        if company is None:
            dispatcher.utter_message("您要查找哪个公司的福利状况？")
            return []
        data, id = conn(job, company, None, None, None)
        len1 = len(data)
        dataa = ""
        welfares = []
        for i in data.values():
            txt = eval(i)
            welfare = txt.get('employee_TextFd3', " ")
            if str(welfare) not in welfares:
                welfares.append(welfare)
        for wel in welfares:
            dataa = dataa + " " + wel
        dispatcher.utter_message("您要查找的{}的福利有{}，详情请查看微信公众号".format(company, dataa), id)
        return []

class welfareyornaskForm(FormValidationAction):

    def name(self) -> Text:
        """Unique identifier of the form"""
        return 'validate_welfareyorn_form'

    async def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: "Tracker",
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        """Define what the form has to do
            after all required slots are filled"""
        job = tracker.get_slot('job')
        welfare = tracker.get_slot('welfare')
        company = tracker.get_slot('company')
        if company is None:
            dispatcher.utter_message("您要查找哪个公司的福利状况？")
            return []
        data,id = conn(job, company, None, None, welfare)
        len1 = len(data)
        for i in data.values():
            txt = eval(i)
            if str(welfare) in txt.get('employee_TextFd3', " "):
                dispatcher.utter_message("您查找的{}存在该福利".format(company))
                return []
        dispatcher.utter_message("您查找的{}不存在该福利".format(company))
        return []

class salaryaskForm(FormValidationAction):

    def name(self) -> Text:
        """Unique identifier of the form"""
        return 'validate_salaryask_form'

    async def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: "Tracker",
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        """Define what the form has to do
            after all required slots are filled"""
        job = tracker.get_slot('job')
        company = tracker.get_slot('company')
        if job is None:
            dispatcher.utter_message("您要找什么岗位工作的薪资状况？")
            return []
        data,id = conn(job, company, None, None, None)
        len1 = len(data)
        for i in data.values():
            txt = eval(i)
            dispatcher.utter_message("为您找到{}的{}工作，月薪为{}，详情请查看微信公众号".format(txt['employee_unitName'], txt['employee_quar'], txt['employee_salary']), id)
        return []

class addressaskForm(FormValidationAction):

    def name(self) -> Text:
        """Unique identifier of the form"""
        return 'validate_addressask_form'

    async def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: "Tracker",
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        """Define what the form has to do
            after all required slots are filled"""
        job = tracker.get_slot('job')
        company = tracker.get_slot('company')
        welfare = tracker.get_slot('welfare')
        salary = tracker.get_slot('salary')
        if job is None:
            dispatcher.utter_message("您要找什么工作")
            return []
        data,id = conn(job, company, None, salary, welfare)
        for i in data.values():
            txt = eval(i)
            dispatcher.utter_message("为您找到{}的{}工作，地址为{}，详情请查看微信公众号".format(txt['employee_unitName'], txt['employee_quar'], txt['employee_address'], id))
        return []

class jobrequirementForm(FormValidationAction):

    def name(self) -> Text:
        """Unique identifier of the form"""
        return 'validate_jobrequirement_form'

    async def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: "Tracker",
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        """Define what the form has to do
            after all required slots are filled"""
        job = tracker.get_slot('job')
        company = tracker.get_slot('company')
        welfare = tracker.get_slot('welfare')
        salary = tracker.get_slot('salary')
        address = tracker.get_slot('address')
        data,id = conn(job, company, address, salary, welfare)
        len1 = len(data)
        dataa = ""
        requires = []
        for i in data.values():
            txt = eval(i)
            require = txt.get('employee_TextFd2', " ")
            if require not in requires:
                requires.append(require)
        for wel in requires:
            dataa = dataa + " " + wel
        dispatcher.utter_message("您要查找的{}工作的要求有{}，详情请查看微信公众号".format(job, dataa), id)
        return []